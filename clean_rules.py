"""深度清理规则定义（MIT 原创，非复制自任何 GPL 规则库）。

设计原则：
- 只纳入公认可安全清理的「缓存 / 日志 / 临时 / 崩溃转储」目录。
- 不纳入用户文档、聊天记录正文、已安装程序主体、系统关键组件（如 WinSxS、
  DriverStore），避免误删导致软件或系统异常。
- 路径用环境变量模板，运行时展开；支持通配符 *（匹配单层子目录，如浏览器 Profile *）。
"""

import os

# 变量展开表（运行时计算）
VARS = {
    "LOCALAPPDATA": os.environ.get("LOCALAPPDATA", os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local")),
    "APPDATA": os.environ.get("APPDATA", os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Roaming")),
    "USERPROFILE": os.environ.get("USERPROFILE", ""),
    "WINDIR": os.environ.get("WINDIR", "C:\\Windows"),
    "PROGRAMDATA": os.environ.get("PROGRAMDATA", "C:\\ProgramData"),
    "TEMP": os.environ.get("TEMP", ""),
}

# 规则：(显示名, 分类, 路径模板)
# 路径模板中的 {LOCALAPPDATA} 等会在运行时展开；结尾的 \* 表示遍历该目录下所有子目录
DEEP_CLEAN_RULES = [
    # ── 浏览器缓存 ──────────────────────────────────────────
    ("Edge 缓存", "浏览器缓存", "{LOCALAPPDATA}\\Microsoft\\Edge\\User Data\\Default\\Cache"),
    ("Edge 代码缓存", "浏览器缓存", "{LOCALAPPDATA}\\Microsoft\\Edge\\User Data\\Default\\Code Cache"),
    ("Edge GPU 缓存", "浏览器缓存", "{LOCALAPPDATA}\\Microsoft\\Edge\\User Data\\Default\\GPUCache"),
    ("Edge 媒体缓存", "浏览器缓存", "{LOCALAPPDATA}\\Microsoft\\Edge\\User Data\\Default\\Media Cache"),
    ("Chrome 缓存", "浏览器缓存", "{LOCALAPPDATA}\\Google\\Chrome\\User Data\\Default\\Cache"),
    ("Chrome 代码缓存", "浏览器缓存", "{LOCALAPPDATA}\\Google\\Chrome\\User Data\\Default\\Code Cache"),
    ("Chrome GPU 缓存", "浏览器缓存", "{LOCALAPPDATA}\\Google\\Chrome\\User Data\\Default\\GPUCache"),
    ("Chrome 媒体缓存", "浏览器缓存", "{LOCALAPPDATA}\\Google\\Chrome\\User Data\\Default\\Media Cache"),
    ("Firefox 缓存", "浏览器缓存", "{LOCALAPPDATA}\\Mozilla\\Firefox\\Profiles"),
    ("Brave 缓存", "浏览器缓存", "{LOCALAPPDATA}\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Cache"),
    ("Opera 缓存", "浏览器缓存", "{LOCALAPPDATA}\\Opera Software\\Opera Stable\\Cache"),
    ("Vivaldi 缓存", "浏览器缓存", "{LOCALAPPDATA}\\Vivaldi\\User Data\\Default\\Cache"),
    ("IE 缓存", "浏览器缓存", "{LOCALAPPDATA}\\Microsoft\\Windows\\INetCache"),
    ("IE Cookie 缓存", "浏览器缓存", "{LOCALAPPDATA}\\Microsoft\\Windows\\INetCookies"),

    # ── Windows 系统缓存与日志 ──────────────────────────────
    ("缩略图缓存数据库", "系统缓存", "{LOCALAPPDATA}\\Microsoft\\Windows\\Explorer\\thumbcache_*.db"),
    ("字体缓存", "系统缓存", "{LOCALAPPDATA}\\Microsoft\\Windows\\FontCache"),
    ("崩溃转储文件", "系统日志", "{LOCALAPPDATA}\\CrashDumps"),
    ("Windows 错误报告", "系统日志", "{PROGRAMDATA}\\Microsoft\\Windows\\WER"),
    ("传递优化缓存", "系统更新", "{WINDIR}\\SoftwareDistribution\\DeliveryOptimization"),
    ("Windows 更新缓存", "系统更新", "{WINDIR}\\SoftwareDistribution\\Download"),
    ("CBS 日志", "系统日志", "{WINDIR}\\Logs\\CBS"),
    ("磁盘清理临时", "临时文件", "{WINDIR}\\Temp"),
    ("Windows 安装临时", "临时文件", "{WINDIR}\\Installer\\Temp"),
    ("预读取文件", "系统缓存", "{WINDIR}\\Prefetch"),
    ("最近文档记录", "系统记录", "{APPDATA}\\Microsoft\\Windows\\Recent"),
    ("注册表备份缓存", "系统缓存", "{WINDIR}\\System32\\config\\RegBackup"),
    ("软件分发临时", "临时文件", "{PROGRAMDATA}\\Microsoft\\Windows\\Temp"),

    # ── 开发者工具缓存 ──────────────────────────────────────
    ("npm 缓存", "开发缓存", "{LOCALAPPDATA}\\npm-cache"),
    ("npm 缓存(v6+)", "开发缓存", "{LOCALAPPDATA}\\npm\\Cache"),
    ("pip 缓存", "开发缓存", "{LOCALAPPDATA}\\pip\\Cache"),
    ("NuGet 缓存", "开发缓存", "{USERPROFILE}\\.nuget\\packages"),
    ("Gradle 缓存", "开发缓存", "{USERPROFILE}\\.gradle\\caches"),
    ("Maven 缓存", "开发缓存", "{USERPROFILE}\\.m2\\repository"),
    ("Go 构建缓存", "开发缓存", "{LOCALAPPDATA}\\go-build"),
    ("Yarn 缓存", "开发缓存", "{LOCALAPPDATA}\\Yarn\\Cache"),
    ("pnpm 缓存", "开发缓存", "{LOCALAPPDATA}\\pnpm-store"),
    ("Docker 桌面缓存", "开发缓存", "{LOCALAPPDATA}\\Docker\\wsl"),
    ("Android Studio 缓存", "开发缓存", "{LOCALAPPDATA}\\Google\\AndroidStudio"),
    ("VS Code 缓存", "开发缓存", "{APPDATA}\\Code\\Cache"),
    ("VS Code CachedData", "开发缓存", "{APPDATA}\\Code\\CachedData"),
    ("JetBrains 缓存", "开发缓存", "{LOCALAPPDATA}\\JetBrains"),

    # ── 显卡/系统着色器缓存（自动重建，安全）────────────────
    ("NVIDIA 着色器缓存", "显卡缓存", "{LOCALAPPDATA}\\NVIDIA\\DXCache"),
    ("NVIDIA 着色器缓存(旧版)", "显卡缓存", "{LOCALAPPDATA}\\NVIDIA\\GLCache"),
    ("NVIDIA 下载缓存", "显卡缓存", "{LOCALAPPDATA}\\NVIDIA\\Download"),
    ("DirectX 着色器缓存", "显卡缓存", "{LOCALAPPDATA}\\D3DSCache"),

    # ── 影音/创作软件缓存 ──────────────────────────────────
    ("剪映缓存", "应用缓存", "{LOCALAPPDATA}\\JianyingPro\\User Data\\Cache"),
    ("剪映新版本缓存", "应用缓存", "{LOCALAPPDATA}\\JianyingPro\\Cache"),
    ("网易云音乐缓存", "应用缓存", "{LOCALAPPDATA}\\NetEase\\CloudMusic\\Cache"),
    ("网易云音乐数据缓存", "应用缓存", "{LOCALAPPDATA}\\NetEase\\CloudMusic\\Data\\Cache"),

    # ── 浏览器缓存补充 ────────────────────────────────────
    ("夸克浏览器缓存", "浏览器缓存", "{LOCALAPPDATA}\\Quark\\User Data\\Cache"),
    ("夸克浏览器代码缓存", "浏览器缓存", "{LOCALAPPDATA}\\Quark\\User Data\\Code Cache"),

    # ── 常用应用缓存 ────────────────────────────────────────
    ("Office 缓存", "应用缓存", "{LOCALAPPDATA}\\Microsoft\\Office\\16.0\\OfficeFileCache"),
    ("Discord 缓存", "应用缓存", "{APPDATA}\\discord\\Cache"),
    ("Slack 缓存", "应用缓存", "{APPDATA}\\Slack\\Cache"),
    ("Zoom 缓存", "应用缓存", "{APPDATA}\\Zoom\\Cache"),
    ("Steam 下载缓存", "应用缓存", "{PROGRAMDATA}\\Steam"),
    ("腾讯会议缓存", "应用缓存", "{APPDATA}\\Tencent\\Meeting\\Cache"),
    ("企业微信缓存", "应用缓存", "{APPDATA}\\Tencent\\WXWork\\Cache"),
    ("钉钉缓存", "应用缓存", "{APPDATA}\\DingTalk\\Cache"),
    ("阿里云盘缓存", "应用缓存", "{APPDATA}\\aDrive\\Cache"),
    ("阿里云盘代码缓存", "应用缓存", "{APPDATA}\\aDrive\\Code Cache"),
    ("阿里云盘 GPU 缓存", "应用缓存", "{APPDATA}\\aDrive\\GPUCache"),
    ("阿里云盘日志", "应用缓存", "{APPDATA}\\aDrive\\logs"),

    # ── 微信/QQ 新版路径（缓存部分）────────────────────────
    ("微信 v4 缓存", "微信缓存", "{LOCALAPPDATA}\\com.tencent.wechat\\Cache"),
    ("微信临时文件", "微信缓存", "{LOCALAPPDATA}\\com.tencent.xinWeChat\\Temp"),
    ("QQ 新版缓存", "QQ缓存", "{LOCALAPPDATA}\\Tencent\\QQ\\Cache"),
]


def expand_rule_path(template: str) -> str:
    """展开规则路径模板中的变量"""
    result = template
    for key, value in VARS.items():
        result = result.replace("{" + key + "}", value)
    return os.path.normpath(result)
