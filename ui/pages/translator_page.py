import flet as ft

from ui.components.panels.translator_panel import TranslatorPanel

class TranslatorPage:

    def __init__(self, page):
        self.page = page

    def build(self):
        return TranslatorPanel(
            self.page   
        )