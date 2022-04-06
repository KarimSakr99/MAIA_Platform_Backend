import numpy as np
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
