"""图2 模型结构与信息流 —— 15cm x 8.0cm。运行: python3 fig2_model.py"""
from matplotlib.patches import Circle
from figstyle import *

W, H = 15.0, 8.0
fig, ax = new_fig(W, H)
MATH = "STIXGeneral"


def mbox(x, y, w, h, fc=WHITE, **kw):
    return box(ax, x, y, w, h, fc, lw=1.0, z=2, **kw)


def cx(x, w):
    return x + w / 2


# ================= 三个分组底色 =================
GY0, GY1 = 4.00, 7.90
box(ax, 0.10, GY0, 3.60, GY1 - GY0, BLUE, r=0.15, z=0)
box(ax, 3.90, GY0, 7.20, GY1 - GY0, PURPLE, r=0.15, z=0)
box(ax, 11.30, GY0, 3.60, GY1 - GY0, GREEN, r=0.15, z=0)
for xc, s in [(1.90, "图像支路"), (7.50, "跨模态对齐层"), (13.10, "文本支路")]:
    text(ax, xc, 7.65, s, size=8.5, color=ACCENT, weight="bold")

# ================= 图像支路 =================
mbox(0.55, 6.80, 2.70, 0.50)
text(ax, 1.90, 7.05, "胸部 X 线图像", size=7.5)
mbox(0.55, 5.70, 2.70, 0.80)
text(ax, 1.90, 6.28, "视觉主干", size=8, color=ACCENT, weight="bold")
text(ax, 1.90, 5.95, "ViT / ResNet（中等规模）", size=6.5)
arrow(ax, [(1.90, 6.80), (1.90, 6.50)], head=5)
arrow(ax, [(1.90, 5.70), (1.90, 5.40)], head=5)
vhot = {(r, c): 0.12 + 0.10 * ((r * 3 + c * 5) % 4) for r in range(4) for c in range(4)}
grid(ax, 1.10, 5.30, 0.22, 0.22, 4, 4, hot=vhot)
text(ax, 2.15, 4.86, r"$\{v_1,\dots,v_J\}$", size=7.5, ha="left")
text(ax, 1.54, 4.20, r"$J\times d$", size=7)

# ================= 文本支路 =================
mbox(11.70, 6.80, 2.80, 0.50)
text(ax, 13.10, 7.05, "影像报告", size=7.5)
mbox(11.70, 5.70, 2.80, 0.80)
text(ax, 13.10, 6.28, "LLM 结构化解析", size=8, color=ACCENT, weight="bold")
text(ax, 13.10, 5.95, "提示模板 + 少样本示例", size=6.5)
arrow(ax, [(13.10, 6.80), (13.10, 6.50)], head=5)
arrow(ax, [(13.10, 5.70), (13.10, 5.40)], head=5)
thot = {(r, c): 0.12 + 0.10 * ((r * 5 + c * 3) % 4) for r in range(4) for c in range(4)}
grid(ax, 11.65, 5.30, 0.22, 0.22, 4, 4, hot=thot)
text(ax, 12.70, 5.10, r"$\{t_1,\dots,t_K\}$", size=7.5, ha="left")
text(ax, 12.70, 4.78, r"含 $l_k$ 与 $a_k$", size=7, ha="left")
text(ax, 12.09, 4.20, r"$K\times d$", size=7)

# ================= 对齐层 =================
mbox(4.10, 4.20, 1.10, 0.75)
text(ax, 4.65, 4.74, "投影", size=6.5)
text(ax, 4.65, 4.44, r"$\varphi(\cdot)$", size=9)
mbox(9.80, 4.20, 1.10, 0.75)
text(ax, 10.35, 4.74, "投影", size=6.5)
text(ax, 10.35, 4.44, r"$\psi(\cdot)$", size=9)

PY = 4.575
arrow(ax, [(1.98, PY), (4.10, PY)], head=5)
arrow(ax, [(11.65, PY), (10.90, PY)], head=5)

# 匹配矩阵 S
shot = {(0, 0): .85, (1, 1): .55, (2, 2): .90, (3, 3): .60, (4, 4): .75,
        (1, 0): .25, (0, 2): .25, (3, 2): .30, (2, 4): .30, (4, 3): .20}
grid(ax, 6.75, 6.35, 0.30, 0.30, 5, 5, hot=shot)
arrow(ax, [(5.20, PY), (5.60, PY), (5.60, 5.60), (6.75, 5.60)], head=5)
arrow(ax, [(9.80, PY), (9.40, PY), (9.40, 5.60), (8.25, 5.60)], head=5)
text(ax, 5.50, 5.15, r"$J\times d'$", size=7, ha="right")
text(ax, 9.50, 5.15, r"$K\times d'$", size=7, ha="left")

# 损失 L_align / L_soft
mbox(6.00, 6.85, 3.00, 0.45)
text(ax, 7.50, 7.075, r"$L_{\mathrm{align}}$  +  $L_{\mathrm{soft}}$", size=8)
arrow(ax, [(7.50, 6.38), (7.50, 6.85)], head=5)
text(ax, 7.62, 6.62, "对比 + 软标签", size=6, ha="left", color=ACCENT)

# S -> 关系图
arrow(ax, [(7.50, 4.85), (7.50, 3.30)], head=6)
text(ax, 7.65, 4.50, "匹配矩阵 $S$", size=7, ha="left")
text(ax, 7.65, 4.20, r"$J\times K$", size=7, ha="left")

# ================= 第二行 =================
RY0, RH = 1.00, 2.30
# 构建匹配关系图
mbox(5.40, RY0, 4.20, RH, fc=TEAL)
text(ax, 7.50, 3.02, r"构建匹配关系图 $G=(V,E)$", size=8, color=ACCENT, weight="bold")
nodes = {"a": (5.85, 2.40), "b": (6.75, 2.50), "c": (7.10, 1.80), "d": (6.40, 1.60), "e": (5.80, 1.50)}
solid = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("a", "e")]
dashed = [("a", "d"), ("b", "d")]
for u, v in solid:
    ax.plot(*zip(nodes[u], nodes[v]), color=ACCENT, lw=1.0, zorder=3)
for u, v in dashed:
    ax.plot(*zip(nodes[u], nodes[v]), color=ACCENT, lw=1.0, ls=(0, (3, 2)), zorder=3)
for p in nodes.values():
    ax.add_patch(Circle(p, 0.11, fc=WHITE, ec=ACCENT, lw=1.0, zorder=4))
for y, s in [(2.40, "节点：局部匹配"), (2.05, "实线：解剖邻近性"), (1.70, "虚线：病理共现性")]:
    text(ax, 7.38, y, s, size=7, ha="left")

# 图聚合
arrow(ax, [(9.60, 2.10), (10.00, 2.10)], head=5)
mbox(10.00, RY0, 1.90, RH, fc=TEAL)
text(ax, 10.95, 3.02, "图聚合 AGG", size=8, color=ACCENT, weight="bold")
text(ax, 10.95, 2.50, "聚合邻居信息", size=6.5)
text(ax, 10.95, 2.18, "更新局部表征", size=6.5)
grid(ax, 10.40, 1.85, 0.275, 0.25, 1, 4, hot={(0, 0): .6, (0, 1): .3, (0, 2): .75, (0, 3): .45})
text(ax, 10.95, 1.38, "更新后局部表征", size=6.5)

# 层次分类头
arrow(ax, [(11.90, 2.10), (12.20, 2.10)], head=5)
mbox(12.20, RY0, 2.70, RH, fc=BLUE)
text(ax, 13.55, 3.06, "层次分类头", size=8, color=ACCENT, weight="bold")
text(ax, 13.55, 2.74, r"监督：$L_{\mathrm{cls}}$", size=6.5)
for i, s in enumerate(["病灶层", "器官层", "全局层"]):
    yy = 2.35 - 0.50 * i
    box(ax, 12.75, yy - 0.16, 1.60, 0.32, WHITE, lw=0.8, r=0.06, z=3)
    text(ax, 13.55, yy, s, size=7)
    if i < 2:
        arrow(ax, [(13.55, yy - 0.16), (13.55, yy - 0.34)], head=4, lw=1.0)

# 符号说明
box(ax, 0.10, RY0, 5.00, RH, WHITE, ec=EDGE, lw=0.8, r=0.12, ls=(0, (3, 2)), z=1)
text(ax, 0.30, 3.02, "符号说明", size=8, color=ACCENT, weight="bold", ha="left")
for y, s in [(2.60, r"$v_j$：第 $j$ 个图像区域特征"),
             (2.28, r"$t_k$：第 $k$ 个语义单元，$l_k$ 层级、$a_k$ 属性"),
             (1.96, r"$s_{jk}$：区域 $j$ 与语义单元 $k$ 的匹配分数"),
             (1.64, r"$G=(V,E)$：匹配关系图（$V$ 节点、$E$ 边）"),
             (1.32, r"$\varphi,\ \psi$：投影到共同空间（维度 $d'$）")]:
    text(ax, 0.30, y, s, size=7, ha="left")

# ================= 总损失 =================
box(ax, 0.10, 0.12, 14.80, 0.62, BLUE, lw=1.0, r=0.12, z=1)
text(ax, 7.50, 0.43,
     r"总损失  $L=L_{\mathrm{align}}+L_{\mathrm{soft}}+L_{\mathrm{cls}}$（三项加权求和）",
     size=9, color=ACCENT, weight="bold")

if __name__ == "__main__":
    audit(fig, ax)
    save(fig, "图2-模型结构与信息流")
