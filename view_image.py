"""
view_image.py
Ouvre un viewer générique de fichier de format .nii (nifti). Est utiliser avec l'argument "view".

Arguments
--image (REQUIS): Chemin vers les images à analyser dans le viewer. ("path/to/image.nii")
--grayscale: Affiche l'image en niveaux de gris. (Choix possibles: yes -> affichage noir et blanc | no -> palette de couleurs par défaut )
--mrinfo: Fait les appels nécessaire pour voir les information de mrinfo sur l'orientation. (Choix possibles: yes -> fait les appels à mrinfo | no -> ne fait pas les appels à mrinfo )

Exemple d'usage:
    python main.py view --image "C:path/to/Data_TP1/Data_TP0/IRM/Brain/flair.nii" --grayscale yes --mrinfo yes
"""

import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import subprocess

from pathlib import Path
from matplotlib.widgets import Slider

from utils import load_image

def mrinfo_orientation(image_path):

    # Exemple:
    # | 0  -1   0  12| -> Axe des X
    # | 1   0   0  34| -> Axe des Y
    # | 0   0   1  56| -> Axe des Z
    # | 0   0   0   1|
    #
    # Si on prend l'axe des x, on voit que le terme dominant est 1 qui indique une direction pointé dans l'axe de y.
    # Si cette direction est positive, elle pointe vers la droite (R), si elle est négative, elle pointe vers la gauche (L)
    # Ici, pour -1, c'est Left.

    # Modifier au besoin, nécessaire pour windows
    mrinfo_exe = r"C:\msys64\mingw64\bin\mrinfo.exe"

    cmd_return = subprocess.run(
        [mrinfo_exe, image_path, "-transform"], # Nous devons regarder la transform pour déterminer l'orientation
        capture_output=True,
        text=True,
        check=True
    )

    # --- Code fournit par Copilot ---

    lines = cmd_return.stdout.strip().split("\n")

    # Extraire la matrice 4x4 de transform
    matrix = []
    for line in lines:
        values = line.strip().split()
        if len(values) == 4:
            try:
                matrix.append([float(v) for v in values])
            except ValueError:
                pass

    # --- Fin du code fournit par Copilot ---

    # Matrice transform extraite:
    matrix_affine = np.array(matrix)

    print(matrix_affine)

    orientation = "" # Orientation, rempli dans la boucle si-dessous

    for axis in range(3):

        col = matrix_affine[:3, axis]

        dominant_term = np.argmax(np.abs(col))
        sign = np.sign(col[dominant_term]) # 1 ou -1

        # print(dominant_term)
        # print(sign)

        # Info sur l'interprétation des orientations: http://www.grahamwideman.com/gw/brain/orientation/orientterms.htm

        # Axe des X -> positif = Right | négatif = Left
        if dominant_term == 0:
            orientation += "R" if sign > 0 else "L"

        # Axe des Y -> positif = Anterior | négatif = Posterior
        elif dominant_term == 1:
            orientation += "A" if sign > 0 else "P"

        # Axe des Z -> positif = Superior | négatif = Inferior
        elif dominant_term == 2:
            orientation += "S" if sign > 0 else "I"

    return orientation


def view_image(image_path, grayscale, mrinfo):

    suffix = Path(image_path).suffix
    if suffix != ".nii":
        raise Exception(f"Provided file is not a .nii file. Provided file format: {suffix}")

    # --- Setup général du viewer ---

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    plt.subplots_adjust(bottom=0.10) # Espace pour les sliders sous les images

    # Setup d'une grille pour obtenir ce format de visuel
    #|___________|
    #|img|img|img|
    #|___________|
    #|sld|sld|sld|
    #|___________|
    grid = fig.add_gridspec (
        nrows = 2,
        ncols = 3,
        height_ratios = [15, 1]
    )

    # Placer les images dans le haut de la grille
    pos_img_sag = fig.add_subplot(grid[0,0])
    pos_img_coro = fig.add_subplot(grid[0,1])
    pos_img_axia = fig.add_subplot(grid[0,2])

    # Placer les slider dans le bas de la grille
    pos_sld_sag = fig.add_subplot(grid[1,0])
    pos_sld_coro = fig.add_subplot(grid[1,1])
    pos_sld_axia = fig.add_subplot(grid[1,2])


    # --- Setup des données des images ---

    # Chercher les informations des images
    data, img = load_image(image_path)
    # print(img.header)

    # Orientation des nifti selon mrinfo/MrTrix
    if mrinfo == "yes":
        mrinfo_orient = mrinfo_orientation(image_path)
        print("MrInfo orientation: ", mrinfo_orient)

    # --- Standardiser l'orientation des images affichés (Viser RAS (Right-Anterior-Superior)) ---
    og_orientation = "Nibabel original orientation: ", nib.aff2axcodes(img.affine)
    print(og_orientation)

    img_ras = nib.as_closest_canonical(img) # Convertission en RAS

    can_orientation = "Nibabel canonical orientation: ", nib.aff2axcodes(img_ras.affine)
    print(can_orientation)


    data = img_ras.get_fdata()  # Données de l'image, // 2 pour mettre le point de départ au centre

    initial_x = data.shape[0] // 2
    initial_y = data.shape[1] // 2
    initial_z = data.shape[2] // 2

    sag = data[initial_x, :, :]
    coro = data[:, initial_y, :]
    axia = data[:, :, initial_z]

    # --- Setup de la présentation des images dans leur grille ---

    # Taille physique des voxels afin d'adapter la résolution des images pour l'affichage
    voxel_size_x, voxel_size_y, voxel_size_z = img_ras.header.get_zooms()[:3]

    # Sagittale : Y-Z
    sag_extent = [
        0,
        data.shape[1] * voxel_size_y,
        0,
        data.shape[2] * voxel_size_z
    ]

    # Coronale : X-Z
    coro_extent = [
        0,
        data.shape[0] * voxel_size_x,
        0,
        data.shape[2] * voxel_size_z
    ]

    # Axiale : X-Y
    axia_extent = [
        0,
        data.shape[0] * voxel_size_x,
        0,
        data.shape[1] * voxel_size_y
    ]

    if grayscale == "yes":
        sag_img = pos_img_sag.imshow(sag, aspect="equal", cmap="gray", origin="lower", extent=sag_extent, interpolation="none")
        coro_img = pos_img_coro.imshow(coro, aspect="equal", cmap="gray", origin="lower", extent=coro_extent, interpolation="none")
        axia_img = pos_img_axia.imshow(axia, aspect="equal", cmap="gray", origin="lower", extent=axia_extent, interpolation="none")
    else:
        sag_img = pos_img_sag.imshow(sag, aspect="equal", origin="lower", extent=sag_extent, interpolation="none")
        coro_img = pos_img_coro.imshow(coro, aspect="equal", origin="lower", extent=coro_extent, interpolation="none")
        axia_img = pos_img_axia.imshow(axia, aspect="equal", origin="lower",  extent=axia_extent, interpolation="none")


    # --- Titres des graphs et modifications des affichages ---

    # Sagittale
    axes[0].set_title("Sagittale")
    axes[0].axis("off")

    # Coronale
    axes[1].set_title("Coronale")
    axes[1].axis("off")

    # Axiale
    axes[2].set_title("Axiale")
    axes[2].axis("off")


    # --- Setup des sliders sous les images et dans leurs grille ---

    # Slider Coupe Sagittale
    x_slider = Slider(
        ax = pos_sld_sag,
        label = "",
        valmin = 0,
        valmax = data.shape[0] - 1,
        valinit = initial_x,
        valstep = 1
    )

    # Slider Coupe Coronale
    y_slider = Slider(
        ax = pos_sld_coro,
        label = "",
        valmin = 0,
        valmax = data.shape[1] - 1,
        valinit=initial_y,
        valstep = 1
    )

    # Slider Coupe Axiale
    z_slider = Slider(
        ax = pos_sld_axia,
        label = "",
        valmin = 0,
        valmax = data.shape[2] - 1,
        valinit = initial_z,
        valstep = 1
    )

    def update(_):
        new_x = x_slider.val
        new_y = y_slider.val
        new_z = z_slider.val

        sag_img.set_data(data[new_x, :, :])
        coro_img.set_data(data[:, new_y, :])
        axia_img.set_data(data[:, :, new_z])

    x_slider.on_changed(update)
    y_slider.on_changed(update)
    z_slider.on_changed(update)

    plt.show()