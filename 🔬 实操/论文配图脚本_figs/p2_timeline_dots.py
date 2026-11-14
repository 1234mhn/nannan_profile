# -*- coding: utf-8 -*-
"""
第2页：医学 CLIP 发展时间线
一条水平主线 + 圆点 + 文字（无卡片框）
说明文字自动换行，控制在栏宽内
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyArrowPatch, Circle

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
    return fs if w <= avail else fs * avail / w * 0.97


def wrap(s, fs, avail):
    """按实测宽度折成最多两行，返回行列表"""
    if tw(s, fs) <= avail:
        return [s]
    best, bestd = None, 1e9
    for i in range(1, len(s)):
        a, b = s[:i], s[i:]
        w = max(tw(a, fs), tw(b, fs))
        d = abs(len(a) - len(b))
        if w <= avail and d < bestd:
            best, bestd = [a, b], d
    if best:
        return best
    f = fit(s, fs, avail)
    return [s]


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
                   ha=ha, va=va, zorder=6, linespacing=1.5)


W, H = 14.6, 7.8
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.50, "医学图文对比学习的发展脉络", 20, NAVY, "bold",
  ha="center", avail=W - 0.9)
P(ax, W / 2, H - 0.92,
  "四条路线并行推进：细粒度对齐 · 知识注入 · 数据与规模 · 三维扩展",
  11, GRAY, ha="center", avail=W - 0.9)

axis_y = 3.85
ax.add_patch(FancyArrowPatch((0.55, axis_y), (W - 0.55, axis_y),
                             arrowstyle="-|>", mutation_scale=16,
                             lw=1.6, color=PALE, zorder=1))

nodes = [
    ("2020", "up", [("ConVIRT", "图文对比学习\n首次进入医学影像")], False),
    ("2021", "down", [("GloRIA", "拆出局部区域\n做细粒度对齐")], False),
    ("2022", "up", [("MedCLIP", "解耦假阴性\n改善配对质量"),
                    ("CheXzero · BioViL", "零样本诊断\n通用医学图文模型")], False),
    ("2023", "down", [("MedKLIP · KAD", "抽取病名实体\n注入医学先验")], False),
    ("2025", "up", [("MedFILIP", "实体级解耦\n去报告噪声"),
                    ("CP-CLIP", "核心—外围分解\n分别对齐")], True),
    ("2026", "down", [("MG-3D", "多粒度知识增强\n三维预训练"),
                      ("Merlin", "千万级 CT 数据集\n三维基础模型")], False),
]

N = len(nodes)
x0, x1 = 1.05, W - 1.05
xs = [x0 + i * (x1 - x0) / (N - 1) for i in range(N)]
half_w = (x1 - x0) / (N - 1) / 2 - 0.10
avail = half_w * 1.9   # 两行折行后可用宽度

for (yr, side, items, hi), cx in zip(nodes, xs):
    col = ACCENT if hi else SLATE
    ax.add_patch(Circle((cx, axis_y), 0.16 if hi else 0.12,
                        fc=col, ec=WHITE, lw=2.0, zorder=5))
    if hi:
        ax.add_patch(Circle((cx, axis_y), 0.31, fc="none", ec=ACCENT, lw=1.1,
                            alpha=0.45, zorder=4))
    up = (side == "up")
    yr_y = axis_y + 0.50 if up else axis_y - 0.50
    P(ax, cx, yr_y, yr, 13.5, col, "bold", ha="center")

    # 由内向外：名称 → 说明
    base = axis_y + (1.05 if up else -1.05)
    step = 0.78 if len(items) > 1 else 0.0
    for j, (nm, desc) in enumerate(items):
        ny = base + ((len(items) - 1 - j) * step if up else -j * step)
        P(ax, cx, ny, nm, 11.0, ACCENT if hi else NAVY, "bold",
          ha="center", avail=avail)
        fy = ny + (0.30 if up else -0.30)
        P(ax, cx, fy, desc, 9.0, TXT, ha="center", va="bottom" if up else "top",
          avail=avail)

P(ax, W / 2, 0.92,
  "演进主线：对齐粒度不断变细 —— 整图对整文 → 区域对片段 → 核心对外围",
  11.5, NAVY, "bold", ha="center", avail=W - 1.0)
P(ax, W / 2, 0.45,
  "资料来源：CLIP in Medical Imaging: A Survey, Medical Image Analysis 2025；各方法原始论文",
  8.8, GRAY, ha="center", avail=W - 1.0)

fig.savefig(f"{OUT}/p2_evolution_dots.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
