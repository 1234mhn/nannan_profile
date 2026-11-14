import os
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

OUT = "/root/.openclaw/workspace/figs"

# --- font ---
if not [f for f in fm.fontManager.ttflist if f.name == "Noto Sans CJK SC"]:
    for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
              "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"]:
        if os.path.exists(p):
            fm.fontManager.addfont(p)
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False

DARK = "#243141"
GRAY = "#8b949e"
TXT = "#2b3645"
ORANGE = "#c87d14"
BLUE = "#3d6fa8"
GREEN = "#2e7d5b"
PURPLE = "#8a5cb8"
BRICK = "#c0642f"
YELLOW = "#fff8e1"


def setup(w, h):
    fig = plt.figure(figsize=(w, h), dpi=200, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def rbox(ax, x, y, w, h, fc, ec, lw=1.8, r=0.12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw))


# ================= Fig 1 =================
W, H = 15, 8.8
fig, ax = setup(W, H)
ax.text(W / 2, H - 0.55, "医学影像中的 CLIP：方法演进时间线", ha="center", va="center",
        fontsize=22, fontweight="bold", color=DARK)
ax.text(W / 2, H - 1.08, "核心矛盾：文本是 CLIP 的监督信号，但医学报告太长、太脏、又和图像对不齐",
        ha="center", va="center", fontsize=12.5, color=GRAY)

bx, bw, by, bh = 0.9, W - 1.8, H - 2.05, 0.68
rbox(ax, bx, by, bw, bh, YELLOW, ORANGE, lw=1.6)
ax.text(W / 2, by + bh / 2,
        "起点澄清 —— 医学图文对比学习（ConVIRT，2020.10）与 OpenAI 的 CLIP（2021.01）几乎同期独立提出，\n"
        "并非医学领域照搬 CLIP，两者想到的是同一个思路。",
        ha="center", va="center", fontsize=11.5, color=TXT, linespacing=1.5)

# 按年份分组：同年份的方法放进同一个节点
nodes = [
    ("2020", ["ConVIRT"], "整份报告代表整张图", "起点（早于 CLIP）", ORANGE),
    ("2021", ["GloRIA"], "拆区域，局部也参与对齐", "粒度变细", BLUE),
    ("2022", ["MedCLIP"], "配对不等于真相关，解耦假阴性", "数据质量", BLUE),
    ("2023", ["MedKLIP"], "先抽病名再对齐", "知识注入", BLUE),
    ("2025", ["MedFILIP", "CP-CLIP"], "细粒度实体对齐 / 病变与背景分开对齐", "细粒度 · 空间结构化", GREEN),
    ("2026", ["MG-3D", "Merlin"], "从 2D 到 3D，从小数据到千万级", "当前前沿", GREEN),
]
axis_y = 4.45
ax.add_patch(FancyArrowPatch((0.5, axis_y), (W - 0.4, axis_y), arrowstyle="-|>",
                             mutation_scale=26, lw=3, color="#b8c0cc"))
cw, ch = 3.55, 2.05
n_nodes = len(nodes)
# 等距排布，左右留足边距，卡片之间保持间隙
margin = 0.45
span = W - 2 * margin - cw
xs = [margin + cw / 2 + i * span / (n_nodes - 1) for i in range(n_nodes)]
for i, ((yr, names, desc, tag, col), cx) in enumerate(zip(nodes, xs)):
    up = (i % 2 == 0)
    ax.add_patch(Circle((cx, axis_y), 0.13, fc=col, ec="white", lw=2, zorder=5))
    cy0 = axis_y + 0.55 if up else axis_y - 0.55 - ch
    left = cx - cw / 2
    ax.plot([cx, cx], [axis_y + (0.13 if up else -0.13), cy0 if up else cy0 + ch],
            color=col, lw=1.6, zorder=2)
    rbox(ax, left, cy0, cw, ch, "white", col, lw=2)
    mx = cx
    ax.text(mx, cy0 + ch - 0.34, yr, ha="center", va="center",
            fontsize=16, fontweight="bold", color=col)
    ax.text(mx, cy0 + ch - 0.74, " · ".join(names), ha="center", va="center",
            fontsize=12.5 if len(names) > 1 else 13, fontweight="bold", color=TXT)
    d = "\n".join(textwrap.wrap(desc, 15)) if len(desc) > 16 else desc
    ax.text(mx, cy0 + 0.80, d, ha="center", va="center", fontsize=10.5, color=TXT, linespacing=1.5)
    ax.text(mx, cy0 + 0.26, tag, ha="center", va="center", fontsize=9.5, color=GRAY)

ax.text(W / 2, 1.28, "共同假设：一份报告可以代表整张图。", ha="center", va="center",
        fontsize=13, color=DARK, fontweight="bold")
ax.text(W / 2, 0.88, "每一次进步都是在这个假设上打补丁 —— 看清补丁，才找得到自己的可质疑点。",
        ha="center", va="center", fontsize=13, color=TXT)
ax.text(W / 2, 0.3, "依据：CLIP in Medical Imaging: A Survey · Medical Image Analysis 2025",
        ha="center", va="center", fontsize=9.5, color=GRAY)
fig.savefig(f"{OUT}/clip_evolution_cc.png", dpi=200, facecolor="white")
plt.close(fig)

# ================= Fig 2 =================
W, H = 14.5, 9.2
fig, ax = setup(W, H)
ax.text(W / 2, H - 0.55, "医学 CLIP 的四类问题：后续方法都在补什么", ha="center", va="center",
        fontsize=22, fontweight="bold", color=DARK)
ax.text(W / 2, H - 1.08, "CLIP 解决了「不靠人工标签」；但医学场景带来了新的四个洞",
        ha="center", va="center", fontsize=12.5, color=GRAY)

rbox(ax, 0.6, H - 2.05, W - 1.2, 0.6, "#f1f3f5", "#f1f3f5", lw=0)
ax.text(W / 2, H - 1.75,
        "CLIP 的原始贡献：用「图 + 自然语言」做对比学习，视觉模型摆脱人工标签，可零样本分类。",
        ha="center", va="center", fontsize=11.2, color=TXT)

rows = [
    ("①", "对齐粒度太粗", BLUE,
     "整图压成一个向量、整份报告压成一个向量，对齐一次就完事；\n但一张胸片有多个器官和病灶，报告也讲好几件事。",
     ["GloRIA", "MedFILIP", "CP-CLIP", "MG-3D"]),
    ("②", "文本脏、配对不准", GREEN,
     "医学报告冗长啰嗦、说法不统一，还常有「正常报告配异常图像」\n的假阴性，硬对齐会学到错误关联。",
     ["MedCLIP", "MedKLIP"]),
    ("③", "缺医学先验知识", PURPLE,
     "通用 CLIP 只学到「图上有什么」；\n医学要判断病变、疾病、解剖关系。",
     ["MedKLIP", "MG-3D", "Abn-BLIP"]),
    ("④", "只做 2D、规模上不去", BRICK,
     "CT、MRI 是三维体数据，早期方法只切 2D 片，丢掉空间信息；\n配对数据量也上不去。",
     ["Merlin", "MG-3D", "Abn-BLIP"]),
]
rh, gap = 1.15, 0.22
top = H - 2.45
sq = 0.95
for i, (num, title, col, desc, meth) in enumerate(rows):
    y = top - (i + 1) * rh - i * gap
    rbox(ax, 0.6, y + (rh - sq) / 2, sq, sq, col, col, lw=0, r=0.14)
    ax.text(0.6 + sq / 2, y + rh / 2, num, ha="center", va="center", fontsize=17,
            fontweight="bold", color="white")
    cx0, cwid = 1.75, 7.9
    rbox(ax, cx0, y, cwid, rh, "white", col, lw=1.8)
    ax.text(cx0 + 0.22, y + rh - 0.27, title, ha="left", va="center", fontsize=13.5,
            fontweight="bold", color=col)
    ax.text(cx0 + 0.22, y + 0.37, desc, ha="left", va="center", fontsize=10.2, color=TXT,
            linespacing=1.5)
    mx = cx0 + cwid + 0.3
    ax.text(mx, y + rh - 0.27, "代表方法", ha="left", va="center", fontsize=9.5, color=GRAY)
    ms = " · ".join(meth)
    if len(ms) > 22:
        k = len(meth) // 2
        ms = " · ".join(meth[:k]) + " ·\n" + " · ".join(meth[k:])
    ax.text(mx, y + 0.4, ms, ha="left", va="center", fontsize=11, fontweight="bold",
            color=col, linespacing=1.4)

by = 0.9
rbox(ax, 0.6, by, W - 1.2, 1.05, YELLOW, ORANGE, lw=1.8)
ax.text(0.9, by + 0.74, "你的位置（M3GCD）—— 同时落在 ② 和 ③", ha="left", va="center",
        fontsize=12.5, fontweight="bold", color=ORANGE)
ax.text(0.9, by + 0.32, "用「类别描述」替代原始报告（绕开文本脏），并用软标签建模类别之间的语义关系（注入先验知识）。",
        ha="left", va="center", fontsize=10.8, color=TXT)
ax.text(W / 2, 0.4, "依据：CLIP in Medical Imaging: A Survey · Medical Image Analysis 2025",
        ha="center", va="center", fontsize=9, color=GRAY)
fig.savefig(f"{OUT}/clip_taxonomy_cc.png", dpi=200, facecolor="white")
plt.close(fig)
print("done")
