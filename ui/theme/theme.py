import flet as ft

from ui.theme.colors import AppColors


class AppTheme:

    @staticmethod
    def apply(page: ft.Page):

        page.title = "Beyond - AI Translator"
        page.padding = 0
        page.bgcolor = AppColors.BACKGROUND
        page.theme_mode = ft.ThemeMode.LIGHT
        page.theme = ft.Theme(
            color_scheme_seed=AppColors.PRIMARY,
            use_material3=True,
        )
        page.dark_theme = ft.Theme(
            color_scheme_seed=AppColors.PRIMARY,
            use_material3=True,
        )