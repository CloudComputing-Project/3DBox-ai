#!/bin/bash

#base_dir="/home/janett1005/project/data/crop/merge"
base_dir="/project/data/crop/merge"
#tfds_dir="/home/janett1005/project/data/tfrecord"
tfds_dir="/project/data/tfrecord"
#script_path="/home/janett1005/project/few-shot-gan/dataset_tool.py"
script_path="/project/few-shot-gan/dataset_tool.py"

for folder in "$base_dir"/*; do
    echo "Try: $folder"
  if [ -d "$folder" ]; then
    target_path="$tfds_dir/$(basename $folder)"
    echo "Processing: $folder"
    echo "Target TFDS path: $target_path"
    
    python $script_path create_from_images $target_path $folder --resolution 1024 --partition 1
    
    echo "Finished processing $folder"
  fi
done

echo "All folders processed."
