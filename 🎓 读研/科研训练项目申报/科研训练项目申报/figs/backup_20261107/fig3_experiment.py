"""图 3 实验设计与评价框架：数据集 → 划分 → 内部/外部测试 → 评价指标 → 层级衰减归因 → 调整策略（闭环）。16cm x 8cm，配色沿用图 1/图 2。"""
import re
import matplotlib.pyplot as plt
from figstyle import new_fig, box, arrow, line, audit, save

plt.rcParams["font.family"] = ["Noto Serif CJK SC", "STIXGeneral"]

INK = "#1E1E1E"
SIDE_FC, SIDE_EC = "#FFFFFF", "#4D4D4D"
MID_FC, MID_EC = "#FFFFFF", "#4D4D4D"
ARROW = "#4D4D4D"
PT = 0.03528

fig, ax = new_fig(16, 8)
R = fig.canvas.get_renderer()
INV = ax.transData.inverted()


def mt(x, y, s, size=7.5, ha="center", weight="normal", color=INK):
    parts = [p for p in re.split(r"(\$[^$]*\$)", s) if p]
    yb = y - 0.34 * size * PT
    objs, ws = [], []
    for p in parts:
        t = ax.text(0, yb, p, fontsize=size, color=color, ha="left", va="baseline",
                    fontweight=weight, zorder=5)
        (a, _), (b, _) = INV.transform(t.get_window_extent(R).get_points())
        objs.append(t)
        ws.append(b - a)
    total = sum(ws) + 0.03 * (len(ws) - 1)
    cur = {"center": x - total / 2, "right": x - total}.get(ha, x)
    for t, w in zip(objs, ws):
        t.set_x(cur)
        cur += w + 0.03
    return total


def block(x, yc, ss, dy=0.27, **kw):
    """多行文字，整体以 yc 为竖直中心。"""
    n = len(ss)
    for i, s in enumerate(ss):
        mt(x, yc + (n - 1) * dy / 2 - i * dy, s, **kw)


def main_box(x, y, w, h):
    box(ax, x, y, w, h, fc=MID_FC, ec=MID_EC, lw=1.4)


def sub_box(x, y, w, h):
    box(ax, x, y, w, h, fc=SIDE_FC, ec=SIDE_EC, lw=0.6)


def chip(x, y, w, h):
    box(ax, x, y, w, h, fc=MID_FC, ec=MID_EC, lw=1.2)


def arr(pts, lw=1.4, head=0.2):
    arrow(ax, pts, color="#FFFFFF", lw=lw + 1.6, head=head + 0.07, z=3)
    arrow(ax, pts, color=ARROW, lw=lw, head=head, z=4)


def seg(pts, lw=1.4):
    line(ax, pts, color="#FFFFFF", lw=lw + 1.6, z=3)
    line(ax, pts, color=ARROW, lw=lw, z=4)


TOP, TOP_H = 3.95, 3.85
TITLE_Y = 7.55

# ============ 数据集 ============
AX_, AW = 0.2, 3.75
main_box(AX_, TOP, AW, TOP_H)
mt(AX_ + AW / 2, TITLE_Y, "公开数据集", size=8.5, weight="bold")
DS = [("MIMIC-CXR", "报告结构相对完整", "适合语义解析实验"),
      ("CheXpert", "类别体系清晰", "适合分类"),
      ("NIH ChestX-ray14", "类别体系清晰", "适合分类与跨数据集验证")]
ds_c = []
for i, (n, a, b) in enumerate(DS):
    y0 = 6.25 - i * 1.05
    sub_box(0.35, y0, 3.45, 0.95)
    yc = y0 + 0.475
    ds_c.append(yc)
    mt(AX_ + AW / 2, yc + 0.28, n, size=8, weight="bold")
    mt(AX_ + AW / 2, yc, a, size=7)
    mt(AX_ + AW / 2, yc - 0.27, b, size=7)

# ============ 数据划分 ============
BX, BW = 4.35, 2.45
main_box(BX, TOP, BW, TOP_H)
mt(BX + BW / 2, TITLE_Y, "数据划分", size=8.5, weight="bold")
sub_box(4.5, 4.75, 2.15, 1.9)
chip(4.65, 5.8, 1.85, 0.65)
mt(5.575, 6.125, "训练集", size=8)
chip(4.65, 4.95, 1.85, 0.65)
mt(5.575, 5.275, "验证集", size=8)
# 三个数据集汇入划分
SEG_X = 4.07
seg([(3.8, ds_c[0]), (SEG_X, ds_c[0]), (SEG_X, ds_c[1])])
seg([(3.8, ds_c[2]), (SEG_X, ds_c[2]), (SEG_X, ds_c[1])])
arr([(3.8, ds_c[1]), (4.5, ds_c[1])])

# ============ 测试 ============
CX, CW = 7.3, 2.8
main_box(CX, TOP, CW, TOP_H)
mt(CX + CW / 2, TITLE_Y, "测试", size=8.5, weight="bold")
INT_Y, EXT_Y = 6.5, 4.85
sub_box(7.45, 5.8, 2.5, 1.4)
mt(8.7, INT_Y + 0.2, "内部测试", size=8, weight="bold")
mt(8.7, INT_Y - 0.2, "（同分布）", size=7)
sub_box(7.45, 4.15, 2.5, 1.4)
mt(8.7, EXT_Y + 0.2, "外部测试", size=8, weight="bold")
mt(8.7, EXT_Y - 0.2, "（跨数据集）", size=7)
# 划分分叉：同分布 / 跨数据集
SPLIT_Y = 5.7
seg([(6.65, SPLIT_Y), (7.05, SPLIT_Y), (7.05, EXT_Y)])
arr([(7.05, EXT_Y), (7.45, EXT_Y)])
arr([(7.05, SPLIT_Y), (7.05, INT_Y), (7.45, INT_Y)])

# ============ 评价指标 ============
DX, DW = 10.5, 5.3
main_box(DX, TOP, DW, TOP_H)
mt(DX + DW / 2, TITLE_Y, "评价指标", size=8.5, weight="bold")
EV = [("分类任务", ["各类别的准确率、F1 值、AUC"]),
      ("对齐质量", ["区域—文本匹配的定位精度", "注意力图与报告提及区域的吻合程度"]),
      ("跨数据集", ["跨数据集测试 + 外部数据集测试"])]
DC = DX + DW / 2
ev_c = []
for i, (lab, ls) in enumerate(EV):
    y0 = 6.25 - i * 1.05
    sub_box(10.65, y0, 5.0, 0.95)
    yc = y0 + 0.475
    ev_c.append(yc)
    n = 1 + len(ls)
    dy = 0.3
    ys = [yc + (n - 1) * dy / 2 - k * dy for k in range(n)]
    mt(DC, ys[0], lab, size=8, weight="bold")
    for y, s in zip(ys[1:], ls):
        mt(DC, y, s, size=7)
# 内外测试汇入评价
MG_X = 10.3
seg([(9.95, INT_Y), (MG_X, INT_Y), (MG_X, ev_c[1])])
seg([(9.95, EXT_Y), (MG_X, EXT_Y), (MG_X, ev_c[1])])
arr([(MG_X, ev_c[1]), (10.65, ev_c[1])])

# ============ 层级衰减归因 ============
GX, GW = 7.1, 8.7
main_box(GX, 0.2, GW, 3.25)
mt(GX + 0.2, 3.18, "层级衰减归因", size=8.5, ha="left", weight="bold")
mt(GX + 2.3, 3.18, "（分析衰减在语义层级中的分布）", size=7, ha="left")
ATT = [("病灶层衰减", "视觉识别受成像条件影响较大"),
       ("器官层衰减", "区域定位存在偏差"),
       ("全局层衰减", "可能与类别体系差异有关")]
for i, (lay, why) in enumerate(ATT):
    y0 = 2.12 - i * 0.88
    yc = y0 + 0.39
    sub_box(7.25, y0, 8.4, 0.78)
    chip(7.4, y0 + 0.11, 1.5, 0.56)
    mt(8.15, yc, lay, size=7.5)
    arr([(8.9, yc), (9.35, yc)], lw=1.2, head=0.14)
    mt(9.55, yc, why, size=7.5, ha="left")
# 评价 → 归因
arr([(14.9, ev_c[2] - 0.475), (14.9, 3.0)], head=0.16)

# ============ 据此调整（闭环） ============
JX, JW = 0.2, 6.3
main_box(JX, 0.2, JW, 3.25)
mt(JX + 0.2, 3.18, "据此调整", size=8.5, ha="left", weight="bold")
for x0, name in ((0.4, "对齐策略"), (3.45, "归一化方案")):
    sub_box(x0, 0.95, 2.85, 1.55)
    mt(x0 + 1.425, 1.725, name, size=8)
# 归因 → 调整
arr([(7.1, 1.725), (6.5, 1.725)], head=0.18)
# 闭环：回到训练 / 验证
arr([(5.575, 3.45), (5.575, 4.75)], head=0.18)
mt(5.8, 3.7, "闭环反馈", size=7, ha="left")

ax.set_xlim(0, 16)
ax.set_ylim(0, 8)
audit(fig, ax)
save(fig, "图3-实验设计与评价框架")
