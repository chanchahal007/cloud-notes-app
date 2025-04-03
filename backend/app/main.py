from fastapi import FastAPI
from .auth import router as auth_router
from .notes import router as notes_router

app = FastAPI()

# Routes
app.include_router(auth_router, prefix="/auth")
app.include_router(notes_router, prefix="/notes")

@app.get("/")
def root():
    return {"message": "Cloud Notes API is running"}
