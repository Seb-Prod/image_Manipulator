import flet as ft
import os
from PIL import Image

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

    # Variables globales pour l'image sélectionnée
    current_image_path = None
    temp_path = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_path, exist_ok=True)

    # Image affichée
    displayed_image = ft.Image(
        width=500, height=500, fit=ft.ImageFit.CONTAIN
    )

    # Fonction pour gérer la sélection exclusive des cases à cocher
    def toggle_checkbox(e):
        if e.control == c1:  # Si la case "Noir et Blanc" est cochée
            c2.value = False
        elif e.control == c2:  # Si la case "Couleur" est cochée
            c1.value = False
        page.update()

    # Action des boutons
    def button_clicked(e):
        nonlocal current_image_path
        if current_image_path is None:
            t.value = "Veuillez d'abord sélectionner une image."
            page.update()
            return

        if c1.value:  # Noir et Blanc
            bw_path = os.path.join(temp_path, "bw_" + os.path.basename(current_image_path))
            convertir_nb(current_image_path, bw_path)
            displayed_image.src = bw_path
        elif c2.value:  # Couleur
            displayed_image.src = current_image_path

        t.value = f"Mode activé : {'Noir et Blanc' if c1.value else 'Couleur'}"
        page.update()

    # Action quand on clique sur un nom d'image
    def cliqueListe(e):
        nonlocal current_image_path
        selected_image = os.path.join(path, e.control.data)
        current_image_path = selected_image

        if c1.value:  # Mode Noir et Blanc
            bw_path = os.path.join(temp_path, "bw_" + os.path.basename(selected_image))
            convertir_nb(selected_image, bw_path)
            displayed_image.src = bw_path
        else:  # Mode Couleur
            displayed_image.src = selected_image

        t.value = f"Image sélectionnée : {os.path.basename(current_image_path)}"
        page.update()

    # Créer les Checkbox et le bouton
    t = ft.Text()
    c1 = ft.Checkbox(label="Noir et Blanc", value=True, on_change=toggle_checkbox)
    c2 = ft.Checkbox(label="Couleur", value=False, on_change=toggle_checkbox)
    b = ft.ElevatedButton(text="Valider", on_click=button_clicked)

    boutons_column = ft.Column(
        controls=[c1, c2, b, t],
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

    # Variables pour redimensionner l'image
    new_width = ft.TextField(label="Nouvelle Largeur", value="400", keyboard_type=ft.KeyboardType.NUMBER)
    new_height = ft.TextField(label="Nouvelle Hauteur", value="400", keyboard_type=ft.KeyboardType.NUMBER)

    # Action pour le bouton de redimensionnement
    def resize_image(e):
        nonlocal current_image_path
        if current_image_path is None:
            t.value = "Veuillez d'abord sélectionner une image."
            page.update()
            return

        try:
            new_w = int(new_width.value)
            new_h = int(new_height.value)
            if new_w <= 0 or new_h <= 0:
                raise ValueError("La largeur et la hauteur doivent être des entiers positifs.")

            resized_path = os.path.join(temp_path, "resized_" + os.path.basename(current_image_path))
            with Image.open(current_image_path) as img:
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                img.save(resized_path)

            displayed_image.src = resized_path
            t.value = f"Image redimensionnée à {new_w}x{new_h} pixels."
            page.update()
        except ValueError as e:
            t.value = f"Erreur : {str(e)}"
            page.update()

    # Ajouter le bouton de redimensionnement et les champs de texte pour la taille
    boutons_column.controls.append(ft.ElevatedButton(text="Redimensionner", on_click=resize_image))
    boutons_column.controls.append(new_width)
    boutons_column.controls.append(new_height)

ft.app(target=main)
