import flet as ft
import os

def main(page : ft.Page):
    page.title = "Image Manipulator LITE"

    def lister_fichiers(repertoire):
        return os.listdir(repertoire)

    path = os.getcwd() + "/img"

    print("Le répertoire courant est : " + path)
    print(lister_fichiers(path))

    img = ft.Image(
        src=path+"/Git-logo.png",
        width=100,
        height=100,
        fit=ft.ImageFit.CONTAIN,
    )
    
    images = ft.Row(expand=1, wrap=False, scroll="always")

    page.add(img, images)


ft.app(main)