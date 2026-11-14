# -*- coding: utf-8 -*-
"""
第3页：医学 CLIP 的四类问题（改版·去大方框）
4 条横带，只有一条细分隔线，无整块大框
左：序号圆 中：问题 + 说明 右：代表方法（小胶囊）
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Circle, FancyBboxPatch

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
GRAY = "#8B99A6"
ACCENT = "#C8873E"
WHITE = "#FFFFFF"

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


def P(ax, x, y, s, fs, color, weight="normal", ha="left", va="center", avail=None):
    if avail is not None:
        fs = fit(s, fs, avail, weight)
    return ax.text(x, y, s, fontsize=fs, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=6, linespacing=1.55)


def pill(ax, x, y, s, fs, color, h=0.40):
    w = tw(s, fs, "bold") + 0.34
    ax.add_patch(FancyBboxPatch((x, y - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=0.20",
                                fc=WHITE, ec=color, lw=1.15, zorder=4))
    ax.text(x + w / 2, y, s, fontsize=fs, color=color, fontweight="bold",
            ha="center", va="center", zorder=6)
    return w


W, H = 14.6, 7.5
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.44, "医学 CLIP 的四类问题：后续方法都在补什么", 20, NAVY, "bold",
  ha="center", avail=W - 0.8)

rows = [
    ("①", "对齐粒度太粗", SLATE,
     "整图对整文、对齐一次就结束；一张胸片有多个器官病灶，报告也讲好几件事",
     ["GloRIA", "MedFILIP", "CP-CLIP"]),
    ("②", "文本脏、配对不准", MIST,
     "报告冗长、说法不统一，常有「正常报告配异常图像」的假阴性，硬对齐学到错关联",
     ["MedCLIP", "MedKLIP"]),
    ("③", "缺医学先验知识", SLATE,
     "通用 CLIP 只学到「图上有什么」；医学还要判断病变性质、疾病类别与解剖关系",
     ["MedKLIP", "Abn-BLIP"]),
    ("④", "只做 2D、规模上不去", MIST,
     "CT/MRI 是三维体数据，早期方法只切 2D 切片、丢空间信息；配对数也上不去",
     ["MG-3D", "Merlin"]),
]

top = H - 1.10
rh = 1.42
num_x = 0.72
tx = 1.42
tw_avail = 7.55
mx = 9.35
mw_avail = W - mx - 0.45

for i, (num, title, col, desc, meth) in enumerate(rows):
    yc = top - i * rh
    # 序号圆
    ax.add_patch(Circle((num_x, yc), 0.235, fc=col, ec="none", zorder=5))
    ax.text(num_x, yc, num, fontsize=15, color=WHITE, fontweight="bold",
            ha="center", va="center", zorder=6)
    # 标题 + 说明（两行，不套框）
    P(ax, tx, yc + 0.34, title, 13.5, col, "bold", avail=tw_avail)
    P(ax, tx, yc - 0.30, desc, 9.8, TXT, avail=tw_avail)
    # 右侧方法小胶囊
    px = mx
    for nm in meth:
        pw = pill(ax, px, yc, nm, 9.4, col)
        px += pw + 0.16
    # 细分隔线
    if i < len(rows) - 1:
        ax.plot([0.60, W - 0.50], [yc - rh / 2, yc - rh / 2],
                color="#E8EDF2", lw=1.0, zorder=1)

P(ax, W / 2, 0.72, "本文聚焦问题①中的「核心—外围」这一支：把病灶与背景显式拆开，分别对齐",
  11.5, ACCENT, "bold", ha="center", avail=W - 1.0)

fig.savefig(f"{OUT}/p3_taxonomy.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
