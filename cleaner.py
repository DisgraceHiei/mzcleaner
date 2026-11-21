"""清理操作模块 - 执行文件删除、目录清理等操作"""

import os
import shutil
import stat
import ctypes
from ctypes import wintypes
from pathlib import Path
from dataclasses import dataclass
from typing import Callable


@dataclass
class CleanResult:
    """清理操作结果"""
    success: bool
    path: str
    size: int
    error: str = ""


def empty_recycle_bin(drive_path: str, size: int = 0) -> CleanResult:
    """通过 Windows 官方接口 SHEmptyRecycleBinW 清空指定盘的回收站。

    注意：不能直接 rmtree $Recycle.Bin 目录。该目录下除回收文件外，还存放
    系统用于维护回收站的元数据（每个用户 SID 子目录及 desktop.ini 等），
    直接删除会破坏结构，导致系统弹出"回收站损坏"提示。
    交给系统接口清空可保证目录结构完整。
    """
    try:
        shell32 = ctypes.windll.shell32
        shell32.SHEmptyRecycleBinW.argtypes = [
            wintypes.HWND, wintypes.LPCWSTR, wintypes.DWORD
        ]
        shell32.SHEmptyRecycleBinW.restype = ctypes.c_long  # HRESULT
        # SHERB_NOCONFIRMATION | SHERB_NOPROGRESSUI | SHERB_NOSOUND
        flags = 0x1 | 0x2 | 0x4
        hr = shell32.SHEmptyRecycleBinW(None, drive_path, flags)
        if hr == 0:  # S_OK
            return CleanResult(success=True, path=drive_path, size=size)
        return CleanResult(success=False, path=drive_path, size=0,
                           error=f"系统接口返回 {hr}")
    except Exception as ex:
        return CleanResult(success=False, path=drive_path, size=0, error=str(ex))


def handle_remove_readonly(func, path, exc):
    """处理只读文件的删除权限问题"""
    os.chmod(path, stat.S_IWRITE)
    func(path)


class FileCleaner:
    """文件清理器"""

    def __init__(self, progress_callback: Callable = None):
        self.progress_callback = progress_callback
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def delete_files(self, paths: list[str]) -> list[CleanResult]:
        """删除指定的文件列表"""
        self._cancelled = False
        results = []
        total = len(paths)

        for i, path in enumerate(paths):
            if self._cancelled:
                break

            if self.progress_callback:
                self.progress_callback(f"正在删除 ({i + 1}/{total})", i + 1, total)

            try:
                size = os.path.getsize(path)
                os.remove(path)
                results.append(CleanResult(success=True, path=path, size=size))
            except PermissionError:
                try:
                    os.chmod(path, stat.S_IWRITE)
                    size = os.path.getsize(path)
                    os.remove(path)
                    results.append(CleanResult(success=True, path=path, size=size))
                except Exception as ex:
                    results.append(CleanResult(success=False, path=path, size=0, error=str(ex)))
            except FileNotFoundError:
                results.append(CleanResult(success=True, path=path, size=0))
            except Exception as ex:
                results.append(CleanResult(success=False, path=path, size=0, error=str(ex)))

        return results

    def clean_directory_contents(self, dir_path: str) -> CleanResult:
        """清空目录内容（保留目录本身）"""
        if not os.path.isdir(dir_path):
            return CleanResult(success=False, path=dir_path, size=0, error="目录不存在")

        total_size = 0
        try:
            for entry in os.scandir(dir_path):
                if self._cancelled:
                    break
                try:
                    if entry.is_file(follow_symlinks=False):
                        total_size += entry.stat().st_size
                        os.remove(entry.path)
                    elif entry.is_dir(follow_symlinks=False):
                        total_size += self._get_dir_size(entry.path)
                        shutil.rmtree(entry.path, onerror=handle_remove_readonly)
                except Exception:
                    continue
            return CleanResult(success=True, path=dir_path, size=total_size)
        except Exception as ex:
            return CleanResult(success=False, path=dir_path, size=0, error=str(ex))

    @staticmethod
    def _get_dir_size(path: str) -> int:
        total = 0
        try:
            for entry in os.scandir(path):
                try:
                    if entry.is_file(follow_symlinks=False):
                        total += entry.stat().st_size
                    elif entry.is_dir(follow_symlinks=False):
                        total += FileCleaner._get_dir_size(entry.path)
                except (OSError, PermissionError):
                    continue
        except (OSError, PermissionError):
            pass
        return total
