from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, UploadFile, File
from conf import *
from pathlib import Path
import boto3
import os

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class DownloadRequest(BaseModel):
    user_id: str


app = FastAPI()


# boto3 클라이언트 생성
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

#uvicorn main:app --reload
@app.post("/download")
async def download_files(user_id: str, file: UploadFile = File(...)):
    
 # folder = f'crop/{request.user_id}/'
 # user_id + imagefile이름 + uuid
    folder = f'{user_id}/'
    local_base_directory = f'project/data/{user_id}/crop/'
    
    
    try:
        #대표 이미지 1개 업로드받아 로컬 "downloads/main/{user_id}" 디렉토리에 저장
        save_directory = f"project/main/{user_id}"
        os.makedirs(save_directory, exist_ok=True)
        
        file_path = os.path.join(save_directory, file.filename)
        
        file_path = os.path.join(save_directory, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.read())
        
        print({"message": f"File '{file.filename}' uploaded successfully"}) 
    
        # S3 객체 목록 가져오기
        response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME, Prefix=folder)
        print(response)
        if 'Contents' not in response:
            raise HTTPException(status_code=404, detail="No objects found in the specified folder")

        #각 객체에 대한 정보는 'Contents'라는 키를 사용하여 접근
        #obj는 S3 버킷 내의 한 객체에 대한 정보를 담고 있는 사전
        for obj in response['Contents']:
            key = obj['Key']
            
             # 연도 추출
            year = key.split('/')[1]
            
            local_year_directory = local_base_directory
            local_year_directory += year + "/"
            
            if not os.path.exists(local_year_directory):
                os.makedirs(local_year_directory)
            
            #이미지 파일명 추출
            filename = key.split('/')[2]
            local_year_directory += filename
            
            # S3 객체 다운로드
            s3_client.download_file(AWS_BUCKET_NAME, key, local_year_directory)

        return {"message": "Files downloaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name in {ModelName.alexnet, ModelName.resnet}:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
@app.post("/items/")
async def create_item(item: Item):
    return {"item": item}