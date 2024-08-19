#!/bin/bash
#SBATCH --job-name=rgb_fitting
#SBATCH --gres=gpu:1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=rqg23
set -e

/usr/bin/nvidia-smi
uptime

######################### Configuration #########################
# input_dir: the directory of the input images
# output_dir: the directory of the output results
# checkpoints_dir: the directory of the used checkpoints
# topo_assets_dir: the directory of the topo assets, e.g., 3DMM, masks, etc.
#################################################################
input_dir=../data/inputs
output_dir=../data/outputs
checkpoints_dir=../checkpoints
topo_assets_dir=../topo_assets


#################### Step 1. Preprocess Data ####################
# Read the input images in ${input_dir}
# Save the processed data in ${input_dir}/processed_data and ${input_dir}/processed_data_vis
#################################################################
cd ./RGB_Fitting
python step1_process_data.py \
    --input_dir ${input_dir} \
    --output_dir ${input_dir}/processed_data \
    --checkpoints_dir ${checkpoints_dir} \
    --topo_dir ${topo_assets_dir}


###################### Step 2. RGB Fitting ######################
# Read the processed data in ${input_dir}/processed_data
# Save the output results in ${output_dir}
#################################################################
python step2_fit_processed_data.py \
    --input_dir ${input_dir}/processed_data \
    --output_dir ${output_dir} \
    --checkpoints_dir ${checkpoints_dir} \
    --topo_dir ${topo_assets_dir} \
    --texgan_model_name texgan_ffhq_uv.pth


###################### Step 3. Add Eyeballs #####################
# Obtain necessary files from output for eyeballs
# Save the output results in directory 'render_files'
#################################################################
cd ../Mesh_Add_EyeBall
mesh_dir=$(find ${output_dir} -mindepth 1 -maxdepth 1 -type d | head -n 1)

python run_mesh_add_eyeball.py \
    --mesh_path ${mesh_dir}/stage3_mesh_id.obj



# ###################### Step 3. Obtain blend file ################
# # Blend the outputs
# #################################################################
# cd ..
# export PATH=$PATH:/Applications/Blender.app/Contents/MacOS
# export FILE_DIR="/Users/raymondguo/Desktop/meshesFFHQ/outputs/015309"
# blender --background --python blend_copy.py




