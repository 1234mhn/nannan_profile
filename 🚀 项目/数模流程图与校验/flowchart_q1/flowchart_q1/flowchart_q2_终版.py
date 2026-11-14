#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题二 思路流程图 —— 论文流程图标准格式（flowchart-paper-standard）
规范: 纯白底 / 全黑线条文字 / 竖版 / 菱形判断 / 分支同高汇合 / 无图题
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
import matplotlib.font_manager as fm

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
prop = fm.FontProperties(fname=FONT)
plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

WHITE = 'white'
INK = '#000000'

BW, BH  = 5.2, 0.80         # 主块宽/高
DW, DH  = 3.4, 1.10         # 菱形
SW, SH  = 4.6, 0.80         # 分支块
TX, TH  = 3.4, 0.72         # 终端（胶囊）
XS = 8.0; LX = 2.85; RX = 13.15
GAP = 1.42; XMAX = 16.0

MAIN = [
    ('term', '输入：问题一质量评分 S\n与配比模型 f_p(p)'),
    ('proc', '经典 Chinchilla 型标度律稳健拟合'),
    ('proc', '领域配比有效性修正'),
    ('dec',  '配比 p ≈ p_ref ？'),
    ('proc', '构造两种候选质量扩展形式\n（有效数据量式 / 乘性质量式）'),
    ('proc', 'B6 估计新增参数\nAIC/BIC + B7 留出误差择优'),
    ('proc', '分层验证与弹性、质量—参数替代关系计算'),
    ('out',  '输出广义标度律\n与质量—参数替代关系'),
    ('term', '结束'),
]
DI = 3      # 菱形索引
YTOP = 13.15

fig, ax = plt.subplots(figsize=(11.2, 13.7), dpi=220)
ax.set_xlim(0, XMAX); ax.set_ylim(0, 13.7); ax.axis('off')

def box(x, y, w, h, text, fs=11.0, round_r=0.07, lw=1.2):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={round_r}",
        edgecolor=INK, facecolor=WHITE, linewidth=lw, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=INK,
            fontproperties=prop, zorder=4, linespacing=1.6)

def terminal(x, y, text, w=None, fs=11.5):
    box(x, y, w or TX, TH, text, fs=fs, round_r=0.34, lw=1.3)

def diamond(x, y, w, h, text, fs=10.5):
    ax.add_patch(Polygon([(x,y+h/2),(x+w/2,y),(x,y-h/2),(x-w/2,y)],
        closed=True, edgecolor=INK, facecolor=WHITE, linewidth=1.2, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=INK,
            fontproperties=prop, zorder=4)

def seg(p1, p2, head=False):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>' if head else '-',
        mutation_scale=13, color=INK, linewidth=1.2, zorder=2,
        shrinkA=0, shrinkB=0))

def hlabel(x, y, text):
    ax.text(x, y, text, ha='center', va='bottom', fontsize=10.5,
            color=INK, fontproperties=prop, zorder=6)

ys = [YTOP - i*GAP for i in range(len(MAIN))]
for i,(t,txt) in enumerate(MAIN):
    y = ys[i]
    if t == 'dec':
        diamond(XS, y, DW, DH, txt)
    elif t == 'term':
        terminal(XS, y, txt, w=(BW if len(txt) > 8 else TX), fs=(11.0 if len(txt) > 8 else 11.5))
    else:
        box(XS, y, BW, BH, txt, fs=11.0)

for i in range(len(MAIN)-1):
    if i == DI: continue
    seg((XS, ys[i]-BH/2), (XS, ys[i+1]+BH/2), head=True)

yd = ys[DI]; NY = ys[DI+1]

# === 分支（与菱形同层）===
# 右分支（是）：延续问题一配比模型，p_ref 均匀参考配比
box(RX, yd, SW, SH+0.30, '按均匀参考配比取 p_ref\nΔ_p(p) = 0', fs=10.5)
# 左分支（否）：计算 Δ_p
box(LX, yd, SW, SH+0.30, '问题一配比模型 f_p(p)\n计算 Δ_p(p) = f_p(p) − f_p(ref)', fs=10.5)

# 菱形 → 左（否）
seg((XS-DW/2, yd), (LX+SW/2, yd), head=True)
hlabel((XS-DW/2 + LX+SW/2)/2, yd+0.08, '否')
# 菱形 → 右（是）
seg((XS+DW/2, yd), (RX-SW/2, yd), head=True)
hlabel((XS+DW/2 + RX-SW/2)/2, yd+0.08, '是')

# === 汇合：同高横线合并成一个交点，再下行 ===
SH2 = SH + 0.30
midy = (yd - SH2/2) - (yd - SH2/2 - (NY + BH/2))/3
seg((LX, yd-SH2/2), (LX, midy))
seg((LX, midy), (XS, midy))
seg((RX, yd-SH2/2), (RX, midy))
seg((RX, midy), (XS, midy))
seg((XS, midy), (XS, NY+BH/2), head=True)

plt.subplots_adjust(left=0.01, right=0.99, top=0.995, bottom=0.005)
out = '/root/.openclaw/workspace/flowchart_q1/流程图_问题二_终版'
plt.savefig(out+'.png', dpi=220, bbox_inches='tight', facecolor='white')
plt.savefig(out+'.pdf', bbox_inches='tight', facecolor='white')
plt.savefig(out+'.svg', bbox_inches='tight', facecolor='white')
print('OK ->', out)

# ===== 自检 =====
print('\n--- 几何自检 ---')
print('左块 x=[%.2f,%.2f]  右块 x=[%.2f,%.2f]  主块 x=[%.2f,%.2f]' % (
    LX-SW/2, LX+SW/2, RX-SW/2, RX+SW/2, XS-BW/2, XS+BW/2))
print('左间隙=%.2f  右间隙=%.2f' % ((XS-BW/2)-(LX+SW/2), (RX-SW/2)-(XS+BW/2)))
print('分支块下沿=%.2f  下节点上沿=%.2f  汇合线 y=%.2f  汇合竖箭=%.2f' % (
    yd-SH/2, NY+BH/2, midy, midy-(NY+BH/2)))
print('画布 13.7 | 顶节点上沿=%.2f 底节点下沿=%.2f' % (ys[0]+BH/2, ys[-1]-TH/2))
print('顶部余量=%.2f  底部余量=%.2f' % (13.7-(ys[0]+BH/2), ys[-1]-TH/2))
