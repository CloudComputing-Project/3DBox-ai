# 3DBox-ai
image dropbox에서 GAN을 활용
사용자가 드롭박스에 저장한 이미지들을 활용해 시간에 따른 사용자의 얼굴 변화를 초상화로 그려 보여주기 위한 기능 구현

* model : DualStyleGAN
* data : CACD2000의 EmmaWatson 이미지

## 필요성
![image](https://github.com/CloudComputing-Project/3DBox-ai/assets/81574359/0d72f9e9-9f93-4d66-9ebe-6f26d2f00a30)
![image](https://github.com/CloudComputing-Project/3DBox-ai/assets/81574359/b35828a6-3a1e-4fb5-85b9-8f0115dc6f04)

## Problems & Requirements
![image](https://github.com/CloudComputing-Project/3DBox-ai/assets/81574359/a12a8c90-4998-4d1a-a38c-f21b7b3428ed)
![image](https://github.com/CloudComputing-Project/3DBox-ai/assets/81574359/7b5ca993-d000-4409-89fc-57bb7ea0cb96)
![image](https://github.com/CloudComputing-Project/3DBox-ai/assets/81574359/d91940a7-01ef-4ae5-8c6a-6eff819c4e7b)
![image](https://github.com/CloudComputing-Project/3DBox-ai/assets/81574359/e4306cc9-75e0-41d3-96b3-e19df0e48d52)
![image](https://github.com/CloudComputing-Project/3DBox-ai/assets/81574359/80cfdb8b-01b9-464a-8f32-c5331a813ee7)
![image](https://github.com/CloudComputing-Project/3DBox-ai/assets/81574359/243fc2d0-d971-4116-ad51-531f90625de7)

### 주의 
해당 github 코드는 Google Cloud platform의 compute instance와 AWS Lambda, AWS EC2에서 사용하기 위해 AI 파트만 부분적으로 작성한 코드로, local에서는 작동하지 않음.
'CloudComputing-Project' organization에서의 backend, frontend repository 참조 필요 
