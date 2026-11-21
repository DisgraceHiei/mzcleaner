"""生成应用图标 app.ico（纯标准库，无第三方依赖）。

画一个靛蓝圆角方块 + 白色简化磁盘图案，内嵌 PNG。
"""

import struct
import zlib

SIZE = 64
BG = (79, 70, 229)        # 靛蓝 #4F46E5
FG = (255, 255, 255)      # 白色


def make_pixels():
    """生成 RGBA 像素矩阵（行优先）"""
    px = [[(0, 0, 0, 0) for _ in range(SIZE)] for _ in range(SIZE)]
    # 圆角方块背景：半径 14
    r = 14
    for y in range(SIZE):
        for x in range(SIZE):
            # 圆角判定
            cx = min(max(x, r), SIZE - 1 - r)
            cy = min(max(y, r), SIZE - 1 - r)
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                px[y][x] = (*BG, 255)

    def rect(x0, y0, x1, y1, color):
        for y in range(max(0, y0), min(SIZE, y1)):
            for x in range(max(0, x0), min(SIZE, x1)):
                px[y][x] = (*color, 255)

    # 白色磁盘外形：主体 16..48 x 14..50
    rect(16, 14, 48, 50, FG)
    # 挖出靛蓝内部，形成边框
    rect(19, 17, 45, 47, BG)
    # 顶部读写头区域
    rect(24, 17, 40, 28, FG)
    # 读写头小方块
    rect(28, 19, 35, 25, BG)
    # 底部标签
    rect(23, 33, 41, 43, FG)
    # 标签横线（靛蓝）
    rect(25, 36, 39, 38, BG)
    rect(25, 40, 36, 42, BG)
    return px


def png_bytes(px):
    """把像素矩阵编码为 PNG"""
    raw = b""
    for row in px:
        raw += b"\x00" + b"".join(bytes(p) for p in row)

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        c += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return c

    ihdr = struct.pack(">IIBBBBB", SIZE, SIZE, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))


def main():
    png = png_bytes(make_pixels())
    # ICO: header(6) + entry(16) + PNG data
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", SIZE, SIZE, 0, 0, 1, 32, len(png), 22)
    with open("app.ico", "wb") as f:
        f.write(header + entry + png)
    print("已生成 app.ico", len(header + entry + png), "bytes")


if __name__ == "__main__":
    main()
