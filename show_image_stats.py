"""
show_image_stats.py
...

Arguments
--image (REQUIS): Chemin vers les images à analyser. ("path/to/image.abc")

Exemple d'usage:
    python main.py stats --image "C:path/to/Data_TP1/Data_TP0/IRM/Brain/flair.nii"
"""

import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from pathlib import Path
from matplotlib.widgets import Slider
from nibabel.affines import voxel_sizes

from utils import load_image

def contraste_de_michelson(image_path):
    # Selon les notes de cours:
    #   Cm = (Imax - Imin) / (Imax + Imin)

    # Chercher les informations des images
    data, img = load_image(image_path)

    imax = np.max(data)
    imin = np.min(data)

    Cm = (imax - imin) / (imax + imin)
    return Cm


def contraste_rms(image_path):
    # rms <-> Root-Mean-Square <-> La Racine de la moyenne au carré.
    # Selon les notes de cours:
    #   Crms(f) = sqrt( (1/M*N - 1) * sum(M, sum(N, (l(i,j) - lbarre)^2 )
    #   ou lbarre = 1/M*N sum(M, sum(N, (l(i,j))

    # En python, ça devrait ressembler à:
    #   sqrt(mean((i - mean(i))^2))
    #   ou i sont les intensité

    # Chercher les informations des images
    data, img = load_image(image_path)

    Crms = np.sqrt(np.mean(np.square(data - np.mean(data))))

    return Crms


def snr():
    return


def show_stats(image_path):

    # Chercher les informations des images
    data, img = load_image(image_path)

    dimensions = data.shape

    # Recherche de la taille des voxels
    if img is not None:
        voxel_sizes = img.header.get_zooms()[:3]
        voxel_str = (
            f"{voxel_sizes[0]:.3f} x "
            f"{voxel_sizes[1]:.3f} x "
            f"{voxel_sizes[2]:.3f} mm"
        )
    else:
        voxel_str = "N/A"

    Cm = contraste_de_michelson(image_path)

    Crms = contraste_rms(image_path)

    # --- Affichage fournit par Copilot ---

    print("\n" + "=" * 70)
    print("IMAGE STATISTICS")
    print("=" * 70)
    stats = [
        ("Dimensions", f"{dimensions} voxels"),
        ("Voxel size", voxel_str),
        ("Min intensity", f"{np.min(data):.3f}"),
        ("Max intensity", f"{np.max(data):.3f}"),
        ("Mean intensity", f"{np.mean(data):.3f}"),
        ("Std intensity", f"{np.std(data):.3f}"),
        ("Michelson contrast", f"{Cm:.6f}"),
        ("RMS contrast", f"{Crms:.6f}"),
        #("Estimated SNR", f"{snr:.6f}")
    ]

    for key, value in stats:
        print(f"{key:<25} : {value}")

    print("=" * 70)