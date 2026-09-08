import flet as ft
import asyncio
from pathlib import Path
import math
import random


class OpeningScreen:
    """
    Beyond AI Translator - Opening Screen

    Flow:
    1. Light background
    2. Particles appear
    3. Particles converge
    4. Approved leaf is revealed
    5. Particles disperse
    6. Beyond appears
    7. AI TRANSLATOR appears
    8. Tagline appears
    9. Initializing...
    """

    def __init__(self, page: ft.Page, on_complete):
        self.page = page
        self.on_complete = on_complete

        # APPROVED LEAF IMAGE
        self.asset_path = (
            Path(__file__).resolve().parent
            / "assets"
            / "beyond_tech_nature_leaf.png"
        )

        # PARTICLES
        self.particles = []
        
        # LOGO
        self.logo = ft.Image(
            src=self.asset_path.read_bytes(),
            width=360,
            height=300,
            opacity=0,
            animate_opacity=ft.Animation(
                1200,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
            animate_scale=ft.Animation(
                1200,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
        )

        # BRAND NAME
        self.brand_name = ft.Text(
            "Beyond",
            size=56,
            weight=ft.FontWeight.W_700,
            color="#205C45",
            opacity=0,
            animate_opacity=ft.Animation(
                800,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
        )

        # BRAND TYPE
        self.brand_type = ft.Text(
            "AI TRANSLATOR",
            size=21,
            weight=ft.FontWeight.W_600,
            color="#5B8F72",
            opacity=0,
            animate_opacity=ft.Animation(
                700,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
        )

        # TAGLINE
        self.tagline = ft.Text(
            "Translate. Understand. Listen.",
            size=18,
            italic=True,
            color="#52615A",
            opacity=0,
            animate_opacity=ft.Animation(
                800,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
        )

        # LOADING DOTS
        self.loading_dots = ft.Row(
            spacing=7,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self._make_dot(),
                self._make_dot(),
                self._make_dot(),
            ],
        )

        self.loading_text = ft.Text(
            "Initializing...",
            size=14,
            color="#6C8D78",
        )

        self.loading = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=7,
            opacity=0,
            animate_opacity=ft.Animation(
                700,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
            controls=[
                self.loading_dots,
                self.loading_text,
            ],
        )

        # LOGO AREA
        self.logo_area = ft.Stack(
            width=600,
            height=420,
            controls=[
                self._build_particle_layer(),
                ft.Container(
                    content=self.logo,
                    width=600,
                    height=420,
                    alignment=ft.Alignment(0, 0),
                ),
            ],
        )

        # BRANDING AREA
        self.branding = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                self.brand_name,
                ft.Container(
                    content=self.brand_type,
                    margin=ft.Margin(top=12, right=0, bottom=0, left=0),
                ),
                ft.Container(
                    content=self.tagline,
                    margin=ft.Margin(top=20, right=0, bottom=0, left=0),
                ),
            ],
        )

        # COMPLETE OPENING SCREEN
        self.view = ft.Container(
            expand=True,
            bgcolor="#F8FBF9",
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=0,
                controls=[
                    self.logo_area,
                    self.branding,
                    ft.Container(
                        content=self.loading,
                        margin=ft.Margin(
                            top=26,
                            right=0,
                            bottom=0,
                            left=0,
                        ),
                    ),
                ],
            ),
        )

    # DOT
    def _make_dot(self):
        return ft.Container(
            width=7,
            height=7,
            border_radius=50,
            bgcolor="#9FC879",
        )
        
    # PARTICLE LAYER
    def _build_particle_layer(self):
        random.seed(42)
        controls = []
        center_x = 300
        center_y = 210
        for _ in range(55):
            angle = random.uniform(0, math.pi * 2)
            distance = random.uniform(170, 290)

            start_x = (
                center_x
                + math.cos(angle) * distance
            )

            start_y = (
                center_y
                + math.sin(angle) * distance
            )

            particle = ft.Container(
                left=start_x,
                top=start_y,
                width=random.uniform(3, 6),
                height=random.uniform(3, 6),
                border_radius=50,
                bgcolor="#6CAE57",
                opacity=0,
                animate_opacity=ft.Animation(
                    500,
                    curve=ft.AnimationCurve.EASE_OUT,
                ),
                animate_position=ft.Animation(
                    2200,
                    curve=ft.AnimationCurve.EASE_OUT,
                ),
            )

            particle.data = {
                "start_x": start_x,
                "start_y": start_y,
                "target_x": (
                    center_x
                    + random.uniform(-100, 100)
                ),
                "target_y": (
                    center_y
                    + random.uniform(-110, 110)
                ),
            }

            self.particles.append(particle)
            controls.append(particle)

        return ft.Stack(
            width=600,
            height=420,
            controls=controls,
        )

    # START
    async def start(self):
        # INITIAL STATE
        self.logo.opacity = 0
        self.brand_name.opacity = 0
        self.brand_type.opacity = 0
        self.tagline.opacity = 0
        self.loading.opacity = 0

        self.page.update()

        # QUIET LIGHT INTRO
        await asyncio.sleep(0.7)

        # PARTICLES APPEAR
        for particle in self.particles:
            particle.opacity = random.uniform(0.35, 0.8)
        self.page.update()
        await asyncio.sleep(0.6)

        # PARTICLES MOVE TOWARD CENTER
        for particle in self.particles:

            target = particle.data

            particle.left = target["target_x"]
            particle.top = target["target_y"]

        self.page.update()

        await asyncio.sleep(1.7)

        # LOGO REVEAL
        self.logo.opacity = 1

        # Slight enlargement during reveal
        self.logo.scale = 1.04

        self.page.update()

        await asyncio.sleep(1.1)

        # Return logo to normal size
        self.logo.scale = 1

        self.page.update()

        # PARTICLES DISPERSE
        for particle in self.particles:

            target = particle.data

            dx = target["target_x"] - 300
            dy = target["target_y"] - 210

            length = math.sqrt(
                dx * dx + dy * dy
            )

            if length == 0:
                length = 1

            direction_x = dx / length
            direction_y = dy / length

            particle.left = (
                target["target_x"]
                + direction_x * 130
            )

            particle.top = (
                target["target_y"]
                + direction_y * 130
            )

            particle.opacity = 0
        self.page.update()
        await asyncio.sleep(1.0)
        
        # BEYOND
        self.brand_name.opacity = 1
        self.page.update()
        await asyncio.sleep(0.4)

        # AI TRANSLATOR
        self.brand_type.opacity = 1
        self.page.update()
        await asyncio.sleep(0.45)

        # TAGLINE
        self.tagline.opacity = 1
        self.page.update()
        await asyncio.sleep(0.6)

        # INITIALIZING
        self.loading.opacity = 1
        self.page.update()
        await asyncio.sleep(1.2)

        # FINISH
        await self.on_complete()