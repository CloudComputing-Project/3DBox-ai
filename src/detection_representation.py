import os
from PIL import Image
from deepface import DeepFace
import pickle


def detection_representation_faces(year, detector, model):
    '''
    폴더의 모든 이미지에서 얼굴 detection후 encoding 값 dict로 저장
    파일명에 ASCII문자만 포함하는 이미지만 고려 
    '''
    input_dir = f'data/original_date_corrected/{year}'
    output_dir = f'data/faces'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    images_dir=[]
    for f in os.listdir(input_dir):
        if f.endswith(('.jpg', '.jpeg', '.png')):
            try: 
                f.encode('ascii')
                images_dir.append(os.path.join(input_dir, f))
            except UnicodeEncodeError:
                continue

    face_representations_dict={}
    for image_idx, image_dir in enumerate(images_dir):
        # face detection -> alignment -> normalization -> face representation
        # return : list, 얼굴 하나당 dictionary 1개
        try: 
            # if model in 'VGG'
            # Default is base. Options: base, raw, Facenet, Facenet2018, VGGFace, VGGFace2, ArcFace
            face_representations = DeepFace.represent(image_dir,
                                            detector_backend=detector,
                                            normalization='base', model_name=model)
        except ValueError:
            continue

        for face_idx, face_representation in enumerate(face_representations):
            crop_save_face(image_dir, image_idx, face_idx, face_representation['facial_area'], output_dir+f'/{year}_{detector}_{model}')
            face_representations_dict[f'image{image_idx}_face{face_idx}'] = face_representation['embedding']
    
    with open(f'{output_dir}/{year}_face_representations_{model}.pickle','wb') as fw:
        pickle.dump(face_representations_dict, fw)

def crop_save_face(image_dir, image_idx, face_idx, facial_area, output_dir):
    """
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image=Image.open(image_dir)
    image = image.convert('RGB') # RGBA형식의 이미지는 RGB형식 이미지인 JPEG파일로 저장이 불가능

    top, right, bottom, left = facial_area['y'], facial_area['x']+facial_area['w'], facial_area['y']+facial_area['h'], facial_area['x']
    face_image = image.crop((left, top, right, bottom))

    face_filename = f"image{image_idx}_face{face_idx}.jpg"
    face_image.save(os.path.join(output_dir, face_filename))

# years = os.listdir('data/original_date_corrected')
years=['2022', '2023']
detectors = ['retinaface']#'opencv', 'retinaface','mtcnn', 'ssd','', 'yolov8', 'centerface', 'mediapipe'
models = ['VGG-Face'] #'VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'SFace' 'GhostFaceNet'
for detector in detectors:
    for model in models:
        for year in years:
            detection_representation_faces(year, detector, model)