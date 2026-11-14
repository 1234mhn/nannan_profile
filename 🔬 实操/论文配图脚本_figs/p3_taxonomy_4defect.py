# -*- coding: utf-8 -*-
"""
第3页：原生 CLIP 在医学影像上的四项固有缺陷（学术表述版）
术语对齐综述与论文：全局-局部语义粒度缺失 / 数据稀缺与假阴性 /
缺乏领域先验知识 / 三维体数据建模缺失
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


W, H = 14.6, 8.3
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.48, "原生 CLIP 在医学影像上的四项固有缺陷", 21, NAVY, "bold",
  ha="center", avail=W - 0.9)
P(ax, W / 2, H - 0.92, "现有方法针对上述缺陷改造预训练范式", 12.0, GRAY,
  ha="center", avail=W - 0.9)

cols = [
    ("01", "语义粒度单一", MIST,
     "仅在全局层级做图文对齐：\n整图压缩为单一向量，\n整份报告压缩为单一向量。",
     "病灶占像素比例极低，\n全局对齐难以捕捉\n区域级诊断线索。",
     ["GLoRIA · 词—子区域语义对齐", "LoVT · 双向局部对比", "CP-CLIP · 核心/外围解耦"]),
    ("02", "数据稀缺与假阴性", SLATE,
     "医学图文对受隐私约束，\n规模与自然图文对相差\n数个量级，难满足\nCLIP 的数据饥渴特性。",
     "语义重叠报告被误判为\n负样本，引入假阴性，\n削弱对比学习信号。",
     ["MedCLIP · 相关性软标签", "MGCA · 疾病级对齐", "CXR-CLIP · 不确定性挖掘"]),
    ("03", "缺乏领域先验知识", SLATE,
     "预训练仅习得表观语义，\n不具备临床概念间的\n层级依赖与因果约束。",
     "面对分布偏移易性能退化，\n甚至收敛至捷径解。",
     ["MedKLIP · 实体+知识库增强", "KAD · 知识图谱注入", "KoBo · 解剖先验约束"]),
    ("04", "三维体数据建模缺失", MIST,
     "预训练语料为二维自然图像，\n缺乏容积数据上的\n时空建模能力。",
     "CT/MRI 仅以 2D 切片输入，\n层间空间连续性丢失。",
     ["MG-3D · 体素级对齐", "Merlin · 3D CT 预训练", "fVLM · 解剖结构级对齐"]),
]

mx, gx = 0.50, 0.44
cw = (W - 2 * mx - 3 * gx) / 4
top = H - 1.38
bot_limit = 1.28

TFS, DFS, CFS, MITFS = 14.8, 10.2, 10.0, 10.0
PAD_T, PAD_B = 0.30, 0.28
GAP_TD, GAP_DC, GAP_CM, GAP_ITEM = 0.24, 0.30, 0.26, 0.14
inner = cw - 0.46

maxh = 0
for num, title, col, desc, cons, items in cols:
    h = (PAD_T + th(title, TFS, "bold") + GAP_TD
         + th(desc, DFS, ls=1.8) + GAP_DC
         + th(cons, CFS, ls=1.8) + GAP_CM
         + len(items) * (th("测", MITFS, ls=1.6) + GAP_ITEM) + PAD_B)
    maxh = max(maxh, h)

ch = min(maxh + 0.28, top - bot_limit)

for i, (num, title, col, desc, cons, items) in enumerate(cols):
    x = mx + i * (cw + gx)
    y = top - ch

    ax.add_patch(FancyBboxPatch((x, y), cw, ch,
                                boxstyle="round,pad=0,rounding_size=0.13",
                                fc=FOG, ec="none", zorder=1))

    cy = y + ch - PAD_T
    P(ax, x + 0.23, cy - th(title, TFS, "bold") / 2, title, TFS, NAVY, "bold",
      va="center", avail=inner)
    P(ax, x + cw - 0.23, cy - th(title, TFS, "bold") / 2, num, 18, PALE, "bold",
      ha="right", va="center")
    cy -= th(title, TFS, "bold") + GAP_TD

    dfs = min(DFS, fit(desc, DFS, inner))
    dh = th(desc, dfs, ls=1.8)
    P(ax, x + 0.23, cy - dh / 2, desc, dfs, TXT, va="center", avail=inner, ls=1.8)
    cy -= dh + GAP_DC

    cfs = min(CFS, fit(cons, CFS, inner))
    chh = th(cons, cfs, ls=1.8)
    P(ax, x + 0.23, cy - chh / 2, cons, cfs, GRAY, va="center", avail=inner, ls=1.8)
    cy -= chh + GAP_CM

    for j, it in enumerate(items):
        mfs = min(MITFS, fit(it, MITFS, inner))
        ih = th("测", mfs, ls=1.6)
        yy = cy - (ih + GAP_ITEM) * (j + 0.5)
        P(ax, x + 0.23, yy, it, mfs, col, "bold", va="center", avail=inner)

P(ax, W / 2, 0.66,
  "本文针对缺陷 01：将病灶与背景解耦为核心 / 外围两支，分别施加对比约束",
  12.0, ACCENT, "bold", ha="center", avail=W - 1.1)

fig.savefig(f"{OUT}/p3_taxonomy_4defect.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print(f"saved ch={ch:.2f}")
