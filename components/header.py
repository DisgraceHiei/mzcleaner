"""顶部栏组件 - 标题 + 状态指示"""

import flet as ft
from theme import COLORS


class Header(ft.Container):
    """顶部栏"""

    def __init__(self, page: ft.Page):
        self.page = page

        title = ft.Text(
            value="磁盘清理与空间分析",
            size=14,
            color=COLORS["text"],
            weight=ft.FontWeight.W_600,
        )
        subtitle = ft.Text(
            value="C盘清理",
            size=11,
            color=COLORS["secondary"],
        )

        status = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(width=7, height=7, border_radius=4,
                                 bgcolor=COLORS["success"]),
                    ft.Text("本地运行", size=11, color=COLORS["secondary"]),
                ],
                spacing=6,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor="#F3F4F8",
            border_radius=16,
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
        )

        btn_exit = ft.IconButton(
            icon=ft.Icons.CLOSE_ROUNDED,
            icon_size=18,
            icon_color=COLORS["secondary"],
            tooltip="退出",
            on_click=lambda e: page.window.close(),
        )

        super().__init__(
            content=ft.Row(
                controls=[
                    ft.Column(controls=[title, subtitle], spacing=0),
                    ft.Row(controls=[status, btn_exit], spacing=8),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            height=64,
            bgcolor=COLORS["header_bg"],
            padding=ft.padding.only(left=28, right=20),
            border=ft.border.only(bottom=ft.BorderSide(1, COLORS["border"])),
        )
