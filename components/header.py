"""顶部导航栏组件"""

import flet as ft
from theme import COLORS


class Header(ft.Container):
    """顶部标题栏，包含导航链接"""

    def __init__(self, page: ft.Page):
        self.page = page

        # 联系客服 - 红色
        self.btn_contact = ft.TextButton(
            text="联系客服",
            style=ft.ButtonStyle(
                color=COLORS["link_red"],
                text_style=ft.TextStyle(size=14),
            ),
        )

        # 教程及问题
        self.btn_tutorial = ft.TextButton(
            text="教程及问题",
            style=ft.ButtonStyle(
                color=COLORS["header_text"],
                text_style=ft.TextStyle(size=14),
            ),
        )

        # 打开官网
        self.btn_website = ft.TextButton(
            text="打开官网",
            style=ft.ButtonStyle(
                color=COLORS["header_text"],
                text_style=ft.TextStyle(size=14),
            ),
        )

        # 退出
        self.btn_exit = ft.TextButton(
            text="退出",
            style=ft.ButtonStyle(
                color=COLORS["header_text"],
                text_style=ft.TextStyle(size=14),
            ),
            on_click=lambda e: page.window.close(),
        )

        # 复制微信号
        self.btn_copy_wechat = ft.TextButton(
            text="复制微信号",
            style=ft.ButtonStyle(
                color=COLORS["header_text"],
                text_style=ft.TextStyle(size=14),
            ),
        )

        super().__init__(
            content=ft.Row(
                controls=[
                    self.btn_contact,
                    self.btn_tutorial,
                    self.btn_website,
                    self.btn_exit,
                    self.btn_copy_wechat,
                ],
                alignment=ft.MainAxisAlignment.END,
                spacing=4,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            height=60,
            bgcolor=COLORS["header_bg"],
            padding=ft.padding.only(left=20, right=20),
            border=ft.border.only(bottom=ft.BorderSide(1, COLORS["border"])),
        )
