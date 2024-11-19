import os

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