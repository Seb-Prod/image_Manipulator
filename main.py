import flet as ft
import os
import liste_fichier
from PIL import Image

def main(page: ft.Page):
    page.title = "Image Manipulator LITE"
    
    #le chemin vers le repertoir
    path = os.getcwd() + "/img/"
   
   
     #initialisation de l'image
    img = ft.Image(
        #src=path+"Git-logo.png",
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )
    
    #boite de la liste
    liste = ft.ListView(expand=1, spacing=10, padding=20,)

    #action quand on clique sur le nom de l'image
    def cliqueListe(e):
        img.src=path + e.control.data
        page.update()
        
    #boucle qui ajoute les bouton sur les noms des images
    for fichier in liste_fichier.lister_fichiers(path):
        liste.controls.append(ft.TextButton(text = fichier, on_click= cliqueListe,data= fichier))
        
    page.add(
        ft.OutlinedButton(text="Noir et Blanc"),
        ft.OutlinedButton("Couleur"),
    )

    # Fonction pour lister les fichiers
    def lister_fichiers(repertoire):
        return os.listdir(repertoire)

    # Obtenir le chemin du répertoire des images
    path = os.getcwd() + "/img"

    # Créer un répertoire temporaire pour les images modifiées
    temp_path = os.path.join(path, "temp")
    os.makedirs(temp_path, exist_ok=True)

    print("Le répertoire courant est : " + path)
    print(lister_fichiers(path))

    # Fonction pour convertir une image en noir et blanc
    def convertir_nb(image_path, output_path):
        img = Image.open(image_path)
        img = img.convert("L")  # Convertir en niveaux de gris
        img.save(output_path)  # Sauvegarder l'image convertie

    # Convertir les deux images en noir et blanc
    img1_path = os.path.join(path, "natureHD.jpg")

    img1_bw_path = os.path.join(temp_path, "natureHD_bw.jpg")
    
    convertir_nb(img1_path, img1_bw_path)
    
    # Charger les images modifiées dans Flet
    img1 = ft.Image(
        src=img1_bw_path,
        width=500,
        height=500,
    )

    # Centrer les images individuellement dans des conteneurs
    img1_container = ft.Container(content=img1, alignment=ft.alignment.center)

    # Ajouter les conteneurs dans un Row (affiche côte à côte)
    images = ft.Row(
        controls=[img1_container],
        expand=1,
        alignment=ft.MainAxisAlignment.CENTER,  # Centre les images dans la ligne
    )

    #bloc qui vont contenir les éléments de la page
    container_gestion_fichier = ft.Container(width=200, height=500, bgcolor=ft.colors.RED, content=liste)
    container_image = ft.Container(width=300, height=500, bgcolor=ft.colors.BLUE, content=img)
    container_boutons = ft.Container(width=100, height=500, bgcolor=ft.colors.ORANGE)

    #les blocs sont en ligne
    page.add(
        ft.Row([
            container_gestion_fichier,
            container_image,
            container_boutons
        ])
    )

    # for i in range(0, 60):
    #     lv.controls.append(ft.Text(f"Line {count}"))
    #     count += 1
    #     page.update()
    # Ajouter le Row contenant les images centrées à la page
    page.add(images)

ft.app(target=main)

