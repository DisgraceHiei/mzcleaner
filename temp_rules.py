"""临时文件后缀规则（事实信息，MIT 原创整理）。

判定方式：文件名（小写）以这些后缀结尾即视为临时文件。
后缀清单是公开事实（Czkawka 等开源清理工具均使用同类清单），
此处为独立整理，不含任何第三方代码。

安全第一：
- 排除游戏/应用的缓存目录（如 Cache.Windows），这类 .cache 文件虽大，
  但属于程序运行时缓存，删除会导致重新下载，不算"垃圾"。
- 排除用户明确可能需要的目录（Documents、Desktop、Downloads 下的 .bak），
  备份文件可能是用户主动保留的。
"""

import os

# 变量展开表
VARS = {
    "LOCALAPPDATA": os.environ.get("LOCALAPPDATA", os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local")),
    "WINDIR": os.environ.get("WINDIR", "C:\\Windows"),
    "PROGRAMDATA": os.environ.get("PROGRAMDATA", "C:\\ProgramData"),
    "TEMP": os.environ.get("TEMP", ""),
}

# 临时文件后缀（小写匹配 ends_with）
TEMP_SUFFIXES = [
    "#", "thumbs.db", ".bak", "~", ".tmp", ".temp",
    ".ds_store", ".crdownload", ".part", ".cache", ".dmp",
    ".download", ".partial",
]

# 扫描范围：明确的临时/缓存目录，递归找匹配后缀的文件
# 不扫整个 LOCALAPPDATA（太慢且易误伤），只扫这些公认的临时目录
SCAN_ROOTS = [
    "{LOCALAPPDATA}\\Temp",
    "{WINDIR}\\Temp",
    "{LOCALAPPDATA}\\CrashDumps",
    "{LOCALAPPDATA}\\Microsoft\\Windows\\Explorer\\IconCacheToDelete",
    "{PROGRAMDATA}\\Microsoft\\Windows\\Temp",
    "{LOCALAPPDATA}",  # 整个 LocalAppData：覆盖散落在各软件目录的 .tmp/.dmp
]

# 排除目录（这些目录下的文件即使匹配后缀也不清理）
EXCLUDE_PATH_PARTS = [
    "cache.windows",      # 游戏缓存（Warframe 等），删了会重新下载
    "\\steam\\",
    "\\games\\",
    "\\node_modules\\",   # 依赖缓存，删了影响构建
    "\\.git\\",
]
