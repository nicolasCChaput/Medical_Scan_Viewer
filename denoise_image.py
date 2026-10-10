"""
denoise_image.py

Script permettant d'appliquer différentes méthodes de débruitage sur
des images médicales et d'afficher les résultats obtenus.

Méthodes disponibles :
    - NLMeans (Non-Local Means)
    - Diffusion anisotrope
    - Filtre bilatéral

Arguments
--image (REQUIS): Chemin vers les images à débruiter. ("path/to/image.abc")
--method:
    nlmeans      : Applique seulement NLMeans
    anisotrope   : Applique seulement la diffusion anisotrope
    bilateral    : Applique seulement le filtre bilatéral
    all          : Compare les trois méthodes simultanément

Exemple d'usage:

    Comparer toutes les méthodes avec les paramètres par défaut :
        python main.py denoise --image "C:/path/to/Data_TP1/Data_TP0/IRM/Brain/flair.nii" --method all

    Appliquer NLMeans :
        python main.py denoise --image "C:/path/to/Data_TP1/Data_TP0/IRM/Brain/flair.nii" --method nlmeans --h 0.8 --patch_size 5 --patch_distance 6

    Appliquer la diffusion anisotrope :
        python main.py denoise --image "C:/path/to/Data_TP1/Data_TP0/IRM/Brain/flair.nii" --method anisotrope --nbre_iter 10 --gamma 0.1

    Appliquer le filtre bilatéral :
        python main.py denoise --image "C:/path/to/Data_TP1/Data_TP0/IRM/Brain/flair.nii" --method bilateral --sigma_color 0.05 --sigma_spatial 15

    Comparer les méthodes avec des paramètres personnalisés :
        python main.py denoise --image "C:/path/to/Data_TP1/Data_TP0/IRM/Brain/flair.nii" --method all --h 1.2 --patch_size 7 --patch_distance 11 --nbre_iter 20 --gamma 0.15 --sigma_color 0.1 --sigma_spatial 20

Auteur: Nicolas Claveau-Chaput
"""

import numpy as np
import matplotlib.pyplot as plt

from skimage.restoration import denoise_nl_means
from skimage.restoration import estimate_sigma
from skimage.restoration import denoise_bilateral
from scipy.ndimage import gaussian_filter

from utils import load_image


def nlmeans(image,h, patch_size, patch_distance):

    # Estimation de l'écart-type du bruit dans l'image
    sigma_estimate = np.mean(estimate_sigma(image, channel_axis=None))

    return denoise_nl_means(image, h=h * sigma_estimate, patch_size=patch_size, patch_distance=patch_distance)


def anisotrope(image, nbre_iter, gamma):
    # Initialisation du résultat pour la boucle d'itérations
    result = image.copy()

    # Iterations de diffusion anisotrope
    for _ in range(nbre_iter):
        result = gaussian_filter(result, sigma=gamma)

    return result


def bilateral(image, sigma_color, sigma_spatial):
    return denoise_bilateral(image, sigma_color=sigma_color, sigma_spatial=sigma_spatial)


def denoise_image(
    image_path, method="nlmeans",
    # NLMeans:
    h=0.8, patch_size=5, patch_distance=6,
    # Anisotrope:
    nbre_iter=10, kappa=50, gamma=0.1,
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
            h,
            patch_size,
            patch_distance
        )
        # Anisotrope
        resultats["anisotrope"] = anisotrope(
            image,
            nbre_iter,
            gamma
        )
        # Bilateral
        resultats["bilateral"] = bilateral(
            image,
            sigma_color,
            sigma_spatial
        )

        # Affichage
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
            h,
            patch_size,
            patch_distance
        )
        denoised = resultats[method]

        difference = np.abs(image - denoised)

        # Affichage
        images_to_show = [
            ("Originale", image),
            ("Débruitée NLMean", denoised),
            ("Différence", difference)
        ]

    elif method == "anisotrope":

        # Anisotrope
        resultats["anisotrope"] = anisotrope(
            image,
            nbre_iter,
            gamma
        )
        denoised = resultats[method]

        difference = np.abs(image - denoised)

        # Affichage
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

        # Affichage
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