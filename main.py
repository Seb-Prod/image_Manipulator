import flet as ft
import os
import liste_fichier

def main(page : ft.Page):
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

ft.app(main)