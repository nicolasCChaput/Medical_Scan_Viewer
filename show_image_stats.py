"""
show_image_stats.py
...

Arguments
--image (REQUIS): Chemin vers les images à analyser. ("path/to/image.abc")

Exemple d'usage:
    python main.py stats --image "C:path/to/Data_TP1/Data_TP0/IRM/Brain/flair.nii"
"""

import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

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


def snr(image_path, ignore_background):
    # Selon les notes de cours:
    #   SNR = moyenne du signal / écart-type du bruit

    # Chercher les informations des images
    data, img = load_image(image_path)

    signal = data

    # Retirer le fond noir
    if(ignore_background == True):
        signal = data[data > 0]

    # Moyenne du signal
    signal_mean = np.mean(signal)

    # Estimation du bruit à partir des voxels appartenant aux 10 % plus faibles intensités
    percent_10 = np.percentile(signal, 10)
    noise_voxels = signal[signal <= percent_10]

    # Écart type du bruit
    noise_std = np.std(noise_voxels)

    return signal_mean / noise_std


def histogram(image_path):

    # Chercher les informations des images
    data, img = load_image(image_path)

    # Séparer les zéros et les autres valeurs
    zeros = data[data == 0]
    non_zeros = data[data != 0]

    # Conserver au plus 10000 zéros (les images médicales sont bourré de 0)
    max_zeros = 5000

    if len(zeros) > max_zeros:
        zeros = np.random.choice(zeros, size=max_zeros, replace=False)

    values = np.concatenate([zeros, non_zeros])

    # Définitions de l'affichage de l'histogramme
    plt.figure(figsize=(8, 5))
    plt.hist(
        values,
        bins=512,
        color="steelblue"
    )

    plt.title(f"Histogramme des intensités de\n{Path(image_path).name}")
    plt.xlabel("Intensité")
    plt.ylabel("Nombre de voxels/pixels")
    plt.grid(True, alpha=0.3)

    plt.show()


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

    SNR = snr(image_path, False)
    SNR_ignore_background = snr(image_path, True)

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
        ("SNR", f"{SNR:.6f}"),
        ("SNR ignoring background", f"{SNR_ignore_background:.6f}")
    ]

    for key, value in stats:
        print(f"{key:<25} : {value}")

    print("=" * 70)

    # Afficher l'histogram pour analyser le bruit
    histogram(image_path)