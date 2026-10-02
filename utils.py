from pathlib import Path
from skimage import io
import nibabel as nib

def load_image(image_path):

    ext = Path(image_path).suffix.lower()

    if ext in [".nii", ".nii.gz"]:
        img = nib.load(image_path)
        return img.get_fdata(), img

    elif ext == ".pgm":
        data = io.imread(image_path)
        return data.astype(float), None

    else:
        raise ValueError(f"Format non supporté : {ext}")