"""顶部导航栏组件"""

import flet as ft
from theme import COLORS


class Header(ft.Container):
    """顶部标题栏"""

    def __init__(self, page: ft.Page):
        self.page = page

        title = ft.Text(
            value="C盘清理 · 免费开源版",
            size=16,
            color=COLORS["text"],
            weight=ft.FontWeight.W_600,
        )

        btn_exit = ft.TextButton(
            text="退出",
            style=ft.ButtonStyle(
                color=COLORS["header_text"],
                text_style=ft.TextStyle(size=14),
            ),
            on_click=lambda e: page.window.close(),
        )

        super().__init__(
            content=ft.Row(
                controls=[
                    title,
                    btn_exit,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=4,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            height=60,
            bgcolor=COLORS["header_bg"],
            padding=ft.padding.only(left=20, right=20),
            border=ft.border.only(bottom=ft.BorderSide(1, COLORS["border"])),
        )
