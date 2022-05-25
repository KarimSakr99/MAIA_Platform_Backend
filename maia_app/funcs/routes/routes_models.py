from flask import request
from PIL import Image, ImageOps
import numpy as np
import torch


from torchcam.utils import overlay_mask
from torchvision.transforms.functional import to_pil_image


from . import save_file, extract_info, animate_volume, extract_info
from . import transform_image_skin, transform_image_pneumonia
from . import prep_pneumonia_model, prep_skin_model
from . import transform_image_hip, prep_hip_model

pneumonia_model = prep_pneumonia_model()
skin_model = prep_skin_model()
hip_model = prep_hip_model()


def chest():
    file, user = extract_info(request)
    user_ill_path, file_path = save_file(file, user, 'chest')

    img = Image.open(file_path).convert('RGB')
    img = ImageOps.exif_transpose(img)
    with torch.no_grad():
        prop, cam = pneumonia_model(transform_image_pneumonia(img))
        prop, cam = prop.sigmoid().item(), cam.squeeze()

    overlay_mask(img, to_pil_image(cam, mode='F'), alpha=0.5).save(
        f'{user_ill_path}/cams/cam.jpg')

    state = 'Positive' if prop > 0.54 else 'Negative'
    return f'Pneumonia {state}\nProbability = {prop*100 if state=="Positive" else 100-prop*100:.1f}%'


def skin():
    file, user = extract_info(request)
    user_ill_path, file_path = save_file(file, user, 'skin')

    img = Image.open(file_path).convert('RGB')
    img = ImageOps.exif_transpose(img)
    with torch.no_grad():
        prop, cam = skin_model(transform_image_skin(img))
        prop, cam = prop.sigmoid().item(), cam.squeeze()

    overlay_mask(img, to_pil_image(cam, mode='F'), alpha=0.5).save(
        f'{user_ill_path}/cams/cam.jpg')
    state = 'Positive' if prop > 0.5 else 'Negative'
    return f'Melanoma {state}\nProbability = {prop*100 if state=="Positive" else 100-prop*100:.1f}%'


def hip():
    file, user = extract_info(request)
    user_ill_path, file_path = save_file(file, user, 'hip')

    with torch.no_grad():
        volume, volume_tensor = transform_image_hip(file_path)
        pred = hip_model(volume_tensor)
        pred = torch.squeeze(pred.detach())
        pred = torch.argmax(pred, dim=0)
        pred = pred.numpy()
        pred = pred[: volume.shape[0], : volume.shape[1], : volume.shape[2]]
        volume_in_mm3 = np.sum(pred > 0)

    animate_volume(volume, pred).save(f'{user_ill_path}/cams/gif.gif')

    return f'Hippocampus volume equals {volume_in_mm3:.1f} mm3'
