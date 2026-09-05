import flet as ft

from ui.theme.colors import AppColors
from ui.theme.radius import AppRadius

class NatureButton(ft.FilledButton):

    def __init__(self, text: str, on_click=None):
        
        self.button_text = ft.Text(
            text,
            size=15,
            weight=ft.FontWeight.BOLD,
            color="white",
        )

        super().__init__(
            content=self.button_text,
            on_click=on_click,
            height=46,
            style=ft.ButtonStyle(
                bgcolor=AppColors.PRIMARY,
                color="white",
                shape=ft.RoundedRectangleBorder(
                    radius=AppRadius.MEDIUM,
                ),
                padding=ft.Padding(
                    left=24,
                    right=24,
                    top=10,
                    bottom=10,
                ),
            ),
        )
        
    def set_text(self, text: str):
        self.button_text.value = text
        self.button_text.update()
        
        