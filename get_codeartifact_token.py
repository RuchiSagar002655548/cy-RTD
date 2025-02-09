
import boto3
import os
import subprocess

# Retrieve AWS CodeArtifact token dynamically
client = boto3.client('codeartifact', region_name=os.getenv('AWS_REGION', 'us-east-1'))
token_response = client.get_authorization_token(
    domain='cellarity-test',
    domainOwner='581351078906'
)
codeartifact_token = token_response['authorizationToken']

# Set PIP_EXTRA_INDEX_URL and install packages
codeartifact_url = os.getenv('CODEARTIFACT_URL')
subprocess.run([
    'pip', 'install',
    f'--extra-index-url={codeartifact_url}:{codeartifact_token}',
    '--trusted-host', codeartifact_url.split("/")[2],
    'my-test-package'
], check=True)
