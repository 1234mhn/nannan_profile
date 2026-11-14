#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题四 思路流程图（单栏竖排 · 按用户参考图规格）
规格：单栏竖排 / 普通字重(非粗) / 框为扁长条(宽高比≈6:1) / 框间距≈框高的1/3~1/2 / 无图题
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'   # 普通字重
prop = fm.FontProperties(fname=FONT)
plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

WHITE='white'; INK='#000000'
BW = 9.6                    # 框宽（扁长条）
BH = 1.60                    # 框高 → 宽高比 6:1
TH = 1.50                    # 终端框
YTOP = 18.0
PITCH = 2.40                 # 框中心距 → 框间距 = 2.70-1.80 = 0.90 = 框高的 0.5 ✓
CX = BW + 1.4
LW, FS, ARROW_LW, MS = 1.6, 16.0, 1.6, 18   # 细线 + 大字（按参考图：线较细、字中等偏大）
XS = CX/2
CY = YTOP + BH/2 + 0.7

NODES = [
    ('term', '输入：六项 Benchmark 数据'),
    ('proc', '稳健归一化处理'),
    ('proc', '等权汇总，得到综合能力分数'),
    ('proc', '匹配训练算力与训练数据量'),
    ('proc', '构建模型家族面板'),
    ('proc', '建立面板回归模型'),
    ('proc', '分解规模投入贡献与非规模技术贡献'),
    ('proc', '采用 Shapley 方法进行贡献测算'),
    ('proc', '设定算力增速放缓情景'),
    ('proc', '预测未来能力前沿'),
    ('proc', '通过 Bootstrap 和滚动回测检验可靠性'),
    ('term', '得到结果分析与结论'),
]

fig, ax = plt.subplots(figsize=(CX*0.95, CY*0.95), dpi=220)
ax.set_xlim(0, CX); ax.set_ylim(0, CY); ax.axis('off')

def hh(t): return TH/2 if t=='term' else BH/2

def box(x, y, w, h, text, fs=FS, round_r=0.07, lw=LW):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={round_r}",
        edgecolor=INK, facecolor=WHITE, linewidth=lw, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=INK,
            fontproperties=prop, zorder=4, linespacing=1.5)

def terminal(x, y, text, fs=FS):
    box(x, y, BW, TH, text, fs=fs, round_r=0.28, lw=LW)

def arrow(p1, p2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>', mutation_scale=MS,
        color=INK, linewidth=ARROW_LW, zorder=2, shrinkA=0, shrinkB=0,
        joinstyle='miter', capstyle='butt'))

ys = [YTOP - i*PITCH for i in range(len(NODES))]
for i,(t,txt) in enumerate(NODES):
    y = ys[i]
    terminal(XS, y, txt) if t=='term' else box(XS, y, BW, BH, txt)

for i in range(len(NODES)-1):
    arrow((XS, ys[i]-hh(NODES[i][0])), (XS, ys[i+1]+hh(NODES[i+1][0])))

plt.subplots_adjust(left=0.004, right=0.996, top=0.996, bottom=0.004)
out = '/root/.openclaw/workspace/flowchart_q1/流程图_问题四_单栏版'
plt.savefig(out+'.png', dpi=220, bbox_inches='tight', facecolor='white', pad_inches=0.05)
plt.savefig(out+'.pdf', bbox_inches='tight', facecolor='white', pad_inches=0.05)
plt.savefig(out+'.svg', bbox_inches='tight', facecolor='white', pad_inches=0.05)
print('OK ->', out)
print('\n--- 自检 ---')
print('框 %.1f x %.1f → 宽高比 %.1f:1 (参考图≈6:1)' % (BW, BH, BW/BH))
print('框间距=%.2f = 框高的 %.0f%% (参考图 33~50%%)' % (PITCH-BH, (PITCH-BH)/BH*100))
print('字号=%.1f 线宽=%.1f 字重=普通' % (FS, LW))
print('画布 %.1f x %.1f 比例 %.2f (参考图 0.78)' % (CX, CY, CX/CY))
print('顶余量=%.2f 底余量=%.2f' % (CY-(ys[0]+BH/2), ys[-1]-BH/2))
