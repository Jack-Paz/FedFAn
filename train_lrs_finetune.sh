#! /bin/bash
# data_path='/home/paz/code/phd/fedfan/RAD-NeRF/data/lrs_debug' 
data_path='/home/paz/data/lrs3/trainval_cut' 
pretrained_model='/home/paz/code/phd/fedfan/RAD-NeRF/data/pretrained/obama_eo.pth'

# # train head
# CUDA_VISIBLE_DEVICES=1 python RAD-NeRF/lrs_finetune.py data/obama/ --workspace trial_obama_eo/ -O --iters 200000
# # finetune lips
# CUDA_VISIBLE_DEVICES=1 python RAD-NeRF/lrs_finetune.py data/obama/ --workspace trial_obama_eo/ -O --finetune_lips --iters 250000
# do lrs finetune
CUDA_VISIBLE_DEVICES=1 python RAD-NeRF/lrs_finetune.py $data_path --workspace trial_lrs/ --exp_eye --finetune_lips --iters 250000 --head_ckpt $pretrained_model

# #do torso
# CUDA_VISIBLE_DEVICES=1 python RAD-NeRF/lrs_finetune.py data/obama/ --workspace trial_obama_eo_torso/ -O --torso --iters 200000 --head_ckpt trial_obama_eo/checkpoints/ngp_ep0035.pth
# # test
# CUDA_VISIBLE_DEVICES=1 python RAD-NeRF/lrs_finetune.py data/obama/ --workspace trial_obama_eo_torso/ -O --torso --test


#existing train script:
# #! /bin/bash

# # train
# CUDA_VISIBLE_DEVICES=1 python main.py data/obama/ --workspace trial_obama_eo/ -O --iters 200000
# CUDA_VISIBLE_DEVICES=1 python main.py data/obama/ --workspace trial_obama_eo/ -O --finetune_lips --iters 250000

# CUDA_VISIBLE_DEVICES=1 python main.py data/obama/ --workspace trial_obama_eo_torso/ -O --torso --iters 200000 --head_ckpt trial_obama_eo/checkpoints/ngp_ep0035.pth

# # test
# CUDA_VISIBLE_DEVICES=1 python main.py data/obama/ --workspace trial_obama_eo_torso/ -O --torso --test
