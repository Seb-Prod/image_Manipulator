import flet as ft
import os
from PIL import Image
import webbrowser
import liste_fichier
import bouton
import modificationImage as modif

infoImage: liste_fichier.Image = liste_fichier.Image(rep="", nom="", ext="")
paramModif: modif.ParamModif = modif.ParamModif(nb=False, rotation=0, largeur=0, hauteur=0, mode="RGB")


def main(page: ft.Page):
    page.title = "Image Manipulator LITE"
    
    #Préparation modification de l'image (rotation)
    def actionRotationDroite(e):
        actionRotation(-90)

    def actionRotationGauche(e):
        actionRotation(90)

    def actionRotation(angle:int):
        paramModif.largeur = int(new_height.value)
        paramModif.hauteur = int(new_width.value)

        new_width.value = paramModif.largeur
        new_height.value = paramModif.hauteur

        paramModif.rotation = paramModif.rotation + 90
        lanceModif()

    #Préparation modification de l'image (taille)
    def actionChangeTaille(e):
        paramModif.largeur = int(new_width.value)
        paramModif.hauteur = int(new_height.value)
        lanceModif()

    #Préparation modifcation de l'image (N/B)
    def actionChangeCouleur(e):
        if not paramModif.nb:
            mode_button.text = "Passer en Couleur"
            paramModif.nb = True
        else:
            mode_button.text = "Passer en Noir et Blanc"
            paramModif.nb = False
        lanceModif()
    
    #Application des modification
    def lanceModif():
        displayed_image.src_base64 = modif.lanceLesModif(infoImage, paramModif)
        page.update()

    #Enregistrement des modification
    def actionBoutonEnregistrerImg(e):
        page.open(demandeConfimationSauvegarde)
        

    def traitementReponseSauvegarde(e):
        page.close(demandeConfimationSauvegarde)
        print(e.control.text)
        if e.control.text == "Oui":
            modif.lanceLesModif(infoImage, paramModif, True)
            page.open(confimationSauvegarde)

    demandeConfimationSauvegarde = ft.AlertDialog(
        modal=True,
        title=ft.Text("Enregistrement"),
        content=ft.Text("Voulez vous enregistrer les modification ?"),
        actions=[
            ft.TextButton("Oui", on_click=traitementReponseSauvegarde),
            ft.TextButton("Non", on_click=traitementReponseSauvegarde),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    confimationSauvegarde = ft.AlertDialog(
        title=ft.Text("Sauvegarde faite")
    )

    #Lance l'actualisation de la liste selon la recherche
    def actionBoutonRecherche(e):
        liste.controls.clear()
        fichiers = liste_fichier.lister_recherche(infoImage.rep, saisieRecherche.value)
        fichiers_trie = sorted(fichiers, key=lambda f: f.nom.lower())  # Trie les fichiers par nom
        for fichier in fichiers_trie:
            liste.controls.append(ft.TextButton(text=fichier.nom, on_click=cliqueListe, data=fichier))
        page.update()
    
    #Affiche le popup du choix du fichier à inporter
    def actionBoutonAjoutImg(e):
        file_pickerAdd.pick_files(
                allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"],dialog_title="Sélectionnez l'image à ajouter")

    #Lance l'ajout de l'image séléctionné à la bibliothèque
    def ajoutImg(e: ft.FilePickerResultEvent):
        if not e.files == None:
            for file in e.files:
                modif.ajoutImage(file.path, file.name, infoImage.rep)
            liste.controls.clear()
            chargeListe(infoImage.rep)
            page.update()

    #Image d'aperçus
    displayed_image = ft.Image()

    # Action quand on choisie une image à afficher
    def cliqueListe(e):
        container_image.visible = True
        container_boutons.visible = True
        # selected_image = os.path.join(e.control.data.rep, e.control.data.nom)
        # current_image_path = selected_image
        # displayed_image.src = selected_image

        infoImage.nom = e.control.data.nom
        infoImage.rep = e.control.data.rep
        infoImage.ext = e.control.data.ext
        paramModif.largeur = modif.getTailleInitiale(infoImage).largeur
        paramModif.hauteur = modif.getTailleInitiale(infoImage).hauteur
        paramModif.mode = modif.getTailleInitiale(infoImage).mode
        paramModif.nb = False
        mode_button.text = "Passer en Noir et Blanc"
        paramModif.rotation = 0
        new_width.value = paramModif.largeur
        new_height.value = paramModif.hauteur

        
        displayed_image.src_base64 = modif.lanceLesModif(infoImage, paramModif)

        #t.value = f"Image sélectionnée : {os.path.basename(current_image_path)}"
        page.update()


    # Texte d'information
    t = ft.Text()

    # Bouton pour basculer le mode Noir et Blanc / Couleur
    mode_button = ft.ElevatedButton(text="Passer en Noir et Blanc", on_click=actionChangeCouleur)

    # Champs pour entrer les dimensions de redimensionnement (sans valeurs par défaut)
    new_width = ft.TextField(label="Largeur (max 1920)", input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""))
    new_height = ft.TextField(label="Hauteur (max 1080)", input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""))

    # Bouton pour redimensionner l'image
    resize_button = ft.ElevatedButton(text="Redimensionner", on_click=actionChangeTaille)
    
    # Bouton pour faire une rotation de l'image
    rotate_button_right = bouton.monBouton(actionRotationDroite, ft.icons.ROTATE_RIGHT,"Rotation à Droite")
    rotate_button_left = bouton.monBouton(actionRotationGauche, ft.icons.ROTATE_LEFT, "Rotation à Gauche")
    
    
    #ligne des boutons de ratation
    ligneBoutonRotation = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[rotate_button_left, rotate_button_right])
    
    bouton_enregistrer = bouton.monBouton(actionBoutonEnregistrerImg, ft.icons.SAVE_ALT_SHARP, "Enregistrer")

    # Colonne des contrôles
    boutons_column = ft.Column(
        controls=[mode_button, new_width, new_height, resize_button, ligneBoutonRotation, bouton_enregistrer ,t],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Liste des fichiers
    liste = ft.ListView(expand=1, spacing=10, padding=20)

    def chargeListe(rep: str):
        fichiers = liste_fichier.lister_fichiers2(os.path.join(rep))
        fichiers_trie = sorted(fichiers, key=lambda f: f.nom.lower())  # Trie les fichiers par nom, insensible à la casse
        for fichier in fichiers_trie:
            liste.controls.append(ft.TextButton(text=fichier.nom, on_click=cliqueListe, data=fichier))

    # Cache le container gestion fichier
    def cacheListe(e):
        container_menu.visible = True
        container_gestion_fichier.visible = False
        page.update()

    # Affiche le container gestion fichier
    def afficheListe(e):
        container_menu.visible = False
        container_gestion_fichier.visible = True
        page.update()

    # Action quand on valide un répertoire
    def getFolder(e):
        if not e.path==None:
            liste.controls.clear()
            infoImage.rep = e.path
            chargeListe(e.path)
            ligneRecherche.visible=True
            boutonAjoutImage.visible = True
        page.update()

    # Le popup du choix du répertoire
    file_picker = ft.FilePicker(on_result=getFolder)
    page.overlay.append(file_picker)

    # Le popup du choix du fichier à ajouter
    file_pickerAdd = ft.FilePicker(on_result=ajoutImg)
    page.overlay.append(file_pickerAdd)

    # Bouton qui affiche le popup du choix du répertoire
    bt = ft.ElevatedButton("Choisir le répertoire", on_click=lambda _: file_picker.get_directory_path())
    saisieRecherche = ft.TextField(label="Recherche", width=185)
    boutonLanceRecherche = bouton.monBouton(actionBoutonRecherche, ft.icons.SEARCH, "Lancer la recherche")
    boutonAjoutImage = bouton.monBouton(actionBoutonAjoutImg, ft.icons.ADD_CIRCLE, "Ajouter une image")
    boutonAjoutImage.visible = False

    # Ligne avec le bouton
    ligneBoutonsFichier = ft.Row([bt, bouton.monBouton(cacheListe, ft.icons.CLOSE, "Masquer la liste")])
    ligneRecherche = ft.Row([saisieRecherche, boutonLanceRecherche], visible=False)
    blocGestionFichier = ft.Column([ligneBoutonsFichier, ligneRecherche , liste,boutonAjoutImage])

    # Conteneurs pour chaque section
    container_menu = ft.Container(width=60, content=bouton.monBouton(afficheListe, ft.icons.FOLDER, "Afficher la liste"), visible=False)
    container_gestion_fichier = ft.Container(content=blocGestionFichier, width=250, visible=True)
    container_image = ft.Container(content=displayed_image, expand=1, visible=False)
    container_boutons = ft.Container(content=boutons_column, width=250, visible=False)

    # Ajouter les conteneurs alignés horizontalement
    page.add(
        ft.Row(
            [
                container_menu,
                container_gestion_fichier,
                container_image,
                container_boutons
            ],
            expand=1
        )
        
        
    )

ft.app(target=main)
