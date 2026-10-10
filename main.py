"""
main.py

Gestionnaire du argparser.

Ce fichier agit comme point d'entrée principal du projet et permet
d'accéder aux différentes fonctionnalités développées dans le cadre
du TP1.

Sous-commandes disponibles :
    view        : Affichage d'images médicales
    projection  : Calcul de projections MIP et MinIP
    stats       : Calcul de statistiques d'images
    denoise     : Application de méthodes de débruitage

Auteur: Nicolas Claveau-Chaput
"""

import argparse

from view_image import view_image
from compute_mIP_MIP import compute_projection
from show_image_stats import show_stats
from denoise_image import denoise_image

def main():

    parser = argparse.ArgumentParser(
        description= "Voici le argparser du TP1 d'IMN530"
    )
    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )


    # ---
    # Pour view_image.py
    # ---
    parser_view = subparsers.add_parser(
        "view",
        help="Display an image"
    )

    parser_view.add_argument(
        "--image",
        required=True,
        help="Path to the image"
    )
    parser_view.add_argument(
        "--grayscale",
        choices=["yes", "no"],
        help="Grayscale the images",
        default="yes"
    )
    parser_view.add_argument(
        "--mrinfo",
        choices=["yes", "no"],
        help="Grayscale the images",
        default="no"
    )
    # --- Fin view_image.py ---


    # ---
    # Pour compute_mIP_MIP.py
    # ---
    parser_proj = subparsers.add_parser(
        "projection",
        help="Compute MIP or MinIP"
    )

    parser_proj.add_argument(
        "--image",
        required=True
    )
    parser_proj.add_argument(
     "--axis",
        choices=["x", "y", "z"],
        default="x"
    )
    parser_proj.add_argument(
        "--mode",
        choices=["max", "min"],
        default="max",
    )
    parser_proj.add_argument(
        "--grayscale",
        choices=["yes", "no"],
        help="Grayscale the images",
        default="yes"
    )
    # --- Fin compute_mIP_MIP.py ---

    # ---
    # Pour show_image_stats.py
    # ---
    parser_stats = subparsers.add_parser(
        "stats",
        help="Display image statistics"
    )

    parser_stats.add_argument(
        "--image",
        required=True
    )
    # --- Fin show_image_stats.py ---

    # ---
    # Pour denoise_image.py
    # ---

    parser_denoise = subparsers.add_parser(
        "denoise",
        help="Apply denoising methods"
    )

    parser_denoise.add_argument(
        "--image",
        required=True
    )
    parser_denoise.add_argument(
        "--method",
        choices=["nlmeans", "anisotrope", "bilateral", "all" ],
        default="nlmeans"
    )

    # NLMeans
    parser_denoise.add_argument(
        "--h",
        type=float,
        default=2,
        help="NLMeans - Force du débruitage"
    )
    parser_denoise.add_argument(
        "--patch_size",
        type=int,
        default=5,
        help="NLMeans - Taille des patches comparés"
    )
    parser_denoise.add_argument(
        "--patch_distance",
        type=int,
        default=15,
        help="NLMeans - Rayon de recherche des patches"
    )

    # Diffusion anisotrope
    parser_denoise.add_argument(
        "--nbre_iter",
        type=int,
        default=10,
        help="Anisotrope - Nombre d'itérations de diffusion"
    )

    parser_denoise.add_argument(
        "--gamma",
        type=float,
        default=0.1,
        help="Anisotrope - Vitesse de diffusion"
    )

    # Bilateral
    parser_denoise.add_argument(
        "--sigma_color",
        type=float,
        default=0.05,
        help="Bilateral - Sensibilité aux différences d'intensité"
    )

    parser_denoise.add_argument(
        "--sigma_spatial",
        type=float,
        default=12,
        help="Bilateral - Étendue spatiale du filtre bilateral"
    )
    # --- Fin denoise_image.py ---


    # --- Gestion de l'appel de main.py ---

    args = parser.parse_args()

    if args.command == "view":
         view_image(
             args.image,
             args.grayscale,
             args.mrinfo
         )

    elif args.command == "projection":
        compute_projection(
            args.image,
            args.axis,
            args.mode,
            args.grayscale
        )

    elif args.command == "stats":
        show_stats(args.image)

    elif args.command == "denoise":
        denoise_image(
            # Image
            args.image,

            # NLMean
            args.method,
            args.h,
            args.patch_size,
            args.patch_distance,

            # Anisotrope
            args.nbre_iter,
            args.gamma,

            # Bilateral
            args.sigma_color,
            args.sigma_spatial
        )


if __name__ == "__main__":
    main()