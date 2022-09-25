from typing import Optional

import yaml
from pydantic import BaseModel

from .authenticate import get_auth


class Login(BaseModel):
    email: Optional[str]
    password: Optional[str]

    def __init__(self, filepath: str):
        data = get_auth(filepath)
        super(Login, self).__init__(**data)


class Config(BaseModel):
    login_filepath: str
    shelf: str

    login: Optional[Login]
    user_id: Optional[int]

    def __init__(self, filepath: str):
        with open(filepath) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        super(Config, self).__init__(**data)

        self.login = Login(self.login_filepath)
