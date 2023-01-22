user_schema = {
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "refresh_token": {"type": "string"},
    },
    "required": ["name", "email", "password"],
}
