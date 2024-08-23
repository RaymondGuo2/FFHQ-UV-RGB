import torch
from model.hifi3dpp import ParametricFaceModel
import os
from utils.mesh_utils import write_mesh_obj

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

if __name__ == '__main__':
    # Load the coefficients file
    coeffs = torch.load('../coeff_testing_framework/stage3_coeffs.pt')
    # Manipulate a desired expression basis
    coeffs_dict = split_coeff(coeffs)
    coeffs_dict['exp'][0, 0] += 0.5

    # Initialise the parametric model for expression alteration
    fm_model_path = '../topo_assets/hifi3dpp_model_info.mat'
    unwrap_info_path = '../topo_assets/unwrap_1024_info.mat'
    face_model = ParametricFaceModel(fm_model_file=fm_model_path, unwrap_info_file=unwrap_info_path)
    
    # Save mesh
    output_path = '../coeff_testing_framework'
    mesh_name = 'exp1_1.obj'
    saved_meshes = save_mesh(path=output_path, mesh_name=mesh_name, coeffs=coeffs, facemodel=face_model)
    print(f"Saved mesh files: {saved_meshes}")
