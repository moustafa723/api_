import os
import shutil
import tempfile
import zipfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse

from utils.loader import load_case
from utils.slice_selector import find_best_slice
from utils.preprocessing import extract_best_slice, apply_window
from utils.image_saver import save_image
from utils.glb_converter import nifti_to_glb

app = FastAPI(title="Best Slice & GLB API")


@app.post("/process")
async def process_case(file: UploadFile = File(...)):

    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Upload ZIP file only.")

    temp_dir = tempfile.mkdtemp()

    try:

        zip_path = os.path.join(temp_dir, file.filename)

        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        case_folder = None

        for root, dirs, files in os.walk(temp_dir):
            if (
                "liver_mask_pvp.nii.gz" in files
                and "mask_pvp.nii.gz" in files
                and os.path.exists(os.path.join(root, "NIFTI", "pvp.nii.gz"))
            ):
                case_folder = root
                break

        if case_folder is None:
            raise HTTPException(status_code=400, detail="Case folder not found.")

        ct, liver, tumor = load_case(case_folder)

        best_slice, pixels = find_best_slice(tumor)

        image = extract_best_slice(ct, best_slice)
        image = apply_window(image)

        outputs = "storage"
        os.makedirs(outputs, exist_ok=True)

        image_path = save_image(
            image,
            outputs,
            "best_slice.png"
        )

        glb_path = os.path.join(outputs, "liver_tumor.glb")

        nifti_to_glb(
            os.path.join(case_folder, "liver_mask_pvp.nii.gz"),
            os.path.join(case_folder, "mask_pvp.nii.gz"),
            glb_path,
        )

        return JSONResponse(
            {
                "success": True,
                "best_slice": best_slice,
                "tumor_pixels": pixels,
                "message": "Processing completed successfully."
            }
        )

    finally:
        file.file.close()


@app.get("/best-slice")
def get_best_slice():

    path = os.path.join("storage", "best_slice.png")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Best slice not found.")

    return FileResponse(
        path,
        media_type="image/png",
        filename="best_slice.png"
    )


@app.get("/glb")
def get_glb():

    path = os.path.join("storage", "liver_tumor.glb")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="GLB not found.")

    return FileResponse(
        path,
        media_type="model/gltf-binary",
        filename="liver_tumor.glb"
    )