signup_schema = {
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "refresh_token": {"type": "string", "default": None}
    },
    "required": ["name", "email", "password"]
}