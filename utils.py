"""
utils.py

Fonctions utilitaires utilisées dans les différents scripts du TP1.
Permet principalement le chargement des images médicales et des images
2D selon leur format de fichier.

Formats supportés :
    - .nii : Images NIfTI via nibabel
    - .pgm : Images PGM via scikit-image

Auteur: Nicolas Claveau-Chaput
"""

from pathlib import Path
from skimage import io
import nibabel as nib

def load_image(image_path):

    ext = Path(image_path).suffix.lower()

    if ext in [".nii"]:
        img = nib.load(image_path)
        return img.get_fdata(), img

    # https://scikit-image.org/docs/stable/api/skimage.io.html
    elif ext in [".pgm"]:
        data = io.imread(image_path)
        return data.astype(float), None

    else:
        raise ValueError(f"Format de fichier non supporté")