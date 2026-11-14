"""图 2 模型结构与信息流：双支路 → 匹配 → 关系图 → 层次分类/回溯 → 总损失。16cm x 8cm，配色沿用图 1。"""
import re
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from figstyle import new_fig, box, text, arrow, line, audit, save, xray

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
    """中文 + $公式$ 混排，基线对齐。"""
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


def lines(x, y, ss, dy=0.30, **kw):
    for i, s in enumerate(ss):
        mt(x, y - i * dy, s, **kw)


def main_box(x, y, w, h):
    box(ax, x, y, w, h, fc=MID_FC, ec=MID_EC, lw=1.4)


def sub_box(x, y, w, h):
    box(ax, x, y, w, h, fc=SIDE_FC, ec=SIDE_EC, lw=0.6)


def arr(pts, lw=1.4, head=0.2):
    arrow(ax, pts, color="#FFFFFF", lw=lw + 1.6, head=head + 0.07, z=3)
    arrow(ax, pts, color=ARROW, lw=lw, head=head, z=4)


# ============ 总损失条（2026-11-07 去公式版：只留名称，公式在正文）============
main_box(0.2, 0.2, 15.6, 1.45)
mt(8.0, 1.40, "总损失 = 各项损失加权求和（具体形式见正文）", size=8, ha="center")
LEG1 = "区域—语义对比损失    软标签正则项    关系图结构一致性损失"
LEG2 = "层次分类损失    常规正则项"
mt(8.0, 0.90, LEG1, size=7.5, ha="center")
mt(8.0, 0.50, LEG2, size=7.5, ha="center")

# ============ 左：图像支路 / 文本支路 ============
IMG_C, TXT_C = 6.35, 3.3
main_box(0.2, 5.15, 5.2, 2.65)
mt(0.4, 7.58, "图像支路", size=8.5, ha="left", weight="bold")
main_box(0.2, 1.9, 5.2, 3.0)
mt(0.4, 4.68, "文本支路", size=8.5, ha="left", weight="bold")

sub_box(0.32, 5.4, 1.5, 1.9)
for (dx, dy, seed) in ((0.20, 0.22, 3), (0.0, 0.0, 1)):
    x0, y0, w, h = 0.47 + dx, 6.05 + dy, 0.8, 0.95
    ax.imshow(xray(seed=seed, lesion=(0.65, 0.5, 0.08) if seed == 1 else None), cmap="gray",
              vmin=0, vmax=0.85, extent=(x0, x0 + w, y0, y0 + h), aspect="auto", zorder=3)
    ax.add_patch(Rectangle((x0, y0), w, h, fc="none", ec=SIDE_EC, lw=0.5, zorder=4))
for (rx, ry) in ((0.55, 6.15), (0.92, 6.55)):
    ax.add_patch(Rectangle((rx, ry), 0.26, 0.26, fc="none", ec=ARROW, lw=0.8, ls=(0, (2, 1.5)), zorder=5))
mt(1.07, 5.65, "胸部X线图像", size=7)

sub_box(2.0, 5.8, 1.1, 1.1)
lines(2.55, 6.57, ["预训练", "视觉主干"], dy=0.34, size=7.5)
sub_box(3.3, 5.7, 1.3, 1.3)
lines(3.95, 6.75, ["区域特征", r"$v_j$", r"$j=1,\ldots,J$"], dy=0.30, size=7.5)
sub_box(4.8, 6.1, 0.48, 0.5)
mt(5.04, IMG_C, r"$\varphi$", size=9)
arr([(1.82, IMG_C), (2.0, IMG_C)])
arr([(3.1, IMG_C), (3.3, IMG_C)])
arr([(4.61, IMG_C), (4.8, IMG_C)])

sub_box(0.32, 2.8, 1.1, 1.0)
lines(0.87, 3.45, ["原始报告", r"$R_i$"], dy=0.34, size=7.5)
sub_box(1.6, 2.45, 1.4, 1.7)
lines(2.3, 3.78, ["大语言模型", "解析", "（提示模板", "+ 少样本）"], dy=0.32, size=7.5)
sub_box(3.19, 2.15, 1.45, 2.25)
mt(3.915, 4.12, "语义单元 " + r"$t_k$", size=7.5)
mt(3.915, 3.82, r"$k=1,\ldots,K$", size=7.5)
for i, name in enumerate(("全局层", "器官层", "病灶层")):
    yy = 3.0 - i * 0.46
    box(ax, 3.33, yy - 0.2, 1.17, 0.4, fc=MID_FC, ec=MID_EC, lw=0.6)
    mt(3.915, yy, name, size=7.5)
sub_box(4.8, 3.05, 0.48, 0.5)
mt(5.04, TXT_C, r"$\psi$", size=9)
arr([(1.42, TXT_C), (1.6, TXT_C)])
arr([(3.0, TXT_C), (3.19, TXT_C)])
arr([(4.64, TXT_C), (4.8, TXT_C)])

# ============ Z2 匹配 ============
Z2X, Z2W = 5.75, 3.15
Z2C = Z2X + Z2W / 2
main_box(Z2X, 1.9, Z2W, 5.9)
mt(Z2C, 7.55, "细粒度图文对齐", size=8.5, weight="bold")
sub_box(5.9, 5.25, 2.85, 1.6)
mt(Z2C, 6.62, "匹配分数", size=7.5)
mt(Z2C, 6.12, "区域—语义相似度", size=8)
mt(Z2C, 5.55, "（温度系数缩放）", size=7)
sub_box(5.9, 3.3, 2.85, 1.45)
mt(Z2C, 4.5, "软标签机制", size=7.5, weight="bold")
lines(Z2C, 4.18, ["语义相近但表述不同的", "语义单元获部分正样本", "权重，缓解假阴性"], dy=0.28, size=7)
box(ax, Z2C - 1.28, 2.05, 2.56, 0.45, fc=SIDE_FC, ec=SIDE_EC, lw=0.6)
mt(Z2C, 2.275, "对比损失+软标签", size=7.5)
arr([(5.28, IMG_C), (5.9, IMG_C)])
arr([(5.28, TXT_C), (5.62, TXT_C), (5.62, 5.62), (5.9, 5.62)])
arr([(Z2C, 5.25), (Z2C, 4.75)], head=0.16)
arr([(Z2C, 3.3), (Z2C, 2.5)], head=0.16)
arr([(Z2C, 2.05), (Z2C, 1.45)], head=0.16)

# ============ Z3 关系图 ============
Z3X, Z3W = 9.2, 3.2
Z3C = Z3X + Z3W / 2
main_box(Z3X, 1.9, Z3W, 5.9)
mt(Z3C, 7.55, "匹配关系图建模", size=8.5, weight="bold")
sub_box(9.35, 5.4, 2.9, 1.65)
nodes = [(9.58, 6.62), (9.86, 6.82), (10.02, 6.45), (9.76, 6.15), (9.58, 5.8), (10.0, 5.78)]
edges = [(0, 1), (1, 2), (0, 3), (3, 2), (3, 4), (3, 5), (2, 5)]
for a, b in edges:
    line(ax, [nodes[a], nodes[b]], color=SIDE_EC, lw=0.7, z=3)
for (nx, ny) in nodes:
    ax.add_patch(Circle((nx, ny), 0.065, fc=MID_FC, ec=MID_EC, lw=0.8, zorder=4))
lines(10.15, 6.8, ["关系图 " + r"$G=(V,E)$", "节点 " + r"$V$：局部匹配", "边 " + r"$E$：解剖邻近性", "+ 病理共现性"],
      dy=0.30, size=7, ha="left")
sub_box(9.35, 3.15, 2.9, 1.9)
mt(Z3C, 4.82, "图推理：节点更新", size=7.5, weight="bold")
lines(Z3C, 4.40, ["聚合邻接节点的特征，", "更新当前匹配的表示"], dy=0.30, size=7.5)
box(ax, Z3C - 0.98, 2.05, 1.96, 0.45, fc=SIDE_FC, ec=SIDE_EC, lw=0.6)
mt(Z3C, 2.275, "结构一致性损失", size=7.5)
arr([(8.75, 6.05), (9.35, 6.05)])
arr([(Z3C, 5.4), (Z3C, 5.05)], head=0.16)
arr([(Z3C, 3.15), (Z3C, 2.5)], head=0.16)
arr([(Z3C, 2.05), (Z3C, 1.45)], head=0.16)

# ============ Z4 层次分类 / 回溯 ============
Z4X, Z4W = 12.7, 3.1
Z4C = Z4X + Z4W / 2
main_box(Z4X, 1.9, Z4W, 5.9)
mt(Z4C, 7.55, "层次化分类与语义回溯", size=8.5, weight="bold")
sub_box(12.85, 4.35, 2.8, 2.6)
mt(Z4C, 6.72, "层次化分类", size=7.5, weight="bold")
for i, name in enumerate(("病灶层", "器官层", "全局层")):
    yy = 6.35 - i * 0.55
    box(ax, Z4C - 0.65, yy - 0.18, 1.3, 0.36, fc=MID_FC, ec=MID_EC, lw=0.6)
    mt(Z4C, yy, name, size=7.5)
    if i < 2:
        arr([(Z4C, yy - 0.18), (Z4C, yy - 0.37)], lw=1.2, head=0.12)
lines(Z4C, 4.8, ["每级与报告对应层级", "语义单元建立监督"], dy=0.27, size=7)
sub_box(12.85, 2.62, 2.8, 1.35)
mt(Z4C, 3.76, "语义回溯", size=7.5, weight="bold")
lines(Z4C, 3.46, ["注意力权重：全局层", "→ 器官层 → 病灶层 →", "报告中对应的描述片段"], dy=0.28, size=7)
box(ax, Z4C - 0.9, 2.05, 1.8, 0.45, fc=SIDE_FC, ec=SIDE_EC, lw=0.6)
mt(Z4C, 2.275, "层次分类损失", size=7.5)
arr([(12.25, 4.6), (12.55, 4.6), (12.55, 6.3), (12.85, 6.3)])
arr([(Z4C, 4.35), (Z4C, 3.97)], head=0.12)
arr([(Z4C, 2.05), (Z4C, 1.45)], head=0.16)

ax.set_xlim(0, 16)
ax.set_ylim(0, 8)
audit(fig, ax)
save(fig, "图2-模型结构与信息流")
