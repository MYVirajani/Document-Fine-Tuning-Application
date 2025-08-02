from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import upload, users, inference
from backend.db.database import Base, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(users.router)
app.include_router(inference.router)

# Create tables on startup
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"msg": "Welcome to LLaMA App Backend!"}
