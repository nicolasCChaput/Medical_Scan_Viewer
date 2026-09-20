import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from pathlib import Path
from matplotlib.widgets import Slider

"""
show_image_stats.py
...

Arguments
--image (REQUIS): Chemin vers les images à analyser. ("path/to/image.abc")

Exemple d'usage:
    python main.py stats --image "C:path\to\Data_TP1\Data_TP0\IRM\Brain\flair.nii"
"""

def show_stats(image_path):
    return