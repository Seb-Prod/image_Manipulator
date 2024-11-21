
from io import BytesIO
import os
from PIL import Image
import liste_fichier
from dataclasses import dataclass
import base64

@dataclass
class ParamModif:
        nb:bool
        rotation:int
        largeur:int
        hauteur:int
        mode:str

def lanceLesModif(infoImage:liste_fichier.Image, lesModif:ParamModif) ->str:
        imgModifier = Image.open(os.path.join(infoImage.rep, infoImage.nom))
        imgModifier = imgModifier.convert('RGB')
        
        #Si noir et blanc
        if lesModif.nb:
                imgModifier = imgModifier.convert("L")  # Convertir en niveaux de gris
        #Angle de l'image
        imgModifier = imgModifier.rotate(lesModif.rotation, expand=True)

        #taille image
        imgModifier = imgModifier.resize((lesModif.largeur, lesModif.hauteur))
        #imgModifier.save(os.path.join(os.getcwd(), "temp" + infoImage.ext))
        
        buffered = BytesIO()
        imgModifier.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()

def getTailleInitiale(infoImage:liste_fichier.Image) ->ParamModif:
        imgOrigin = Image.open(os.path.join(infoImage.rep, infoImage.nom))
        tailleImage = imgOrigin.size
        return ParamModif(nb=False, rotation=0, largeur=tailleImage[0], hauteur=tailleImage[1], mode=imgOrigin.mode)

def saveModif(infoImage:liste_fichier.Image, lesModif:ParamModif):
        imgModifier = Image.open(os.path.join(infoImage.rep, infoImage.nom))
        imgModifier = imgModifier.convert('RGB')
        #Si noir et blanc
        if lesModif.nb:
                imgModifier = imgModifier.convert("L")  # Convertir en niveaux de gris
        #Angle de l'image
        imgModifier = imgModifier.rotate(lesModif.rotation, expand=True)

        #taille image
        imgModifier = imgModifier.resize((lesModif.largeur, lesModif.hauteur))
        
        #Sauvegarde
        imgModifier.save(os.path.join(infoImage.rep, infoImage.nom))
        #imgModifier.save(os.path.join(infoImage.rep, infoImage.nom))

def ajoutImage(lien:str, nom:str, destination:str ):
        imgModifier = Image.open(lien)
        imgModifier = imgModifier.convert('RGB')
        imgModifier.save(os.path.join(destination, nom))
