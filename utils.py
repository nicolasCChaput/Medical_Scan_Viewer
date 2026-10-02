from pathlib import Path
from skimage import io
import nibabel as nib

'''
def convert_vff_to_nifti(image_path):

    data, header = load_vff(image_path)

    img = nib.Nifti1Image(data, affine=np.eye(4))

    nib.save(img, "converted.nii.gz")
'''


def load_image(image_path):

    ext = Path(image_path).suffix.lower()

    if ext in [".nii"]:
        img = nib.load(image_path)
        return img.get_fdata(), img

    elif ext in [".pgm"]:
        data = io.imread(image_path)
        return data.astype(float), None

    #elif ext in [".fdf"]:
    #    return

    #elif ext in [".fdf"]:
    #    return


    else:
        raise ValueError(f"Format de fichier non supporté")