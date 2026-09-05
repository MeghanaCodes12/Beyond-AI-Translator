import flet as ft

from ui.components.panels.settings_panel import SettingsPanel


class SettingsPage:

    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        return ft.Container(
            expand=True,
            content=SettingsPanel(),
        )