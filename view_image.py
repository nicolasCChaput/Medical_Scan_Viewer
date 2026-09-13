import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from pathlib import Path


def view_image(image_path):

    suffix = Path(image_path).suffix
    if suffix != ".nii":
        raise Exception(f"Provided file is not a .nii file. Provided file format: {suffix}")

    # Chercher information de l'image
    img = nib.load(image_path)
    data = img.get_fdata()

    x = data.shape[0] // 2
    y = data.shape[1] // 2
    z = data.shape[2] // 2

    sag = data[x, :, :].T
    coro = data[:, y, :].T
    axia = data[:, :, z].T

    # Flip up-down
    sag = np.flipud(sag)
    coro = np.flipud(coro)
    axia = np.flipud(axia)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Sagittale
    axes[0].imshow(sag, aspect="auto")
    axes[0].set_title("Sagittal")

    # Coronale
    axes[1].imshow(coro, aspect="auto")
    axes[1].set_title("Coronal")

    # Axiale
    axes[2].imshow(axia, aspect="auto")
    axes[2].set_title("Axial")

    plt.show()
