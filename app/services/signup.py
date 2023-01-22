from app.utils.auth_response import Tokens
from app.utils.signup_dto import SignupDto


def signup_service(body: SignupDto) -> Tokens:
    return {
        'access_token': f'access_token for {body.name}',
        'refresh_token': 'refresh_token'
    }