import flet as ft

from ui.theme.colors import AppColors
from ui.theme.radius import AppRadius

def LanguagePicker(languages, on_select):
    
    items = [
        ft.PopupMenuItem(
            content=ft.Text(
                language,
                color=AppColors.TEXT_PRIMARY,
                size=14,
            ),
            data=language,
            on_click=on_select,
        )
        for language in languages
    ]
    
    ## Add an option for languages that are not included in the list.
    items.append(
        ft.PopupMenuItem(
            content=ft.Text(
                "🌐 Other language...",
                color=AppColors.PRIMARY,
                size=14,
                weight=ft.FontWeight.BOLD,
            ),
            data="__other_language__",
            on_click=on_select,
        )
    )
    
    return ft.PopupMenuButton(
        icon=ft.Icons.LANGUAGE,
        icon_color=AppColors.PRIMARY,
        tooltip="Choose language",
        items=items,
    )