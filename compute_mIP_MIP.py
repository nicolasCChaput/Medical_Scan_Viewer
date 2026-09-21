import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from pathlib import Path
from matplotlib.widgets import Slider

"""
compute_mIP_MIP.py
...

Arguments
--image (REQUIS): Chemin vers les images à analyser dans le viewer. ("path/to/image.nii")
--axis: ...
--mode: ...
--grayscale: Affiche l'image sous des intensités de noir à blanc. (Choix: yes, no)

Exemple d'usage:
    python main.py projection --image "C:path\to\Data_TP1\Data_TP0\IRM\Brain\flair.nii" --axis x --mode max --grayscale yes
"""

def compute_projection(image_path, axis, mode, grayscale):

    # Chercher les informations de l'image
    img = nib.load(image_path)
    data = img.get_fdata()  # Données de l'image

    # À partir dce l'entrée de l'axis, déterminer prendre l'id de l'axe
    if axis== "x":
        axis_id = 0
    elif axis== "y":
        axis_id = 1
    elif axis== "z":
        axis_id = 2

    # Maximum Intensity Projection (mip)
    if mode=="max":
        projection = np.max(data, axis=axis_id)
        projection_title = f"Maximum Intensity Projection (mip) of the axis {axis}"

    # Minimum Intensity Projection (min-ip)
    elif mode=="min":
        projection = np.min(data, axis=axis_id)
        projection_title = f"Minimum Intensity Projection (min-ip) of the axis {axis}"

    plt.figure(figsize=(8, 8))

    if grayscale== "yes":
        plt.imshow(projection, aspect="auto", cmap="gray")
    else:
        plt.imshow(projection, aspect="auto")
    plt.title(projection_title)
    plt.axis("off")
    plt.show()
