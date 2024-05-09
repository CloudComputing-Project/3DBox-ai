<!-- @article{robb2020fsgan,
  title   = {Few-Shot Adaptation of Generative Adversarial Networks},
  author  = {Robb, Esther and Chu, Wen-Sheng and Kumar, Abhishek and Huang, Jia-Bin},
  journal = {arXiv preprint arXiv:2010.11943},
  year    = {2020}
} -->

## preparing datasets
python dataset_tool.py \
create_from_images \
/path/to/target/tfds \
/path/to/source/folder \
--resolution 1024

## training networks
python run_training.py \
--config=config-ada-sv-flat \
--data-dir=/path/to/datasets \
--dataset-train=path/to/train \
--dataset-eval=path/to/eval \
--resume-pkl-dir=/path/to/pickles \
--total-kimg=30 \
--metrics=None \