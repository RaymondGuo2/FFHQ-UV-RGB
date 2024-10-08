# This code was taken directly from the original github implementation of FFHQ-UV (Bai et al. (2023)), which can be found here: https://github.com/csbhr/FFHQ-UV

#!/bin/bash
set -e

/usr/bin/nvidia-smi
uptime


######################### Configuration #########################
# input_dir: the directory of the input images
# output_dir: the directory of the output results
# checkpoints_dir: the directory of the used checkpoints
# topo_assets_dir: the directory of the topo assets, e.g., 3DMM, masks, etc.
#################################################################
input_dir=../fitting_realy/inputs/processed_data_lm86
output_dir=../fitting_realy/outputs
checkpoints_dir=../checkpoints
topo_assets_dir=../topo_assets


########################## RGB Fitting ##########################
# Read the processed data in ${input_dir}
# Save the output results in ${output_dir}
#################################################################
cd ./RGB_Fitting
python step2_fit_processed_data_realy.py \
    --input_dir ${input_dir} \
    --output_dir ${output_dir} \
    --checkpoints_dir ${checkpoints_dir} \
    --topo_dir ${topo_assets_dir} \
    --texgan_model_name texgan_ffhq_uv.pth


####################### Copy Fitted Mesh ########################
# Copy fitted meshes from ${output_dir} to ${output_dir}_fitted_mesh
#################################################################
python step3_copy_fitted_mesh.py \
    --fitted_results_dir ${output_dir} \
    --mesh_dir ${output_dir}_fitted_mesh