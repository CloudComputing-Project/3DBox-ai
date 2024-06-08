#!/bin/bash

# 대상 폴더 설정
#base_dir="/home/janett1005/project/data/crop/merge"
base_dir="/project/data/crop/merge"
# 출력할 tfds 디렉토리의 기본 경로
#tfds_dir="/home/janett1005/project/data/tfrecord"
tfds_dir="/project/data/tfrecord"
# Python 스크립트 위치
#script_path="/home/janett1005/project/few-shot-gan/dataset_tool.py"
script_path="/project/few-shot-gan/dataset_tool.py"
# 각 폴더를 순회하면서 Python 스크립트 실행
for folder in "$base_dir"/*; do
    echo "Try: $folder"
  if [ -d "$folder" ]; then  # 폴더인지 확인
    # tfds 경로에 폴더 이름을 사용
    target_path="$tfds_dir/$(basename $folder)"
    echo "Processing: $folder"
    echo "Target TFDS path: $target_path"
    
    # dataset_tool.py 스크립트 실행
    python $script_path create_from_images $target_path $folder --resolution 1024 --partition 1
    
    echo "Finished processing $folder"
  fi
done

echo "All folders processed."
