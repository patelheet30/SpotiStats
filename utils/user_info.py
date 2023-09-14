from utils.get_json import get_json
from utils.models import User


def get_user_info(data_needed):
    return User(**data_needed)
