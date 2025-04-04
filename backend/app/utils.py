import requests
import jwt
from jwt.algorithms import RSAAlgorithm
from fastapi import HTTPException

COGNITO_REGION = "us-east-1"
USER_POOL_ID = "us-east-1_NYIMPnqNU"
CLIENT_ID = "6miqrdeqj5giaomrdl3ft0d0l3"


cognito_issuer = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}"
cognito_jwks_url = f"{cognito_issuer}/.well-known/jwks.json"

jwks = requests.get(cognito_jwks_url).json()

def verify_jwt_token(token: str):
    try:
        headers = jwt.get_unverified_header(token)
        kid = headers["kid"]

        key = next((k for k in jwks["keys"] if k["kid"] == kid), None)
        if key is None:
            raise HTTPException(status_code=401, detail="Invalid token: key not found")

        public_key = RSAAlgorithm.from_jwk(key)
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=CLIENT_ID,
            issuer=cognito_issuer,
        )
        return decoded
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
