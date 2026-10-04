import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from pathlib import Path
from skimage.restoration import denoise_nl_means
from skimage.restoration import estimate_sigma

"""
denoise_image.py
...

Arguments
--image (REQUIS): Chemin vers les images à débruiter. ("path/to/image.abc")
--method: 

Exemple d'usage:
    python main.py denoise --image "C:path\to\Data_TP1\Data_TP0\IRM\Brain\flair.nii"
"""





def denoise_image(
    image_path,
    method="nlmeans",
    patch_size=5,
    patch_distance=6,
    h=0.8
):

    suffix = Path(image_path).suffix

    if suffix != ".nii":
        raise Exception(
            f"Provided file is not a .nii file. Provided file format: {suffix}"
        )

    img = nib.load(image_path)
    data = img.get_fdata()

    print("Image shape :", data.shape)

    if method == "nlmeans":

        print("Estimation du bruit...")

        sigma_est = np.mean(
            estimate_sigma(
                data,
                channel_axis=None
            )
        )

        print(f"Sigma estimé : {sigma_est:.4f}")

        print("Application du filtre NL-Means...")

        denoised = denoise_nl_means(
            data,
            h=h * sigma_est,
            sigma=sigma_est,
            patch_size=patch_size,
            patch_distance=patch_distance,
            fast_mode=True,
            channel_axis=None
        )

    else:
        raise ValueError(f"Méthode inconnue : {method}")

    mid_slice = data.shape[2] // 2

    fig, ax = plt.subplots(
        1,
        2,
        figsize=(10, 5)
    )

    ax[0].imshow(
        data[:, :, mid_slice],
        cmap="gray",
        origin="lower"
    )
    ax[0].set_title("Original")

    ax[1].imshow(
        denoised[:, :, mid_slice],
        cmap="gray",
        origin="lower"
    )
    ax[1].set_title("NL-Means")

    plt.tight_layout()
    plt.show()

    output_path = image_path.replace(
        ".nii",
        "_nlmeans.nii"
    )

    output_img = nib.Nifti1Image(
        denoised,
        img.affine,
        img.header
    )

    nib.save(
        output_img,
        output_path
    )

    print(f"Image sauvegardée : {output_path}")