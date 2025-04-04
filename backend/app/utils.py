import requests
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

AWS_REGION = "your-region"
COGNITO_USER_POOL_ID = "your-user-pool-id"

# Token validator
cognito_jwks_url = f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
jwks = requests.get(cognito_jwks_url).json()

security = HTTPBearer()

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        unverified_header = jwt.get_unverified_header(token)
        key = next((k for k in jwks["keys"] if k["kid"] == unverified_header["kid"]), None)
        if not key:
            raise HTTPException(status_code=401, detail="Invalid token header")
        payload = jwt.decode(token, key, algorithms=["RS256"], audience=None, issuer=f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}")
        return payload  # You can return username or email from payload
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
