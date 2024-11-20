import flet as ft
import os
from PIL import Image
import webbrowser

def main(page: ft.Page):
    page.title = "Image Manipulator LITE"

    # Fonction pour convertir une image en noir et blanc
    def convertir_nb(image_path, output_path):
        img = Image.open(image_path)
        img = img.convert("L")  # Convertir en niveaux de gris
        img.save(output_path)  # Sauvegarder l'image convertie

    # Fonction pour lister les fichiers (en excluant le dossier 'temp')
    def lister_fichiers(repertoire):
        # Filtrer les fichiers pour exclure "temp"
        return [f for f in os.listdir(repertoire) if f != "temp" and os.path.isfile(os.path.join(repertoire, f))]

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
        nonlocal mode_nb, current_image_path
        mode_nb = not mode_nb  # Bascule le mode
        mode_button.text = "Passer en Couleur" if mode_nb else "Passer en Noir et Blanc"

        if current_image_path is not None:
            if mode_nb:  # Noir et Blanc
                bw_path = os.path.join(temp_path, "bw_" + os.path.basename(current_image_path))
                convertir_nb(current_image_path, bw_path)
                displayed_image.src = bw_path
            else:  # Couleur
                displayed_image.src = current_image_path

        page.update()

    # Action quand on clique sur un nom d'image
    def cliqueListe(e):
        nonlocal current_image_path
        selected_image = os.path.join(path, e.control.data)
        current_image_path = selected_image

        # Appliquer le mode actuel à l'image sélectionnée
        if mode_nb:  # Noir et Blanc
            bw_path = os.path.join(temp_path, "bw_" + os.path.basename(selected_image))
            convertir_nb(selected_image, bw_path)
            displayed_image.src = bw_path
        else:  # Couleur
            displayed_image.src = selected_image

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
    mode_button = ft.ElevatedButton(text="Passer en Noir et Blanc", on_click=toggle_mode)

    # Champs pour entrer les dimensions de redimensionnement
    new_width = ft.TextField(label="Largeur (max 1920)", value="1920", keyboard_type=ft.KeyboardType.NUMBER)
    new_height = ft.TextField(label="Hauteur (max 1080)", value="1080", keyboard_type=ft.KeyboardType.NUMBER)

    # Bouton pour redimensionner l'image
    resize_button = ft.ElevatedButton(text="Redimensionner", on_click=resize_image)

    # Colonne des contrôles
    boutons_column = ft.Column(
        controls=[mode_button, new_width, new_height, resize_button, t],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Définir le chemin des images
    path = os.path.join(os.getcwd(), "img")
    os.makedirs(path, exist_ok=True)

    # Liste des fichiers sans le dossier "temp"
    liste = ft.ListView(expand=1, spacing=10, padding=20)

    for fichier in lister_fichiers(path):
        liste.controls.append(ft.TextButton(text=fichier, on_click=cliqueListe, data=fichier))

    # Conteneurs pour chaque section
    container_gestion_fichier = ft.Container(
        bgcolor=ft.colors.RED, content=liste, expand=1
    )
    container_image = ft.Container(
        bgcolor=ft.colors.BLUE, content=displayed_image, expand=1
    )
    container_boutons = ft.Container(
        bgcolor=ft.colors.ORANGE, content=boutons_column, expand=1
    )

    # Ajouter les conteneurs alignés horizontalement
    page.add(
        ft.Row(
            [
                container_gestion_fichier,
                container_image,
                container_boutons
            ],
            expand=1
        )
    )

ft.app(target=main)
