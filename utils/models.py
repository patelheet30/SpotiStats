from dataclasses import dataclass

@dataclass
class Media:
    pass

@dataclass
class User:
    username: str
    image_URL: str
    large_image_URL: str
    email: str
    followers: int
    following: int
    creation_date: str
    country: str

