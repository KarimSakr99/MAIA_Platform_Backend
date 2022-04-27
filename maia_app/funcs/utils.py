import os
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import numpy as np
from celluloid import Camera


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
        user = request.form['user']
        return file, user


def animate_volume(volume, pred):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 4))
    camera = Camera(fig)

    for i in range(volume.shape[0]):
        ax1.imshow(volume[i, :, :], 'bone')
        ax1.axis('off')

        ax2.imshow(volume[i, :, :], 'bone')
        mask = np.ma.masked_where(pred[i] == 0, pred[i])
        ax2.imshow(mask > 0, 'Wistia', alpha=0.8)
        ax2.axis('off')
        camera.snap()

    return camera.animate()
