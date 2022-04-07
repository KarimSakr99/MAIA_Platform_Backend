import numpy as np
import nibabel as nib
import torch
from torchvision import transforms as T

mean = np.array([0.485, 0.456, 0.406])
std = np.array([0.229, 0.224, 0.225])


def transform_image_pneumonia(img):
    input_transforms = T.Compose([T.Resize(255),
                                  T.CenterCrop(224),
                                  T.ToTensor(),
                                  T.Normalize(mean, std)])
    return input_transforms(img).unsqueeze_(0)


def transform_image_skin(img):
    input_transforms = T.Compose([T.Resize(255),
                                  T.CenterCrop(224),
                                  T.ToTensor(),
                                  T.Normalize(mean, std)])
    return input_transforms(img).unsqueeze_(0)


def transform_image_hip(path):
    volume = nib.load(path).get_fdata()
    reshaped_volume = np.zeros((48, 64, 64))

    size = volume.shape
    reshaped_volume[:size[0], :size[1], :size[2]] = volume
    volume_tensor = torch.from_numpy(reshaped_volume.astype(
        np.single)/np.max(reshaped_volume)).unsqueeze(0).unsqueeze(0)
    return volume, volume_tensor
