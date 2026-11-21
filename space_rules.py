"""空间占用分析规则（只读，不删除任何文件）。

按软件类别归纳常见目录，用于还原"磁盘被谁占了"的视图。
注意：这里统计的是"占用空间"，不是"可清理垃圾"，
包含程序本体与用户数据，仅用于定位空间大户。
"""

import os

VARS = {
    "LOCALAPPDATA": os.environ.get("LOCALAPPDATA", os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local")),
    "APPDATA": os.environ.get("APPDATA", os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Roaming")),
    "USERPROFILE": os.environ.get("USERPROFILE", ""),
    "WINDIR": os.environ.get("WINDIR", "C:\\Windows"),
    "PROGRAMDATA": os.environ.get("PROGRAMDATA", "C:\\ProgramData"),
    "PROGRAMFILES": os.environ.get("PROGRAMFILES", "C:\\Program Files"),
    "PROGRAMFILES86": os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"),
}

# (显示名, 类别, 路径模板, 颜色) - 颜色用于树状图
SPACE_RULES = [
    # 系统
    ("Windows 系统", "系统", "{WINDIR}", "#6366F1"),
    ("ProgramData", "系统", "{PROGRAMDATA}", "#818CF8"),
    # 程序安装
    ("Program Files", "应用", "{PROGRAMFILES}", "#0EA5E9"),
    ("Program Files (x86)", "应用", "{PROGRAMFILES86}", "#38BDF8"),
    ("本地程序", "应用", "{LOCALAPPDATA}\\Programs", "#22D3EE"),
    # 用户数据
    ("用户文档", "用户", "{USERPROFILE}\\Documents", "#10B981"),
    ("用户下载", "用户", "{USERPROFILE}\\Downloads", "#34D399"),
    ("用户桌面", "用户", "{USERPROFILE}\\Desktop", "#6EE7B7"),
    ("用户图片", "用户", "{USERPROFILE}\\Pictures", "#A7F3D0"),
    ("用户视频", "用户", "{USERPROFILE}\\Videos", "#2DD4BF"),
    ("Roaming 数据", "用户", "{APPDATA}", "#14B8A6"),
    ("Local 数据", "用户", "{LOCALAPPDATA}", "#5EEAD4"),
    # 常见大类（从 Local 里单列，避免全算到 Local）
    ("Edge 浏览器", "浏览器", "{LOCALAPPDATA}\\Microsoft\\Edge", "#F59E0B"),
    ("Chrome 浏览器", "浏览器", "{LOCALAPPDATA}\\Google\\Chrome", "#FBBF24"),
    ("腾讯/微信", "通讯", "{LOCALAPPDATA}\\Tencent", "#8B5CF6"),
    ("微信文档", "通讯", "{USERPROFILE}\\Documents\\WeChat Files", "#A78BFA"),
    ("Steam 游戏", "游戏", "{PROGRAMFILES86}\\Steam", "#EF4444"),
    ("Epic 游戏", "游戏", "{PROGRAMFILES}\\Epic Games", "#F87171"),
    ("Adobe", "设计", "{LOCALAPPDATA}\\Adobe", "#EC4899"),
    ("JetBrains", "开发", "{LOCALAPPDATA}\\JetBrains", "#06B6D4"),
    ("Android Studio", "开发", "{LOCALAPPDATA}\\Google\\AndroidStudio", "#0891B2"),
]


def expand_template(tpl: str) -> str:
    p = tpl
    for k, v in VARS.items():
        p = p.replace("{" + k + "}", v)
    return os.path.normpath(p)
