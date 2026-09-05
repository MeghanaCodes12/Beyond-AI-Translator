import flet as ft

from services.history_service import HistoryService

class HistoryPanel(ft.Container):

    def __init__(self):

        self.history_service = HistoryService()

        self.history_column = ft.Column(
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
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                spacing=5,
                                controls=[
                                    ft.Text(
                                        "History",
                                        size=32,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        "Your previous translations",
                                        size=16,
                                    ),
                                ],
                            ),

                            ft.TextButton(
                                content=ft.Text(
                                    "Clear History"
                                ),
                                icon=ft.Icons.DELETE_SWEEP,
                                on_click=self.clear_history,
                            ),
                        ],
                    ),

                    self.history_column,
                ],
            ),
        )

        self.load_history()
        
    ### LOAD HISTORY
    def load_history(self):
        self.history_column.controls.clear()
        history = self.history_service.get_history()
        if not history:
            self.history_column.controls.append(
                ft.Container(
                    padding=30,
                    content=ft.Column(
                        horizontal_alignment=(
                            ft.CrossAxisAlignment.CENTER
                        ),
                        controls=[
                            ft.Icon(
                                ft.Icons.HISTORY,
                                size=50,
                            ),
                            ft.Text(
                                "No translation history yet.",
                                size=20,
                            ),
                            ft.Text(
                                "Your successful translations"
                                " will appear here."
                            ),
                        ],
                    ),
                )
            )
        else:
            for index, item in enumerate(history):
                self.history_column.controls.append(
                    self.create_history_card(
                        index,
                        item,
                    )
                )
                
    ### HISTORY CARD
    def create_history_card(
        self,
        index,
        item
    ):
        source_language = item.get(
            "source_language",
            "",
        )
        target_language = item.get(
            "target_language",
            "",
        )
        source_text = item.get(
            "source_text",
            "",
        )
        translated_text = item.get(
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
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                tooltip="Delete",
                                data=index,
                                on_click=self.delete_history,
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
        
    ### DELETE ONE
    def delete_history(self, e):
        index = e.control.data
        self.history_service.delete_history(
            index
        )
        self.load_history()
        self.update()
        
    ### CLEAR ALL
    def clear_history(self, e):
        self.history_service.clear_history()
        self.load_history()
        self.update()
        
    ### COPY
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
        
        