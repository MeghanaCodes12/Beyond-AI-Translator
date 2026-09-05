import flet as ft

from ui.theme.colors import AppColors
from ui.theme.radius import AppRadius
from ui.theme.spacing import AppSpacing

class NatureCard(ft.Container):
    def __init__(self, content):
        super().__init__(
            bgcolor=AppColors.SURFACE,
            border_radius=AppRadius.LARGE,
            padding=AppSpacing.LG,
            border=ft.Border.all(
                1,
                AppColors.BORDER,
            ),
            content=content,
        )