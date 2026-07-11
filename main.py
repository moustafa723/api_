from tkinter import Tk, filedialog
from utils.loader import load_case
from utils.slice_selector import find_best_slice
from utils.preprocessing import extract_best_slice, apply_window
from utils.image_saver import save_image
from utils.glb_converter import nifti_to_glb
import os

# إخفاء نافذة Tk
root = Tk()
root.withdraw()

# اختيار مجلد الحالة
case_folder = filedialog.askdirectory(title="Select Case Folder")

if not case_folder:
    print("No folder selected.")
    exit()

print(f"\nSelected Folder:\n{case_folder}\n")

# تحميل البيانات
ct, liver, tumor = load_case(case_folder)

# استخراج أفضل Slice
best_slice, pixels = find_best_slice(tumor)

# استخراج صورة الـ CT
image = extract_best_slice(ct, best_slice)

# تحسين الصورة
image = apply_window(image)

# حفظ الصورة
save_image(image)

# إنشاء GLB
liver_mask_path = os.path.join(case_folder, "liver_mask_pvp.nii.gz")
tumor_mask_path = os.path.join(case_folder, "mask_pvp.nii.gz")

nifti_to_glb(
    liver_mask_path,
    tumor_mask_path,
    r"outputs\liver_tumor.glb"
)

print("\n✅ Finished Successfully")