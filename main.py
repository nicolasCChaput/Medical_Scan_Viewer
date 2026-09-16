import argparse

from view_image import view_image
#from compute_mIP_MIP import compute_projection
#from show_image_stats import show_stats
#from denoise_image import denoise_image

def main():

    parser = argparse.ArgumentParser(
        description= "Voici le parser du TP1 d'IMN530"
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
        "--flip",
        choices=["yes", "no"],
        required=False,
        default="no"
    )

    # parser_view.add_argument(
    #     "--slice",
    #     choices=["axiale", "coronale", "sagittale"],
    #     default="axiale"
    # )

    # ---
    # Pour compute_mIP-MIP.py
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

    args = parser.parse_args()

    if args.command == "view":
         view_image(args.image, args.flip)
    #
    # elif args.command == "projection":
    #     compute_projection(
    #         args.image,
    #         args.axis,
    #         args.mode
    #     )
    #
    # elif args.command == "stats":
    #     show_stats(args.image)
    #
    # elif args.command == "denoise":
    #     denoise_image(args.image)


if __name__ == "__main__":
    main()

