import flet as ft

from ui.pages.home_page import HomePage
from ui.components.sidebar import SideBar
from services.settings_service import SettingsService

from animations.opening.opening_screen import OpeningScreen
from animations.closing.ending_screen import EndingScreen


async def main(page: ft.Page):

    page.title = "Beyond - AI Translator"
    page.padding = 0


    # ============================================================
    # BUILD ACTUAL APPLICATION
    # ============================================================

    def build_application():

        settings_service = SettingsService()

        settings = settings_service.get_settings()

        if settings.get("dark_mode", False):
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT

        # --------------------------------------------------------
        # CONTENT
        # --------------------------------------------------------

        content_area = ft.Container(
            expand=True,
            content=HomePage(page).build(),
        )

        # --------------------------------------------------------
        # SIDEBAR
        # --------------------------------------------------------

        sidebar = SideBar(
            page,
            content_area,
        )

        page.sidebar = sidebar

        # --------------------------------------------------------
        # LAYOUT
        # --------------------------------------------------------

        main_layout = ft.Row(
            expand=True,
            spacing=0,
            controls=[
                sidebar,
                content_area,
            ],
        )

        return main_layout


    # ============================================================
    # START APPLICATION
    # ============================================================

    async def show_application():

        page.controls.clear()

        page.add(
            build_application()
        )

        page.update()


    # ============================================================
    # SHOW ENDING SCREEN
    # ============================================================

    async def show_ending():

        page.controls.clear()

        ending = EndingScreen(
            page,
            show_starting_page,
        )

        page.add(
            ending.view
        )

        page.update()

        await ending.start()


    # ============================================================
    # BACK TO STARTING PAGE
    # ============================================================

    async def show_starting_page():

        page.controls.clear()

        opening = OpeningScreen(
            page,
            show_application,
        )

        page.add(
            opening.view
        )

        page.update()

        await opening.start()


    # ============================================================
    # MAKE ENDING SCREEN AVAILABLE TO THE APP
    # ============================================================

    page.show_ending = show_ending


    # ============================================================
    # START WITH OPENING ANIMATION
    # ============================================================

    await show_starting_page()


# ================================================================
# RUN
# ================================================================

ft.run(main)