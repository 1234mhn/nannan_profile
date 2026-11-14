#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题一 思路流程图 v5 —— 2024 华为杯优秀论文图表规范
布局: 主轴居中竖排; 菱形判断→ 否(左) / 是(右) 两条分支, 再汇合
图题: 图下方, 五号 10.5pt, 宋体+TNR, 不加粗, 居中
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
import matplotlib.font_manager as fm

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
prop = fm.FontProperties(fname=FONT)
plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

C_IN = C_PROC = C_DEC = C_OUT = C_END = 'white'   # 无背景色：全部白底
EDGE, ARROW, TXT, RED = '#37474F','#546E7A','#212121','#B71C1C'

BW, BH = 5.2, 0.80          # 主块宽/高
DW, DH = 3.2, 1.10          # 菱形
SW, SH = 4.4, 0.80          # 分支块
XS = 8.0                    # 主轴中心
LX = 2.85                   # 左分支中心
RX = 13.15                  # 右分支中心
GAP = 1.42
XMAX = 16.0

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
    ('end',  '结束'),
]
DI = 4

fig, ax = plt.subplots(figsize=(11.2, 18.6), dpi=220)
ax.set_xlim(0, XMAX); ax.set_ylim(0, 18.6); ax.axis('off')

def box(x, y, w, h, text, fc, fs=11.5):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.07",
        edgecolor=EDGE, facecolor=fc, linewidth=1.2, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=TXT,
            fontproperties=prop, zorder=4, linespacing=1.55)

def diamond(x, y, w, h, text, fs=11):
    ax.add_patch(Polygon([(x,y+h/2),(x+w/2,y),(x,y-h/2),(x-w/2,y)],
        closed=True, edgecolor=EDGE, facecolor=C_DEC, linewidth=1.2, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=TXT,
            fontproperties=prop, zorder=4)

def arr(p1, p2, style='-|>'):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=13,
        color=ARROW, linewidth=1.2, zorder=2, shrinkA=1, shrinkB=1))

def poly(pts, label=None, lpos=None):
    """折线（多段直线），末端带箭头"""
    for i in range(len(pts)-1):
        last = (i == len(pts)-2)
        arr(pts[i], pts[i+1], '-|>' if last else '-')
    if label and lpos:
        ax.text(lpos[0], lpos[1], label, ha='center', va='center', fontsize=10.5,
                color=RED, fontproperties=prop, zorder=6,
                )

YTOP = 17.90
ys = [YTOP - i*GAP for i in range(len(MAIN))]

for i,(t,txt) in enumerate(MAIN):
    y = ys[i]
    if t=='dec': diamond(XS, y, DW, DH, txt)
    else:
        box(XS, y, BW, BH, txt, {'in':C_IN,'proc':C_PROC,'out':C_OUT,'end':C_END}[t],
            fs=(11.0 if '\n' in txt else 11.5))

# 主轴箭头（菱形出口另画）
for i in range(len(MAIN)-1):
    if i == DI: continue
    arr((XS, ys[i]-BH/2), (XS, ys[i+1]+BH/2))

yd = ys[DI]
# ── 左分支(否) : 菱形左尖 → 左走 → 下行 → 左块 → 再下行 → 回到主轴下一节点 ──
poly([(XS-DW/2-0.04, yd), (LX, yd), (LX, yd), (LX, yd)], None)   # 水平到左
box(LX, yd, SW, SH, '使用综合质量评分', C_PROC, fs=11)
#   左块下 → 需回主轴 (ys[DI+1])：先下到中线，再右折
midy = (yd - SH/2 + ys[DI+1] + BH/2) / 2   # 汇合中线：介于分支块下沿与下一节点上沿之间
poly([(LX, yd-SH/2), (LX, midy), (XS, midy)], None)

# ── 右分支(是) : 菱形右尖 → 右走 → 右块 → 下 → 汇合同一点 ──
poly([(XS+DW/2+0.04, yd), (RX, yd)], '是', (XS+DW/2+0.85, yd+0.26))
box(RX, yd, SW, SH, '计算稳健评分，标记冲突', C_PROC, fs=11)
poly([(RX, yd-SH/2), (RX, midy), (XS, midy)], None)

# 汇合点 → 主轴下一节点（统一补一段竖直箭头，确保不断头）
arr((XS, midy), (XS, ys[DI+1]+BH/2))

# "否" 标签
ax.text(XS-DW/2-0.85, yd+0.26, '否', ha='center', va='center', fontsize=10.5,
        color=RED, fontproperties=prop, zorder=6,
        )

# 图题
ax.text(XMAX/2, 0.42, '图 3.1  问题一数据处理与建模总体流程', ha='center', va='center',
        fontsize=10.5, color=TXT, fontproperties=prop)

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
out = '/root/.openclaw/workspace/flowchart_q1/流程图_问题一_v4_无底色'
plt.savefig(out+'.png', dpi=220, bbox_inches='tight', facecolor='white')
plt.savefig(out+'.pdf', bbox_inches='tight', facecolor='white')

print('OK ->', out)
print('主块 x:', XS-BW/2, XS+BW/2, '| 左块 x:', LX-SW/2, LX+SW/2, '| 右块 x:', RX-SW/2, RX+SW/2)
print('左间隙 %.2f  右间隙 %.2f' % ((XS-BW/2)-(LX+SW/2), (RX-SW/2)-(XS+BW/2)))
