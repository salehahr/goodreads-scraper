from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel

from .authenticate import get_auth


class Login(BaseModel):
    email: str
    password: str

    def __init__(self, filepath: Path):
        data = get_auth(filepath)
        super(Login, self).__init__(**data)


class Config(BaseModel):
    chromedriver_path: Path
    login_filepath: Path
    shelf: str

    login: Login = None
    user_id: int = None

    def __init__(self, **kwargs):
        super(Config, self).__init__(**kwargs)

        self.login = Login(self.login_filepath)

    @staticmethod
    def from_file(filepath: Path | str) -> Config:
        with open(filepath) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return Config(**data)
