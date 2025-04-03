from fastapi import APIRouter

router = APIRouter()

@router.post("/signup")
def signup():
    return {"message": "Signup endpoint placeholder"}

@router.post("/login")
def login():
    return {"message": "Login endpoint placeholder"}
