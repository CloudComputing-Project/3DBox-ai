import sys
sys.path.append(".")
sys.path.append("..")

# import numpy as np
import torch
from util import save_image, load_image, visualize
# import argparse
from argparse import Namespace
from torchvision import transforms
from torch.nn import functional as F
import torchvision
import matplotlib.pyplot as plt
# from model.dualstylegan import DualStyleGAN
# from model.sampler.icp import ICPTrainer
from model.encoder.psp import pSp
import os
import dlib
from model.encoder.align_all_parallel import align_face
import wget, bz2

os.environ['CUDA_VISIBLE_DEVICES'] = "0"
# os.chdir('../')
CODE_DIR = './'
MODEL_DIR = os.path.join(CODE_DIR, 'checkpoint')
DATA_DIR = os.path.join( CODE_DIR, 'data')
device = 'cuda'

# load encoder
model_path = os.path.join(MODEL_DIR, 'encoder.pt')
ckpt = torch.load(model_path, map_location='cpu')
opts = ckpt['opts']
opts['checkpoint_path'] = model_path
opts = Namespace(**opts)
opts.device = device
encoder = pSp(opts)
encoder.eval()
encoder = encoder.to(device)
print('Model successfully loaded!')

transform = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(256),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
    ]
)

def run_alignment(image_path):
    modelname = os.path.join(MODEL_DIR, 'shape_predictor_68_face_landmarks.dat')
    if not os.path.exists(modelname):
        wget.download('http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2', modelname+'.bz2')
        zipfile = bz2.BZ2File(modelname+'.bz2')
        data = zipfile.read()
        open(modelname, 'wb').write(data)
    predictor = dlib.shape_predictor(modelname)
    aligned_image = align_face(filepath=image_path, predictor=predictor)
    return aligned_image


def createEmbeddingImage(image_path, transform, encoder):
    I = transform(run_alignment(image_path)).unsqueeze(dim=0).to(device)

    with torch.no_grad():
        img_rec, instyle = encoder(I, randomize_noise=False, return_latents=True,
                                z_plus_latent=True, return_z_plus_latent=True, resize=False)
        img_rec = torch.clamp(img_rec.detach(), -1, 1)
    return img_rec

def saveImg(img, img_name):
    vis = torchvision.utils.make_grid(F.adaptive_avg_pool2d(torch.cat([img], dim=0), 256), 1,1)
    plt.figure(figsize=(3,3),dpi=120)
    visualize(vis.cpu())
    plt.show()
    plt.savefig(f'../results/{img_name}.png')

img_dir = '../data/represent'
for img_name in os.listdir(img_dir):
    img_path = f'{img_dir}/{img_name}'
    saveImg(createEmbeddingImage(img_path, transform, encoder), img_name)