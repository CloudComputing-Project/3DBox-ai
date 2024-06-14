import numpy as np
import shutil
from deepface import DeepFace
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

def verification_face(main_image_dir, input_dir, year, model, detector):
    """

    """
    main_distance=np.inf
    main_img_name = ''

    for image_name in os.listdir(input_dir):
        img_dir = os.path.join(input_dir, image_name)
        result = DeepFace.verify(main_image_dir, img_dir,
                                 detector_backend='skip',
                                 model_name= model, normalization = "base",
                                 distance_metric = "cosine",
                                #  enforce_detection=False,
                                 silent=True)
        print(f'{image_name} / {result["distance"]}' )
        if result['verified'] and result['distance'] < main_distance:
            main_distance = result['distance']
            main_img_name = image_name
    
    print(f"Year : {year} , main distance : {main_distance}") 
    return main_img_name

def chain_verification_face(main_img_name, model, detector):
    output_dir = f'data/represent'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for year_idx, year in enumerate(os.listdir('data/crop')[::-1]):
        input_dir=f'data/crop/{year}'

        if year_idx==0:
            continue
        else:
            main_img_name = verification_face(f"{output_dir}/{main_img_name}", input_dir, year, model, detector)
            shutil.copy2(f'{input_dir}/{main_img_name}', f"{output_dir}/{main_img_name}")
            
models=["VGG-Face"]
detectors=["retinaface"]
main_img_name = '2013_image10_face0.jpg'

for model in models:
    for detector in detectors:
        chain_verification_face(main_img_name, model, detector)