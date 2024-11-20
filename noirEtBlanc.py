import liste_fichier
from PIL import Image
import os

def noirEtBlanc(infoImage:liste_fichier.Image):
    path = os.getcwd()
    imageModif = Image.open(os.path.join(infoImage.rep, infoImage.nom))
    imageModif = imageModif.convert("L")
    imageModif.save(os.path.join(path, "temp" + infoImage.ext))