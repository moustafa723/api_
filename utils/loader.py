import os
import nibabel as nib
import numpy as np


def load_case(case_folder):

    ct_path = os.path.join(case_folder, "NIFTI", "pvp.nii.gz")
    liver_path = os.path.join(case_folder, "liver_mask_pvp.nii.gz")
    tumor_path = os.path.join(case_folder, "mask_pvp.nii.gz")

    print("=" * 60)
    print("Loading Case...")
    print("=" * 60)

    print("Loading CT...")
    ct = nib.load(ct_path).get_fdata().astype(np.float32)
    print("CT Loaded")

    print("Loading Liver...")
    liver = nib.load(liver_path).get_fdata().astype(np.uint8)
    print("Liver Loaded")

    print("Loading Tumor...")
    tumor = nib.load(tumor_path).get_fdata().astype(np.uint8)
    print("Tumor Loaded")

    print("Checking Shapes...")

    if ct.shape != liver.shape:
        raise ValueError("CT and Liver mask have different shapes.")

    if ct.shape != tumor.shape:
        raise ValueError("CT and Tumor mask have different shapes.")

    print("Loaded Successfully")

    return ct, liver, tumor