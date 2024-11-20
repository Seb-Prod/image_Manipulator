import flet as ft
import os
import liste_fichier
from PIL import Image
import noirEtBlanc

import bouton

infoImage:liste_fichier.Image = liste_fichier.Image(rep="", nom="", ext="")

def main(page : ft.Page):
    page.title = "Image Manipulator LITE"
    
    #le chemin vers le repertoir
    path = os.getcwd()
    temp_path = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_path, exist_ok=True)
   
     #initialisation de l'image
    img = ft.Image(width=200, height=200, fit=ft.ImageFit.CONTAIN)
    
    #boite de la liste
    liste = ft.ListView(expand=1, spacing=10, padding=20,)

    #action quand on clique sur le nom de l'image
    def cliqueListe(e):
        # global srcImageOrigine
        srcImageOrigine = os.path.join(e.control.data.rep, e.control.data.nom)
        img.src= os.path.join(srcImageOrigine)
        infoImage.nom = e.control.data.nom
        infoImage.rep = e.control.data.rep
        infoImage.ext = e.control.data.ext
        page.update()
        
    #boucle qui ajoute les bouton sur les noms des images
    def chargeListe(rep:str):
        for fichier in liste_fichier.lister_fichiers(os.path.join(rep)):
            liste.controls.append(ft.TextButton(text = fichier.nom, on_click=cliqueListe, data= fichier))
    
    #action quand on valide un répertoire
    def getFolder(e):
        liste.controls.clear()
        chargeListe(e.path)
        page.update()
       
    #affiche le popup du choix du fichier
    file_picker = ft.FilePicker(on_result=getFolder)
    page.overlay.append(file_picker)
    
    bt = ft.ElevatedButton("Choisir le répertoire", on_click=lambda _: file_picker.get_directory_path())
    
    def clickCheckBox(e):
        if(e.data == 'true'):
            noirEtBlanc.noirEtBlanc(infoImage)
            img.src = os.path.join(path, "temp" + infoImage.ext)
            page.update()
        else:
            img.src = os.path.join(infoImage.rep, infoImage.nom)
            page.update()

    c1 = ft.Checkbox(label="Noir et Blanc", value=False, on_change=clickCheckBox)

    def cacheListe(e):
        container_menu.visible = True
        container_gestion_fichier.visible = False
        page.update()

    def afficheListe(e):
        container_menu.visible = False
        container_gestion_fichier.visible = True
        page.update()

    
    #Ligne avec le bouton qui affiche le popup du choix du répertoire et du bouton qui cache le container
    ligneBoutonsFichier = ft.Row([bt, bouton.monBouton(cacheListe, ft.icons.CLOSE)])
    blocGestionFichier = ft.Column([ligneBoutonsFichier, liste])

    #bloc qui vont contenir les éléments de la page
    container_menu = ft.Container(width=60, height=60, content=bouton.monBouton(afficheListe, ft.icons.FOLDER))
    container_gestion_fichier = ft.Container(width=250, height=500, content=blocGestionFichier, visible=False)
    container_image = ft.Container(expand=3, height=500, bgcolor=ft.colors.BLUE, content=img)
    container_boutons = ft.Container(width=200, height=500, bgcolor=ft.colors.ORANGE, content=c1)



    #les blocs sont en ligne
    page.add(
        ft.Row([
            container_menu,
            container_gestion_fichier,
            container_image,
            container_boutons
        ])
    )

    

ft.app(main)

