"""This module provides the response for authentication"""
from typing import TypedDict


class Tokens(TypedDict):
    """This class provides the response for tokens"""

    access_token: str
    refresh_token: str
