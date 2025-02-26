import boto3

# Set CodeArtifact details
domain = 'cellarity-test'
domain_owner = '581351078906'
region = 'us-east-1'

# Retrieve the authorization token
client = boto3.client('codeartifact', region_name=region)
token_response = client.get_authorization_token(domain=domain, domainOwner=domain_owner)
token = token_response['authorizationToken']

# Print the token instead of running `pip install`
print(token)


