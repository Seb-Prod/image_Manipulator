import flet as ft
import os
from PIL import Image
import liste_fichier

def rotate_image_with_pil(infoImage:liste_fichier.Image, angle:int):
    """
    Cette fonction utilise PIL pour effectuer une rotation d'image et enregistre le résultat.

    Args:
        image_path (str): Le chemin vers l'image d'origine.
        angle (float): L'angle de rotation en degrés.
        output_path (str): Le chemin où enregistrer l'image tournée.
    """
    try:
        # Ouvrir l'image
        print(infoImage)
        with Image.open(os.path.join(infoImage.rep, infoImage.nom)) as img:
            rotated_img = img.rotate(angle, expand=True)
            
            # Enregistrer l'image tournée
            rotated_img.save(os.path.join(os.getcwd(), "temp" + infoImage.ext))

            
    except Exception as e:
        print(f"Erreur lors de la rotation de l'image : {e}")

