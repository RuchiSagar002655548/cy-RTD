import requests
import json
import os
import boto3

# List of RTD projects (For testing, we only have one project: "cy-rtd")
RTD_PROJECTS = ["cy-rtd"]

# RTD API Headers (Ensure `RTD_API_TOKEN` is set in GitHub Secrets)
RTD_API_TOKEN = os.getenv("RTD_API_TOKEN")
if not RTD_API_TOKEN:
    raise ValueError("RTD_API_TOKEN is missing! Ensure it is set in GitHub Secrets.")

HEADERS = {
    "Authorization": f"Token {RTD_API_TOKEN}",
    "Content-Type": "application/json",
}

def assume_aws_role():
    """Uses default AWS credentials from GitHub Actions OIDC session or ~/.aws/credentials"""
    try:
        print("Fetching AWS credentials...")
        session = boto3.Session()
        return session.get_credentials().get_frozen_credentials()
    except Exception as e:
        print(f"Failed to retrieve AWS credentials: {str(e)}")
        return None

def fetch_new_aws_keys():
    """Creates a new AWS Access Key & Secret for the codeartifact-rtd IAM user"""
    try:
        aws_creds = assume_aws_role()
        if not aws_creds:
            print("AWS credential retrieval failed. Exiting.")
            return None

        # Create an IAM client with the retrieved credentials
        iam = boto3.client("iam")

        # List all existing access keys
        existing_keys = iam.list_access_keys(UserName="codeartifact-rtd")["AccessKeyMetadata"
                                                                          ]
        # If 2 keys exist, delete the oldest one
        if len(existing_keys) >= 2:
            oldest_key = sorted(existing_keys, key=lambda k: k["CreateDate"])[0]  # Find oldest key
            print(f"Deleting oldest AWS Access Key: {oldest_key['AccessKeyId']}...")
            iam.delete_access_key(UserName="codeartifact-rtd", AccessKeyId=oldest_key["AccessKeyId"])
            print(f"Successfully deleted old key: {oldest_key['AccessKeyId']}")
            
        print("Creating new AWS Access Key for codeartifact-rtd...")
        new_key = iam.create_access_key(UserName="codeartifact-rtd")["AccessKey"]

        # Do not print the secret key for security reasons
        print(f"New AWS Access Key created: {new_key['AccessKeyId']} (SECRET HIDDEN)")

        return {
            "AWS_ACCESS_KEY_ID": new_key["AccessKeyId"],
            "AWS_SECRET_ACCESS_KEY": new_key["SecretAccessKey"],
        }

    except Exception as e:
        print(f"Failed to create AWS keys: {str(e)}")
        return None

def list_env_variables(project):
    """Fetches all environment variables for a given RTD project"""
    try:
        url = f"https://readthedocs.org/api/v3/projects/{project}/environmentvariables/"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to list RTD environment variables for {project}: {response.text}")
            return None
    except Exception as e:
        print(f"Exception while listing RTD variables: {str(e)}")
        return None

def delete_env_variable(project, var_id):
    """Deletes a specific environment variable in RTD"""
    try:
        url = f"https://readthedocs.org/api/v3/projects/{project}/environmentvariables/{var_id}/"
        response = requests.delete(url, headers=HEADERS)

        if response.status_code == 204:
            print(f"Successfully deleted variable {var_id} from {project}")
            return True
        else:
            print(f"Failed to delete variable {var_id} from {project}: {response.text}")
            return False
    except Exception as e:
        print(f"Exception while deleting RTD variable: {str(e)}")
        return False

def add_env_variable(project, name, value):
    """Adds a new environment variable to RTD"""
    try:
        url = f"https://readthedocs.org/api/v3/projects/{project}/environmentvariables/"
        data = {"name": name, "value": value}
        response = requests.post(url, headers=HEADERS, data=json.dumps(data))

        if response.status_code == 201:
            print(f"Successfully added {name} to {project}")
            return True
        else:
            print(f"Failed to add {name} to {project}: {response.text}")
            return False
    except Exception as e:
        print(f"Exception while adding RTD variable: {str(e)}")
        return False

def update_rtd_aws_keys():
    """Deletes old AWS keys and updates RTD with new ones"""
    print("Fetching new AWS credentials from IAM...")
    aws_keys = fetch_new_aws_keys()
    if not aws_keys:
        print("AWS key creation failed. Exiting.")
        return

    for project in RTD_PROJECTS:
        print(f"Listing current environment variables for {project}...")
        existing_vars = list_env_variables(project)
        
        # Check if response is valid before proceeding
        if not existing_vars or "results" not in existing_vars:
            print(f"Skipping {project} due to API error.")
            continue

        # Delete existing AWS keys in RTD
        for var in existing_vars["results"]:
            if var["name"] in aws_keys:
                print(f"Deleting {var['name']} from {project}...")
                delete_env_variable(project, var["pk"])  # RTD API uses "pk" instead of "id"

        # Add new AWS keys to RTD
        for name, value in aws_keys.items():
            print(f"Adding {name} to {project}...")
            add_env_variable(project, name, value)

        print(f"RTD AWS credentials updated for {project}!\n")

if __name__ == "__main__":
    update_rtd_aws_keys()
