"""图 1 本项目主要研究内容：挑战 ⇒ 研究内容 → 效果，四行三列，无表头。16cm x 9.6cm。
   2026-11-06：研究内容由 3 条改为 4 条（补 2.4 跨数据集泛化验证），与新标题口径一致。"""
import matplotlib.pyplot as plt
from figstyle import new_fig, box, text, dbl_arrow, arrow, audit, save

plt.rcParams["font.family"] = ["Noto Serif CJK SC", "STIXGeneral"]

INK, RED = "#1E1E1E", "#C00000"
SIDE_FC, SIDE_EC = "#FCFCFC", "#BFBFBF"
MID_FC, MID_EC = "#E4DFF1", "#C9C1DE"
ARROW = "#B7CCE7"

fig, ax = new_fig(16, 9.6)

LX, LW = 0.3, 4.3
MX, MW = 5.6, 5.6
RX, RW = 12.0, 3.7
ROW_H, GAP, TOP = 1.75, 0.28, 9.0

rows = [
    ("挑战一", "报告语义冗余、\n粒度失配",
     "研究内容 2.1", "基于大语言模型的报告语义\n多粒度结构化解析",
     "三级语义单元明确\n语义层级可控\n模板与阴性表述可过滤"),
    ("挑战二", "局部匹配关系\n未被显式建模",
     "研究内容 2.2", "细粒度图文对齐与\n匹配关系图建模",
     "病灶级匹配表征\n相似征象可消歧\n结构关系可解释"),
    ("挑战三", "分类依据不可追溯、\n类别体系扁平",
     "研究内容 2.3", "层次化分类与语义回溯",
     "可回溯的疾病类别预测\n层级间监督可传递\n长尾叶节点可稳定表征"),
    ("挑战四", "跨数据集条件下\n性能衰减、归因不清",
     "研究内容 2.4", "跨数据集泛化验证",
     "跨中心性能衰减可量化\n衰减层级可归因\n对齐策略可据此调整"),
]

for i, (ct, cb, mt, mb, ob) in enumerate(rows):
    y = TOP - ROW_H * (i + 1) - GAP * i
    c = y + ROW_H / 2

    box(ax, LX, y, LW, ROW_H, fc=SIDE_FC, ec=SIDE_EC, lw=0.6)
    text(ax, LX + LW / 2, c + 0.48, ct, size=8.5, color=RED, weight="bold")
    text(ax, LX + LW / 2, c - 0.22, cb, size=8, color=INK, linespacing=1.5)

    box(ax, MX, y, MW, ROW_H, fc=MID_FC, ec=MID_EC, lw=0.8)
    text(ax, MX + MW / 2, c + 0.48, mt, size=9, color=INK, weight="bold")
    text(ax, MX + MW / 2, c - 0.20, mb, size=8, color=INK, linespacing=1.5)

    box(ax, RX, y, RW, ROW_H, fc=SIDE_FC, ec=SIDE_EC, lw=0.6)
    text(ax, RX + RW / 2, c, ob, size=7.5, color=INK, linespacing=1.7)

    dbl_arrow(ax, LX + LW + 0.12, MX - 0.12, c, gap=0.10, lw=1.6, color=ARROW)
    arrow(ax, [(MX + MW + 0.12, c), (RX - 0.12, c)], color=ARROW, lw=0.9, head=0.2)

audit(fig, ax)
save(fig, "图1-本项目主要研究内容")
