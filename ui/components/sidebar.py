import flet as ft

from ui.theme.colors import AppColors
from ui.pages.translator_page import TranslatorPage

class SideBar(ft.Container):

    def __init__(self, app_page, content_area):
        self.app_page = app_page
        self.content_area = content_area
        self.expanded = True
        self.pages = {}
        self.active_page = "home"

        # MENU ITEMS
        self.menu_items = [
            ("🏠", "Home", "home", self.open_home),
            ("🌍", "Translate", "translator", self.open_translator),
            ("🕘", "History", "history", self.open_history),
            ("⭐", "Favorites", "favorites", self.open_favorites),
            ("⚙", "Settings", "settings", self.open_settings),
            ("ℹ", "About", "about", self.open_about),
        ]

        self.nav_buttons = []

        for icon, label, page_name, handler in self.menu_items:
            button = self.create_nav_button(
                icon,
                label,
                page_name,
                handler,
            )
            self.nav_buttons.append(button)
            
        self.finish_button = ft.Container(
            width=158,
            height=44,
            border_radius=12,
            bgcolor="white12",
            padding=0,
            on_click=self.finish_app,
            content=ft.Row(
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                   ft.Text("🚪", size=18),
                   ft.Text(
                       "Finish",
                       size=14,
                       color="white",
                   ),
                ],
            ),
        )

        # LOGO
        self.logo = ft.Text(
            "🌿",
            size=28,
            color="white",
        )

        # BRAND TEXT
        self.brand_text = ft.Column(
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Beyond",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                ),
                ft.Text(
                    "AI Translator",
                    size=13,
                    color="white70",
                ),
            ],
        )
        
        # BRAND CONTAINER
        self.brand_container = ft.Column(
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.logo,
                self.brand_text,
            ],
        )

        # TOGGLE BUTTON
        self.toggle_button = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            icon_color="white",
            tooltip="Collapse sidebar",
            on_click=self.toggle_sidebar,
        )
        
        # SIDEBAR CONTENT
        self.sidebar_content = ft.Column(
            spacing=6,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.brand_container,
                ft.Divider(
                    height=16,
                    thickness=1,
                    color="white24",
                ),
                *self.nav_buttons,
                ft.Container(
                    expand=True,
                ),
                self.finish_button,
                self.toggle_button,
            ],
        )

        # SIDEBAR
        super().__init__(
            width=190,
            bgcolor=AppColors.PRIMARY,
            padding=16,
            content=self.sidebar_content,
        )

    # NAVIGATION BUTTON
    def create_nav_button(
        self,
        icon,
        label,
        page_name,
        handler,
    ):
        is_active = page_name == self.active_page

        return ft.Container(
            width=158,
            height=44,
            border_radius=12,
            bgcolor=(
                "white24"
                if is_active
                else "transparent"
            ),
            padding=0,
            on_click=handler,
            content=ft.Row(
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Text(
                        icon,
                        size=18,
                    ),
                    ft.Text(
                        label,
                        size=14,
                        color="white",
                        weight=(
                            ft.FontWeight.BOLD
                            if is_active
                            else ft.FontWeight.NORMAL
                        ),
                    ),
                ],
            ),
        )
    
    # ACTIVE PAGE
    def set_active_page(self, page_name):
        self.active_page = page_name

        for button, (_, _, current_page, _) in zip(
            self.nav_buttons,
            self.menu_items,
        ):
            button.bgcolor = (
                "white24"
                if current_page == page_name
                else "transparent"
            )

            row = button.content

            row.controls[1].weight = (
                ft.FontWeight.BOLD
                if current_page == page_name
                else ft.FontWeight.NORMAL
            )
        self.update()
        
    # TOGGLE SIDEBAR
    def toggle_sidebar(self, e):
        self.expanded = not self.expanded
        if self.expanded:
            # EXPANDED
            self.width = 190
            self.padding = 16
            self.toggle_button.icon = (
                ft.Icons.CHEVRON_LEFT
            )
            self.toggle_button.tooltip = (
                "Collapse sidebar"
            )
            # Show title
            self.brand_text.visible = True
            for button, (
                icon,
                label,
                _,
                _,
            ) in zip(
                self.nav_buttons,
                self.menu_items,
            ):
                button.width = 158
                row = button.content
                row.controls[0].visible = True
                row.controls[1].visible = True
        else:
            # COLLAPSED
            self.width = 70
            self.padding = 8
            self.toggle_button.icon = (
                ft.Icons.CHEVRON_RIGHT
            )
            self.toggle_button.tooltip = (
                "Expand sidebar"
            )
            # Hide title
            # Keep only 🌿 logo
            self.brand_text.visible = False
            for button, (
                icon,
                label,
                _,
                _,
            ) in zip(
                self.nav_buttons,
                self.menu_items,
            ):
                button.width = 54
                row = button.content
                # Keep icon
                row.controls[0].visible = True
                # Hide text
                row.controls[1].visible = False
        self.update()

    # CONTENT
    def show_page(
        self,
        page_name,
        page_content_factory,
    ):
        self.set_active_page(page_name)

        if page_name not in self.pages:
            self.pages[page_name] = (
                page_content_factory()
            )

        self.content_area.content = (
            self.pages[page_name]
        )

        self.content_area.update()
    
    # HOME
    def open_home(self, e):
        from ui.pages.home_page import HomePage
        self.show_page(
            "home",
            lambda: HomePage(
                self.app_page
            ).build(),
        )

    # TRANSLATOR
    def open_translator(self, e):
        self.show_page(
            "translator",
            lambda: TranslatorPage(
                self.app_page
            ).build(),
        )
    
    # HISTORY
    def open_history(self, e):
        from ui.components.panels.history_panel import HistoryPanel
        self.show_page(
            "history",
            lambda: HistoryPanel(),
        )

    # FAVORITES
    def open_favorites(self, e):
        from ui.components.panels.favorites_panel import FavoritesPanel
        self.show_page(
            "favorites",
            lambda: FavoritesPanel(),
        )

    # SETTINGS
    def open_settings(self, e):
        from ui.pages.settings_page import SettingsPage
        self.show_page(
            "settings",
            lambda: SettingsPage(
                self.app_page
            ).build(),
        )

    # ABOUT
    def open_about(self, e):
        from ui.pages.about_page import AboutPage
        self.show_page(
            "about",
            lambda: AboutPage(
                self.app_page
            ).build(),
        )
        
    # FINISH
    async def finish_app(self, e):
        await self.app_page.show_ending()