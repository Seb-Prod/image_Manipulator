import os
from dataclasses import dataclass
from typing import List
import pathlib

def lister_fichiers(repertoire):
        #initialisation du tableau qui stockera les noms des images
        result =[]

        #Tableau d'extensions des fichiers images
        extension = [".png", ".jpeg", ".jpg", ".webp"]

        #Boucle qui parcour le répertoire et ajoute dans le tableau result uniquement les fichiers images
        for file in os.listdir(repertoire):
                if file.endswith(tuple(extension)):
                        result.append(file)

        #Retourne le tableau        
        return result



@dataclass
class Image:
        nom:str
        rep:str
        ext:str

# retourne un tableau avec la liste des fichier image du répertoire sélectioné
def lister_fichiers2(repertoire) ->List[Image]:
        #initialisation du tableau qui stockera les noms des images
        result:Image =[]

        #Tableau d'extensions des fichiers images
        extension = [".png", ".jpeg", ".jpg", ".webp"]

        #Boucle qui parcour le répertoire et ajoute dans le tableau result uniquement les fichiers images
        for file in os.listdir(repertoire):
                if file.endswith(tuple(extension)):
                        path = pathlib.Path(os.path.join(repertoire, file))
                        result.append(Image(nom=file, rep=repertoire, ext=path.suffix))
                        

        #Retourne le tableau        
        return result

# retourne un tableau avec la liste des fichier image du répertoire sélectioné
def lister_recherche(repertoire, recherche) ->List[Image]:
        result:Image =[]
        extension = [".png", ".jpeg", ".jpg", ".webp"]

        for file in os.listdir(repertoire):
                if file.endswith(tuple(extension)):
                        if recherche in file:
                                print("Le mot", recherche, "est présent dans le texte.")
                                path = pathlib.Path(os.path.join(repertoire, file))
                                result.append(Image(nom=file, rep=repertoire, ext=path.suffix))
        
        return result