import flet as ft

#création d'un bouton avec son icon
def monBouton(fonction, icon) ->ft.IconButton:
    return ft.IconButton(icon=icon, alignment=ft.alignment.top_center, icon_size=40, on_click=fonction)

