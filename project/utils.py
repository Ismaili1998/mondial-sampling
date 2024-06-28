import msal
from django.conf import settings

def get_access_token():
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    authority = settings.AUTHORITY
    scopes = settings.SCOPES
    
    client = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret,
    )
    
    # Check if we already have a token in cache
    accounts = client.get_accounts()
    if accounts:
        result = client.acquire_token_silent(scopes, account=accounts[0])
    else:
        # If no token is found in cache, perform a full OAuth2 flow
        result = client.acquire_token_for_client(scopes=scopes)
    
    if 'access_token' in result:
        return result['access_token']
    else:
        return None
