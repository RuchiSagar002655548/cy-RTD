import requests
import json
import os
import boto3  # AWS SDK

# Read RTD API Token from environment variables (set in GitHub Secrets)
RTD_API_TOKEN = os.getenv("RTD_API_TOKEN")
if not RTD_API_TOKEN:
    raise ValueError(" RTD_API_TOKEN is missing! Make sure it's set in GitHub Secrets.")

# AWS IAM User whose keys will be rotated
IAM_USER_NAME = "codeartifact-rtd"

# RTD API Headers
HEADERS = {
    "Authorization": f"Token {RTD_API_TOKEN}",
    "Content-Type": "application/json",
}

# List of RTD projects to update
RTD_PROJECTS = ["cy-rtd"]  # Add more project slugs if needed

# Authenticate to AWS using OIDC Role from GitHub Actions
def assume_aws_role():
    """Uses OIDC to assume the AWS role for IAM access."""
    sts_client = boto3.client("sts")
    assumed_role = sts_client.assume_role(
        RoleArn="arn:aws:iam::581351078906:role/GitHubActions_OIDC_role",
        RoleSessionName="GitHubActions"
    )
    print(f"Successfully assumed role")
    return assumed_role["Credentials"]


def fetch_new_aws_keys():
    """Fetches new AWS Access Key & Secret from AWS IAM"""
    try:
        print("Assuming AWS IAM role using OIDC...")
        aws_creds = assume_aws_role()
        if not aws_creds:
            print("AWS role assumption failed.")
            return None

        # Use the assumed role credentials to authenticate AWS IAM API
        iam = boto3.client(
            "iam",
            aws_access_key_id=aws_creds["AccessKeyId"],
            aws_secret_access_key=aws_creds["SecretAccessKey"],
            aws_session_token=aws_creds["SessionToken"]
        )

        print(f"Creating new AWS Access Key for {IAM_USER_NAME}...")
        new_key = iam.create_access_key(UserName=IAM_USER_NAME)["AccessKey"]

        # Mask credentials in logs (Security Best Practice)
        print(f"New AWS Access Key created: {new_key['AccessKeyId']} (SECRET HIDDEN)")

        return {
            "AWS_ACCESS_KEY_ID": new_key["AccessKeyId"],
            "AWS_SECRET_ACCESS_KEY": new_key["SecretAccessKey"],
        }

    except Exception as e:
        print(f"Failed to create AWS keys: {str(e)}")
        return None


def list_env_variables(project):
    """Lists all environment variables in the RTD project"""
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
    """Deletes an existing environment variable in RTD"""
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
                delete_env_variable(project, var["pk"])

        # Add new AWS keys to RTD
        for name, value in aws_keys.items():
            print(f"Adding {name} to {project}...")
            add_env_variable(project, name, value)

        print(f"RTD AWS credentials updated for {project}!\n")


if __name__ == "__main__":
    update_rtd_aws_keys()
