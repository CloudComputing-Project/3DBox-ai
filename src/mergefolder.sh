#!/bin/bash

# 대상 디렉토리 설정
project_dir="/home/janett1005/project/data/crop"

# 새로운 폴더를 저장할 상위 디렉토리
output_base_dir="/home/janett1005/project/data/crop/merge"

# 연도별 폴더 정렬 및 배열로 저장
cd "$project_dir"
folders=($(ls -d 20*/))

# 3개 폴더씩 그룹화
group_size=4

# 각 그룹을 순회
for (( i=0; i<${#folders[@]}; i+=group_size )); do
  # 그룹에 대한 새 폴더 생성
  start_folder="${folders[i]%/}"  # 마지막 슬래시 제거
  end_folder="${folders[i+group_size-1]%/}"  # 마지막 슬래시 제거

  group_folder="${start_folder}_to_${end_folder}"
  mkdir -p "$output_base_dir/$group_folder"

  # 현재 그룹의 폴더들에서 모든 이미지를 새 폴더로 복사
  for (( j=i; j<i+group_size && j<${#folders[@]}; j++ )); do
    cp "${folders[j]}"/* "$output_base_dir/$group_folder/"
    echo "모든 그룹의 이미지가 새 폴더로 복사되었습니다."
  done
done