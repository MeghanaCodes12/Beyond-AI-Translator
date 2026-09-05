import flet as ft


class NatureTextField(ft.TextField):

    def __init__(self, **kwargs):

        super().__init__(

            border_radius=12,

            border_color="#D8D8D8",

            focused_border_color="#2F6B4F",

            **kwargs,
        )