from flask import request
from PIL import Image
import torch
from torchcam.utils import overlay_mask
from torchvision.transforms.functional import to_pil_image

from . import save_file, extract_info
from . import transform_image_skin, transform_image_pneumonia
from . import prep_pneumonia_model, prep_skin_model

pneumonia_model = prep_pneumonia_model()
skin_model = prep_skin_model()


def chest():
    file, user = extract_info(request)
    user_ill_path, file_path = save_file(file, user, 'chest')

    img = Image.open(file_path).convert('RGB')
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
    with torch.no_grad():
        prop, cam = skin_model(transform_image_skin(img))
        prop, cam = prop.sigmoid().item(), cam.squeeze()

    overlay_mask(img, to_pil_image(cam, mode='F'), alpha=0.5).save(
        f'{user_ill_path}/cams/cam.jpg')
    state = 'Positive' if prop > 0.5 else 'Negative'
    return f'Melanoma {state}\nProbability = {prop*100 if state=="Positive" else 100-prop*100:.1f}%'
