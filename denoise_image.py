import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from pathlib import Path
from matplotlib.widgets import Slider

"""
denoise_image.py
...

Arguments
--image (REQUIS): Chemin vers les images à débruiter. ("path/to/image.abc")
--method: 

Exemple d'usage:
    python main.py denoise --image "C:path\to\Data_TP1\Data_TP0\IRM\Brain\flair.nii"
"""

def denoise_image(image_path):
    return