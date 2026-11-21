"""侧栏菜单项组件"""

import flet as ft
from theme import COLORS


class MenuItem(ft.Container):
    """可点击的菜单项：图标徽章 + 文字 + 选中指示条"""

    def __init__(self, icon, text: str, selected: bool = False, on_click=None):
        self.icon_name = icon
        self.text_value = text
        self._selected = selected

        icon_color = "#FFFFFF" if selected else COLORS["sidebar_text"]
        self._icon_box = ft.Container(
            content=ft.Icon(name=icon, size=18, color=icon_color),
            width=32,
            height=32,
            border_radius=8,
            bgcolor=COLORS["primary"] if selected else "#2C3350",
            alignment=ft.alignment.center,
        )
        self._label = ft.Text(
            value=text,
            size=13,
            color=COLORS["sidebar_selected_text"] if selected else COLORS["sidebar_text"],
            weight=ft.FontWeight.W_600 if selected else ft.FontWeight.NORMAL,
        )
        self._indicator = ft.Container(
            width=3,
            height=20,
            border_radius=2,
            bgcolor=COLORS["primary"] if selected else "#00000000",
        )

        super().__init__(
            content=ft.Row(
                controls=[
                    self._indicator,
                    self._icon_box,
                    self._label,
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(left=10, right=12, top=4, bottom=4),
            height=44,
            bgcolor=COLORS["sidebar_selected_bg"] if selected else None,
            border_radius=ft.border_radius.only(top_left=10, bottom_left=10),
            margin=ft.margin.only(right=8, top=2, bottom=2),
            on_click=on_click,
            animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
        )

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool):
        self._selected = value
        color = COLORS["sidebar_selected_text"] if value else COLORS["sidebar_text"]
        self._icon_box.bgcolor = COLORS["primary"] if value else "#2C3350"
        self._icon_box.content.color = "#FFFFFF" if value else COLORS["sidebar_text"]
        self._label.color = color
        self._label.weight = ft.FontWeight.W_600 if value else ft.FontWeight.NORMAL
        self._indicator.bgcolor = COLORS["primary"] if value else "#00000000"
        self.bgcolor = COLORS["sidebar_selected_bg"] if value else None
        self.update()
