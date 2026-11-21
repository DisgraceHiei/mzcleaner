"""树状图视图 - WizTree/SpaceSniffer 风格。

方块面积代表占用空间，显示名称与大小，点击下钻到子目录。
纯只读，不提供删除。
"""

import flet as ft
from theme import COLORS


def _short_size(size: int) -> str:
    if size >= 1024 ** 3:
        return f"{size / 1024 ** 3:.1f}GB"
    if size >= 1024 ** 2:
        return f"{size / 1024 ** 2:.0f}MB"
    return f"{size / 1024:.0f}KB"


def treemap(items, x, y, w, h):
    """递归二分布局：按面积交替横竖对半分，永不产生细条。"""
    nodes = [(node, s) for node, s in items if s > 0]
    result = []
    if not nodes:
        return result

    def split(sub, rx, ry, rw, rh, horizontal):
        if not sub:
            return
        if len(sub) == 1:
            result.append((sub[0][0], rx, ry, rw, rh))
            return
        total = sum(s for _, s in sub)
        half = total / 2
        acc, cut = 0, 1
        for i, (_, s) in enumerate(sub[:-1]):
            acc += s
            if acc >= half:
                cut = i + 1
                break
        left, right = sub[:cut], sub[cut:]
        ratio = sum(s for _, s in left) / total
        if horizontal:
            lw = rw * ratio
            split(left, rx, ry, lw, rh, False)
            split(right, rx + lw, ry, rw - lw, rh, False)
        else:
            lh = rh * ratio
            split(left, rx, ry, rw, lh, True)
            split(right, rx, ry + lh, rw, rh - lh, True)

    split(nodes, x, y, w, h, w >= h)
    return result


# 按类别的柔和配色（WizTree 风格：低饱和大地色/蓝/绿）
CATEGORY_COLORS = {
    "系统": "#D9C4A8",     # 浅棕
    "应用": "#A9C4DE",     # 浅蓝
    "用户": "#B3D4C0",     # 浅绿
    "浏览器": "#E0CBA0",   # 浅黄棕
    "通讯": "#C9BBD9",     # 浅紫
    "游戏": "#DDB6B0",     # 浅红棕
    "设计": "#D9BFD0",     # 浅粉棕
    "开发": "#AECED3",     # 浅青
    "目录": "#C5CDD9",     # 浅灰蓝
}
FALLBACK_COLORS = ["#C5CDD9", "#D9C4A8", "#A9C4DE", "#B3D4C0", "#E0CBA0", "#C9BBD9"]


class SpaceView(ft.Container):
    """树状图视图"""

    CANVAS_W = 860
    CANVAS_H = 460

    def __init__(self, page: ft.Page):
        self.page = page
        self._stack = []
        self._nodes = []
        self._canvas = ft.Stack(controls=[], width=self.CANVAS_W, height=self.CANVAS_H)
        self._breadcrumb = ft.Text("全部磁盘", size=12, color=COLORS["text"],
                                   weight=ft.FontWeight.W_600)
        self._hint = ft.Text(
            "方块面积 = 占用空间 · 点击下钻 · 数值为估算（仅用于定位空间大户，非可清理垃圾）",
            size=10, color=COLORS["secondary"],
        )

        super().__init__(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                self._breadcrumb,
                                ft.TextButton("← 返回", on_click=self._go_back, visible=False),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        bgcolor="#F1F3F8",
                        border_radius=8,
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    ),
                    ft.Container(
                        content=ft.Row(controls=[self._canvas],
                                       alignment=ft.MainAxisAlignment.CENTER),
                        bgcolor="#FFFFFF",
                        border_radius=10,
                        border=ft.border.all(1, COLORS["border"]),
                        padding=ft.padding.all(1),
                        expand=True,
                    ),
                    self._hint,
                ],
                spacing=8,
                expand=True,
            ),
            visible=False,
            expand=True,
        )
        self._back_btn = self.content.controls[0].content.controls[1]

    def set_nodes(self, nodes: list):
        self._stack = []
        self._nodes = nodes
        self._breadcrumb.value = "全部磁盘"
        self._draw()

    def _go_back(self, e):
        if self._stack:
            _, nodes = self._stack.pop()
            self._nodes = nodes
            names = [n for n, _ in self._stack]
            self._breadcrumb.value = " / ".join(names) if names else "全部磁盘"
            self._draw()

    def _on_tap(self, node):
        children = node.get("children")
        if not children:
            return
        self._stack.append((self._breadcrumb.value, self._nodes))
        self._nodes = children
        self._breadcrumb.value = node["name"]
        self._draw()

    def _draw(self):
        self._canvas.controls.clear()
        nodes = sorted(self._nodes, key=lambda n: -n["size"])[:50]
        total = sum(n["size"] for n in nodes) or 1
        # 占比过小的项不单独成块，避免挤成 2x2 细点
        nodes = [n for n in nodes if n["size"] / total >= 0.004]
        boxes = treemap([(n, n["size"]) for n in nodes],
                        0, 0, self.CANVAS_W, self.CANVAS_H)

        for idx, (node, x, y, w, h) in enumerate(boxes):
            # 裁剪到画布内
            x, y = max(0, x), max(0, y)
            w = min(w, self.CANVAS_W - x)
            h = min(h, self.CANVAS_H - y)
            if w < 3 or h < 3:
                continue
            color = CATEGORY_COLORS.get(node.get("category"),
                                        FALLBACK_COLORS[idx % len(FALLBACK_COLORS)])
            label = node["name"]
            size_label = _short_size(node["size"])

            # 尽量显示名称+大小，空间不足时只显示大小，再不足显示空
            if w >= 70 and h >= 38:
                content = ft.Column(
                    controls=[
                        ft.Text(label, size=10, color="#333333",
                                overflow=ft.TextOverflow.ELLIPSIS, max_lines=2,
                                text_align=ft.TextAlign.CENTER),
                        ft.Text(size_label, size=10, color="#555555",
                                weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER),
                    ],
                    spacing=1,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            elif w >= 40 and h >= 20:
                content = ft.Text(size_label, size=9, color="#444444",
                                  text_align=ft.TextAlign.CENTER)
            else:
                content = None

            self._canvas.controls.append(
                ft.Container(
                    content=ft.Container(content=content, alignment=ft.alignment.center,
                                         padding=ft.padding.all(2),
                                         expand=True) if content else None,
                    left=x + 1, top=y + 1,
                    width=max(2, w - 2), height=max(2, h - 2),
                    bgcolor=color,
                    border=ft.border.all(0.5, "#FFFFFF"),
                    border_radius=2,
                    on_click=lambda e, n=node: self._on_tap(n),
                    tooltip=f"{label}  {size_label}" +
                            ("（点击下钻）" if node.get("children") else ""),
                )
            )
        self._back_btn.visible = bool(self._stack)
        self.update()
