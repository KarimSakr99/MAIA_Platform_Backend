import os
from itertools import product
from . import get_ills, get_users, append_ill

from flask import request


def new_illness():
    if request.method == 'POST':
        ill = request.args['ill']
        if ill not in get_ills():
            append_ill(ill)
            for user, ill in product(get_users(), get_ills()):
                os.makedirs(f'{os.getcwd()}/users/{user}/{ill}', exist_ok=True)
                os.makedirs(
                    f'{os.getcwd()}/users/{user}/{ill}/cams', exist_ok=True)
            return 'Illness created'
        return 'Illness already exists'


def new_user():
    if request.method == 'POST':
        user = request.args['user']
        if user not in get_users():
            os.mkdir(f'{os.getcwd()}/users/{user}')
            for i in get_ills():
                os.mkdir(f'{os.getcwd()}/users/{user}/{i}')
                os.mkdir(f'{os.getcwd()}/users/{user}/{i}/cams')
            return 'User created'
        return 'User already exists'
