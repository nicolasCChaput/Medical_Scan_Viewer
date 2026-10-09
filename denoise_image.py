"""
denoise_image.py
[...]

Arguments
--image (REQUIS): Chemin vers les images à débruiter. ("path/to/image.abc")
--method: 

Exemple d'usage:
    python main.py denoise --image "C:path/to/Data_TP1/Data_TP0/IRM/Brain/flair.nii"
"""

import numpy as np
import matplotlib.pyplot as plt

from skimage.restoration import denoise_nl_means
from skimage.restoration import estimate_sigma
from skimage.restoration import denoise_bilateral
from scipy.ndimage import gaussian_filter

from utils import load_image


def nlmeans(image, patch_size=5, patch_distance=6, h=0.8):

    sigma_estimate = np.mean(estimate_sigma(image, channel_axis=None))

    return denoise_nl_means(image, h=h * sigma_estimate, patch_size=patch_size, patch_distance=patch_distance, fast_mode=True)


def anisotrope(image, niter=10, kappa=50, gamma=0.1):
    result = image.copy()

    for _ in range(niter):
        result = gaussian_filter(result, sigma=gamma)

    return result


def bilateral(image, sigma_color=0.05, sigma_spatial=15):
    return denoise_bilateral(image, sigma_color=sigma_color, sigma_spatial=sigma_spatial)


def denoise_image(
    image_path, method="nlmeans",
    # NLMeans:
    patch_size=5, patch_distance=6, h=0.8,
    # Anisotrope:
    niter=10, kappa=50, gamma=0.1,
    # Bilateral:
    sigma_color=0.05, sigma_spatial=15
):

    # Chercher les informations des images
    data, img = load_image(image_path)

    # Prendre une tranche quelconque
    image = data[:, :, data.shape[2] // 2]

    # Résultats à affiché
    resultats = {}
    images_to_show = []

    # --- Afficher les résultats selon le choix d'affichage ---

    if method == "all":

        # NLMeans
        resultats["nlmeans"] = nlmeans(
            image,
            patch_size,
            patch_distance,
            h
        )
        # Anisotrope
        resultats["anisotrope"] = anisotrope(
            image,
            niter,
            kappa,
            gamma
        )
        # Bilateral
        resultats["bilateral"] = bilateral(
            image,
            sigma_color,
            sigma_spatial
        )

        images_to_show = [
            ("Originale", image),
            ("NLMeans", resultats["nlmeans"]),
            ("Anisotrope", resultats["anisotrope"]),
            ("Bilateral", resultats["bilateral"])
        ]

    elif method == "nlmeans":

        # NLMeans
        resultats["nlmeans"] = nlmeans(
            image,
            patch_size,
            patch_distance,
            h
        )
        denoised = resultats[method]

        difference = np.abs(image - denoised)

        images_to_show = [
            ("Originale", image),
            ("Débruitée NLMean", denoised),
            ("Différence", difference)
        ]

    elif method == "anisotrope":

        # Anisotrope
        resultats["anisotrope"] = anisotrope(
            image,
            niter,
            kappa,
            gamma
        )
        denoised = resultats[method]

        difference = np.abs(image - denoised)

        images_to_show = [
            ("Originale", image),
            ("Débruitée Anisotrope", denoised),
            ("Différence", difference)
        ]

    elif method == "bilateral":

        # Bilateral
        resultats["bilateral"] = bilateral(
            image,
            sigma_color,
            sigma_spatial
        )
        denoised = resultats[method]

        difference = np.abs(image - denoised)

        images_to_show = [
            ("Originale", image),
            ("Débruitée bilateral", denoised),
            ("Différence", difference)
        ]

    n = len(images_to_show)

    fig, axes = plt.subplots(1, n, figsize=(5 * n, 5))

    if n == 1:
        axes = [axes]

    for ax, item in zip(axes, images_to_show):
        title = item[0]
        image = item[1]

        ax.imshow(image, cmap="gray")
        ax.set_title(title)
        ax.axis("off")

    plt.tight_layout()
    plt.show()