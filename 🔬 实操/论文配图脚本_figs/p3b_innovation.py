# -*- coding: utf-8 -*-
"""
插页：医学 CLIP 领域的六种常见创新套路
不逐个列模型，而是归纳「大家是怎么找到创新点的」
每个套路：做法 + 代表模型
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
GRAY = "#8B99A6"
ACCENT = "#C8873E"
WHITE = "#FFFFFF"
BG1 = "#F4F7FA"
BG2 = "#F2F6F9"

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


def th(s, fs, weight="normal", ls=1.7):
    _init()
    t = _A.text(0, 0, s, fontsize=fs, fontweight=weight, linespacing=ls)
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


def P(ax, x, y, s, fs, color, weight="normal", ha="center", va="center",
      avail=None, ls=1.7):
    if avail is not None:
        fs = fit(s, fs, avail, weight)
    return ax.text(x, y, s, fontsize=fs, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=7, linespacing=ls)


def pod(ax, x, y, w, h, fc, r=0.15, z=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec="none", zorder=z))


W, H = 14.6, 8.0
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.54, "医学 CLIP 的几类创新路径", 23, NAVY, "bold",
  ha="center", avail=W - 1.4)
P(ax, W / 2, H - 0.98, "这些工作大体沿几个方向改造：换部件、改目标、拆结构、借工具、换维度",
  12.0, GRAY, ha="center", avail=W - 1.4)

cards = [
    ("加外挂", "在 CLIP 之外接一个知识来源，\n如知识库、知识图谱、解剖标注",
     "MedKLIP · KAD · KoBo", "外部知识"),
    ("改目标函数", "网络结构不动，只在损失函数上做文章，\n重新定义正负样本或加约束项",
     "MedCLIP · CXR-CLIP · LocalMI", "监督信号"),
    ("拆结构", "把输入或输出分成两部分分别处理，\n如核心与外围、区域与整体、器官与病灶",
     "CP-CLIP · GLoRIA · MGCA", "输入组织"),
    ("套别的方法", "借用其他领域已成熟的手段，\n如互信息、因果推断、对比聚类、图网络",
     "LocalMI · ARL · KAD", "方法迁移"),
    ("放大输入", "把二维换成三维、切片换成体积，\n补上原本缺失的空间维度",
     "Merlin · MG-3D · fVLM", "数据维度"),
]

MX = 0.52
GX = 0.34
CW = (W - 2 * MX - 2 * GX) / 3
TOP = H - 1.45
CH = 2.75
GAP_ROW = 0.30

TFS, DFS, MFS, LFS = 16.0, 10.8, 9.8, 9.0

ROW_N = [3, 2]
for i, (name, what, models, tag) in enumerate(cards):
    if i < 3:
        row, col, n = 0, i, 3
    else:
        row, col, n = 1, i - 3, 2
    row_w = n * CW + (n - 1) * GX
    x0 = (W - row_w) / 2
    x = x0 + col * (CW + GX)
    y = TOP - CH - row * (CH + GAP_ROW)

    pod(ax, x, y, CW, CH, BG1 if (i % 2 == 0) else BG2)
    cx = x + CW / 2

    # 标签（右上小字）
    P(ax, cx, y + CH - 0.30, tag, LFS, PALE, "bold", avail=CW - 0.5)
    # 名称
    P(ax, cx, y + CH - 0.72, name, TFS, NAVY, "bold", avail=CW - 0.35)
    # 做法
    P(ax, cx, y + CH - 1.42, what, DFS, TXT, avail=CW - 0.45, ls=1.85)
    # 代表
    P(ax, cx, y + 0.36, models, MFS, SLATE, "bold", avail=CW - 0.4)

# 底部
P(ax, W / 2, 0.92,
  "找创新点的思路：先定位当前方法最受限的环节，再看上述方向中哪些可以组合",
  12.4, ACCENT, "bold", ha="center", avail=W - 1.3)
P(ax, W / 2, 0.54,
  "CP-CLIP 属于「拆结构」这一类：将图像与文本同时拆为核心 / 外围，再做两级对齐",
  11.0, NAVY, ha="center", avail=W - 1.3)

fig.savefig(f"{OUT}/p3b_innovation.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
