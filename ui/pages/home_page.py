import flet as ft


class HomePage:

    def __init__(self, page: ft.Page):
        self.page = page

    # NAVIGATION HELPERS

    def open_translator(self, e):
        if hasattr(self.page, "sidebar"):
            self.page.sidebar.open_translator(e)

    def open_history(self, e):
        if hasattr(self.page, "sidebar"):
            self.page.sidebar.open_history(e)

    def open_favorites(self, e):
        if hasattr(self.page, "sidebar"):
            self.page.sidebar.open_favorites(e)

    def open_settings(self, e):
        if hasattr(self.page, "sidebar"):
            self.page.sidebar.open_settings(e)

    def build(self):

        return ft.Container(
            expand=True,
            padding=30,
            content=ft.Column(
                spacing=24,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                controls=[

                    # HEADER
                    ft.Column(
                        spacing=8,
                        horizontal_alignment=(
                            ft.CrossAxisAlignment.CENTER
                        ),
                        controls=[
                            ft.Text(
                                "🌿 Beyond - AI Translator",
                                size=34,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Translate. Understand. Listen.",
                                size=18,
                                italic=True,
                            ),
                            ft.Text(
                                "Your AI-powered translation companion.",
                                size=16,
                            ),
                        ],
                    ),

                    ft.Container(height=10),

                    # QUICK ACTIONS
                    ft.Text(
                        "Quick Actions",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                    ),

                    ft.Row(
                        spacing=16,
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                        controls=[

                            # TRANSLATE
                            ft.Container(
                                width=220,
                                padding=20,
                                border_radius=16,
                                border=ft.Border.all(
                                    1,
                                    "#DDDDDD",
                                ),
                                on_click=self.open_translator,
                                content=ft.Column(
                                    spacing=10,
                                    horizontal_alignment=(
                                        ft.CrossAxisAlignment.CENTER
                                    ),
                                    controls=[
                                        ft.Text(
                                            "🌍",
                                            size=36,
                                        ),
                                        ft.Text(
                                            "Translate",
                                            size=20,
                                            weight=(
                                                ft.FontWeight.BOLD
                                            ),
                                        ),
                                        ft.Text(
                                            "Translate text using AI.",
                                            text_align=(
                                                ft.TextAlign.CENTER
                                            ),
                                        ),
                                        ft.FilledButton(
                                            "Start Translating",
                                            on_click=self.open_translator,
                                        ),
                                    ],
                                ),
                            ),

                            # HISTORY
                            ft.Container(
                                width=220,
                                padding=20,
                                border_radius=16,
                                border=ft.Border.all(
                                    1,
                                    "#DDDDDD",
                                ),
                                on_click=self.open_history,
                                content=ft.Column(
                                    spacing=10,
                                    horizontal_alignment=(
                                        ft.CrossAxisAlignment.CENTER
                                    ),
                                    controls=[
                                        ft.Text(
                                            "🕘",
                                            size=36,
                                        ),
                                        ft.Text(
                                            "History",
                                            size=20,
                                            weight=(
                                                ft.FontWeight.BOLD
                                            ),
                                        ),
                                        ft.Text(
                                            "View your previous translations.",
                                            text_align=(
                                                ft.TextAlign.CENTER
                                            ),
                                        ),
                                    ],
                                ),
                            ),

                            # FAVORITES
                            ft.Container(
                                width=220,
                                padding=20,
                                border_radius=16,
                                border=ft.Border.all(
                                    1,
                                    "#DDDDDD",
                                ),
                                on_click=self.open_favorites,
                                content=ft.Column(
                                    spacing=10,
                                    horizontal_alignment=(
                                        ft.CrossAxisAlignment.CENTER
                                    ),
                                    controls=[
                                        ft.Text(
                                            "⭐",
                                            size=36,
                                        ),
                                        ft.Text(
                                            "Favorites",
                                            size=20,
                                            weight=(
                                                ft.FontWeight.BOLD
                                            ),
                                        ),
                                        ft.Text(
                                            "Access your saved translations.",
                                            text_align=(
                                                ft.TextAlign.CENTER
                                            ),
                                        ),
                                    ],
                                ),
                            ),

                            # SETTINGS
                            ft.Container(
                                width=220,
                                padding=20,
                                border_radius=16,
                                border=ft.Border.all(
                                    1,
                                    "#DDDDDD",
                                ),
                                on_click=self.open_settings,
                                content=ft.Column(
                                    spacing=10,
                                    horizontal_alignment=(
                                        ft.CrossAxisAlignment.CENTER
                                    ),
                                    controls=[
                                        ft.Text(
                                            "⚙️",
                                            size=36,
                                        ),
                                        ft.Text(
                                            "Settings",
                                            size=20,
                                            weight=(
                                                ft.FontWeight.BOLD
                                            ),
                                        ),
                                        ft.Text(
                                            "Customize your application.",
                                            text_align=(
                                                ft.TextAlign.CENTER
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),

                    ft.Container(height=10),

                    # FEATURES
                    ft.Text(
                        "Features",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                    ),

                    ft.Text(
                        "🌍 AI-powered translation\n"
                        "🔊 Text-to-speech support\n"
                        "⭐ Save important translations\n"
                        "🕘 Translation history\n"
                        "🌙 Light and dark mode",
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )