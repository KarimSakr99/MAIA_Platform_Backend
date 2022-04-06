import os
import torch
from torch import nn
from torchvision import models
from medcam import medcam

models_dir = f'{os.getcwd()}/assets/Models'


def prep_pneumonia_model():
    model = models.googlenet(pretrained=True)

    model.fc = nn.Sequential(nn.Linear(model.fc.in_features, 128, bias=False),
                             nn.BatchNorm1d(128),
                             nn.ReLU(),
                             nn.Dropout(0.25),
                             nn.Linear(128, 1))

    model.eval()
    # model.load_state_dict(torch.load('./model4.pt'))

    model = medcam.inject(model, return_attention=True, backend='gcampp')
    return model


def prep_skin_model(path=f'{models_dir}/skin_efficientnet_b3_40epoch.pt'):
    model = models.efficientnet_b3(pretrained=True)
    model.classifier[-1] = nn.Sequential(nn.Linear(model.classifier[-1].in_features, 128, bias=False),
                                         nn.BatchNorm1d(128),
                                         nn.ReLU(),
                                         nn.Dropout(0.3),
                                         nn.Linear(128, 1))
    model.load_state_dict(torch.load(path))
    model.eval()

    model = medcam.inject(model, return_attention=True, backend='gcampp')
    return model
