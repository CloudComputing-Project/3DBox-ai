<!-- @article{robb2020fsgan,
  title   = {Few-Shot Adaptation of Generative Adversarial Networks},
  author  = {Robb, Esther and Chu, Wen-Sheng and Kumar, Abhishek and Huang, Jia-Bin},
  journal = {arXiv preprint arXiv:2010.11943},
  year    = {2020}
} -->

## preparing datasets
for year in {2004..2013}; do
python /project/few-shot-gan/dataset_tool.py \
create_from_images \
/project/data/tfrecords/$year \
/project/data/crop/$year \
--resolution 1024 \
--partition 1
done


## training networks
python /project/few-shot-gan/run_training.py \
--config=config-ada-sv-flat \
--data-dir=/project/data/tfrecords/2004 \
--dataset-train=/project/data/tfrecords/2004/train \
--dataset-eval=/project/data/tfrecords/2004/eval \
--resume-pkl-dir=/project/models \
--resume-pkl='gogh-pca-000020.pkl' \
--total-kimg=9 \
--metrics=None

gpu_executor.cc:991] could not open file to read NUMA node: /sys/bus/pci/devices/0000:2d:00.0/numa_node
Your kernel may have been built without NUMA support.

ass.cc:1412] (One-time warning): Not using XLA:CPU for cluster because envvar TF_XLA_FLAGS=--tf_xla_cpu_global_jit was not set.  If you want XLA:CPU, either set that envvar, or use experimental_jit_scope to enable XLA:CPU.  To confirm that XLA is active, pass --vmodule=xla_compilation_cache=1 (as a proper command-line flag, not via TF_XLA_FLAGS) or set the envvar XLA_FLAGS=--xla_hlo_profile.

https://atsit.in/176