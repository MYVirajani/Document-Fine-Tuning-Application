from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import upload, users, inference

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api/upload")
app.include_router(users.router, prefix="/api/users")
app.include_router(inference.router, prefix="/api/inference")

@app.get("/")
def read_root():
    return {"msg": "Welcome to LLaMA App Backend!"}
