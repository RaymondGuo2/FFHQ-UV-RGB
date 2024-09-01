# FFHQ-UV RGB-Fitting Implementation

This is an implementation of the RGB UV-texture map fitting from the original FFHQ-UV repository, which can be found [here](https://github.com/csbhr/FFHQ-UV). The relevant research paper is linked below:

### FFHQ-UV: Normalized Facial UV-Texture Dataset for 3D Face Reconstruction
By [Haoran Bai](https://csbhr.github.io/), [Di Kang](https://scholar.google.com.hk/citations?user=2ztThPwAAAAJ&hl=zh-CN), Haoxian Zhang, [Jinshan Pan](https://jspan.github.io/), and [Linchao Bao](https://linchaobao.github.io/)  
*In CVPR 2023 [[Paper: https://arxiv.org/abs/2211.13874]](https://arxiv.org/abs/2211.13874)*  
*Rendering demos [[YouTube video]](https://youtu.be/dXFRJODJlNY)*

The **FFHQ-UV** dataset comprises over 50,000 texture maps, derived from a multi-step methodology taking single 
"in-the-wild" images as input and rendering complete UV-texture maps for head models. Using this FFHQ-UV dataset, a 
GAN-based texture decoder was trained to simplify the single image to texture map process, with the further capacity to integrate with head 
model .OBJ files. In this repository, the steps to successful reproduction are described, with further code implementation used to facilitate ease 
of reconstruction for various applications.

## Step 1: Install Dependencies

Create a conda environment for the project. Ensure that the Python version is specified at 3.7, which is crucial for managing the Tensorflow 
dependency.

```
conda create -n myenv python=3.7
conda activate myenv
```

Install the following dependencies:
- dlib: `pip install dlib`
- PyTorch 1.7.1: `pip install torch==1.7.1 torchvision==0.8.2 torchaudio==0.7.2`
- TensorBoard: `pip install tensorboard`
- TensorFlow 1.15.0: `pip install tensorflow-gpu==1.15.0`
- Other packages: `pip install tqdm scikit-image opencv-python pillow imageio matplotlib mxnet Ninja google-auth google-auth-oauthlib click requests pyspng imageio-ffmpeg==0.4.3 scikit-learn torchdiffeq==0.0.1 flask kornia==0.2.0 lmdb psutil dominate rtree`
- **Important: OpenCV's version needs to be higher than 4.5, otherwise it will not work well.**

PyTorch3D and Nvdiffrast are important third party packages, and can be downloaded by executing these commands in the environment:

```
mkdir thirdparty
cd thirdparty
git clone https://github.com/facebookresearch/iopath
git clone https://github.com/facebookresearch/fvcore
git clone https://github.com/facebookresearch/pytorch3d
git clone https://github.com/NVlabs/nvdiffrast
conda install -c bottler nvidiacub
pip install -e iopath
pip install -e fvcore
pip install -e pytorch3d
pip install -e nvdiffrast
```

One might find that pip installing outside of the third party directories might not work, so it may be worth entering each third party directory separately, and executing `pip install -e .`. A likely source of the issue may lie in the compilation of [PyTorch3D](https://pytorch3d.org/) due to it being highly dependent on CUDA versions. If one is operating on Linux using the conda environment, a potential solution could be 
found in `conda install pytorch3d -c pytorch3d`. Alternatively, one might try to install from source:

```angular2html
pip install "git+https://github.com/facebookresearch/pytorch3d.git"
```

For more details on the installation of PyTorch3D, the link to the installation guide can be found [here](https://github.
com/facebookresearch/pytorch3d/blob/main/INSTALL.md).

Given the dependencies involving PyTorch and Tensorflow and managing deprecated versions as was implemented in the original paper, it is crucial 
to ensure that the right CUDA dependencies are established. In this implementation, a working version was achieved using CUDA 10.0.130 with 
CUDNN 7.6.4.38. These environment variables must be set in the `.bashrc` file shown below (note that `export FORCE_CUDA=1` is used to explicitly 
specify CUDA support for PyTorch3D).  

```angular2html
export CUDA_HOME=/vol/cuda/10.0.130-cudnn7.6.4.38
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
export FORCE_CUDA=1
```

## Step 2: Download Checkpoints and Topology Assets
The checkpoints and topology assets must be downloaded in order to run the scripts. For details on how to download and organise these files, refer 
to the [[README]](./README_ckp_topo.md) by Bai et al. Put simply, new directories called `checkpoints` and `topo_assets` must be created in the 
root directory containing their respective files.

## Step 3: Load Input Images
The final preparation step is to load the images ready for fitting. Note that this must be specified in either '.jpg', '.jpeg' or '.png' format. 
These need to be placed in a directory structure like so, whereby the images (can be any amount) must be placed inside the inputs folder, but not 
inside the `processed_data` and `processed_data_vis` folders.

```
|--FFHQ-UV-RGB  
    |--data 
        |--inputs
            |--processed_data
            |--processed_data_vis
            |--image1.png
            |--image2.jpg
            |--image3.jpeg
            |--image4.jpg
            |-- ...
```

Since some images may hold potential metadata affecting the face detection algorithm in the code, it is advised to preprocess these images, which 
can be done automatically by executing these commands.

```angular2html
cd utils
python process_image.py
```

After the first time running the source code, it may be desired to clear the files in the input and output folders ready for another batch (or 
single) image. A simple script in the utils folder can be run to do so:

```angular2html
python clear_data.py
```

## Step 3: Run Source Codes

With the conda environment activated, CUDA environment variables sorted, checkpoints and topology assets downloaded, and input images established 
and processed, the reconstruction code can be run to obtain the outputs. Simply enter back into the root directory, and execute:

```angular2html
sh run_rgb_fitting.sh
```
This will run the entire pipeline altogether, including the fitting of eyeballs.

## Step 4: Visualising the Output

Once the model has completed its run, the final output is ready to visualise. The results of each image will be stored in their own separate 
folders in the output, with 7 crucial files to notice:

```angular2html
# Head mesh and texture
stage3_mesh_id.obj
stage3_mesh.mtl
stage3_uv.png

# Eye mesh and texture
L_ball.obj
R_ball.obj
eye_ball_tex.mtl
eye_ball_tex.png
```

There are two ways to visualise these results as a reconstructed head. The first is to install MeshLab, and load all three OBJ files, which should 
automatically import the texture through material files. The second is to use Blender, which is slightly more complicated, but offers more 
flexibility in applying to further applications such as loading the model into Unity. The steps for establishing the Blender processing pipeline 
are described below.

### Blender Pipeline Steps

**Step 1**
Ensure that Blender has been downloaded and you can access the command line tool. This can be checked simply by typing `blender` in the console. 
In some cases, it may not return a value even if Blender has been downloaded. In that case, you can either export the path directly into the 
command line or adding it to the end of the `.bashrc` file. An example for MacOS is shown, but can be tweaked for other OS.

```angular2html
export PATH=$PATH:/Applications/Blender.app/Contents/MacOS
```

**Step 2**
After this, another path variable called `FILE_DIR` must be exported, serving as an argument to the python blender command pointing towards the 
output directory that you want to blend. For example, if one wants to apply the head model for LeBron James in the output directory `lebron_james`, the below 
command is an example:

```angular2html
export FILE_DIR="/Users/rqg/Desktop/FFHQ-UV-RGB/data/outputs/lebron_james"
```
Note two things of crucial importance. Firstly, make sure to export the absolute and not relative path, and secondly, do not add `"/"` to the end 
of the path. 

**Step 3**
Once `FILE_DIR` has been exported, you can finally run the command below by entering into the utils directory and executing blend.py 
through Blender (4.0???):

```angular2html
blender --background --python blend.py
```

**Step 4**

Enter into the output directory, and there should be a `.blend` file named after your directory (e.g. `lebron_james.blend`). Click into the file 
provided you have a local version of Blender, and a rendered model should be available to see in the main view. If you are unable to see the 
texture colouring, simply click the Material Preview sphere for Viewport shading, or go to the shading tab.


## Citation

This reproduction uses the code [here](https://github.com/csbhr/FFHQ-UV), and is based off the paper cited below.

```
@InProceedings{Bai_2023_CVPR,
  title={FFHQ-UV: Normalized Facial UV-Texture Dataset for 3D Face Reconstruction},
  author={Bai, Haoran and Kang, Di and Zhang, Haoxian and Pan, Jinshan and Bao, Linchao},
  booktitle={IEEE Conference on Computer Vision and Pattern Recognition},
  month={June},
  year={2023}
}
```

## Acknowledgments
This implementation builds upon the awesome works done by Tov et al. ([e4e](https://github.com/omertov/encoder4editing)), Zhou et al. ([DPR](https://github.com/zhhoper/DPR)), Abdal et al. ([StyleFlow](https://github.com/RameenAbdal/StyleFlow)), and Karras et al. ([StyleGAN2](https://github.com/NVlabs/stylegan2), [StyleGAN2-ADA-PyTorch](https://github.com/NVlabs/stylegan2-ada-pytorch), [FFHQ](https://github.com/NVlabs/ffhq-dataset)).

This work is based on [HiFi3D++](https://github.com/czh-98/REALY) topology, and was supported by Tencent AI Lab.
