"""左侧功能导航组件 - 深色分组式侧栏"""

import flet as ft
from theme import COLORS
from components.menu_item import MenuItem


class Sidebar(ft.Container):
    """左侧功能导航菜单（分组）"""

    # 顺序必须与 scan_panel.SCAN_TYPE_KEYS 完全一致
    MENU_ITEMS = [
        {"icon": ft.Icons.CLEANING_SERVICES_OUTLINED, "text": "基础清理"},
        {"icon": ft.Icons.SECURITY_OUTLINED, "text": "系统清理"},
        {"icon": ft.Icons.CHAT_OUTLINED, "text": "微信清理"},
        {"icon": ft.Icons.MESSAGE_OUTLINED, "text": "QQ清理"},
        {"icon": ft.Icons.FOLDER_OPEN_OUTLINED, "text": "用户目录迁移"},
        {"icon": ft.Icons.LIST_ALT_OUTLINED, "text": "软件占用查询"},
        {"icon": ft.Icons.ARROW_FORWARD_OUTLINED, "text": "软件搬家"},
        {"icon": ft.Icons.DESCRIPTION_OUTLINED, "text": "大文件查找"},
        {"icon": ft.Icons.CONTENT_COPY_OUTLINED, "text": "重复文件查找"},
        {"icon": ft.Icons.LOOP_OUTLINED, "text": "相似文件查找"},
        {"icon": ft.Icons.PIE_CHART_OUTLINE, "text": "目录大小查看"},
        {"icon": ft.Icons.AUTO_AWESOME_OUTLINED, "text": "深度清理"},
        {"icon": ft.Icons.DESCRIPTION_OUTLINED, "text": "临时文件扫描"},
        {"icon": ft.Icons.GRID_VIEW_OUTLINED, "text": "空间占用分析"},
    ]

    # 分组：(标题, 起始索引, 结束索引) - 与上面顺序对应
    GROUPS = [
        ("快速清理", 0, 4),
        ("空间分析", 4, 11),
        ("深度工具", 11, 14),
    ]

    def __init__(self, on_menu_change=None):
        self.on_menu_change = on_menu_change
        self._menu_items: list[MenuItem] = []
        self._selected_index = 0

        self._menu_column = ft.Column(
            controls=[],
            spacing=2,
            scroll=ft.ScrollMode.AUTO,
        )

        super().__init__(
            content=ft.Column(
                controls=[
                    # Logo 区
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(
                                        name=ft.Icons.STORAGE_ROUNDED,
                                        size=20,
                                        color="#FFFFFF",
                                    ),
                                    width=36,
                                    height=36,
                                    border_radius=10,
                                    bgcolor=COLORS["primary"],
                                    alignment=ft.alignment.center,
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("C盘清理", size=15, color="#FFFFFF",
                                                weight=ft.FontWeight.W_700),
                                        ft.Text("磁盘空间管理", size=10, color=COLORS["sidebar_text"]),
                                    ],
                                    spacing=0,
                                ),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        height=72,
                        padding=ft.padding.only(left=18, right=16),
                    ),
                    # 菜单
                    ft.Container(content=self._menu_column, expand=True,
                                 padding=ft.padding.only(top=4)),
                    # 底部标识
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(name=ft.Icons.LOCK_OUTLINED, size=13,
                                        color=COLORS["sidebar_text"]),
                                ft.Text("本地运行 · 不上传数据", size=10,
                                        color=COLORS["sidebar_text"]),
                            ],
                            spacing=6,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        height=44,
                        padding=ft.padding.only(bottom=8),
                    ),
                ],
                spacing=0,
            ),
            width=224,
            bgcolor=COLORS["sidebar_bg"],
        )

        self._build_menu()

    def _build_menu(self):
        """按分组构建菜单"""
        for title, start, end in self.GROUPS:
            self._menu_column.controls.append(
                ft.Container(
                    content=ft.Text(title, size=10, color="#7C83A0",
                                    weight=ft.FontWeight.W_600),
                    padding=ft.padding.only(left=22, top=12, bottom=4),
                )
            )
            for i in range(start, min(end, len(self.MENU_ITEMS))):
                item = self.MENU_ITEMS[i]
                menu_item = MenuItem(
                    icon=item["icon"],
                    text=item["text"],
                    selected=(i == self._selected_index),
                    on_click=lambda e, idx=i: self._on_item_click(idx),
                )
                self._menu_items.append(menu_item)
                self._menu_column.controls.append(menu_item)

    def _on_item_click(self, index: int):
        if index == self._selected_index:
            return
        if 0 <= self._selected_index < len(self._menu_items):
            self._menu_items[self._selected_index].selected = False
        self._selected_index = index
        self._menu_items[index].selected = True
        if self.on_menu_change:
            self.on_menu_change(index, self.MENU_ITEMS[index]["text"])

    @property
    def current_title(self) -> str:
        return self.MENU_ITEMS[self._selected_index]["text"]
