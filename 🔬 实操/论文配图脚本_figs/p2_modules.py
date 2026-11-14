# -*- coding: utf-8 -*-
"""
第2页（第二张图）：CLIP 预训练的可改模块 × 各模型的改法
五列模块 · 每格方法 + 一句改法
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

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


def fit(s, fs, avail, weight="normal"):
    w = tw(s, fs, weight)
    return fs if w <= avail else fs * avail / w * 0.97


def setup(w, h):
    fig = plt.figure(figsize=(w, h), dpi=200, facecolor=WHITE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def rbox(ax, x, y, w, h, fc, ec, lw=1.4, r=0.09, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, zorder=z))


def P(ax, x, y, s, fs, color, weight="normal", ha="left", va="center", avail=None):
    if avail is not None:
        fs = fit(s, fs, avail, weight)
    return ax.text(x, y, s, fontsize=fs, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=6, linespacing=1.45)


W, H = 14.6, 7.9
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.46, "CLIP 预训练的五个可改模块与代表方法", 19.5, NAVY, "bold",
  ha="center", avail=W - 0.9)
P(ax, W / 2, H - 0.86,
  "综述把「精化预训练」的方法按改动位置归为五类：对齐粒度 · 正负样本 · 文本处理 · 知识注入 · 视觉编码",
  10.5, GRAY, ha="center", avail=W - 0.9)

cols = [
    ("① 对齐粒度", "整图↔整文 → 更细的对应", [
        ("GLoRIA", "词 ↔ 图像子区域"),
        ("LocalMI", "局部图像 ↔ 整句"),
        ("LoVT", "句 ↔ 切片，双向 + 注意力加权"),
        ("PRIOR", "加跨模态条件重建"),
        ("fVLM", "解剖级：104 个结构分别对齐"),
    ]),
    ("② 正负样本", "谁和谁算一对", [
        ("MedCLIP", "报告间语义相关做软标签"),
        ("MGCA", "疾病级聚类，同病互为正例"),
        ("SAT", "正 / 中 / 负三分，可插拔"),
        ("UMCL", "多热标签构造正负对"),
        ("Jang 2022", "只惩罚真负样本"),
    ]),
    ("③ 文本处理", "报告怎么读、怎么造", [
        ("BioViL", "补印象段 + 句子打乱"),
        ("BioViL-T", "引入前次检查的时间信息"),
        ("CXR-CLIP", "标签生成 prompt"),
        ("MRM", "报告补全 + 掩码重建"),
        ("Müller 2022a", "弃局部对齐，改均匀性损失"),
    ]),
    ("④ 知识注入", "外挂知识编码器", [
        ("ARL", "UMLS 实体关系图 + GAT"),
        ("MedKLIP", "病名三元组 + top-K 实体"),
        ("KAD", "疾病描述查询，识别未见过病"),
        ("KoBo / MOTOR", "知识图区分噪声负样本"),
        ("FLAIR / FetalCLIP", "领域知识提示词"),
    ]),
    ("⑤ 视觉编码", "视觉侧与多任务", [
        ("Merlin", "加诊断码多任务监督"),
        ("EchoPrime", "编码器前加视图分类器"),
        ("TCSA", "多视图专属隐空间再投影"),
        ("M-FLAG", "冻结文本编码器 + 正交损失"),
        ("PeskaVLP", "clip→phase→整段分层对齐"),
    ]),
]

n = len(cols)
x_margin = 0.42
gap = 0.16
colw = (W - 2 * x_margin - gap * (n - 1)) / n
head_h = 0.92
top = H - 1.30
rowh = 0.94

for i, (title, sub, items) in enumerate(cols):
    x = x_margin + i * (colw + gap)
    # 列头
    rbox(ax, x, top - head_h, colw, head_h, SLATE, SLATE, lw=0, r=0.09, z=3)
    P(ax, x + colw / 2, top - 0.30, title, 12.5, WHITE, "bold",
      ha="center", avail=colw - 0.14)
    P(ax, x + colw / 2, top - 0.66, sub, 8.4, "#E8EEF3",
      ha="center", avail=colw - 0.14)

    for j, (nm, how) in enumerate(items):
        y = top - head_h - 0.14 - (j + 1) * rowh - j * 0.06
        rbox(ax, x, y, colw, rowh, WHITE, PALE, lw=1.1, r=0.07, z=2)
        P(ax, x + colw / 2, y + rowh - 0.30, nm, 10.3, NAVY, "bold",
          ha="center", avail=colw - 0.12)
        P(ax, x + colw / 2, y + 0.62, how, 8.3, TXT,
          ha="center", avail=colw - 0.16, va="center")

# 底部：本文定位
by = 0.60
ax.add_patch(FancyBboxPatch((x_margin, by - 0.18), W - 2 * x_margin, 0.46,
                            boxstyle="round,pad=0,rounding_size=0.08",
                            fc="#FBF3E8", ec=ACCENT, lw=1.4, zorder=2))
P(ax, W / 2, by + 0.05,
  "本文工作落在 ① 对齐粒度：CP-CLIP 把「病灶核心 / 背景外围」显式拆开分别对齐；M3GCD 在此基础上衔接 ⑤ 多任务",
  10.8, ACCENT, "bold", ha="center", avail=W - 1.1)

fig.savefig(f"{OUT}/p2_modules.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
