import numpy as np


def apply_window(ct_slice, window_center=50, window_width=350):
    """
    Liver Window
    """

    lower = window_center - window_width / 2
    upper = window_center + window_width / 2

    ct_slice = np.clip(ct_slice, lower, upper)

    ct_slice = (ct_slice - lower) / (upper - lower)

    ct_slice = (ct_slice * 255).astype(np.uint8)

    return ct_slice


def extract_best_slice(ct_volume, slice_index):
    """
    استخراج Slice من الـ CT
    """

    return ct_volume[:, :, slice_index]