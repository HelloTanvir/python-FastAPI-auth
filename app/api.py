from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.signup import signup_service
from app.utils.auth_response import Tokens
from app.utils.signup_dto import SignupDto

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/signup")
def signup(body: SignupDto) -> Tokens:
    return signup_service(body)