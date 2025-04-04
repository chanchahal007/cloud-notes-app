from fastapi import FastAPI
from app.auth import router as auth_router
from app.notes import router as notes_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(notes_router)
