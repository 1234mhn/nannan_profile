# -*- coding: utf-8 -*-
"""文字宽度自动测量 + 超宽检查工具（画图前必用）"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import os

for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
          "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"]:
    if os.path.exists(p):
        fm.fontManager.addfont(p)
plt.rcParams["font.family"] = "Noto Sans CJK SC"

_FIG = _AX = _R = None


def _init():
    global _FIG, _AX, _R
    if _FIG is None:
        _FIG, _AX = plt.subplots(figsize=(20, 10), dpi=200)
        _AX.set_xlim(0, 20)
        _AX.set_ylim(0, 10)
        _AX.axis("off")
        _FIG.canvas.draw()
        _R = _FIG.canvas.get_renderer()


def text_size(s, fs, weight="normal"):
    """返回 (宽, 高) 英寸"""
    _init()
    t = _AX.text(0, 0, s, fontsize=fs, fontweight=weight)
    bb = t.get_window_extent(renderer=_R)
    t.remove()
    return bb.width / 200.0, bb.height / 200.0


def check(label, s, fs, avail_w, weight="normal"):
    w, h = text_size(s, fs, weight)
    ok = w <= avail_w
    flag = "OK " if ok else "OVER"
    print(f"[{flag}] {label}: {w:.2f}in / avail {avail_w:.2f}in  ({s[:30]})")
    return ok, w
