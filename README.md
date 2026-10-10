# Travail pratique 1 — IMN530 : Reconstruction et analyse d'images médicales

Université de Sherbrooke
Faculté des sciences — Département d’informatique

Fait dans le cadre du cours IMN530 pour le professeur Maxime Descoteaux

## Auteur
Nicolas Claveau-Chaput

Sherbrooke, 11 octobre 2026

## Résumé du travail fait

Ce travail pratique porte sur la reconstruction et l'analyse d'images médicales. Les fonctionnalités développées permettent :

- La visualisation interactive d'images médicales au format NIfTI;
- L'analyse de l'orientation des volumes à l'aide de Nibabel et MrInfo;
- Le calcul de projections d'intensité maximale (MIP) et minimale (MinIP);
- Le calcul de statistiques descriptives sur les images;
- L'application et la comparaison de différentes méthodes de débruitage incluant :
  - NLMeans (Non-Local Means);
  - Diffusion anisotrope;
  - Filtrage bilatéral.

L'ensemble est accessible via une interface en ligne de commande basée sur un argparser centralisé.

## Dépendances

Le projet a été développé en Python 3 et nécessite les bibliothèques suivantes :

- numpy
- matplotlib
- nibabel
- scipy
- scikit-image

**Pour rouler MRInfo sur Windows, MRTrix3 est nécessaire.**

### Installation

Avec pip :

```bash
pip install -r requirements.txt 
```

## Screenshot
![viewer.png](../../../Downloads/viewer.png)
![falirnlmeanshauth.png](../../../Downloads/falirnlmeanshauth.png)