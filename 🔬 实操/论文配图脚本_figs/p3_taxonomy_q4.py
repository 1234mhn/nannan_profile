# -*- coding: utf-8 -*-
"""
第3页：医学 CLIP 的四类问题（清晰版 v4）
关键：所有文字位置按「实测高度」排，绝不重叠
- 先算标题高度、正文块高度、方法行高度，再反推格子最小高度
- 正文行距足够，正文与方法行之间强制留白
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch

OUT = "/root/.openclaw/workspace/figs/final9"
os.makedirs(OUT, exist_ok=True)

for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
          "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"]:
    if os.path.exists(p):
        fm.fontManager.addfont(p)
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False

NAVY = "#2C3E50"
SLATE = "#4A6D8C"
MIST = "#8FA5B8"
PALE = "#C5D2DC"
TXT = "#34495E"
ACCENT = "#C8873E"
WHITE = "#FFFFFF"
FOG = "#F7F9FB"

_F = _A = _R = None


def _init():
    global _F, _A, _R
    if _F is None:
        _F, _A = plt.subplots(figsize=(20, 10), dpi=200)
        _A.set_xlim(0, 20)
        _A.set_ylim(0, 10)
        _A.axis("off")
        _F.canvas.draw()
        _R = _F.canvas.get_renderer()


def tw(s, fs, weight="normal"):
    _init()
    t = _A.text(0, 0, s, fontsize=fs, fontweight=weight)
    bb = t.get_window_extent(renderer=_R)
    t.remove()
    return bb.width / 200.0


def th(s, fs, weight="normal", linespacing=1.6):
    """实测多行文字块高度（单位：画布坐标）"""
    _init()
    t = _A.text(0, 0, s, fontsize=fs, fontweight=weight, linespacing=linespacing)
    bb = t.get_window_extent(renderer=_R)
    t.remove()
    return bb.height / 200.0


def fit(s, fs, avail, weight="normal"):
    w = tw(s, fs, weight)
    return fs if w <= avail else fs * avail / w * 0.96


def setup(w, h):
    fig = plt.figure(figsize=(w, h), dpi=200, facecolor=WHITE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def P(ax, x, y, s, fs, color, weight="normal", ha="left", va="center",
      avail=None, ls=1.6):
    if avail is not None:
        fs = fit(s, fs, avail, weight)
    return ax.text(x, y, s, fontsize=fs, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=6, linespacing=ls)


W, H = 14.6, 8.4
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.52, "医学 CLIP 的四类问题：后续方法都在补什么", 21, NAVY, "bold",
  ha="center", avail=W - 0.9)

cells = [
    ("01", "对齐粒度太粗", MIST,
     "整图对整文，一次对齐就结束。一张胸片有多个器官与病灶，报告也在讲好几件事。",
     "GloRIA · MedFILIP · CP-CLIP"),
    ("02", "文本脏、配对不准", SLATE,
     "报告冗长、说法不统一，常有「正常报告配异常图像」的假阴性，硬对齐会学到错误关联。",
     "MedCLIP · MedKLIP"),
    ("03", "缺医学先验知识", SLATE,
     "通用 CLIP 只学到「图上有什么」。医学还要判断病变性质、疾病类别与解剖关系。",
     "MedKLIP · Abn-BLIP"),
    ("04", "只做 2D、规模上不去", MIST,
     "CT、MRI 是三维体数据，早期方法只切 2D 切片、丢空间信息，配对数据量也上不去。",
     "MG-3D · Merlin"),
]

# ---- 先量出各部分高度，据此定格子几何 ----
TFS, DFS, MFS = 17.0, 12.2, 12.4
PAD_T, PAD_B = 0.34, 0.36
GAP_TH = 0.30   # 标题与正文间距
GAP_DM = 0.34   # 正文与方法间距

mx, gx = 0.72, 0.86
top = H - 1.12
bot_limit = 1.55

# 预估正文宽度（两列）
cw = (W - 2 * mx - gx) / 2
desc_avail = cw - 0.64
meth_avail = cw - 0.64

max_h = 0
for num, title, col, desc, meth in cells:
    dfs = min(DFS, fit(desc, DFS, desc_avail))
    mfs = min(MFS, fit(meth, MFS, meth_avail, "bold"))
    h = (PAD_T + th(title, TFS, "bold") + GAP_TH
         + th(desc, dfs, linespacing=1.85) + GAP_DM
         + th(meth, mfs, "bold") + PAD_B)
    max_h = max(max_h, h)

ch = max_h
gy = (top - bot_limit - 2 * ch)
if gy < 0.30:
    gy = 0.30

for i, (num, title, col, desc, meth) in enumerate(cells):
    r, c = i // 2, i % 2
    x = mx + c * (cw + gx)
    y = top - (r + 1) * ch - r * gy

    ax.add_patch(FancyBboxPatch((x, y), cw, ch,
                                boxstyle="round,pad=0,rounding_size=0.14",
                                fc=FOG, ec="none", zorder=1))

    # 从顶往下依次排，每块都用实测高度递推，绝不重叠
    cy = y + ch - PAD_T
    P(ax, x + 0.32, cy - th(title, TFS, "bold") / 2, title, TFS, NAVY, "bold",
      va="center", avail=cw - 0.90)
    P(ax, x + cw - 0.32, cy - th(title, TFS, "bold") / 2, num, 22, PALE, "bold",
      ha="right", va="center")

    cy -= th(title, TFS, "bold") + GAP_TH

    dfs = min(DFS, fit(desc, DFS, desc_avail))
    dh = th(desc, dfs, linespacing=1.85)
    P(ax, x + 0.32, cy - dh / 2, desc, dfs, TXT, va="center",
      avail=desc_avail, ls=1.85)

    cy -= dh + GAP_DM

    mfs = min(MFS, fit(meth, MFS, meth_avail, "bold"))
    P(ax, x + 0.32, y + PAD_B + th(meth, mfs, "bold") / 2, meth, mfs, col, "bold",
      va="center", avail=meth_avail)

P(ax, W / 2, 0.72, "本文聚焦问题 01 中的「核心—外围」这一支：把病灶与背景显式拆开，分别对齐",
  12.2, ACCENT, "bold", ha="center", avail=W - 1.1)

fig.savefig(f"{OUT}/p3_taxonomy_q4.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print(f"saved  ch={ch:.2f} gy={gy:.2f}")
