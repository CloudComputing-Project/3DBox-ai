import os
import re
from PIL import Image
import shutil
from datetime import datetime

def extract_date_from_filename(filename):
    """
    이미지 파일 명에서의 날짜 데이터 추출
    날짜 데이터가 없는 경우, None return

    날짜 데이터 판단 기준
    1. data_patrerns가 가장 앞에 위치한 경우, 뒤에 _or - or “ ”
    2. data_patrerns가 가장 앞에 위치하지 않은 경우, (앞에 _or - or “ ”) and (뒤에 _or - or “ ”)
    """
    date_patterns = [
        r"\d{4}-\d{2}-\d{2}",  # YYYY-MM-DD
        r"\d{2}-\d{2}-\d{2}",  # YY-MM-DD
        r"\d{4}\d{2}\d{2}",     # YYYYMMDD
        r"\d{2}\d{2}\d{2}",     # YYMMDD
    ]
    for pattern in date_patterns:
        patterns=fr"\s{pattern}\s|_{pattern}_|-{pattern}_|-{pattern}-|_{pattern}-"
        start_patterns = fr"{pattern}\s|{pattern}_|{pattern}-"

        match = re.search(patterns, filename)
        if match==None:
            match = re.match(start_patterns, filename)
        if match:
            date_str = match.group(0)
            date_str=date_str.replace("_", "")
            date_str=date_str.replace("-", "")
            date_str=date_str.replace(" ", "")
            try:
                for fmt in ("%Y%m%d", "%Y-%m-%d", "%y%m%d", "%y-%m-%d"):
                    try:
                        return datetime.strptime(date_str, fmt).date()
                    except ValueError:
                        continue
            except ValueError:
                continue
    return None

def get_image_date(filepath):
    """
    이미지 메타 데이터 상의 촬영 날짜 추출
    이미지 메타 데이터가 존재하지 않는 경우, None return
    """
    try:
        image = Image.open(filepath)
        # Exif 태그에서 날짜 추출
        exif_data = image._getexif()

        if exif_data:
            # Exif DateTimeOriginal'
            datetime_original1=exif_data.get(36867)
            datetime_original2=exif_data.get(306)

            if datetime_original1:
                try:
                    return datetime.strptime(datetime_original1, "%Y:%m:%d %H:%M:%S").date()
                except:
                    return datetime.strptime(datetime_original1, "%Y-%m-%d %H:%M:%S:%f").date()
            elif datetime_original2:
                try:
                    return datetime.strptime(datetime_original2, "%Y:%m:%d %H:%M:%S").date()
                except:
                    return datetime.strptime(datetime_original2, "%Y-%m-%d %H:%M:%S:%f").date()
    except Exception as e:
        print(f"Error reading image data: {e}")
    return None

def classify_images(input_year):
    """
    이미지 파일명 혹은 이미지 메타데이터 상의 촬영 날짜와 사용자 업로드 날짜가 다른 경우, 전자를 촬영 날짜로 설정 후 이미지 이동

    촬영 날짜 판단 우선 순위
    1. 이미지 파일명 상의 촬영 일자
    2. 이미지 메타데이터 상의 촬영일자
    3. 이미지 업로드 일자
    """
    input_dir = f'data/original/{input_year}'
    output_dir = f'data/original_date_corrected'

    images_filename = [filename for filename in os.listdir(input_dir) if filename.endswith(('.jpg', '.jpeg', '.png'))]
    for filename in images_filename:
        filepath = os.path.join(input_dir, filename)
        
        date_from_filename = extract_date_from_filename(filename)
        date_from_metadata = get_image_date(filepath)

        if date_from_filename != None:
            date = date_from_filename
        elif date_from_metadata:
            date = date_from_metadata
        else:
            date=None
        
        if date==None:
            year_folder = os.path.join(output_dir, str(input_year))
        else:
            year_folder = os.path.join(output_dir, str(date.year))

        if not os.path.exists(year_folder):
            os.makedirs(year_folder)
        
        shutil.move(filepath, os.path.join(year_folder, filename))

# 2020, 2021 제외
for input_year in os.listdir('data/original'): 
    classify_images(input_year)
