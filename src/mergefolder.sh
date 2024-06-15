#!/bin/bash

project_dir="/home/janett1005/project/data/crop"
output_base_dir="/home/janett1005/project/data/crop/merge"

cd "$project_dir"
folders=($(ls -d 20*/))

group_size=5

for (( i=0; i<${#folders[@]}; i+=group_size )); do
  start_folder="${folders[i]%/}" 
  end_folder="${folders[i+group_size-1]%/}" 

  group_folder="${start_folder}_to_${end_folder}"
  mkdir -p "$output_base_dir/$group_folder"

  for (( j=i; j<i+group_size && j<${#folders[@]}; j++ )); do
    cp "${folders[j]}"/* "$output_base_dir/$group_folder/"
    echo "모든 그룹의 이미지가 새 폴더로 복사되었습니다."
  done
done