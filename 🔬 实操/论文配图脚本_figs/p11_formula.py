# -*- coding: utf-8 -*-
"""
公式页：CP-CLIP 用到的几条核心公式
- 对比对齐损失（InfoNCE）
- 结构解耦后的两级对齐损失（核心 + 外围加权）
- 加权融合
- 零样本推理
用 matplotlib mathtext 渲染（Noto 缺数学斜体，走 DejaVu 数学字体）
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
plt.rcParams["mathtext.fontset"] = "dejavusans"

NAVY = "#2C3E50"
SLATE = "#4A6D8C"
MIST = "#8FA5B8"
PALE = "#C5D2DC"
FOG1 = "#F4F7FA"
FOG2 = "#F2F6F9"
TXT = "#34495E"
GRAY = "#8B99A6"
ACCENT = "#C8873E"
WHITE = "#FFFFFF"

W, H = 14.6, 7.6


def setup():
    fig, ax = plt.subplots(figsize=(W, H), dpi=200)
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig, ax


def P(ax, x, y, s, fs=11, color=TXT, weight="normal", ha="left", va="center"):
    ax.text(x, y, s, fontsize=fs, color=color, fontweight=weight,
            ha=ha, va=va, zorder=5)


def card(ax, x, y, w, h, fc=FOG1):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0,rounding_size=0.14",
        facecolor=fc, edgecolor="none", zorder=1))


def main():
    fig, ax = setup()

    # 标题
    P(ax, 0.62, H - 0.52, "CP-CLIP 涉及的核心公式", fs=19, color=NAVY, weight="bold")

    top = H - 1.05
    bottom = 0.42
    gap = 0.26
    n = 4
    ch = (top - bottom - gap * (n - 1)) / n   # 每个卡片高度
    cw = W - 1.24
    cx = 0.62

    blocks = [
        # (标签, 公式, 说明, 是否重点)
        ("01", r"$s_{ij} = \frac{z^{(I)}_i \cdot z^{(T)}_j}{\|z^{(I)}_i\| \, \|z^{(T)}_j\| \, / \, \tau}$",
         "图文特征先各自归一化，再点积得到相似度；温度系数 τ 控制分布锐度。", False),
        ("02", r"$\mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N} \log \frac{\exp(s_{ii})}{\sum_{j=1}^{N}\exp(s_{ij})}$",
         "原生 CLIP 的 InfoNCE：整图对整文，只在这一个全局层级做一次对比。", False),
        ("03", r"$\mathcal{L}_{\mathrm{CP}} = \mathcal{L}_{\mathrm{core}}(z^{(I)}_{c}, z^{(T)}_{c}) \;+\; \lambda \cdot \mathcal{L}_{\mathrm{peri}}(z^{(I)}_{p}, z^{(T)}_{p})$",
         "CP-CLIP 的两级对齐：核心图只对核心文、外围图只对外围文，外围项乘权重 λ。", True),
        ("04", r"$f = w_c \cdot z^{(I)}_{c} \;+\; w_p \cdot z^{(I)}_{p}$" + "      " +
               r"$\hat{y} = \arg\max_{k} \; \cos(f, t_k)$",
         "两支按权重加权融合成最终特征，再与各个类别的文本嵌入比余弦相似度，取最大即为零样本预测。", True),
    ]

    for idx, (num, formula, desc, key) in enumerate(blocks):
        y = top - (idx + 1) * ch - idx * gap
        card(ax, cx, y, cw, ch, ("#FBF4EA" if key else (FOG1 if idx % 2 == 0 else FOG2)))
        # 重点：左侧竖条 + 边框
        if key:
            ax.add_patch(FancyBboxPatch(
                (cx, y), cw, ch,
                boxstyle="round,pad=0,rounding_size=0.14",
                facecolor="none", edgecolor=ACCENT, linewidth=1.1, zorder=2))
            ax.add_patch(FancyBboxPatch(
                (cx, y + 0.12), 0.075, ch - 0.24,
                boxstyle="square,pad=0", facecolor=ACCENT, edgecolor="none", zorder=3))
        # 序号
        P(ax, cx + 0.42, y + ch / 2, num, fs=13,
          color=(ACCENT if key else SLATE), weight="bold")
        # 公式（居中偏左）
        ax.text(cx + cw / 2 - 0.6, y + ch * 0.62, formula,
                fontsize=(19 if key else 16), color=(ACCENT if key else NAVY),
                ha="center", va="center", zorder=6)
        # 说明
        P(ax, cx + cw / 2 - 0.6, y + ch * 0.24, desc, fs=(10 if key else 9.4),
          color=(NAVY if key else GRAY), weight=("bold" if key else "normal"),
          ha="center", va="center")
        # 重点标签
        if key:
            P(ax, cx + cw - 0.28, y + ch - 0.24, "重点", fs=9.5,
              color=ACCENT, weight="bold", ha="right")

    out = os.path.join(OUT, "p11_formula.png")
    fig.savefig(out, dpi=200, facecolor=WHITE)
    print("saved", out)


if __name__ == "__main__":
    main()
