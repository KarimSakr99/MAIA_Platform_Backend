import os
from werkzeug.utils import secure_filename


def get_users():
    return [i for i in os.listdir(f'{os.getcwd()}/users/') if '.' not in i]


def get_ills(path=f'{os.getcwd()}/assets/ills.txt'):
    with open(path) as f:
        return [i.strip() for i in f.readlines()]


def append_ill(ill, path=f'{os.getcwd()}/assets/ills.txt'):
    with open(path, 'a') as f:
        f.write(f'{ill}\n')


def save_file(file, user, ill):
    user_ill_path = f'{os.getcwd()}/users/{user}/{ill}'
    file_path = os.path.join(user_ill_path, secure_filename(file.filename))
    file.save(file_path)
    return user_ill_path, file_path


def extract_info(request):
    file = request.files['file']
    if file is not None:
        user = request.args['user']
        return file, user
