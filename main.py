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

    def actionCheckBox(e):
        print(paramModif)
        if e.data == "true":
            paramModif.nb = True
        else:
            paramModif.nb = False
        lanceModif()
          
    def actionRotationDroite(e):
        paramModif.largeur = int(new_height.value)
        paramModif.hauteur = int(new_width.value)

        new_width.value = paramModif.largeur
        new_height.value = paramModif.hauteur

        paramModif.rotation = paramModif.rotation - 90
        lanceModif()

    def actionRotationGauche(e):
        paramModif.largeur = int(new_height.value)
        paramModif.hauteur = int(new_width.value)

        new_width.value = paramModif.largeur
        new_height.value = paramModif.hauteur

        paramModif.rotation = paramModif.rotation + 90
        lanceModif()

    def actionChangeTaille(e):
        paramModif.largeur = int(new_width.value)
        paramModif.hauteur = int(new_height.value)
        lanceModif()

    def lanceModif():
        displayed_image.src_base64 = modif.lanceLesModif(infoImage, paramModif)
        page.update()

    # Variables globales
    current_image_path = None
    temp_path = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_path, exist_ok=True)
    mode_nb = False  # Par défaut, le mode est en couleur

    # Image affichée
    displayed_image = ft.Image(
        width=500, height=500, fit=ft.ImageFit.CONTAIN
    )

    # Action pour basculer le mode Couleur / Noir et Blanc
    def toggle_mode(e):
        # nonlocal mode_nb, current_image_path
        # mode_nb = not mode_nb  # Bascule le mode
        # mode_button.text = "Passer en Couleur" if mode_nb else "Passer en Noir et Blanc"

        # if current_image_path is not None:
        #     if mode_nb:  # Noir et Blanc
        #         bw_path = os.path.join(temp_path, "bw_" + os.path.basename(current_image_path))
        #         convertir_nb(current_image_path, bw_path)
        #         displayed_image.src = bw_path
        #     else:  # Couleur
        #         displayed_image.src = current_image_path

        # page.update()
        if not paramModif.nb:
            mode_button.text = "Passer en Couleur"
            paramModif.nb = True
        else:
            mode_button.text = "Passer en Noir t Blanc"
            paramModif.nb = False
        lanceModif()
        page.update()

        print(paramModif)

    # Action quand on clique sur un nom d'image
    def cliqueListe(e):
        nonlocal current_image_path
        container_image.visible = True
        container_boutons.visible = True
        selected_image = os.path.join(e.control.data.rep, e.control.data.nom)
        current_image_path = selected_image
        displayed_image.src = selected_image

        checkboxNoirEtBlanc.value = False
        infoImage.nom = e.control.data.nom
        infoImage.rep = e.control.data.rep
        infoImage.ext = e.control.data.ext
        paramModif.largeur = modif.getTailleInitiale(infoImage).largeur
        paramModif.hauteur = modif.getTailleInitiale(infoImage).hauteur
        paramModif.mode = modif.getTailleInitiale(infoImage).mode
        paramModif.nb = False
        mode_button.text = "Passer en Couleur"
        paramModif.rotation = 0
        new_width.value = paramModif.largeur
        new_height.value = paramModif.hauteur

        
        displayed_image.src_base64 = modif.lanceLesModif(infoImage, paramModif)

        t.value = f"Image sélectionnée : {os.path.basename(current_image_path)}"
        page.update()

    # Action pour redimensionner l'image
    def resize_image(e):
        nonlocal current_image_path
        if current_image_path is None:
            t.value = "Veuillez d'abord sélectionner une image."
            page.update()
            return

        try:
            # Vérifier que les champs ne sont pas vides
            if not new_width.value or not new_height.value:
                raise ValueError("Veuillez entrer une largeur et une hauteur.")

            # Récupérer les dimensions saisies par l'utilisateur
            new_w = int(new_width.value)
            new_h = int(new_height.value)

            # Validation des dimensions
            if new_w <= 0 or new_h <= 0:
                raise ValueError("Les dimensions doivent être des entiers positifs.")
            if new_w > 1920 or new_h > 1080:
                raise ValueError("Les dimensions ne peuvent pas dépasser 1920x1080 pixels.")

            resized_path = os.path.join(temp_path, "resized_" + os.path.basename(current_image_path))
            with Image.open(current_image_path) as img:
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                img.save(resized_path)

            displayed_image.src = resized_path
            t.value = f"Image redimensionnée à {new_w}x{new_h} pixels."

            # Ouvrir l'image redimensionnée dans une nouvelle fenêtre
            webbrowser.open(f"file://{resized_path}")

            page.update()
        except ValueError as e:
            t.value = f"Erreur : {str(e)}"
            page.update()

    # Texte d'information
    t = ft.Text()

    # Bouton pour basculer le mode Noir et Blanc / Couleur
    checkboxNoirEtBlanc = ft.Checkbox(label="Noire et blanc", value=False, on_change=actionCheckBox, visible=False)
    mode_button = ft.ElevatedButton(text="Passer en Noir et Blanc", on_click=toggle_mode)

    # Champs pour entrer les dimensions de redimensionnement (sans valeurs par défaut)
    new_width = ft.TextField(label="Largeur (max 1920)", input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""))
    new_height = ft.TextField(label="Hauteur (max 1080)", input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""))


    # Bouton pour redimensionner l'image
    resize_button = ft.ElevatedButton(text="Redimensionner", on_click=actionChangeTaille)
    
    # Bouton pour faire une rotation de l'image
    rotate_button_right = bouton.monBouton(actionRotationDroite, ft.icons.ROTATE_RIGHT)
    rotate_button_left = bouton.monBouton(actionRotationGauche, ft.icons.ROTATE_LEFT)
    
    #ligne des boutons de ratation
    ligneBoutonRotation = ft.Row(controls=[rotate_button_left, rotate_button_right])


    # Colonne des contrôles
    boutons_column = ft.Column(
        controls=[mode_button,checkboxNoirEtBlanc, new_width, new_height, resize_button, ligneBoutonRotation, t],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Liste des fichiers
    liste = ft.ListView(expand=1, spacing=10, padding=20)

    def chargeListe(rep: str):
        for fichier in liste_fichier.lister_fichiers2(os.path.join(rep)):
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
        liste.controls.clear()
        chargeListe(e.path)
        page.update()

    # Le popup du choix du fichier
    file_picker = ft.FilePicker(on_result=getFolder)
    page.overlay.append(file_picker)

    # Bouton qui affiche le popup du choix du répertoire
    bt = ft.ElevatedButton("Choisir le répertoire", on_click=lambda _: file_picker.get_directory_path())
    
    # Ligne avec le bouton
    ligneBoutonsFichier = ft.Row([bt, bouton.monBouton(cacheListe, ft.icons.CLOSE)])
    blocGestionFichier = ft.Column([ligneBoutonsFichier, liste])

    # Conteneurs pour chaque section
    container_menu = ft.Container(width=60, content=bouton.monBouton(afficheListe, ft.icons.FOLDER), visible=False)
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
