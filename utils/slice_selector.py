import numpy as np


def find_best_slice(tumor_mask):
    """
    اختيار الـ Slice التي تحتوي على أكبر مساحة ورم.

    يستخدم mask_pvp.nii.gz فقط.
    """

    num_slices = tumor_mask.shape[2]

    tumor_pixels = []

    print("\nSearching for the best slice...\n")

    for i in range(num_slices):
        current_slice = tumor_mask[:, :, i]

        pixels = int(np.sum(current_slice > 0))

        tumor_pixels.append(pixels)

        print(f"Slice {i:03d} -> Tumor Pixels: {pixels}")

    best_slice = int(np.argmax(tumor_pixels))
    best_pixels = tumor_pixels[best_slice]

    print("\n" + "=" * 60)
    print("Best Slice Found")
    print("=" * 60)
    print(f"Best Slice Index : {best_slice}")
    print(f"Tumor Pixels     : {best_pixels}")
    print("=" * 60)

    return best_slice, best_pixels