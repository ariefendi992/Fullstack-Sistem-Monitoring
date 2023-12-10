from fastapi import FastAPI
import uvicorn
from app import app

app: app

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, workers=2)
