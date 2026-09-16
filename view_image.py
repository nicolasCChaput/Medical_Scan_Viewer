import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from pathlib import Path

from matplotlib.widgets import Slider


def view_image(image_path):

    suffix = Path(image_path).suffix
    if suffix != ".nii":
        raise Exception(f"Provided file is not a .nii file. Provided file format: {suffix}")

    # --- Setup initial du viewer ---

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    plt.subplots_adjust(bottom=0.30) # Espace pour les sliders sous les images

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
    sag = np.flipud(sag)
    coro = np.flipud(coro)
    axia = np.flipud(axia)

    # Sagittale
    sag_img = axes[0].imshow(sag, aspect="auto")
    axes[0].set_title("Sagittale")

    # Coronale
    coro_img = axes[1].imshow(coro, aspect="auto")
    axes[1].set_title("Coronale")

    # Axiale
    axia_img = axes[2].imshow(axia, aspect="auto")
    axes[2].set_title("Axiale")

    # --- Setup des sliders sous les images

    # Slider Coupe Sagittale
    x_slider_visual = fig.add_axes([0.15, 0.20, 0.7, 0.03])
    x_slider = Slider(
        ax = x_slider_visual,
        label = "Coupe Sagittale",
        valmin = 0,
        valmax = data.shape[0] - 1,
        valinit = initial_x,
        valstep = 1
    )

    # Slider Coupe Coronale
    y_slider_visual = fig.add_axes([0.15, 0.14, 0.7, 0.03])
    y_slider = Slider(
        ax = y_slider_visual,
        label = "Coupe Coronale",
        valmin = 0,
        valmax = data.shape[1] - 1,
        valinit=initial_y,
        valstep = 1
    )

    # Slider Coupe Axiale
    z_slider_visual = fig.add_axes([0.15, 0.08, 0.7, 0.03])
    z_slider = Slider(
        ax = z_slider_visual,
        label = "Coupe Axiale",
        valmin = 0,
        valmax = data.shape[2] - 1,
        valinit = initial_z,
        valstep = 1
    )

    def update(null):
        new_x = x_slider.val
        new_y = y_slider.val
        new_z = z_slider.val

        sag_img.set_data(np.flipud(data[new_x, :, :].T))
        coro_img.set_data(np.flipud(data[:, new_y, :].T))
        axia_img.set_data(np.flipud(data[:, :, new_z].T))

    x_slider.on_changed(update)
    y_slider.on_changed(update)
    z_slider.on_changed(update)

    plt.show()
