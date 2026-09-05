import flet as ft


class AboutPage:

    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):

        return ft.Container(
            expand=True,
            padding=30,
            content=ft.Column(
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                controls=[

                    # HEADER
                    ft.Column(
                        spacing=6,
                        horizontal_alignment=(
                            ft.CrossAxisAlignment.CENTER
                        ),
                        controls=[
                            ft.Text(
                                "🌿 Beyond - AI Translator",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                            ),

                            ft.Text(
                                "Translate. Understand. Listen.",
                                size=17,
                                italic=True,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                    ),

                    ft.Divider(),

                    # ABOUT APPLICATION
                    ft.Container(
                        width=700,
                        padding=24,
                        border_radius=16,
                        border=ft.Border.all(
                            1,
                            "#DDDDDD",
                        ),
                        content=ft.Column(
                            spacing=12,
                            horizontal_alignment=(
                                ft.CrossAxisAlignment.CENTER
                            ),
                            controls=[

                                ft.Text(
                                    "About the Application",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER,
                                ),

                                ft.Text(
                                    "Beyond - AI Translator is an "
                                    "AI-powered desktop translation "
                                    "application designed to provide "
                                    "simple and convenient language "
                                    "translation.",
                                    size=16,
                                    text_align=ft.TextAlign.CENTER,
                                ),

                                ft.Text(
                                    "The application combines AI "
                                    "translation, speech support, "
                                    "translation history, and "
                                    "favorites in one place.",
                                    size=16,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                        ),
                    ),

                    # FEATURES
                    ft.Container(
                        width=700,
                        padding=24,
                        border_radius=16,
                        border=ft.Border.all(
                            1,
                            "#DDDDDD",
                        ),
                        content=ft.Column(
                            spacing=12,
                            horizontal_alignment=(
                                ft.CrossAxisAlignment.CENTER
                            ),
                            controls=[

                                ft.Text(
                                    "Features",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER,
                                ),

                                ft.Text(
                                    "🌍  AI-powered translation",
                                    size=16,
                                    text_align=ft.TextAlign.CENTER,
                                ),

                                ft.Text(
                                    "🔊  Text-to-speech support",
                                    size=16,
                                    text_align=ft.TextAlign.CENTER,
                                ),

                                ft.Text(
                                    "⭐  Save translations to favorites",
                                    size=16,
                                    text_align=ft.TextAlign.CENTER,
                                ),

                                ft.Text(
                                    "🕘  Translation history",
                                    size=16,
                                    text_align=ft.TextAlign.CENTER,
                                ),

                                ft.Text(
                                    "🌙  Light and dark mode",
                                    size=16,
                                    text_align=ft.TextAlign.CENTER,
                                ),

                                ft.Text(
                                    "🌐  Multiple language support",
                                    size=16,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                        ),
                    ),

                    # DEVELOPER
                    ft.Container(
                        width=700,
                        padding=24,
                        border_radius=16,
                        border=ft.Border.all(
                            1,
                            "#DDDDDD",
                        ),
                        content=ft.Column(
                            spacing=10,
                            horizontal_alignment=(
                                ft.CrossAxisAlignment.CENTER
                            ),
                            controls=[

                                ft.Text(
                                    "Developer",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER,
                                ),

                                ft.Text(
                                    "Annaladasu Meghana",
                                    size=20,
                                    italic=True,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER,
                                ),

                                ft.Text(
                                    "Developer & Creator",
                                    size=15,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                        ),
                    ),

                    # BUILT WITH
                    ft.Container(
                        width=700,
                        padding=24,
                        border_radius=16,
                        border=ft.Border.all(
                            1,
                            "#DDDDDD",
                        ),
                        content=ft.Column(
                            spacing=10,
                            horizontal_alignment=(
                                ft.CrossAxisAlignment.CENTER
                            ),
                            controls=[

                                ft.Text(
                                    "Built With",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER,
                                ),

                                ft.Text(
                                    "🐍 Python",
                                    size=16,
                                    text_align=ft.TextAlign.CENTER,
                                ),

                                ft.Text(
                                    "🖥️ Flet",
                                    size=16,
                                    text_align=ft.TextAlign.CENTER,
                                ),

                                ft.Text(
                                    "✨ Google Gemini",
                                    size=16,
                                    text_align=ft.TextAlign.CENTER,
                                ),

                                ft.Text(
                                    "🔊 Edge TTS",
                                    size=16,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                        ),
                    ),

                    # VERSION
                    ft.Column(
                        spacing=5,
                        horizontal_alignment=(
                            ft.CrossAxisAlignment.CENTER
                        ),
                        controls=[

                            ft.Text(
                                "Version 1.0.0",
                                size=14,
                                text_align=ft.TextAlign.CENTER,
                            ),

                            ft.Text(
                                "© 2026 Beyond - AI Translator",
                                size=13,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                    ),
                ],
            ),
        )