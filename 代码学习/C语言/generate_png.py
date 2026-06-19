# -*- coding: utf-8 -*-
"""直接用 Pillow 手画三张 C 语言内存管理流程图，输出 PNG"""

from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = r"D:\code\学习笔记\代码学习\C语言"
FONT_PATH = "C:/Windows/Fonts/msyh.ttc"
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"

# 颜色定义
COLORS = {
    "stack_bg":    (250, 236, 231),  # 浅橙
    "stack_bd":    (216,  90,  48),  # 深橙
    "stack_txt":   ( 74,  27,  12),
    "heap_bg":     (230, 241, 251),  # 浅蓝
    "heap_bd":     ( 55, 138, 221),
    "heap_txt":    (  4,  44,  83),
    "data_bg":     (234, 243, 222),  # 浅绿
    "data_bd":     ( 99, 153,  34),
    "data_txt":    ( 23,  52,   4),
    "rodata_bg":   (250, 238, 218),  # 浅黄
    "rodata_bd":   (239, 159,  39),
    "rodata_txt":  ( 65,  36,   2),
    "text_bg":     (238, 237, 254),  # 浅紫
    "text_bd":     ( 83,  74, 183),
    "text_txt":    ( 38,  33,  92),
    "red_bg":      (252, 235, 235),
    "red_bd":      (226,  75,  74),
    "dark":        ( 44,  44,  42),
    "gray":        (136, 135, 128),
    "light_gray":  (180, 178, 169),
    "footer_bg":   (241, 239, 232),
    "white":       (255, 255, 255),
}

def get_font(size, bold=False):
    path = FONT_BOLD if bold else FONT_PATH
    return ImageFont.truetype(path, size)

def rounded_rect(draw, xy, r, fill, outline):
    """画圆角矩形"""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=2)

def draw_arrow(draw, x1, y1, x2, y2, color, w=2):
    """画箭头线"""
    import math
    draw.line([(x1, y1), (x2, y2)], fill=color, width=w)
    # 箭头头部
    angle = math.atan2(y2 - y1, x2 - x1)
    arr_len = 10
    ax1 = x2 - arr_len * math.cos(angle - 0.5) + w * math.sin(angle - 0.5)
    ay1 = y2 - arr_len * math.sin(angle - 0.5) - w * math.cos(angle - 0.5)
    ax2 = x2 - arr_len * math.cos(angle + 0.5) - w * math.sin(angle + 0.5)
    ay2 = y2 - arr_len * math.sin(angle + 0.5) + w * math.cos(angle + 0.5)
    draw.polygon([(x2, y2), (ax1, ay1), (ax2, ay2)], fill=color)


# ========================
# 图1: 内存分区布局 (800x200)
# ========================
def draw_memory_layout():
    W, H = 800, 200
    img = Image.new("RGB", (W, H), COLORS["white"])
    d = ImageDraw.Draw(img)

    # 标题
    font14b = get_font(14, bold=True)
    d.text((W//2, 10), "C 程序内存布局（高地址 → 低地址）", fill=COLORS["dark"], font=font14b, anchor="mt")

    boxes = [
        ("栈区 Stack", "局部变量 · 自动管理", COLORS["stack_bg"], COLORS["stack_bd"], COLORS["stack_txt"]),
        ("堆区 Heap", "malloc · 手动释放",     COLORS["heap_bg"],  COLORS["heap_bd"],  COLORS["heap_txt"]),
        ("全局/静态区", "Data + BSS",           COLORS["data_bg"],  COLORS["data_bd"],  COLORS["data_txt"]),
        ("只读区 Rodata", "字面量 · 不可修改",      COLORS["rodata_bg"],COLORS["rodata_bd"],COLORS["rodata_txt"]),
        ("代码区 Text", "机器指令 · 只读共享",      COLORS["text_bg"],  COLORS["text_bd"],  COLORS["text_txt"]),
    ]

    bw, bh = 136, 56   # ⭐ 盒子宽高
    gap = 8            # ⭐ 盒子间距
    total_w = 5 * bw + 4 * gap
    start_x = (W - total_w) // 2
    y = 42

    font12b = get_font(12, bold=True)
    font11 = get_font(11)
    font10 = get_font(10)

    for i, (title, desc, bg, bd, txt_c) in enumerate(boxes):
        x = start_x + i * (bw + gap)
        rounded_rect(d, (x, y, x + bw, y + bh), 8, bg, bd)
        # 标题
        d.text((x + bw // 2, y + 16), title, fill=txt_c, font=font12b, anchor="mt")
        # 描述
        d.text((x + bw // 2, y + 38), desc, fill=txt_c, font=font11, anchor="mt")

    # ⭐ 盒子之间的连接箭头
    for i in range(4):
        x1 = start_x + i * (bw + gap) + bw + 4
        x2 = start_x + (i + 1) * (bw + gap) - 4
        cy = y + bh // 2
        d.line([(x1, cy), (x2, cy)], fill=COLORS["gray"], width=1)
        # 小箭头
        d.polygon([(x2, cy-4), (x2, cy+4), (x2+6, cy)], fill=COLORS["gray"])

    # ⭐ 栈/堆增长方向
    mid_x = start_x + bw + gap // 2
    g_y = y + bh + 14
    # 栈向下增长（向右）
    draw_arrow(d, mid_x - 28, g_y, mid_x - 4, g_y, COLORS["stack_bd"], 2)
    d.text((mid_x - 16, g_y + 14), "栈向下增长", fill=COLORS["stack_bd"], font=font10, anchor="mt")
    # 堆向上增长（向左）
    draw_arrow(d, mid_x + 4, g_y, mid_x + 28, g_y, COLORS["heap_bd"], 2)  # ←
    # 堆向上增长实际应该是向左（向高地址），让我调整
    # 重新画，堆向上增长 = 向左
    # 算了，简化处理，两个箭头都画成从中间往两边
    # 栈向下（向右），堆向上（也向右）... 不对，让我重新理解
    # 在布局中 Stack 在高地址端(左)，Heap 在右边(更接近低地址)
    # Stack 向低地址增长 = 向右增长
    # Heap 向高地址增长 = 向左增长
    # 所以两者在中间碰头
    # 清除刚才的
    # 重新画
    pass

    # 重画增长箭头 - 简化：两个都标出来
    # 从中间区域画栈往右、堆往左
    a1_x = start_x + bw + gap//2
    # 栈向右
    draw_arrow(d, a1_x - 30, g_y, a1_x - 4, g_y, COLORS["stack_bd"], 2)
    d.text((a1_x - 17, g_y + 14), "栈 ↓", fill=COLORS["stack_bd"], font=font10, anchor="mt")
    # 堆向左
    ax1 = a1_x + 4
    ax2 = a1_x + 30
    draw_arrow(d, ax2, g_y, ax1, g_y, COLORS["heap_bd"], 2)
    d.text((a1_x + 17, g_y + 14), "堆 ↑", fill=COLORS["heap_bd"], font=font10, anchor="mt")

    # 底部栏
    f_y = g_y + 30
    rounded_rect(d, (start_x, f_y, start_x + total_w, f_y + 22), 4, COLORS["footer_bg"], COLORS["light_gray"])
    d.text((W // 2, f_y + 11), "进程虚拟地址空间 (Virtual Address Space)", fill=COLORS["gray"], font=font11, anchor="mm")

    path = os.path.join(OUT_DIR, "memory-layout.png")
    img.save(path)
    print(f"[OK] {path}")


# ========================
# 图2: str[] vs *ps (800x170)
# ========================
def draw_stack_vs_rodata():
    W, H = 800, 170
    img = Image.new("RGB", (W, H), COLORS["white"])
    d = ImageDraw.Draw(img)

    font14b = get_font(14, bold=True)
    font12b = get_font(12, bold=True)
    font11 = get_font(11)
    font10 = get_font(10)
    font_mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 12)

    d.text((W//2, 12), "char str[] vs char *ps", fill=COLORS["dark"], font=font14b, anchor="mt")

    # 左侧：栈区虚线框
    sx, sy, sw, sh = 30, 32, 420, 102
    for i in range(0, sw, 2):  # 虚线
        if i % 8 < 4:
            d.line([(sx + i, sy), (sx + i + 2, sy)], fill=COLORS["stack_bd"], width=1)
            d.line([(sx + i, sy + sh), (sx + i + 2, sy + sh)], fill=COLORS["stack_bd"], width=1)
    for i in range(0, sh, 2):
        if i % 8 < 4:
            d.line([(sx, sy + i), (sx, sy + i + 2)], fill=COLORS["stack_bd"], width=1)
            d.line([(sx + sw, sy + i), (sx + sw, sy + i + 2)], fill=COLORS["stack_bd"], width=1)
    d.text((sx + 8, sy + 6), "栈区 Stack", fill=COLORS["stack_bd"], font=font11)

    # str[] 盒子
    bx, by, bw, bh = sx + 16, sy + 22, 180, 64
    rounded_rect(d, (bx, by, bx + bw, by + bh), 8, COLORS["stack_bg"], COLORS["stack_bd"])
    d.text((bx + bw//2, by + 12), "char str[6]", fill=COLORS["stack_txt"], font=get_font(12, bold=True), anchor="mt")
    d.text((bx + bw//2, by + 30), "['h','e','l','l','o','\\0']", fill=COLORS["stack_txt"], font=font_mono, anchor="mt")
    d.text((bx + bw//2, by + 50), "可修改", fill=(153, 60, 29), font=font11, anchor="mt")

    # ps 盒子
    px = bx + bw + 24
    rounded_rect(d, (px, by, px + bw - 20, by + bh), 8, COLORS["stack_bg"], COLORS["stack_bd"])
    d.text((px + (bw-20)//2, by + 12), "char *ps", fill=COLORS["stack_txt"], font=get_font(12, bold=True), anchor="mt")
    d.text((px + (bw-20)//2, by + 30), "0x7fff... (8字节)", fill=COLORS["stack_txt"], font=font_mono, anchor="mt")
    d.text((px + (bw-20)//2, by + 50), "指针本身在栈上", fill=(153, 60, 29), font=font11, anchor="mt")

    # 右侧：只读区虚线框
    rx = sx + sw + 16
    for i in range(0, sw-210, 2):
        if i % 8 < 4:
            d.line([(rx + i, sy), (rx + i + 2, sy)], fill=COLORS["rodata_bd"], width=1)
            d.line([(rx + i, sy + sh), (rx + i + 2, sy + sh)], fill=COLORS["rodata_bd"], width=1)
    for i in range(0, sh, 2):
        if i % 8 < 4:
            d.line([(rx, sy + i), (rx, sy + i + 2)], fill=COLORS["rodata_bd"], width=1)
            d.line([(rx + sw - 210, sy + i), (rx + sw - 210, sy + i + 2)], fill=COLORS["rodata_bd"], width=1)
    d.text((rx + 8, sy + 6), "只读区 Rodata", fill=COLORS["rodata_bd"], font=font11)

    # 字面量盒子
    lx, lw = rx + 12, 150
    rounded_rect(d, (lx, by, lx + lw, by + bh), 8, COLORS["rodata_bg"], COLORS["rodata_bd"])
    d.text((lx + lw//2, by + 12), "字符串字面量", fill=COLORS["rodata_txt"], font=get_font(12, bold=True), anchor="mt")
    d.text((lx + lw//2, by + 30), "hello\\0", fill=COLORS["rodata_txt"], font=font_mono, anchor="mt")
    d.text((lx + lw//2, by + 50), "不可修改", fill=(186, 117, 23), font=font11, anchor="mt")

    # 箭头：ps → 只读区
    ax, ay = px + (bw-20) - 4, by + bh//2
    draw_arrow(d, ax, ay, lx - 4, ay, COLORS["stack_bd"], 2)

    # 底部说明
    d.text((W//2, H - 18), "str[] 在栈上有自己的副本（可写），*ps 只是指向只读区（不可写）", fill=COLORS["gray"], font=font11, anchor="mm")

    path = os.path.join(OUT_DIR, "stack-vs-rodata.png")
    img.save(path)
    print(f"[OK] {path}")


# ========================
# 图3: 段错误图解 (800x200)
# ========================
def draw_segfault():
    W, H = 800, 200
    img = Image.new("RGB", (W, H), COLORS["white"])
    d = ImageDraw.Draw(img)

    font14b = get_font(14, bold=True)
    font11 = get_font(11)
    font10 = get_font(10)
    font_mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 11)

    d.text((W//2, 12), "段错误 SIGSEGV 图解", fill=COLORS["dark"], font=font14b, anchor="mt")

    # 5 个内存区域盒子（小号）
    regions = [
        ("代码区 Text",      COLORS["text_bg"],   COLORS["text_bd"]),
        ("只读区 Rodata",    COLORS["rodata_bg"], COLORS["rodata_bd"]),
        ("全局/静态区",      COLORS["data_bg"],   COLORS["data_bd"]),
        ("堆区 Heap",        COLORS["heap_bg"],   COLORS["heap_bd"]),
        ("栈区 Stack",       COLORS["stack_bg"],  COLORS["stack_bd"]),
    ]

    bw, bh = 120, 34
    gap = 6
    total_w = 5 * bw + 4 * gap
    start_x = (W - total_w) // 2
    r_y = 36

    for i, (label, bg, bd) in enumerate(regions):
        x = start_x + i * (bw + gap)
        rounded_rect(d, (x, r_y, x + bw, r_y + bh), 6, bg, bd)
        d.text((x + bw//2, r_y + bh//2), label, fill=COLORS["dark"], font=font11, anchor="mm")

    # 连接箭头
    for i in range(4):
        x1 = start_x + i * (bw + gap) + bw + 2
        x2 = start_x + (i + 1) * (bw + gap) - 2
        cy = r_y + bh//2
        d.line([(x1, cy), (x2, cy)], fill=COLORS["gray"], width=1)
        d.polygon([(x2, cy-3), (x2, cy+3), (x2+5, cy)], fill=COLORS["gray"])

    # PS 指针盒子
    ps_x = start_x + 5 * bw + 4 * gap + 10
    ps_w = 170
    rounded_rect(d, (ps_x, r_y, ps_x + ps_w, r_y + bh), 6, COLORS["stack_bg"], COLORS["stack_bd"])
    d.text((ps_x + ps_w//2, r_y + bh//2), "char *ps = \"hello yanan\"", fill=COLORS["stack_txt"], font=font_mono, anchor="mm")

    # 虚线弧箭头 ps → 只读区
    rodata_x = start_x + bw + gap // 2  # 只读区中心
    d.arc([ps_x - 20, r_y - 30, ps_x + 10, r_y + 20], start=130, end=200, fill=COLORS["stack_bd"], width=2)
    # 更简单的画法：直接用虚线曲线
    from PIL import ImageDraw as PILDraw
    curve_pts = [(ps_x + 4, r_y + bh//2), (ps_x - 10, r_y - 8), (rodata_x + bw//2, r_y - 8), (rodata_x + bw//2, r_y + 2)]
    # 用折线近似
    d.line(curve_pts, fill=COLORS["stack_bd"], width=1)
    # 虚线太复杂，改用实线折线
    pts = [(ps_x - 2, r_y + bh//2), (rodata_x + bw//2, r_y + bh//2), (rodata_x + bw//2, r_y - 4)]
    d.line(pts, fill=COLORS["red_bd"], width=2)
    # 箭头
    d.polygon([(rodata_x + bw//2, r_y-8), (rodata_x + bw//2 - 4, r_y), (rodata_x + bw//2 + 4, r_y)], fill=COLORS["red_bd"])

    # 写入尝试
    w_y = r_y + bh + 26
    rounded_rect(d, (rodata_x + bw//2 - 70, w_y, rodata_x + bw//2 + 70, w_y + 28), 6, COLORS["red_bg"], COLORS["red_bd"])
    d.text((rodata_x + bw//2, w_y + 14), "*(ps+4) = 'w'  试图写入只读区", fill=COLORS["red_bd"], font=font11, anchor="mm")

    # 红色 X 标记
    x_mark_x = rodata_x + bw//2
    x_mark_y = w_y + 28 + 10

    # 大红 ×
    d.line([(x_mark_x - 8, w_y + 28 + 2), (x_mark_x + 8, w_y + 28 + 18)], fill=COLORS["red_bd"], width=3)
    d.line([(x_mark_x + 8, w_y + 28 + 2), (x_mark_x - 8, w_y + 28 + 18)], fill=COLORS["red_bd"], width=3)

    # 说明
    d.text((W//2, H - 16), "ps 指向只读区 → 通过 ps 写入 → SIGSEGV 段错误", fill=COLORS["gray"], font=font11, anchor="mm")

    path = os.path.join(OUT_DIR, "segfault.png")
    img.save(path)
    print(f"[OK] {path}")


if __name__ == "__main__":
    draw_memory_layout()
    draw_stack_vs_rodata()
    draw_segfault()
    print("全部完成!")
