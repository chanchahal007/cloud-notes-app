from fastapi import APIRouter, Depends
from .utils import verify_jwt_token

router = APIRouter()

@router.get("/", dependencies=[Depends(verify_jwt_token)])
def list_notes():
    return {"notes": ["Sample note 1", "Sample note 2"]}
