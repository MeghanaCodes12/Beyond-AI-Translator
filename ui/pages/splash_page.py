import flet as ft
import threading
import time

from ui.pages.home_page import HomePage

class SplashPage:
    def __init__(self, page: ft.Page):
        self.page = page
    def open_home(self):
        time.sleep(3)
        HomePage(self.page).build()
        
    def build(self):
        self.page.clean()
        self.page.add(
            ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(
                            ft.Icons.AUTO_AWESOME,
                            size=70,
                            color="#3E6B48,"
                        ),
                        ft.Text(
                            "Beyond - AI Translator",
                            size=42,
                            weight=ft.FontWeight.BOLD,
                            color="#2E2E2E",
                        ),
                        ft.Text(
                            "Translate Beyond Limits\nUnderstand Beyond Words",
                            text_align=ft.TextAlign.CENTER,
                            size=18,
                            color="#6B6B6B",
                        ),
                        ft.ProgressRing(
                            width=40,
                            height=40,
                            color="#3E6B48",
                        ),
                        ft.Text(
                            "Loading...",
                            color="#6B6B6B",
                        ),
                    ],
                ),
            )
        )
        
        threading.Thread(
            target=self.open_home,
            daemon=True,
        ).start()
        