import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services import auth_service
from app.utils.auth_dto import LoginDto, RefreshTokensDto, SignupDto
from app.utils.auth_response import Tokens
from app.utils.token import get_token, verify_token

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

@app.post("/refresh-tokens")
def refresh_tokens(body: RefreshTokensDto, access_token:str = Depends(get_token)) -> Tokens:
    id = verify_token(access_token, os.environ["AT_SECRET_KEY"])['id']
    return auth_service.refresh_tokens(id, body)