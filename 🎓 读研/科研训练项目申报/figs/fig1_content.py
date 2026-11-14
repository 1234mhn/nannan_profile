"""图 1 本项目主要研究内容：挑战 ⇒ 研究内容 → 预期结果，三行三列。
   2026-11-07：按图2 定稿风格重做——浅色系、细描边、文字精简、留白加大。16cm x 9.6cm。"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from figstyle import new_fig, audit, save

plt.rcParams["font.family"] = ["Noto Serif CJK SC", "STIXGeneral"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["pdf.fonttype"] = 42

INK, GREY = "#1E1E1E", "#5A5A5A"
C_ORG_FC, C_ORG_EC = "#FBF0E2", "#DCB98A"   # 挑战
C_BLU_FC, C_BLU_EC = "#E6EEF8", "#9DBCDE"   # 研究内容
C_GRN_FC, C_GRN_EC = "#E7F1E9", "#9CC3A6"   # 预期结果
ARROW = "#8E8E8E"

W, H = 16.0, 9.6
fig, ax = new_fig(W, H)

LX, LW = 0.45, 3.9
MX, MW = 5.35, 5.3
RX, RW = 11.55, 4.0
GAP_Y = 0.55
TOP, BOTTOM = 8.85, 0.75
ROW_H = (TOP - BOTTOM - GAP_Y * 2) / 3

rows = [
    ("挑战一", "报告语义冗余\n粒度失配",
     "研究内容 2.1", "报告语义多粒度结构化解析",
     "语义层级可控\n模板与阴性表述可过滤"),
    ("挑战二", "局部匹配关系\n未被显式建模",
     "研究内容 2.2", "细粒度图文对齐与匹配关系图",
     "病灶级匹配表征\n相似征象可消歧"),
    ("挑战三", "分类依据不可追溯\n类别体系扁平",
     "研究内容 2.3", "层次化分类与语义回溯",
     "预测结果可回溯\n层级监督可传递"),
]

def box(x, y, w, h, fc, ec, lw=1.0, r=0.10):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, zorder=2))

def ts(x, y, s, size=9, color=INK, weight="normal", ha="center", ls=1.6):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va="center",
            fontweight=weight, linespacing=ls, zorder=6)

def arr(x0, x1, y, lw=1.1, head=0.22):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle=f"-|>,head_width={head*0.55},head_length={head*0.8}",
                                color=ARROW, lw=lw, shrinkA=0, shrinkB=0), zorder=4)

for i, (ct, cb, mtitle, mbody, ob) in enumerate(rows):
    y = TOP - ROW_H * (i + 1) - GAP_Y * i
    c = y + ROW_H / 2

    box(LX, y, LW, ROW_H, C_ORG_FC, C_ORG_EC)
    ts(LX + LW / 2, c + 0.62, ct, size=11, weight="bold")
    ts(LX + LW / 2, c - 0.18, cb, size=9, color=GREY)

    box(MX, y, MW, ROW_H, C_BLU_FC, C_BLU_EC)
    ts(MX + MW / 2, c + 0.62, mtitle, size=11, weight="bold")
    ts(MX + MW / 2, c - 0.18, mbody, size=9, color=GREY)

    box(RX, y, RW, ROW_H, C_GRN_FC, C_GRN_EC)
    ts(RX + RW / 2, c, ob, size=9, color=GREY)

    arr(LX + LW + 0.14, MX - 0.14, c)
    arr(MX + MW + 0.14, RX - 0.14, c)

audit(fig, ax)
save(fig, "图1-本项目主要研究内容")
