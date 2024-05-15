<!-- @article{robb2020fsgan,
  title   = {Few-Shot Adaptation of Generative Adversarial Networks},
  author  = {Robb, Esther and Chu, Wen-Sheng and Kumar, Abhishek and Huang, Jia-Bin},
  journal = {arXiv preprint arXiv:2010.11943},
  year    = {2020}
} -->

## preparing datasets
years=(2008 {2013..2019} {2021..2023})
for year in "${years[@]}"; do
  python /project/few-shot-gan/dataset_tool.py \
  create_from_images \
  /project/results/data/$year \
  /project/data/nochain/ne/$year \
  --resolution 1024
done

## training networks
python /project/few-shot-gan/run_training.py \
--config=config-ada-sv-flat \
--data-dir=/project/results/data/2008 \
--dataset-train=/project/results/data/2008/train \
--dataset-eval=/project/results/data/2008/eval \
--resume-pkl-dir=/project/results/models \
--total-kimg=3 \
--metrics=None