# -*- coding: utf-8 -*-
"""
公式页（定稿）：放原文 Eq.3（邻接矩阵）+ Eq.5（CP 图指导的前向）
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

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


def main():
    fig, ax = setup()
    cx = W / 2

    P(ax, 0.62, H - 0.62, "核心公式", fs=20, color=NAVY, weight="bold")

    # ============ ① 邻接矩阵 ============
    P(ax, 0.62, 6.05, "①  CP 图的邻接矩阵", fs=14, color=NAVY, weight="bold")

    ax.text(1.55, 5.30, r"$A(i,j)=1$", fontsize=24, color=NAVY,
            ha="left", va="center", zorder=6)
    P(ax, 3.45, 5.30, "若 i, j ∈ core，或 i ∈ core 且 j ∈ peri", fs=13, color=NAVY)

    ax.text(1.55, 4.70, r"$A(i,j)=0$", fontsize=24, color=NAVY,
            ha="left", va="center", zorder=6)
    P(ax, 3.45, 4.70, "若 i, j ∈ peri", fs=13, color=NAVY)

    # 右侧核心比
    ax.text(9.55, 5.30, r"$n=N\times p$", fontsize=15, color=TXT,
            ha="left", va="center", zorder=6)
    P(ax, 11.15, 5.30, "核心节点数", fs=11.5, color=TXT)
    ax.text(9.55, 4.70, r"$m=N\times (1-p)$", fontsize=15, color=TXT,
            ha="left", va="center", zorder=6)
    P(ax, 11.15, 4.70, "外围节点数", fs=11.5, color=TXT)

    P(ax, 0.62, 4.12,
      "核心节点连所有节点，外围节点只连核心；p ∈ (0, 1] 为核心比",
      fs=12, color=ACCENT, ha="left", va="center")

    # 分割线
    ax.plot([0.62, W - 0.62], [3.62, 3.62], color="#E3EAF0", lw=1.0, zorder=2)

    # ============ ② CP 图指导的前向 ============
    P(ax, 0.62, 3.16, "②  CP 图指导的网络前向", fs=14, color=NAVY, weight="bold")

    f2 = r"$Z^{(r+1)}=\sigma^{(r)}\left\{(A\odot W^{(r)})\,Z^{(r)}\right\}$"
    ax.text(cx, 2.10, f2, fontsize=40, color=NAVY,
            ha="center", va="center", zorder=6)

    P(ax, cx, 1.20,
      "用邻接矩阵 A 逐元素乘权重 W，把全连接改成按图连接；这就是本文改动的地方",
      fs=12, color=ACCENT, ha="center", va="center")

    out = os.path.join(OUT, "p11_formula_key.png")
    fig.savefig(out, dpi=200, facecolor=WHITE)
    print("saved", out)


if __name__ == "__main__":
    main()
