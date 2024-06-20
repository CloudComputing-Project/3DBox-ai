import os
import re
from datetime import datetime, timezone
import boto3
import io
import json
from PIL import Image

def lambda_handler(event, context):
    try:
        s3_client = boto3.client('s3')
        bucketName = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        uploadTime = event['Records'][0]['eventTime']
        uploadYear = datetime.fromisoformat(uploadTime.replace('Z', '')).replace(tzinfo=timezone.utc).year
        print('메타데이터 준비 완료')
        
        # S3에서 이미지 파일 가져오기
        response = s3_client.get_object(Bucket=bucketName, Key=key)
        image_content = response['Body'].read()
        print('이미지 준비 완료')
        
        year = classify_images(image_content, key, uploadYear)
        return {
            'statusCode': 200,
            'body': {
                'Year': year
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
        
def classify_images(image_content, key, uploadYear):
    """
    조건 : input이 이미지일 경우만 진행
    input : 이미지 경로
    output : 이미지의 촬영 연도(int)
    
    이미지 파일명 혹은 이미지 메타데이터 상의 촬영 날짜와 사용자 업로드 날짜가 다른 경우, 전자를 촬영 날짜로 설정

    촬영 날짜 판단 우선 순위
    1. 이미지 파일명 상의 촬영 일자
    2. 이미지 메타데이터 상의 촬영일자
    3. 이미지 업로드 일자
    """
    if key.endswith(('.jpg', '.jpeg', '.png')):
        date_from_filename = extract_date_from_filename(key)
        date_from_metadata = get_image_date(image_content)

        if date_from_filename != None:
            return date_from_filename.year
        elif date_from_metadata:
            return date_from_metadata.year
        else:
            return uploadYear
    return uploadYear

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

  
def get_image_date(image_content):
    """
    이미지 메타 데이터 상의 촬영 날짜 추출
    이미지 메타 데이터가 존재하지 않는 경우, None return
    """
    try:
        image = Image.open(io.BytesIO(image_content))
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
