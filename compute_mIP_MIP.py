"""
compute_mIP_MIP.py
Calcule et affiche la projection d’intensité minimale (mIP) ou maximale (MIP) de fichier nifti exclusivement selon des entrées d'axes (x, y, z) et du mode (max, min).

Arguments
--image (REQUIS): Chemin vers les images à analyser dans le viewer. ("path/to/image.nii")
--axis: Axe selon lequel la projection est calculée. (Choix possibles: x -> axe sagittal | y -> axe coronal | z -> axe axial )
--mode: Type de projection à effectuer. (Choix possibles: max -> Maximum Intensity Projection (mip) | min -> Minimum Intensity Projection (min-ip) )
--grayscale: Affiche l'image en niveaux de gris. (Choix possibles: yes -> affichage noir et blanc | no -> palette de couleurs par défaut )

Exemple d'usage:
    python main.py projection --image "C:path/to/Data_TP1/Data_TP0/IRM/Brain/flair.nii" --axis x --mode max --grayscale yes
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from utils import load_image

def compute_projection(image_path, axis, mode, grayscale):

    suffix = Path(image_path).suffix
    if suffix != ".nii":
        raise Exception(f"Provided file is not a .nii file. Provided file format: {suffix}")

    # Chercher les informations des images
    data, img = load_image(image_path)

    # À partir de l'entrée de l'axis, déterminer l'id de l'axe
    if axis== "x":
        axis_id = 0
    elif axis== "y":
        axis_id = 1
    elif axis== "z":
        axis_id = 2

    # np.max doc: https://numpy.org/doc/2.2/reference/generated/numpy.max.html
    # Maximum Intensity Projection (mip)
    if mode=="max":
        projection = np.max(data, axis=axis_id)
        projection_title = f"Maximum Intensity Projection (mip) of the axis {axis}"

    # np.min https://numpy.org/doc/2.2/reference/generated/numpy.min.html
    # Minimum Intensity Projection (min-ip)
    elif mode=="min":
        projection = np.min(data, axis=axis_id)
        projection_title = f"Minimum Intensity Projection (min-ip) of the axis {axis}"

    plt.figure(figsize=(8, 8))

    # Afficher l'image selon le choix de grayscale
    if grayscale== "yes":
        plt.imshow(projection, aspect="auto", cmap="gray")
    else:
        plt.imshow(projection, aspect="auto")

    # Titre et axes
    plt.title(projection_title)
    plt.axis("off")

    plt.show()
