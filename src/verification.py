import numpy as np
import shutil
from deepface import DeepFace
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

def verification_face(gt_representation, year, model, detector):
    """

    """
    input_dir='data/faces'
    output_dir=f'data/face/{year}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(f'{input_dir}/{year}_face_representations_{model}.pickle', 'rb') as fr:
        face_representations = pickle.load(fr)

    gt_face_representations=[]
    for image_face_idx, face_representation in face_representations.items():
        result = DeepFace.verify(list(gt_representation), list(map(float, face_representation)),
                                 detector_backend=detector,
                                 model_name= model, normalization = "base",
                                 distance_metric = "cosine",
                                 silent=True)
        if result['verified']:
            #crop_save_face(image_dir, image_idx, face_idx, face_representation['facial_area']['img2'], output_dir+f'/{year}')
            #shutil.move(f"{input_dir}/{year}_{detector}_{model}/{image_face_idx}.jpg", output_dir)
            shutil.copy2(f"{input_dir}/{year}_{detector}_{model}/{image_face_idx}.jpg", f"{output_dir}/{image_face_idx}_{result['distance']:.4f}.jpg")
            gt_face_representations.append(np.array(face_representation))
    
    return np.mean(gt_face_representations, axis=0)

def chain_verification_face(input_image_dir, model, detector):
    gt_representations = DeepFace.represent(input_image_dir,
                                            detector_backend=detector,
                                            normalization='base', model_name=model)
    gt_representation = list(map(float, gt_representations[0]['embedding']))
    
    for year in os.listdir('data/original_date_corrected')[::-1]:
        gt_representation = verification_face(gt_representation, year, model, detector)

models=["VGG-Face"]
detectors=["retinaface"]
input_image_dir='data/me.jpg'

for model in models:
    for detector in detectors:
        chain_verification_face(input_image_dir, model, detector)