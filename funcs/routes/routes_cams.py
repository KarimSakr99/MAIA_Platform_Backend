import os
from flask import request, send_file


def chest_cam():
    user = request.args['user']
    return send_file(f'{os.getcwd()}/users/{user}/chest/cams/cam.jpg', cache_timeout=-1)


def skin_cam():
    user = request.args['user']
    # img_name = request.args['img_name']

    return send_file(f'{os.getcwd()}/users/{user}/skin/cams/cam.jpg', cache_timeout=-1)
    # return send_file(f'./users/{user}/skin/cams/{secure_filename(img_name.rsplit(".")[0])}.jpg', cache_timeout=-1)
