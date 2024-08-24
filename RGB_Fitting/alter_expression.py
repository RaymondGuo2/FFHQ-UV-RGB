import torch
from model.hifi3dpp import ParametricFaceModel
import os
from utils.mesh_utils import write_mesh_obj
import argparse

# Non-class implementation of split_coeff found in hifi3dpp.py
def split_coeff(coeffs):
    '''
    Split the estimated coeffs.
    '''

    if isinstance(coeffs, dict):
        coeffs = coeffs['coeffs']

    # Explicit indices for the coefficients
    id_coeffs = coeffs[:, :532] 
    exp_coeffs = coeffs[:, 532:532 + 45]
    tex_coeffs = coeffs[:, 532 + 45:532 + 45 + 439]
    angles = coeffs[:, 532 + 45 + 439:532 + 45 + 439 + 3]
    gammas = coeffs[:, 532 + 45 + 439 + 3:532 + 45 + 439 + 3 + 27]
    translations = coeffs[:, 532 + 45 + 439 + 3 + 27:]

    return {
        'id': id_coeffs,
        'exp': exp_coeffs,
        'tex': tex_coeffs,
        'angle': angles,
        'gamma': gammas,
        'trans': translations
    }


# Non-class implementation of save_mesh in ours_fit_model.py
def save_mesh(path, mesh_name, coeffs, facemodel):
    if isinstance(coeffs, dict):
        coeffs = coeffs['coeffs']
    coeffs_dict = facemodel.split_coeff(coeffs)
    
    pred_id_vertex, pred_exp_vertex, pred_alb_tex = facemodel.compute_for_mesh(coeffs_dict)
    
    exp_mesh_info = {
        'v': pred_exp_vertex.detach()[0].cpu().numpy(),
        'vt': pred_alb_tex.detach()[0].cpu().numpy(),
        'fv': facemodel.head_buf.cpu().numpy()
    }
    
    exp_mesh_path = os.path.join(path, f'{mesh_name[:-4]}_exp{mesh_name[-4:]}')
    write_mesh_obj(mesh_info=exp_mesh_info, file_path=exp_mesh_path)
    return exp_mesh_path

def main(args):
    # Setup for chnaging expression basis coefficient values
    coeffs = torch.load(args.model_coeffs_path)
    coeffs_dict = split_coeff(coeffs)
    if args.exp_component < 1 or args.exp_component > 45:
        print("The expression component must be between 1 and 45")
        return
    if args.change_value < -2.0 or args.change_value > 2.0:
        print("The amount changed must be between -2 and 2")
        return
    coeffs_dict['exp'][0, args.exp_component - 1] += args.change_value

    # Initialise the parametric model for expression alteration
    face_model = ParametricFaceModel(fm_model_file='../topo_assets/hifi3dpp_model_info.mat', unwrap_info_file='../topo_assets/unwrap_1024_info.mat')
    output_path = args.output_path
    mesh_name = str(args.exp_component) + "_" + str(args.change_value) + ".obj"
    saved_mesh = save_mesh(path=output_path, mesh_name=mesh_name, coeffs=coeffs, facemodel=face_model)
    print(f"Saved mesh files: {saved_mesh}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_coeffs_path', type=str, default='../coeff_testing_framework/stage3_coeffs.pt', help="Provide the path to the outputted estimated coefficients in .pt format")
    parser.add_argument('exp_component', type=int, help="Provide a component from 1 to 45 to modify")
    parser.add_argument('change_value', type=float, help="Provide a float value from -2 to 2 to alter the component expression")
    parser.add_argument('--output_path', type=str, default='../coeff_testing_framework', help="Specify where to output the completed obj")    
    args = parser.parse_args()
    main(args)