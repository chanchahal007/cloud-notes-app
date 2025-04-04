from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import boto3
import os

router = APIRouter()

# AWS Cognito configuration
COGNITO_USER_POOL_ID = "us-east-1_NYIMPnqNU"
COGNITO_CLIENT_ID = "6miqrdeqj5giaomrdl3ft0d0l3"
AWS_REGION = "us-east-1"

client = boto3.client("cognito-idp", region_name=AWS_REGION)

# Pydantic models
class SignUpModel(BaseModel):
    username: str
    password: str
    email: str

class LoginModel(BaseModel):
    username: str
    password: str

# Signup route
@router.post("/signup")
def signup(data: SignUpModel):
    try:
        response = client.sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=data.username,
            Password=data.password,
            UserAttributes=[
                {"Name": "email", "Value": data.email},
                {"Name": "preferred_username", "Value": data.username}
            ]
        )
        return {"message": "Signup successful! Please check your email to confirm your account."}
      except client.exceptions.UsernameExistsException:
        raise HTTPException(status_code=400, detail="Username already exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Login route
@router.post("/login")
def login(data: LoginModel):
    try:
        response = client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": data.username,
                "PASSWORD": data.password
            }
        )
        return {
            "message": "Login successful!",
            "access_token": response['AuthenticationResult']['AccessToken'],
            "id_token": response['AuthenticationResult']['IdToken'],
            "refresh_token": response['AuthenticationResult']['RefreshToken']
        }
    except client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")
    except client.exceptions.UserNotConfirmedException:
        raise HTTPException(status_code=403, detail="User not confirmed. Please confirm your email.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
