import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from pathlib import Path
from matplotlib.widgets import Slider

"""
view_image.py
Ouvre un viewer générique de fichier de format .nii (nifti). Est utiliser avec l'argument "view".

Arguments
--image (REQUIS): Chemin vers les images à analyser dans le viewer. ("path/to/image.nii")
--flip : Inverse les images entrées (Choix: {"yes", "no"})

Exemple d'usage:
    python main.py view --image "C:path\to\Data_TP1\Data_TP0\IRM\Brain\flair.nii" --flip yes
"""

def view_image(image_path, flip):

    suffix = Path(image_path).suffix
    if suffix != ".nii":
        raise Exception(f"Provided file is not a .nii file. Provided file format: {suffix}")

    # --- Setup générale du viewer ---

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

    # Load nifti - Chercher information de l'image
    img = nib.load(image_path)
    data = img.get_fdata()

    initial_x = data.shape[0] // 2
    initial_y = data.shape[1] // 2
    initial_z = data.shape[2] // 2

    sag = data[initial_x, :, :].T
    coro = data[:, initial_y, :].T
    axia = data[:, :, initial_z].T

    # Flip up-down
    if flip == "yes":
        sag = np.flipud(sag)
        coro = np.flipud(coro)
        axia = np.flipud(axia)

    # --- Setup de la présentation des images dans leur grille ---
    # Note: aspect à "auto" semble être le mieux ig pour la visualisation

    # Sagittale
    sag_img = pos_img_sag.imshow(sag, aspect="auto")
    axes[0].set_title("Sagittale")
    axes[0].axis("off")

    # Coronale
    coro_img = pos_img_coro.imshow(coro, aspect="auto")
    axes[1].set_title("Coronale")
    axes[1].axis("off")

    # Axiale
    axia_img = pos_img_axia.imshow(axia, aspect="auto")
    axes[2].set_title("Axiale")
    axes[2].axis("off")

    # --- Setup des sliders sous les images et dans leurs grille ---

    # Slider Coupe Sagittale
    # x_slider_visual = fig.add_axes([0.15, 0.20, 0.7, 0.03])
    x_slider = Slider(
        ax = pos_sld_sag,
        label = "",
        valmin = 0,
        valmax = data.shape[0] - 1,
        valinit = initial_x,
        valstep = 1
    )

    # Slider Coupe Coronale
    # y_slider_visual = fig.add_axes([0.15, 0.14, 0.7, 0.03])
    y_slider = Slider(
        ax = pos_sld_coro,
        label = "",
        valmin = 0,
        valmax = data.shape[1] - 1,
        valinit=initial_y,
        valstep = 1
    )

    # Slider Coupe Axiale
    # z_slider_visual = fig.add_axes([0.15, 0.08, 0.7, 0.03])
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

        # Flip up-down
        if flip == "yes":
            sag_img.set_data(np.flipud(data[new_x, :, :].T))
            coro_img.set_data(np.flipud(data[:, new_y, :].T))
            axia_img.set_data(np.flipud(data[:, :, new_z].T))
        else:
            sag_img.set_data(data[new_x, :, :].T)
            coro_img.set_data(data[:, new_y, :].T)
            axia_img.set_data(data[:, :, new_z].T)

    x_slider.on_changed(update)
    y_slider.on_changed(update)
    z_slider.on_changed(update)

    plt.show()
