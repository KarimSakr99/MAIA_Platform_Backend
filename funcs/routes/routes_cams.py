import os
from flask import request, send_file


def chest_cam():
    user = request.form['user']
    return send_file(f'{os.getcwd()}/users/{user}/chest/cams/cam.jpg', cache_timeout=-1)


def skin_cam():
    user = request.form['user']
    return send_file(f'{os.getcwd()}/users/{user}/skin/cams/cam.jpg', cache_timeout=-1)
    # img_name = request.form['img_name']
    # return send_file(f'./users/{user}/skin/cams/{secure_filename(img_name.rsplit(".")[0])}.jpg', cache_timeout=-1)


def hip_animation():
    user = request.form['user']
    return send_file(f'{os.getcwd()}/users/{user}/hip/cams/gif.gif', cache_timeout=-1)
