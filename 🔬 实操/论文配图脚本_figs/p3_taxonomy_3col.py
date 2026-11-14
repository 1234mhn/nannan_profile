# -*- coding: utf-8 -*-
"""
第3页：CLIP 用在医学影像上的三个缺陷（严格按综述 §3.1 原文）
三栏：① 多尺度特征 ② 数据稀缺 ③ 专业知识要求高
每栏：缺陷说明 + 改进方向 + 代表模型
所有文字位置按实测高度递推，绝不重叠
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


def th(s, fs, weight="normal", ls=1.6):
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


def P(ax, x, y, s, fs, color, weight="normal", ha="left", va="center",
      avail=None, ls=1.6):
    if avail is not None:
        fs = fit(s, fs, avail, weight)
    return ax.text(x, y, s, fontsize=fs, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=6, linespacing=ls)


W, H = 14.6, 8.2
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.50, "原生 CLIP 用在医学影像上的三个缺陷", 21, NAVY, "bold",
  ha="center", avail=W - 0.9)
P(ax, W / 2, H - 0.95, "后续模型分别从这三个方向改造预训练", 12.0, GRAY,
  ha="center", avail=W - 0.9)

cols = [
    ("01", "多尺度特征", MIST,
     "原生 CLIP 只做「整图对整文」一次对齐。\n但病灶在胸片上可能只占一小块，\n报告也是多句、每句讲一个部位。",
     "改进方向：加局部对齐",
     ["GLoRIA · 词对子区域", "LoVT · 双向局部对齐", "CP-CLIP · 核心对外围", "fVLM · 解剖级对齐"]),
    ("02", "数据稀缺", SLATE,
     "医学图文对受隐私限制，规模远达不到\n自然图像的十亿级；而 CLIP 恰恰是\n数据越少、效果越差的范式。",
     "改进方向：更高效地用好数据",
     ["MedCLIP · 软标签挖假阴性", "MGCA · 疾病级对齐", "CXR-CLIP · 不确定性利用", "BioViL · 报告分段增强"]),
    ("03", "专业知识要求高", SLATE,
     "通用 CLIP 只学到「图上有什么」。\n临床概念有层级与因果关系，\n缺医学知识会掉性能甚至走捷径。",
     "改进方向：显式注入医学知识",
     ["MedKLIP · 实体 + 知识库", "KAD · 知识图谱", "KoBo · 解剖结构", "ARL · 因果实体关系"]),
]

mx, gx = 0.62, 0.62
cw = (W - 2 * mx - 2 * gx) / 3
top = H - 1.42
bot_limit = 1.30

# 统一用最高一栏决定格子高度
TFS, DFS, DIFS, MITFS = 17.0, 11.6, 11.8, 11.4
PAD_T, PAD_B = 0.34, 0.32
GAP_NT, GAP_DD, GAP_DM, GAP_ITEM = 0.26, 0.34, 0.30, 0.40
inner = cw - 0.62

maxh = 0
for num, title, col, desc, direc, items in cols:
    h = (PAD_T + th(title, TFS, "bold") + GAP_NT
         + th(desc, DFS, ls=1.85) + GAP_DD
         + th(direc, DIFS, "bold") + GAP_DM
         + len(items) * GAP_ITEM + PAD_B)
    maxh = max(maxh, h)

ch = min(maxh, top - bot_limit)

for i, (num, title, col, desc, direc, items) in enumerate(cols):
    x = mx + i * (cw + gx)
    y = top - ch

    ax.add_patch(FancyBboxPatch((x, y), cw, ch,
                                boxstyle="round,pad=0,rounding_size=0.14",
                                fc=FOG, ec="none", zorder=1))

    cy = y + ch - PAD_T
    # 标题 + 编号
    P(ax, x + 0.30, cy - th(title, TFS, "bold") / 2, title, TFS, NAVY, "bold",
      va="center", avail=inner)
    P(ax, x + cw - 0.30, cy - th(title, TFS, "bold") / 2, num, 21, PALE, "bold",
      ha="right", va="center")
    cy -= th(title, TFS, "bold") + GAP_NT

    # 缺陷说明
    dfs = min(DFS, fit(desc, DFS, inner))
    dh = th(desc, dfs, ls=1.85)
    P(ax, x + 0.30, cy - dh / 2, desc, dfs, TXT, va="center", avail=inner, ls=1.85)
    cy -= dh + GAP_DD

    # 改进方向
    difs = min(DIFS, fit(direc, DIFS, inner, "bold"))
    P(ax, x + 0.30, cy - th(direc, difs, "bold") / 2, direc, difs, ACCENT, "bold",
      va="center", avail=inner)
    cy -= th(direc, difs, "bold") + GAP_DM

    # 代表模型清单
    for j, it in enumerate(items):
        mfs = min(MITFS, fit(it, MITFS, inner))
        yy = cy - GAP_ITEM * (j + 0.5)
        P(ax, x + 0.30, yy, it, mfs, col, "bold", va="center", avail=inner)

P(ax, W / 2, 0.68,
  "本文对应缺陷 01：把病灶与背景显式拆成「核心 / 外围」两块，分别对齐",
  12.2, ACCENT, "bold", ha="center", avail=W - 1.1)

fig.savefig(f"{OUT}/p3_taxonomy_3col.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print(f"saved ch={ch:.2f}")
