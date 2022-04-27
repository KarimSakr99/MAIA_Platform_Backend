import os
import torch
from torch import nn
from torchvision import models
from medcam import medcam
from .hipnet.UNets3D import ResidualUNet3D


models_dir = f'{os.getcwd()}/assets/Models'


def prep_pneumonia_model(path=f'{os.getcwd()}/assets/Models/pneu_googlenet.pt'):
    model = models.googlenet(pretrained=True)

    model.fc = nn.Sequential(nn.Linear(model.fc.in_features, 128, bias=False),
                             nn.BatchNorm1d(128),
                             nn.ReLU(),
                             nn.Dropout(0.25),
                             nn.Linear(128, 1))

    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    model.eval()

    model = medcam.inject(model, return_attention=True, backend='gcampp')
    return model


def prep_skin_model(path=f'{models_dir}/skin_efficientnet_b3_40epoch.pt'):
    model = models.efficientnet_b3(pretrained=False)
    model.classifier[-1] = nn.Sequential(nn.Linear(model.classifier[-1].in_features, 128, bias=False),
                                         nn.BatchNorm1d(128),
                                         nn.ReLU(),
                                         nn.Dropout(0.3),
                                         nn.Linear(128, 1))
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    model.eval()

    model = medcam.inject(model, return_attention=True, backend='gcampp')
    return model


def prep_hip_model(path=f'{models_dir}/hippocampus_seg.pth'):
    model = ResidualUNet3D(in_channels=1, out_channels=3,
                           f_maps=32, final_sigmoid=False)
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    model.eval()
    return model
