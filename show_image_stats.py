"""
show_image_stats.py
...

Arguments
--image (REQUIS): Chemin vers les images à analyser. ("path/to/image.abc")

Exemple d'usage:
    python main.py stats --image "C:path\to\Data_TP1\Data_TP0\IRM\Brain\flair.nii"
"""

import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from pathlib import Path
from matplotlib.widgets import Slider
from nibabel.affines import voxel_sizes

def contraste_de_michelson(image_path):
    # Selon les notes de cours:
    #   Cm = (Imax - Imin) / (Imax + Imin)

    img = nib.load(image_path)
    data = img.get_fdata()

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

    img = nib.load(image_path)
    data = img.get_fdata()

    Crms = np.sqrt(np.mean(np.square(data - np.mean(data))))

    return Crms


def snr():
    return


def show_stats(image_path):

    # Chercher les informations de l'image
    img = nib.load(image_path)
    data = img.get_fdata()  # Données de l'image

    dimensions = data.shape

    voxel_sizes = img.header.get_zooms()

    Cm = contraste_de_michelson(image_path)

    Crms = contraste_rms(image_path)

    # --- Affichage fournit par Copilot ---

    print("\n" + "=" * 70)
    print("IMAGE STATISTICS")
    print("=" * 70)
    stats = [
        ("Dimensions", f"{dimensions} voxels"),

        # (
        #     "Voxel size",
        #     f"{voxel_sizes.3f} x "
        #     f"{voxel_sizes.3f} x "
        #     f"{voxel_sizes.3f} mm"
        # ),
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