import flet as ft
import asyncio
import math
import random
from pathlib import Path


class EndingScreen:

    def __init__(self, page: ft.Page, on_back):
        self.page = page
        self.on_back = on_back

        # LEAF IMAGE

        self.asset_path = (
            Path(__file__).resolve().parent.parent
            / "opening"
            / "assets"
            / "beyond_tech_nature_leaf.png"
        )

        # LOGO
        self.logo = ft.Image(
            src=self.asset_path.read_bytes(),
            width=260,
            height=215,
            opacity=0,
            animate_opacity=ft.Animation(
                1200,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
        )


        # BEYOND
        self.brand_name = ft.Text(
            "Beyond",
            size=54,
            weight=ft.FontWeight.W_700,
            color="#205C45",
            opacity=0,
            animate_opacity=ft.Animation(
                800,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
        )

        # AI TRANSLATOR
        self.brand_type = ft.Text(
            "AI TRANSLATOR",
            size=20,
            weight=ft.FontWeight.W_600,
            color="#5B8F72",
            opacity=0,
            animate_opacity=ft.Animation(
                700,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
        )

        # THANK YOU
        self.thank_you = ft.Text(
            "Thank you for using Beyond!",
            size=23,
            weight=ft.FontWeight.W_500,
            color="#263D33",
            text_align=ft.TextAlign.CENTER,
            opacity=0,
            animate_opacity=ft.Animation(
                800,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
        )

        # SUBTITLE
        self.subtitle = ft.Text(
            "Your world, understood.",
            size=17,
            color="#52615A",
            text_align=ft.TextAlign.CENTER,
            opacity=0,
            animate_opacity=ft.Animation(
                800,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
        )

        # DIVIDER
        self.divider = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=7,
            opacity=0,
            animate_opacity=ft.Animation(
                700,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
            controls=[
                ft.Container(
                    width=45,
                    height=1,
                    bgcolor="#D6E5DA",
                ),
                ft.Container(
                    width=6,
                    height=6,
                    border_radius=50,
                    bgcolor="#9FC879",
                ),
                ft.Container(
                    width=6,
                    height=6,
                    border_radius=50,
                    bgcolor="#78AD69",
                ),
                ft.Container(
                    width=6,
                    height=6,
                    border_radius=50,
                    bgcolor="#9FC879",
                ),
                ft.Container(
                    width=45,
                    height=1,
                    bgcolor="#D6E5DA",
                ),
            ],
        )

        # SEE YOU NEXT TIME
        self.see_you = ft.Text(
            "See you next time! 💚",
            size=16,
            color="#5B8F72",
            opacity=0,
            animate_opacity=ft.Animation(
                800,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
        )

        # BACK BUTTON
        self.back_button = ft.Button(
            content=ft.Text(
                "Back to Starting Page",
                size=14,
                weight=ft.FontWeight.W_500,
            ),
            
            width=210,
            height=45,
            style=ft.ButtonStyle(
                bgcolor="#E2F0E6",
                elevation=0,
                shape=ft.RoundedRectangleBorder(radius=22),
            ),
            opacity=0,
            animate_opacity=ft.Animation(
                800,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
            on_click=self._back_clicked,
        )

        # PARTICLES
        self.particles = []
        particle_controls = []
        random.seed(25)
        for _ in range(32):
            angle = random.uniform(0, math.pi * 2)
            distance = random.uniform(170, 300)
            x = 300 + math.cos(angle) * distance
            y = 200 + math.sin(angle) * distance

            particle = ft.Container(
                left=x,
                top=y,
                width=random.randint(3, 6),
                height=random.randint(3, 6),
                border_radius=50,
                bgcolor="#9FC879",
                opacity=0,
                animate_opacity=ft.Animation(
                    700,
                    curve=ft.AnimationCurve.EASE_OUT,
                ),
                animate_position=ft.Animation(
                    1500,
                    curve=ft.AnimationCurve.EASE_OUT,
                ),
            )

            particle.data = {
                "x": x,
                "y": y,
            }

            self.particles.append(particle)
            particle_controls.append(particle)

        self.particle_layer = ft.Stack(
            width=600,
            height=420,
            controls=particle_controls,
        )

        # LOGO AREA
        self.logo_area = ft.Stack(
            width=480,
            height=280,
            controls=[
                self.particle_layer,

                ft.Container(
                    content=self.logo,
                    width=480,
                    height=280,
                    alignment=ft.Alignment(0, 0),
                ),
            ],
        )

        # MAIN CONTENT
        self.content = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
                ft.Container(
                    content=self.logo_area,
                    expand=True,
                    alignment=ft.Alignment(0, 1),
                ),

                self.brand_name,

                ft.Container(
                    content=self.brand_type,
                    margin=ft.Margin(
                        top=8,
                        right=0,
                        bottom=0,
                        left=0,
                    ),
                ),

                ft.Container(
                    content=self.thank_you,
                    margin=ft.Margin(
                        top=20,
                        right=0,
                        bottom=0,
                        left=0,
                    ),
                ),

                ft.Container(
                    content=self.subtitle,
                    margin=ft.Margin(
                        top=7,
                        right=0,
                        bottom=0,
                        left=0,
                    ),
                ),

                ft.Container(
                    content=self.divider,
                    margin=ft.Margin(
                        top=16,
                        right=0,
                        bottom=0,
                        left=0,
                    ),
                ),

                ft.Container(
                    content=self.see_you,
                    margin=ft.Margin(
                        top=12,
                        right=0,
                        bottom=0,
                        left=0,
                    ),
                ),

                ft.Container(
                    content=self.back_button,
                    margin=ft.Margin(
                        top=18,
                        right=0,
                        bottom=10,
                        left=0,
                    ),
                ),
            ],
        )

        # SCREEN
        self.view = ft.Container(
            expand=True,
            bgcolor="#F8FBF9",
            alignment=ft.Alignment(0, 0),
            content=self.content,
        )

    # BACK BUTTON
    async def _back_clicked(self, e):
        await self.on_back()
        
    # START ANIMATION
    async def start(self):

        # INITIAL STATE
        self.logo.opacity = 0
        self.brand_name.opacity = 0
        self.brand_type.opacity = 0
        self.thank_you.opacity = 0
        self.subtitle.opacity = 0
        self.divider.opacity = 0
        self.see_you.opacity = 0
        self.back_button.opacity = 0

        for particle in self.particles:
            particle.opacity = 0

        self.page.update()

        # WAIT
        await asyncio.sleep(0.5)

        # PARTICLES APPEAR
        for particle in self.particles:
            particle.opacity = random.uniform(0.25, 0.7)

        self.page.update()

        await asyncio.sleep(0.7)

        # PARTICLES MOVE INWARD
        for particle in self.particles:

            x = particle.data["x"]
            y = particle.data["y"]

            dx = 300 - x
            dy = 200 - y

            distance = math.sqrt(
                dx * dx + dy * dy
            )

            if distance == 0:
                distance = 1

            particle.left = (
                x + (dx / distance) * 100
            )

            particle.top = (
                y + (dy / distance) * 100
            )

        self.page.update()

        await asyncio.sleep(1.0)

        # LEAF APPEARS
        self.logo.opacity = 1

        self.page.update()

        await asyncio.sleep(1.0)
        
        # PARTICLES DISAPPEAR
        for particle in self.particles:
            particle.opacity = 0
        self.page.update()
        await asyncio.sleep(0.6)

        # BEYOND
        self.brand_name.opacity = 1
        self.page.update()
        await asyncio.sleep(0.45)

        # AI TRANSLATOR
        self.brand_type.opacity = 1
        self.page.update()
        await asyncio.sleep(0.5)
        
        # THANK YOU
        self.thank_you.opacity = 1
        self.page.update()
        await asyncio.sleep(0.4)

        # SUBTITLE
        self.subtitle.opacity = 1
        self.page.update()
        await asyncio.sleep(0.4)

        # DIVIDER
        self.divider.opacity = 1
        self.page.update()
        await asyncio.sleep(0.35)

        # SEE YOU NEXT TIME
        self.see_you.opacity = 1
        self.page.update()
        await asyncio.sleep(0.4)

        # BACK BUTTON
        self.back_button.opacity = 1
        self.page.update()