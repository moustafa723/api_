import os
import nibabel as nib
import numpy as np
import trimesh
from skimage.measure import marching_cubes


def nifti_to_glb(liver_mask_path, tumor_mask_path, output_path):
    """
    Convert liver_mask_pvp.nii.gz + mask_pvp.nii.gz
    into one GLB file.
    """

    print("Loading masks...")

    liver = nib.load(liver_mask_path).get_fdata()
    tumor = nib.load(tumor_mask_path).get_fdata()

    print("\nLiver Labels :", np.unique(liver))
    print("Tumor Labels :", np.unique(tumor))

    print("Liver Voxels :", np.sum(liver > 0))
    print("Tumor Voxels :", np.sum(tumor > 0))

    print("\nCreating Liver Mesh...")

    liver_volume = (liver > 0).astype(np.uint8)

    liver_vertices, liver_faces, liver_normals, _ = marching_cubes(
        liver_volume,
        level=0.5
    )

    liver_mesh = trimesh.Trimesh(
        vertices=liver_vertices,
        faces=liver_faces,
        vertex_normals=liver_normals,
        process=False
    )

    liver_mesh.visual.vertex_colors = [170, 140, 110, 255]

    print("Creating Tumor Mesh...")

    tumor_volume = (tumor > 0).astype(np.uint8)

    tumor_vertices, tumor_faces, tumor_normals, _ = marching_cubes(
        tumor_volume,
        level=0.5
    )

    tumor_mesh = trimesh.Trimesh(
        vertices=tumor_vertices,
        faces=tumor_faces,
        vertex_normals=tumor_normals,
        process=False
    )

    tumor_mesh.visual.vertex_colors = [255, 0, 0, 255]

    print("Combining Meshes...")

    scene = trimesh.Scene()
    scene.add_geometry(liver_mesh)
    scene.add_geometry(tumor_mesh)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    scene.export(output_path)

    print("\nGLB Saved Successfully")
    print(output_path)