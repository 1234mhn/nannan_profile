"""图 2 模型结构与信息流（2026-11-07 极简重画版）
主线：输入 → 编码 → 对齐 → 关系建模 → 分层分类 → 回溯 → 输出
框少、字少、留白大，浅色系（沿用图 1 淡紫 + 浅蓝/浅绿辅助）
"""
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
if __name__ == "__main__":
    from figstyle import new_fig, xray, audit, save

plt.rcParams["font.family"] = ["Noto Serif CJK SC", "STIXGeneral"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["pdf.fonttype"] = 42

INK = "#1E1E1E"
GREY = "#5A5A5A"
# 配色（浅色系，细描边）
C_PUR_FC, C_PUR_EC = "#E4DFF1", "#A99BD1"   # 主模块（与图1一致）
C_BLU_FC, C_BLU_EC = "#E6EEF8", "#9DBCDE"   # 输入/编码
C_GRN_FC, C_GRN_EC = "#E7F1E9", "#9CC3A6"   # 对齐/关系
C_ORG_FC, C_ORG_EC = "#FBF0E2", "#DCB98A"   # 分类/回溯
NODE_EC = "#7E6FAF"
ARROW = "#8E8E8E"

PT = 0.03528
W, H = 16.0, 8.0


def mt(ax, x, y, s, size=8, ha="center", weight="normal", color=INK, fig=None, R=None, INV=None):
    """中文 + $公式$ 混排，基线对齐。"""
    parts = [p for p in re.split(r"(\$[^$]*\$)", s) if p]
    yb = y - 0.34 * size * PT
    objs, ws = [], []
    for p in parts:
        t = ax.text(0, yb, p, fontsize=size, color=color, ha="left", va="baseline",
                    fontweight=weight, zorder=6)
        (a, _), (b, _) = INV.transform(t.get_window_extent(R).get_points())
        objs.append(t)
        ws.append(b - a)
    total = sum(ws) + 0.04 * max(0, len(ws) - 1)
    cur = {"center": x - total / 2, "right": x - total}.get(ha, x)
    for t, w in zip(objs, ws):
        t.set_x(cur)
        cur += w + 0.04


def build():
    fig, ax = new_fig(W, H)
    R = fig.canvas.get_renderer()
    INV = ax.transData.inverted()

    def box(x, y, w, h, fc, ec, lw=1.0, r=0.10):
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle=f"round,pad=0,rounding_size={r}",
                                    fc=fc, ec=ec, lw=lw, zorder=2))

    def arr(p0, p1, lw=1.1, head=0.22):
        ax.annotate("", xy=p1, xytext=p0,
                    arrowprops=dict(arrowstyle=f"-|>,head_width={head*0.55},head_length={head*0.8}",
                                    color=ARROW, lw=lw, shrinkA=0, shrinkB=0),
                    zorder=4)

    # ---------- 行 1：输入 + 编码 ----------
    # 输入缩略图（无框，直接两张小图）
    ax.imshow(xray(seed=3), cmap="gray", vmin=0, vmax=0.85,
              extent=(0.45, 1.55, 6.05, 7.45), aspect="auto", zorder=3)
    ax.add_patch(Rectangle((0.45, 6.05), 1.1, 1.4, fc="none", ec=C_BLU_EC, lw=1.0, zorder=4))
    ax.imshow(xray(seed=1, lesion=(0.65, 0.5, 0.08)), cmap="gray", vmin=0, vmax=0.85,
              extent=(1.15, 2.25, 5.75, 7.15), aspect="auto", zorder=3)
    ax.add_patch(Rectangle((1.15, 5.75), 1.1, 1.4, fc="none", ec=C_BLU_EC, lw=1.0, zorder=4))
    mt(ax, 1.35, 5.35, "胸部X线", size=7.5, color=GREY, fig=fig, R=R, INV=INV)

    box(2.9, 5.85, 2.3, 1.25, C_BLU_FC, C_BLU_EC)
    mt(ax, 4.05, 6.48, "图像编码", size=9.5, weight="bold", fig=fig, R=R, INV=INV)

    box(2.9, 3.55, 2.3, 1.25, C_BLU_FC, C_BLU_EC)
    mt(ax, 4.05, 4.18, "文本编码", size=9.5, weight="bold", fig=fig, R=R, INV=INV)
    mt(ax, 4.05, 3.05, "诊断报告", size=7.5, color=GREY, fig=fig, R=R, INV=INV)

    arr((2.55, 6.50), (2.88, 6.50))
    arr((4.05, 4.82), (4.05, 5.83))
    arr((4.05, 3.50), (4.05, 4.16)) if False else None

    # ---------- 行 2：对齐 ----------
    box(6.0, 4.35, 3.3, 2.5, C_GRN_FC, C_GRN_EC)
    mt(ax, 7.65, 6.55, "细粒度图文对齐", size=10.5, weight="bold", fig=fig, R=R, INV=INV)
    mt(ax, 7.65, 5.95, "区域—语义匹配", size=8.5, color=GREY, fig=fig, R=R, INV=INV)
    mt(ax, 7.65, 5.45, "软标签", size=8.5, color=GREY, fig=fig, R=R, INV=INV)
    mt(ax, 7.65, 4.90, "对比损失", size=8.5, color=GREY, fig=fig, R=R, INV=INV)
    arr((5.22, 6.50), (5.98, 6.10))
    arr((5.22, 4.18), (5.62, 4.18))
    arr((5.62, 4.18), (5.62, 5.55))
    arr((5.62, 5.55), (5.98, 5.55))

    # ---------- 行 3：关系图 ----------
    box(9.95, 4.35, 3.3, 2.5, C_GRN_FC, C_GRN_EC)
    mt(ax, 11.6, 6.55, "匹配关系图", size=10.5, weight="bold", fig=fig, R=R, INV=INV)
    # 小关系图示意
    nodes = [(10.85, 5.75), (11.30, 6.02), (11.45, 5.55),
             (11.10, 5.28), (11.75, 5.80), (11.95, 5.35)]
    edges = [(0, 1), (1, 2), (0, 3), (2, 4), (3, 4), (3, 5), (4, 5), (2, 3)]
    for a, b in edges:
        ax.plot([nodes[a][0], nodes[b][0]], [nodes[a][1], nodes[b][1]],
                color="#A8C4D6", lw=0.9, zorder=3)
    for (nx, ny) in nodes:
        ax.add_patch(Circle((nx, ny), 0.085, fc="#FFFFFF", ec=NODE_EC, lw=1.1, zorder=4))
    mt(ax, 12.55, 5.70, "解剖邻近", size=8, color=GREY, fig=fig, R=R, INV=INV)
    mt(ax, 12.55, 5.10, "病理共现", size=8, color=GREY, fig=fig, R=R, INV=INV)
    mt(ax, 11.6, 4.72, "结构一致性损失", size=8, color=GREY, fig=fig, R=R, INV=INV)
    arr((9.32, 5.60), (9.93, 5.60))

    # ---------- 行 4：分层分类 ----------
    box(13.55, 4.35, 2.2, 2.5, C_ORG_FC, C_ORG_EC)
    mt(ax, 14.65, 6.55, "分层分类", size=10.5, weight="bold", fig=fig, R=R, INV=INV)
    for i, name in enumerate(("病灶层", "器官层", "全局层")):
        yy = 6.02 - i * 0.50
        ax.add_patch(FancyBboxPatch((14.15, yy - 0.19), 1.0, 0.38,
                                    boxstyle="round,pad=0,rounding_size=0.06",
                                    fc="#FFFFFF", ec=C_ORG_EC, lw=0.9, zorder=3))
        mt(ax, 14.65, yy, name, size=8.5, fig=fig, R=R, INV=INV)
        if i < 2:
            arr((14.65, yy - 0.20), (14.65, yy - 0.30), lw=0.9, head=0.15)
    mt(ax, 14.65, 4.68, "层次分类损失", size=8, color=GREY, fig=fig, R=R, INV=INV)
    arr((13.27, 5.60), (13.53, 5.60))

    # ---------- 行 5：回溯（下方一条） ----------
    box(6.0, 1.75, 9.75, 1.55, C_ORG_FC, C_ORG_EC)
    mt(ax, 10.88, 2.90, "语义回溯", size=10.5, weight="bold", fig=fig, R=R, INV=INV)
    mt(ax, 10.88, 2.30, "注意力权重：全局层 → 器官层 → 病灶层 → 报告中对应的描述片段",
       size=8.5, color=GREY, fig=fig, R=R, INV=INV)
    arr((14.65, 4.33), (14.65, 3.75))
    arr((14.65, 3.75), (10.88, 3.75))
    arr((10.88, 3.75), (10.88, 3.32))

    # ---------- 总损失（收成窄框） ----------
    box(6.0, 0.35, 9.75, 1.05, C_PUR_FC, C_PUR_EC, lw=1.2)
    mt(ax, 8.2, 0.88, "总损失", size=9.5, weight="bold", fig=fig, R=R, INV=INV)
    mt(ax, 11.2, 0.88, "五项加权求和（详见正文）", size=8.5, color=GREY, fig=fig, R=R, INV=INV)

    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    return fig, ax


if __name__ == "__main__":
    fig, ax = build()
    audit(fig, ax)
    save(fig, "图2-模型结构与信息流")
