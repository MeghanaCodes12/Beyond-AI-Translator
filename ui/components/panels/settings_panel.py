import flet as ft

from services.settings_service import SettingsService

class SettingsPanel(ft.Container):
    def __init__(self):
        
        self.settings_service = SettingsService()
        settings = self.settings_service.get_settings()
        
        self.dark_mode = ft.Switch(
            label="Dark Mode",
            value=settings.get("dark_mode", False),
            on_change=self.toggle_theme,
        )
        self.auto_copy = ft.Switch(
            label="Auto Copy Translation",
            value=settings.get("auto_copy", False),
        )
        self.speech_enabled = ft.Switch(
            label="Speech Enabled",
            value=settings.get("speech_enabled",True),
        )
        
        self.auto_copy.on_change = self.toggle_auto_copy
        self.speech_enabled.on_change = self.toggle_speech
        
        super().__init__(
            expand=True,
            padding=20,
            content=ft.Column(
                spacing=16,
                expand=True,
                controls=[
                    ft.Text(
                        "Settings",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Customize your Beyond AI Translator.",
                        size=16,
                    ),
                    ft.Divider(),
                    ft.Text(
                        "Appearance",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    self.dark_mode,
                    ft.Divider(),
                    ft.Text(
                        "Translation",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    self.auto_copy,
                    self.speech_enabled,
                ],
            ),
        )
        
    def toggle_theme(self, e):
        enabled = self.dark_mode.value
        self.settings_service.set(
            "dark_mode",
            enabled,
        )
        
        if enabled:
            self.page.theme_mode = ft.ThemeMode.DARK
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
        
        self.page.update()
        
    ### AUTO COPY
    def toggle_auto_copy(self, e):
        self.settings_service.set(
            "auto_copy",
            self.auto_copy.value,
        )
        
    ### SPEECH
    def toggle_speech(self, e):
        self.settings_service.set(
            "speech_enabled",
            self.speech_enabled.value,
        )
        
        