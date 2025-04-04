from fastapi import APIRouter, Depends, Header
from app.utils import verify_jwt_token

router = APIRouter()

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise Exception("Authorization header must be 'Bearer <token>'")
    token = authorization.split(" ")[1]
    return verify_jwt_token(token)

@router.get("/notes")
def get_notes(user=Depends(get_current_user)):
    return {
        "message": f"Welcome {user['username']} 👋 Here are your secure notes!",
        "user_claims": user
    }
