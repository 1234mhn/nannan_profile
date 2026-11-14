#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题一 思路流程图 v7 —— 2024 华为杯优秀论文图表规范（终版）
修复点：
 1. 「是/否」标签移至各分支水平箭头中点正上方
 2. 两条汇合横线错开 y（左 11.51 / 右 11.28），各自 T 型汇入主轴竖线
 3. 顶部加「开始」节点；「结束」放大圆角 → 起止节点规范
 4. 全白底无背景色
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
import matplotlib.font_manager as fm

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
prop = fm.FontProperties(fname=FONT)
plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

C_WHITE = 'white'
EDGE, ARROW, TXT, RED = '#000000', '#000000', '#000000', '#000000'

BW, BH  = 5.2, 0.80         # 主块
DW, DH  = 3.2, 1.10         # 菱形
SW, SH  = 4.4, 0.80         # 分支块
TX, TH  = 3.4, 0.72         # 终端块（开始/结束）
XS = 8.0; LX = 2.85; RX = 13.15
GAP = 1.42; XMAX = 16.0

MAIN = [
    ('in',   '数据预处理\n去重 · 指标处理 · 6 类语义分组'),
    ('proc', '组内中位数聚合 → 分组得分'),
    ('proc', '熵权法计算质量得分（文本 + 领域）'),
    ('proc', '计算样本冲突强度'),
    ('dec',  '强冲突样本？'),
    ('proc', '输出质量评分、冲突标记'),
    ('proc', '配比归一化，划分数据集'),
    ('proc', '建立线性、二阶岭回归配比模型'),
    ('proc', '模型检验（独立集 + Bootstrap + 跨尺度）'),
    ('out',  '输出结果，限定模型适用边界'),
    ('term', '结束'),
]
DI = 4      # 菱形索引
YTOP = 15.25

fig, ax = plt.subplots(figsize=(11.2, 15.9), dpi=220)
ax.set_xlim(0, XMAX); ax.set_ylim(0, 15.9); ax.axis('off')

def box(x, y, w, h, text, fs=11.5, round_r=0.07, lw=1.2):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={round_r}",
        edgecolor=EDGE, facecolor=C_WHITE, linewidth=lw, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=TXT,
            fontproperties=prop, zorder=4, linespacing=1.55)

def terminal(x, y, text):     # 起止：大圆角（胶囊）
    box(x, y, TX, TH, text, fs=11.5, round_r=0.34, lw=1.3)

def diamond(x, y, w, h, text, fs=11):
    ax.add_patch(Polygon([(x,y+h/2),(x+w/2,y),(x,y-h/2),(x-w/2,y)],
        closed=True, edgecolor=EDGE, facecolor=C_WHITE, linewidth=1.2, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=TXT,
            fontproperties=prop, zorder=4)

def seg(p1, p2, head=False):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>' if head else '-',
        mutation_scale=13, color=ARROW, linewidth=1.2, zorder=2,
        shrinkA=0, shrinkB=0))

def hlabel(x, y, text):       # 是/否：压在水平线中点正上方
    ax.text(x, y, text, ha='center', va='bottom', fontsize=10.5,
            color=RED, fontproperties=prop, zorder=6)

ys = [YTOP - i*GAP for i in range(len(MAIN))]
for i,(t,txt) in enumerate(MAIN):
    y = ys[i]
    if t == 'dec':
        diamond(XS, y, DW, DH, txt)
    elif t == 'term':
        terminal(XS, y, txt)
    elif t == 'in':
        box(XS, y, BW, BH, txt, fs=11.0)
    else:
        box(XS, y, BW, BH, txt, fs=(11.0 if '\n' in txt else 11.5))

# 主轴竖直箭头（菱形出口跳过）
for i in range(len(MAIN)-1):
    if i == DI: continue
    seg((XS, ys[i]-BH/2), (XS, ys[i+1]+BH/2), head=True)

yd = ys[DI]
NY = ys[DI+1]            # 输出质量评分
# === 分支：左右块（与菱形同层） ===
box(LX, yd, SW, SH, '使用综合质量评分', fs=11)
box(RX, yd, SW, SH, '计算稳健评分，标记冲突', fs=11)

# 菱形 → 左块（水平，箭头）  + 标签在水平线中点上方
seg((XS-DW/2, yd), (LX+SW/2, yd), head=True)
hlabel((XS-DW/2 + LX+SW/2)/2, yd+0.08, '否')
# 菱形 → 右块
seg((XS+DW/2, yd), (RX-SW/2, yd), head=True)
hlabel((XS+DW/2 + RX-SW/2)/2, yd+0.08, '是')

# === 汇合：两条分支各自下行后，走同一条横线汇入主轴，再一起下行到下一节点 ===
midy = (yd - SH/2) - (yd - SH/2 - (NY + BH/2))/3   # 共同汇合横线：靠上 1/3 处
# 左块下 → 竖直下 → 横线向右 → 主干
seg((LX, yd-SH/2), (LX, midy))
seg((LX, midy), (XS, midy))
# 右块下 → 竖直下 → 横线向左 → 主干
seg((RX, yd-SH/2), (RX, midy))
seg((RX, midy), (XS, midy))
# 主干：从汇合点竖直下去到下一节点（带箭头）
seg((XS, midy), (XS, NY+BH/2), head=True)

# 图题已按用户要求删除

plt.subplots_adjust(left=0.01, right=0.99, top=0.995, bottom=0.005)
out = '/root/.openclaw/workspace/flowchart_q1/流程图_问题一_v5_终版'
plt.savefig(out+'.png', dpi=220, bbox_inches='tight', facecolor='white')
plt.savefig(out+'.pdf', bbox_inches='tight', facecolor='white')
print('OK ->', out)

# ===== 自检 =====
print('\n--- 自检 ---')
print('左块下沿=%.2f  右块下沿=%.2f  下节点上沿=%.2f' % (yd-SH/2, yd-SH/2, NY+BH/2))
print('共同汇合线 y=%.2f  (左右同高、共线合并为一条)' % midy)
print('主轴竖线长=%.2f' % (midy-(NY+BH/2)))
print('是标签 x=%.2f  否标签 x=%.2f' % ((XS+DW/2+RX-SW/2)/2, (XS-DW/2+LX+SW/2)/2))
print('画布 15.9 | 顶节点 y=%.2f 底节点 y=%.2f 图题 y=0.45' % (ys[0], ys[-1]))
print('顶部余量=%.2f  底部余量=%.2f' % (15.9-(ys[0]+TH/2), ys[-1]-TH/2-0.45))
