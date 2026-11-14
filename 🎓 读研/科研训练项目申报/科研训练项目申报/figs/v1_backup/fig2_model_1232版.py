"""图2 模型结构与信息流 —— 15cm x 8cm，数据流风格。运行: python3 fig2_model.py"""
from matplotlib.patches import Rectangle, Polygon, Circle
from figstyle import *

W, H = 15.0, 8.0
fig, ax = new_fig(W, H)
CAP = ["Noto Serif CJK SC", "STIXGeneral"]
YM = 3.95                      # 主数据流水平线
SUB = "#404040"

# ================= 上方：输入图像（缩略图）=================
text(ax, 0.25, 7.78, "胸部 X 线图像", size=7.5, ha="left", weight="bold")
ax.add_patch(Rectangle((0.25, 5.75), 4.60, 1.80, fc="none", ec=INK, lw=0.6, ls=(0, (3, 2)), zorder=1))
TH_W, TH_H, TH_Y = 1.05, 1.20, 6.15
for x, seed, les, lab in [(0.45, 1, (0.30, 0.55, 0.06), r"$x_1$"), (1.75, 2, None, r"$x_2$"),
                          (3.55, 3, (0.70, 0.40, 0.06), r"$x_N$")]:
    thumb(ax, x, TH_Y, TH_W, TH_H, seed=seed, lesion=les)
    text(ax, x + TH_W / 2, 5.95, lab, size=7)
text(ax, 3.10, TH_Y + TH_H / 2, "···", size=9)
for fx, fy in [(0.17, 0.42), (0.57, 0.25)]:     # 区域框：示意 v_j 的来源区域
    ax.add_patch(Rectangle((0.45 + fx * TH_W, TH_Y + fy * TH_H), 0.26 * TH_W, 0.26 * TH_H,
                           fc="none", ec=WHITE, lw=0.7, ls=(0, (2, 1.5)), zorder=5))

# ================= 左：图像支路 =================
XE = 2.55
line(ax, [(XE, 5.75), (XE, YM)])
arrow(ax, [(XE, YM), (3.00, YM)], head=0.2)
ax.add_patch(Polygon([(3.00, YM + 0.50), (4.15, YM + 0.25), (4.15, YM - 0.25), (3.00, YM - 0.50)],
                     closed=True, fc=PALE, ec=INK, lw=0.8, zorder=3))
text(ax, 3.58, YM - 0.80, "视觉主干", size=7)
arrow(ax, [(4.15, YM), (4.85, YM)], head=0.2)

# ================= 中：匹配矩阵 S (J x K) =================
MX0, MTOP, CW, CH, J, K = 5.60, 5.00, 0.55, 0.42, 5, 4
MBOT, MR = MTOP - J * CH, MX0 + K * CW
hot = {(0, 1): 1.0, (2, 0): 1.0, (3, 3): 1.0, (1, 1): 0.30, (2, 1): 0.22, (3, 2): 0.30, (4, 2): 0.18, (0, 2): 0.15}
for r in range(J):
    for c in range(K):
        ax.add_patch(Rectangle((MX0 + c * CW, MTOP - (r + 1) * CH), CW, CH, fc=WHITE, ec=LGRAY, lw=0.4, zorder=3))
        if (r, c) in hot:
            ax.add_patch(Rectangle((MX0 + c * CW, MTOP - (r + 1) * CH), CW, CH, fc=BLUE, ec="none",
                                   alpha=hot[(r, c)], zorder=4))
ax.add_patch(Rectangle((MX0, MBOT), K * CW, J * CH, fc="none", ec=INK, lw=0.9, zorder=5))
mtext(ax, MX0, 2.68, r"匹配矩阵 $S$", size=7, ha="left")

# v_j 竖条（行）与 t_k 横条（列）
VX = 4.85
for r in range(J):
    ax.add_patch(Rectangle((VX, MTOP - (r + 1) * CH), 0.45, CH, fc=PALE, ec=INK, lw=0.5, zorder=3))
arrow(ax, [(VX + 0.45, YM), (MX0 - 0.02, YM)], head=0.18)
text(ax, VX + 0.45, 5.24, r"$v_j$ · $J\times d$", size=7, ha="right")
TY = 5.35
for c in range(K):
    ax.add_patch(Rectangle((MX0 + c * CW, TY), CW, 0.38, fc=PALE, ec=INK, lw=0.5, zorder=3))
XC = MX0 + K * CW / 2
arrow(ax, [(XC, TY), (XC, MTOP + 0.02)], head=0.18)
text(ax, MR + 0.12, TY + 0.19, r"$t_k$ · $K\times d$", size=7, ha="left")

# ================= 上中：影像报告 → LLM 解析 → t_k =================
text(ax, 5.10, 7.78, "影像报告", size=7.5, ha="left", weight="bold")
box(ax, 5.10, 6.55, 4.25, 1.00, fc=WHITE, lw=0.6)
for i, s in enumerate(["There is a small left pleural effusion",
                       "with adjacent atelectasis.",
                       "No pneumothorax. Heart size is normal."]):
    text(ax, 5.22, 7.30 - i * 0.26, s, size=6.5, ha="left", style="italic")
arrow(ax, [(XC, 6.55), (XC, TY + 0.38 + 0.02)], head=0.18)
text(ax, XC + 0.15, 6.12, "LLM 解析", size=6.5, ha="left")

# ================= 右：关系图 G=(V,E) → AGG → 层次化分类头 =================
arrow(ax, [(MR + 0.02, YM), (8.55, YM)], head=0.18)
text(ax, 8.17, YM + 0.20, "构图", size=6.5)
nodes = {1: (9.00, 4.75), 2: (10.20, 4.80), 3: (9.60, 4.15), 4: (8.95, 3.45), 5: (10.35, 3.80), 6: (9.80, 3.20)}
for a, b in [(1, 3), (3, 2), (3, 4), (3, 5), (2, 5)]:
    line(ax, [nodes[a], nodes[b]], lw=0.8, z=3)
for a, b in [(1, 2), (4, 6), (6, 5), (3, 6)]:
    line(ax, [nodes[a], nodes[b]], lw=0.7, ls=(0, (3, 2)), z=3)
for k, (x, y) in nodes.items():
    ax.add_patch(Circle((x, y), 0.13, fc=BLUE if k in (1, 3, 5) else WHITE, ec=INK, lw=0.8, zorder=4))
mtext(ax, 9.65, 5.17, r"关系图 $G=(V,E)$", size=7)
arrow(ax, [(10.85, YM), (11.25, YM)], head=0.18)
box(ax, 11.25, YM - 0.22, 0.70, 0.44, fc=WHITE, lw=0.8, z=3)
text(ax, 11.60, YM, "AGG", size=7)
text(ax, 11.60, YM + 0.50, "图聚合", size=6.5)

HX, HW_, BUS = 12.35, 2.10, 12.20
text(ax, HX, 5.02, "层次化分类头", size=7, ha="left")
levels = [(4.50, "病灶层"), (3.75, "器官层"), (3.00, "全局层")]
line(ax, [(BUS, 4.50), (BUS, 3.00)])
line(ax, [(11.95, YM), (BUS, YM)])
for y, s in levels:
    box(ax, HX, y - 0.21, HW_, 0.42, fc=PALE, lw=0.8, z=3)
    text(ax, HX + HW_ / 2, y, s, size=7)
    arrow(ax, [(BUS, y), (HX - 0.01, y)], head=0.15)
for (ya, _), (yb, _) in zip(levels[:-1], levels[1:]):
    arrow(ax, [(HX + HW_ / 2, ya - 0.21), (HX + HW_ / 2, yb + 0.22)], head=0.13, lw=0.7)

# ================= 右上：输出（预测 + 可回溯证据）=================
text(ax, 10.20, 7.78, "预测与可回溯证据", size=7.5, ha="left", weight="bold")
box(ax, 10.20, 6.35, 4.50, 1.20, fc=WHITE, lw=0.6)
text(ax, 10.35, 7.22, "疾病类别预测（多标签）", size=7.2, ha="left")
line(ax, [(10.35, 7.02), (14.55, 7.02)], color=GRAY, lw=0.4, ls=(0, (2, 2)))
ax.add_patch(Rectangle((10.33, 6.50), 4.10, 0.34, fc=BLUE, alpha=0.18, ec="none", zorder=3))
text(ax, 10.40, 6.67, "There is a small left pleural effusion …", size=6.8, ha="left", style="italic")
arrow(ax, [(14.15, 4.71), (14.15, 6.35)], head=0.18)
text(ax, 14.28, 5.55, "回溯", size=6.5, ha="left")

# ================= 底部：损失 =================
YF = 1.50
rich(ax, 6.00, YF, [("$L$ = ", INK), (r"$L_{\rm align}$", RED), (" + ", INK), (r"$L_{\rm soft}$", RED),
                    (" + ", INK), (r"$L_{\rm cls}$", RED)], size=10)
mtext(ax, 6.00, 1.02, r"$L_{\rm align}$：区域—语义对比损失　$L_{\rm soft}$：软标签匹配约束　$L_{\rm cls}$：层次化分类损失",
      size=6.3, color=SUB)
arrow(ax, [(7.40, MBOT), (7.40, YF + 0.20)], color=RED, head=0.18, lw=0.7, ls=(0, (3, 2)))
text(ax, 7.52, 2.30, r"$L_{\rm align}$, $L_{\rm soft}$", size=6.5, color=RED, ha="left")
arrow(ax, [(13.40, 2.79), (13.40, YF), (7.90, YF)], color=RED, head=0.18, lw=0.7, ls=(0, (3, 2)))
text(ax, 11.60, YF + 0.16, r"$L_{\rm cls}$", size=6.5, color=RED)

# 符号说明（右下，小字）
for i, s in enumerate(["实线：解剖邻近性　虚线：病理共现性",
                       r"$v_j$：区域特征　$t_k$：语义单元",
                       r"$s_{jk}$：区域 $j$—语义 $k$ 匹配分数"]):
    mtext(ax, 10.55, 1.05 - i * 0.26, s, size=6, ha="left", color=SUB)

text(ax, W / 2, 0.22, "图 2　模型结构与信息流", size=10, family=CAP)

if __name__ == "__main__":
    audit(fig, ax)
    save(fig, "图2-模型结构与信息流")
