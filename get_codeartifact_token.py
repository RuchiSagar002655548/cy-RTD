
import boto3
import subprocess

# Set CodeArtifact details
domain = 'cellarity-test'
domain_owner = '581351078906'
repository = 'python'
region = 'us-east-1'

# Retrieve the authorization token
client = boto3.client('codeartifact', region_name=region)
token_response = client.get_authorization_token(domain=domain, domainOwner=domain_owner)
token = token_response['authorizationToken']

# Construct the package URL
repository_url = f"https://{domain}-{domain_owner}.d.codeartifact.{region}.amazonaws.com/pypi/{repository}/simple/"
trusted_host = repository_url.split('/')[2]

pip_index_url = f"{repository_url}:{token}"
print(pip_index_url)

# Install the package from CodeArtifact
subprocess.run([
    'pip', 'install',
    '--extra-index-url', f"{repository_url}:{token}",
    '--trusted-host', trusted_host,
    'my_test_package'
], check=True)

