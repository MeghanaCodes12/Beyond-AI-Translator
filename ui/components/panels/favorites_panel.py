import flet as ft

from services.favorites_service import FavoritesService


class FavoritesPanel(ft.Container):

    def __init__(self):

        self.favorites_service = FavoritesService()

        self.favorites_column = ft.Column(
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        super().__init__(
            expand=True,
            padding=20,
            content=ft.Column(
                spacing=16,
                expand=True,
                controls=[
                    ft.Text(
                        "Favorites",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                    ),

                    ft.Text(
                        "Your saved translations",
                        size=16,
                    ),

                    self.favorites_column,
                ],
            ),
        )

        self.load_favorites()

    # LOAD FAVORITES

    def load_favorites(self):

        self.favorites_column.controls.clear()

        favorites = self.favorites_service.get_favorites()

        if not favorites:

            self.favorites_column.controls.append(
                ft.Container(
                    padding=30,
                    content=ft.Column(
                        horizontal_alignment=(
                            ft.CrossAxisAlignment.CENTER
                        ),
                        controls=[
                            ft.Icon(
                                ft.Icons.FAVORITE_BORDER,
                                size=50,
                            ),

                            ft.Text(
                                "No favorites yet.",
                                size=20,
                            ),

                            ft.Text(
                                "Save a translation using "
                                "the ⭐ button.",
                            ),
                        ],
                    ),
                )
            )

        else:

            for index, favorite in enumerate(favorites):

                self.favorites_column.controls.append(
                    self.create_favorite_card(
                        index,
                        favorite,
                    )
                )

    # CREATE FAVORITE CARD

    def create_favorite_card(
        self,
        index,
        favorite,
    ):

        source_language = favorite.get(
            "source_language",
            "",
        )

        target_language = favorite.get(
            "target_language",
            "",
        )

        source_text = favorite.get(
            "source_text",
            "",
        )

        translated_text = favorite.get(
            "translated_text",
            "",
        )

        return ft.Container(
            padding=16,
            border_radius=14,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                "#DDDDDD",
            ),
            content=ft.Column(
                spacing=10,
                controls=[

                    ft.Row(
                        alignment=(
                            ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        controls=[

                            ft.Text(
                                f"{source_language} → "
                                f"{target_language}",
                                weight=ft.FontWeight.BOLD,
                                size=16,
                            ),

                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                tooltip="Remove favorite",
                                data=index,
                                on_click=self.remove_favorite,
                            ),
                        ],
                    ),

                    ft.Text(
                        source_text,
                        size=16,
                    ),

                    ft.Divider(),

                    ft.Text(
                        translated_text,
                        size=16,
                    ),

                    ft.Row(
                        alignment=(
                            ft.MainAxisAlignment.END
                        ),
                        controls=[

                            ft.IconButton(
                                icon=ft.Icons.CONTENT_COPY,
                                tooltip="Copy translation",
                                data=translated_text,
                                on_click=self.copy_translation,
                            ),
                        ],
                    ),
                ],
            ),
        )

    # REMOVE FAVORITE

    def remove_favorite(self, e):
        index = e.control.data
        favorites = (
            self.favorites_service.get_favorites()
        )
        if 0 <= index < len(favorites):
            favorites.pop(index)
            self.favorites_service._save(
                favorites
            )
            self.load_favorites()
            self.update()

    # COPY TRANSLATION

    async def copy_translation(self, e):

        text = e.control.data

        if not text:
            return

        await self.page.clipboard.set(text)

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(
                "Translation copied!"
            )
        )

        self.page.snack_bar.open = True

        self.page.update()