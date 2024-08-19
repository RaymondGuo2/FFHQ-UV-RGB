import os
import bpy

# global values
HEAD_WOUT_EYES_OBJ = "stage3_mesh_id.obj"
HEAD_WOUT_EYES_MTL = "stage3_mesh.mtl"
HEAD_WOUT_EYES_PNG = "stage3_uv.png"

L_BALL_OBJ = "L_ball.obj"
R_BALL_OBJ = "R_ball.obj"
EYEBALL_MTL = "eye_ball_tex.mtl"
EYEBALL_PNG = "eye_ball_tex.png"


# Function to apply texture to the relevant .obj file
def apply_tex2obj(obj_name, mtl_path, png_path):
    # Select the relevant object in the Blender interface
    obj = bpy.data.objects.get(obj_name)
    
    # Smooth the triangular mesh 
    for poly in obj.data.polygons:
        poly.use_smooth = True
        
    # Initialise the material to be used for the .obj (as seen in the Properties tab)    
    material_name = os.path.splitext(os.path.basename(mtl_path))[0]
    material = bpy.data.materials.get(material_name)
    
    if material is None:
        # Create a new material if none exist
        material = bpy.data.materials.new(name=material_name)
    
    # If-else statement to ensure that the primary material for that object is material
    if len(obj.data.materials) == 0:
        obj.data.materials.append(material)
    else:
        obj.data.materials[0] = material
    
    # Load the .png file for the object
    texture_image = bpy.data.images.load(png_path)

    if texture_image:

        # Initialise the node and links system in Blender to connect image textures
        if not obj.active_material.use_nodes:
            obj.active_material.use_nodes = True
        nodes = obj.active_material.node_tree.nodes
        links = obj.active_material.node_tree.links

        # Check if "Image Texture node exists"
        image_texture = nodes.get("Image Texture")
        if not image_texture:
            # Create new node for texture image
            image_texture = nodes.new(type="ShaderNodeTexImage")
            image_texture.location = (-400, 0)
        # Open the .png texture for the object as the image for the image texture node
        image_texture.image = texture_image

        # Obtain node for Principled BSDF (default)
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            # Link the colour output of the image texture node to the base colour input of the BSDF node
            links.new(image_texture.outputs['Color'], bsdf.inputs['Base Color'])


def main():
    
    # Delete all objects first (since a cube is often initialised in Blender)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Crucial environment variable that needs to be set prior to render holding the output directory with the global files!
    file_dir = os.getenv('FILE_DIR', '/path/to/default/dir')

    # Establish path from global variables
    head_obj_path = os.path.join(file_dir, HEAD_WOUT_EYES_OBJ)
    head_mtl_path = os.path.join(file_dir, HEAD_WOUT_EYES_MTL)
    head_png_path = os.path.join(file_dir, HEAD_WOUT_EYES_PNG)
    
    l_ball_obj_path = os.path.join(file_dir, L_BALL_OBJ)
    r_ball_obj_path = os.path.join(file_dir, R_BALL_OBJ)
    eyeball_mtl_path = os.path.join(file_dir, EYEBALL_MTL)
    eyeball_png_path = os.path.join(file_dir, EYEBALL_PNG)
    
    # Import .OBJ files into the scene
    bpy.ops.wm.obj_import(filepath=head_obj_path)
    bpy.ops.wm.obj_import(filepath=l_ball_obj_path)
    bpy.ops.wm.obj_import(filepath=r_ball_obj_path)
    
    # Apply textures to all objects
    apply_tex2obj("stage3_mesh_id", head_mtl_path, head_png_path)
    apply_tex2obj("L_ball", eyeball_mtl_path, eyeball_png_path)
    apply_tex2obj("R_ball", eyeball_mtl_path, eyeball_png_path)
    
    # Deselect all OBJs
    bpy.ops.object.select_all(action='DESELECT')
    # bpy.ops.object.select_all(action="SELECT")
    # bpy.ops.object.join()
    
    # Save the blender file as the name of the output folder
    basename = os.path.basename(file_dir)
    save_as_blend = os.path.join(file_dir, f"{basename}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=save_as_blend)


if __name__ == "__main__":
    main()