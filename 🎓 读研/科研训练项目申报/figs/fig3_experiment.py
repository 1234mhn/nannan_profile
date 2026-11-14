"""图 3 实验设计与评价框架（2026-11-07 极简重画版）
主线：数据集 → 数据划分 → 内外测试 → 评价指标 → 层级归因 →(虚线反馈) 调整
框少、字少、留白大，浅色系（与图 1/图 2 统一）。16cm x 8cm。
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from figstyle import new_fig, audit, save

plt.rcParams["font.family"] = ["Noto Serif CJK SC", "STIXGeneral"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["pdf.fonttype"] = 42

INK, GREY = "#1E1E1E", "#5A5A5A"
C_BLU_FC, C_BLU_EC = "#E6EEF8", "#9DBCDE"   # 数据
C_GRN_FC, C_GRN_EC = "#E7F1E9", "#9CC3A6"   # 测试/指标
C_ORG_FC, C_ORG_EC = "#FBF0E2", "#DCB98A"   # 归因/调整
C_PUR_FC, C_PUR_EC = "#E4DFF1", "#A99BD1"   # 闭环
ARROW = "#8E8E8E"

W, H = 16.0, 8.0
fig, ax = new_fig(W, H)


def box(x, y, w, h, fc, ec, lw=1.0, r=0.10):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, zorder=2))


def ts(x, y, s, size=9, color=INK, weight="normal", ha="center", ls=1.6):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va="center",
            fontweight=weight, linespacing=ls, zorder=6)


def arr(x0, y0, x1, y1, lw=1.1, head=0.22, dashed=False):
    kw = dict(arrowstyle=f"-|>,head_width={head*0.55},head_length={head*0.8}",
              color=ARROW, lw=lw, shrinkA=0, shrinkB=0)
    if dashed:
        kw["linestyle"] = (0, (4, 2.5))
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=kw, zorder=4)


# ============ 上行主流程：6 个主框 ============
ROW_Y, ROW_H = 4.35, 2.35
CY = ROW_Y + ROW_H / 2

# 五个等宽等距框
GAP, X0 = 0.32, 0.55
WS = [3.35, 2.55, 2.55, 2.55, 2.55]          # 等宽（数据集框文字最长，整体放宽）
xs = [X0]
for _w in WS[:-1]:
    xs.append(xs[-1] + _w + GAP)
cxs = [x + w / 2 for x, w in zip(xs, WS)]

# 1 数据集 / 2 划分 / 3 测试 / 4 指标 / 5 归因（等宽等距）
MDL = [
    ("公开数据集", "MIMIC-CXR·CheXpert\nNIH ChestXray14", C_BLU_FC, C_BLU_EC),
    ("数据划分", "训练 / 验证", C_BLU_FC, C_BLU_EC),
    ("测试", "内部（同分布）\n外部（跨数据集）", C_GRN_FC, C_GRN_EC),
    ("评价指标", "分类与对齐指标\n跨数据集指标", C_GRN_FC, C_GRN_EC),
    ("层级归因", "病灶层\n器官层\n全局层", C_ORG_FC, C_ORG_EC),
]
for i, (title, body, fc, ec) in enumerate(MDL):
    box(xs[i], ROW_Y, WS[i], ROW_H, fc, ec)
    ts(cxs[i], ROW_Y + 1.72, title, size=11, weight="bold")
    _sz = 7.6 if i in (0, 2) else 8.6
    _ys = ROW_Y + 0.80 if i == 4 else ROW_Y + 0.86
    ts(cxs[i], _ys, body, size=_sz, color=GREY, ls=1.45)

# 主流程箭头（统一接到框边）
for i in range(4):
    arr(xs[i] + WS[i] + 0.01, CY, xs[i + 1] - 0.01, CY)

# ============ 下行：调整（闭环） ============
BOX_Y, BOX_H = 1.05, 1.55
box(xs[1], BOX_Y, xs[4] + WS[4] - xs[1], BOX_H, C_PUR_FC, C_PUR_EC, lw=1.2)
ts((xs[1] + xs[4] + WS[4]) / 2, BOX_Y + 0.98, "策略调整", size=11, weight="bold")
ts((xs[1] + xs[4] + WS[4]) / 2, BOX_Y + 0.42, "对齐策略 · 归一化方案", size=8.8, color=GREY)

# 归因 → 调整（实线向下）
arr(cxs[4], ROW_Y - 0.02, cxs[4], BOX_Y + BOX_H + 0.02, lw=1.1)

# 调整 → 数据划分（虚线反馈，闭环）
ax.plot([cxs[1], cxs[1]], [BOX_Y + BOX_H, ROW_Y - 0.02], color=ARROW, lw=1.1, ls=(0, (4, 2.5)), zorder=4)
arr(cxs[1], 3.60, cxs[1], ROW_Y - 0.02, dashed=True)
ts(cxs[1] + 0.35, 3.72, "反馈", size=9, color="#A9762E", ha="left")

ax.set_xlim(0, W)
ax.set_ylim(0, H)
audit(fig, ax)
save(fig, "图3-实验设计与评价框架")
