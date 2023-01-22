from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services import auth_service
from app.utils.auth_dto import LoginDto, SignupDto
from app.utils.auth_response import Tokens

load_dotenv()

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
    return auth_service.signup(body)

@app.post("/login")
def login(body: LoginDto) -> Tokens:
    return auth_service.login(body)