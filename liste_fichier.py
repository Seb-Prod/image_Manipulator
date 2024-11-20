import os
from dataclasses import dataclass
from typing import List

@dataclass
class Image:
        nom:str
        rep:str

# retourne un tableau avec la liste des fichier image du répertoire sélectioné
def lister_fichiers(repertoire) ->List[Image]:
        #initialisation du tableau qui stockera les noms des images
        result:Image =[]

        #Tableau d'extensions des fichiers images
        extension = [".png", ".jpeg", ".jpg", ".webp"]

        #Boucle qui parcour le répertoire et ajoute dans le tableau result uniquement les fichiers images
        for file in os.listdir(repertoire):
                if file.endswith(tuple(extension)):
                        result.append(Image(nom=file, rep=repertoire))
                        

        #Retourne le tableau        
        return result
