import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from pathlib import Path
from matplotlib.widgets import Slider
from nibabel.affines import voxel_sizes

"""
show_image_stats.py
...

Arguments
--image (REQUIS): Chemin vers les images à analyser. ("path/to/image.abc")

Exemple d'usage:
    python main.py stats --image "C:path\to\Data_TP1\Data_TP0\IRM\Brain\flair.nii"
"""

def contraste_de_michelson():
    return

def contraste_rms():
    return

def snr():
    return

def show_stats(image_path):

    # Chercher les informations de l'image
    img = nib.load(image_path)
    data = img.get_fdata()  # Données de l'image

    dimensions = data.shape

    voxel_sizes = img.header
    print(voxel_sizes)

    stats = [
        ("Dimensions", f"{dimensions} voxels")
        ]