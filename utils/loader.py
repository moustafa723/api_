import os
import nibabel as nib
import numpy as np


def load_case(case_folder):
    """
    Load CT volume, liver mask and tumor mask.

    Expected structure:

    case_folder/
    ├── liver_mask_pvp.nii.gz
    ├── mask_pvp.nii.gz
    └── NIFTI/
        └── pvp.nii.gz
    """

    ct_path = os.path.join(case_folder, "NIFTI", "pvp.nii.gz")
    liver_path = os.path.join(case_folder, "liver_mask_pvp.nii.gz")
    tumor_path = os.path.join(case_folder, "mask_pvp.nii.gz")

    # -------------------------
    # Check files
    # -------------------------

    if not os.path.exists(ct_path):
        raise FileNotFoundError(f"CT not found:\n{ct_path}")

    if not os.path.exists(liver_path):
        raise FileNotFoundError(f"Liver mask not found:\n{liver_path}")

    if not os.path.exists(tumor_path):
        raise FileNotFoundError(f"Tumor mask not found:\n{tumor_path}")

    print("=" * 60)
    print("Loading Case...")
    print("=" * 60)

    print(f"CT         : {ct_path}")
    print(f"Liver Mask : {liver_path}")
    print(f"Tumor Mask : {tumor_path}")

    # -------------------------
    # Load NIfTI
    # -------------------------

    ct = nib.load(ct_path).get_fdata().astype(np.float32)

    liver = nib.load(liver_path).get_fdata().astype(np.uint8)

    tumor = nib.load(tumor_path).get_fdata().astype(np.uint8)

    # -------------------------
    # Check Shapes
    # -------------------------

    if ct.shape != liver.shape:
        raise ValueError("CT and Liver mask have different shapes.")

    if ct.shape != tumor.shape:
        raise ValueError("CT and Tumor mask have different shapes.")

    print("\nLoaded Successfully!\n")

    print(f"CT Shape         : {ct.shape}")
    print(f"Liver Shape      : {liver.shape}")
    print(f"Tumor Shape      : {tumor.shape}")

    print(f"CT Range         : {ct.min():.2f} -> {ct.max():.2f}")

    print(f"Liver Labels     : {np.unique(liver)}")
    print(f"Tumor Labels     : {np.unique(tumor)}")

    print(f"Liver Voxels     : {np.sum(liver > 0)}")
    print(f"Tumor Voxels     : {np.sum(tumor > 0)}")

    print("=" * 60)

    return ct, liver, tumor