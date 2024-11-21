import flet as ft
from PIL import Image
import io
import os

def main(page: ft.Page):
    button = create_rotating_image_button("")
    page.add(button)

# def rotate_image(e):
        
#         image.rotate += math.pi / 2
#         page.update()
#création d'un bouton avec son icon
# def monBouton(fonction, icon) ->ft.IconButton:
#     return ft.IconButton(icon=icon, alignment=ft.alignment.top_center, icon_size=40, on_click=rotate_image)




    # Boutons pour la rotation
# left_button = ft.IconButton(
#         icon=ft.icons.ROTATE_LEFT,
#         on_click=lambda e: rotate_image("left"),
#     )
# right_button = ft.IconButton(
#         icon=ft.icons.ROTATE_RIGHT,
#         on_click=lambda e: rotate_image("right"),
#     )

    # Ajouter les widgets à la page


    # Fonction pour gérer la rotation

def create_rotating_image_button(image_path):
    image = Image.open(image_path)
    bio = io.BytesIO()
    image.save(bio, 'PNG')
    img_bytes = bio.getvalue()

    def rotate_image(e):
        global image
        image = image.rotate(90)
        bio.seek(0)
        image.save(bio, 'PNG')
        e.control.image.src = img_bytes
        page.update()

    return ft.IconButton(
        icon=ft.Image(src=img_bytes),
        on_click=rotate_image
    )
button = create_rotating_image_button(os.path.join("img/Git-logo.png"))
page.add(button)

            
ft.app(target=main)