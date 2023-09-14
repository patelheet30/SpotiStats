from dataclasses import dataclass


@dataclass
class User:
    username: str = None
    email: str = None
    followers: int = None
    following: int = None
    creation_date: str = None
    country: str = None
    gender: str = None
    birth_date: str = None
