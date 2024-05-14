import numpy as np
import shutil
from deepface import DeepFace
import pickle
import os

def verification_face(gt_representation, year):
    """

    """
    input_dir='data/faces'
    output_dir=f'data/face/{year}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(f'{input_dir}/{year}_face_representations.pickle', 'rb') as fr:
        face_representations = pickle.load(fr)

    gt_face_representations=[]
    for image_face_idx, face_representation in face_representations:
        result = DeepFace.verify(gt_representation, face_representation,
                                 detector_backend='skip',
                                 model_name= "VGG-Face", normalization = "base",
                                 distance_metric = "cosine")
        if result['verified']:
            #crop_save_face(image_dir, image_idx, face_idx, face_representation['facial_area']['img2'], output_dir+f'/{year}')
            shutil.move(f"{input_dir}/{year}/{image_face_idx}", output_dir)
            gt_face_representations.append(face_representation)
    
    return np.mean(gt_face_representations, axis=0)

def chain_verification_face(input_image_dir):
    gt_representations = DeepFace.represent(input_image_dir,
                                            detector_backend='skip',
                                            normalization='base', model_name='VGG-Face')
    gt_representation = gt_representations    

    for year in os.listdir('data/original_date_corrected'):
        gt_representation = verification_face(gt_representation, year)

input_image_dir='data/faces/2023/image92_face0.jpg'
chain_verification_face(input_image_dir)