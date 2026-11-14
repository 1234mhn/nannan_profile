# -*- coding: utf-8 -*-
"""
泛读文献页：五篇，每篇给"质疑什么 + 核心做法 + 结果"
沿用 p3_taxonomy_clean.py 的配色与工具函数
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch

OUT = "/root/.openclaw/workspace/figs/final9"
os.makedirs(OUT, exist_ok=True)

for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
          "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"]:
    if os.path.exists(p):
        fm.fontManager.addfont(p)
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False

NAVY = "#2C3E50"
SLATE = "#4A6D8C"
MIST = "#8FA5B8"
PALE = "#C5D2DC"
TXT = "#34495E"
GRAY = "#8B99A6"
ACCENT = "#C8873E"
WHITE = "#FFFFFF"

_F = _A = _R = None


def _init():
    global _F, _A, _R
    if _F is None:
        _F, _A = plt.subplots(figsize=(20, 10), dpi=200)
        _A.set_xlim(0, 20)
        _A.set_ylim(0, 10)
        _A.axis("off")
        _F.canvas.draw()
        _R = _F.canvas.get_renderer()


def tw(s, fs, weight="normal"):
    _init()
    t = _A.text(0, 0, s, fontsize=fs, fontweight=weight)
    bb = t.get_window_extent(renderer=_R)
    t.remove()
    return bb.width / 200.0


def th(s, fs, weight="normal", ls=1.6):
    _init()
    t = _A.text(0, 0, s, fontsize=fs, fontweight=weight, linespacing=ls)
    bb = t.get_window_extent(renderer=_R)
    t.remove()
    return bb.height / 200.0


def fit(s, fs, avail, weight="normal"):
    w = tw(s, fs, weight)
    return fs if w <= avail else fs * avail / w * 0.96


def setup(w, h):
    fig = plt.figure(figsize=(w, h), dpi=200, facecolor=WHITE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def P(ax, x, y, s, fs, color, weight="normal", ha="left", va="center",
      avail=None, ls=1.6):
    if avail is not None:
        fs = fit(s, fs, avail, weight)
    return ax.text(x, y, s, fontsize=fs, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=6, linespacing=ls)


W, H = 14.6, 7.6
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.62, "相关泛读文献", 22, NAVY, "bold",
  ha="center", avail=W - 1.6)

# 五条，每条：序号 | 简称 + 出处 | 质疑什么 | 核心做法 | 结果
rows = [
    ("01", "CheXmix", "arXiv 2026.04 ｜ Stanford",
     "架构",
     "两阶段的投影层会扭曲视觉特征，医学影像上看不出细微线索。改为图文 token 早期同序列融合（Chameleon 路线）。",
     "CheXpert 高掩码下 AUROC 比 CheXagent 高 8.6%，报告生成 GREEN 高 45%"),
    ("02", "SSCD", "arXiv 2026.07 ｜ 成均馆大学",
     "前提",
     "跨模态两队列不配对、特征空间不可比，实例级蒸馏失效。改为共享离散码本，比模态无关的分布相似度。",
     "OCT→眼底 macro-F1 64.5→70.2，CT→胸片 73.8→76.3"),
    ("03", "VLM 粒度受控实验", "arXiv 2026.09 ｜ CMU",
     "粒度",
     "固定编码器与数据，只换九个预训练目标，在五个粒度递增的胸片任务上评测。",
     "局部目标胜异常检测，全局目标胜分类；无普遍最优目标"),
    ("04", "CaMCheX", "ML4H 2025 ｜ Bristol",
     "输入单一",
     "现有方法只吃单视角、图级输入，忽略报告时可得的临床结构化信息。改为正侧位双视角编码，再与病史、体征做 transformer 融合。",
     "MIMIC-CXR 与 CXR-LT 2023/2024 基准上均超过此前最好结果"),
    ("05", "MedTrim", "IEEE JBHI 2026",
     "属性",
     "对比学习只把疾病大类分对，位置、大小、严重度这些细粒度属性没抓住。用报告限定词做三元组挖掘。",
     "检索、分类、生成三个下游任务均优于领先对齐方法"),
]

mx = 0.86
row_gap = 0.14
top = H - 1.28
bot = 0.72
rh = (top - bot - row_gap * (len(rows) - 1)) / len(rows)

c_no = 0.62          # 序号列宽
c_name = 2.55        # 简称列宽
c_seg = 0.95         # 质疑列宽
inner_pad = 0.34

BG = ["#F4F7FA", "#F2F6F9", "#F4F7FA", "#F2F6F9", "#F4F7FA"]

x0 = mx
cw_total = W - 2 * mx
x_name = x0 + c_no
x_seg = x_name + c_name
x_desc = x_seg + c_seg
desc_w = W - mx - x_desc - 0.30
# 描述列内部再分：做法 / 结果
res_w = desc_w * 0.44
do_w = desc_w - res_w - 0.40

for i, (num, name, src, seg, do, res) in enumerate(rows):
    yt = top - i * (rh + row_gap)
    yb = yt - rh
    cy = (yt + yb) / 2

    ax.add_patch(FancyBboxPatch((x0, yb), cw_total, rh,
                                boxstyle="round,pad=0,rounding_size=0.14",
                                fc=BG[i], ec="none", zorder=1))

    # 序号
    P(ax, x0 + inner_pad, cy, num, 13.5, PALE, "bold", ha="left")

    # 简称 + 出处
    P(ax, x_name, cy + 0.22, name, 14.5, NAVY, "bold", ha="left",
      avail=c_name - 0.30)
    P(ax, x_name, cy - 0.24, src, 9.4, GRAY, ha="left",
      avail=c_name - 0.20)

    # 质疑什么（关键词）
    P(ax, x_seg + c_seg / 2 - 0.05, cy, seg, 13.0, SLATE, "bold",
      ha="center", avail=c_seg - 0.10)

    # 核心做法
    P(ax, x_desc, cy, do, 10.6, TXT, ha="left", va="center",
      avail=do_w, ls=1.72)

    # 结果
    P(ax, x_desc + do_w + 0.40, cy, res, 10.2, ACCENT, ha="left", va="center",
      avail=res_w, ls=1.72)

# 底部结论行已按用户要求删除

fig.savefig(f"{OUT}/p10_reading5.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print(f"saved rh={rh:.2f} do_w={do_w:.2f} res_w={res_w:.2f}")
