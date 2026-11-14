#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题三 思路流程图（加粗大字版）—— 论文流程图标准格式
纯白底 / 全黑线条 / 粗体 / 加粗边框箭头 / 竖版线性 / 无图题
数学符号用 mathtext（STIX）渲染
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'   # 粗体
prop = fm.FontProperties(fname=FONT)
plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'stix'

WHITE='white'; INK='#000000'
BW, BH = 8.6, 1.35          # 主块（加宽加高以容纳大字）
TH = 1.24                    # 终端框高
YTOP = 16.50
GAP = 1.85
CX = BW + 1.0                # 画布宽
CY = YTOP + BH/2 + 0.5

LW, FS, ARROW_LW, MS = 3.0, 13.5, 3.0, 23
XS = CX/2

MAIN = [
    ('term', '输入：问题二广义标度律\n$\\hat{L}(N_B, D_B, Q;\\, p_{\\mathrm{star}})$'),
    ('proc', '成本约束：\n$C_{\\mathrm{train}} + C_{\\mathrm{quality}} + C_{\\mathrm{attn}} \\leq C$'),
    ('proc', '联合优化求解：\nSLSQP 多初值 + 对数网格交叉验证'),
    ('proc', '最优解稳定性检验'),
    ('proc', 'KKT 条件解析与数值验证'),
    ('proc', '结构转移识别：\nPELT 变点 + 成本份额变化 + 活跃集跃迁'),
    ('proc', '上下文长度与成本函数敏感性分析'),
    ('proc', '输出：\n最优资源配置与结构性转移结论'),
    ('term', '结束'),
]

fig, ax = plt.subplots(figsize=(CX*0.95, CY*0.95), dpi=220)
ax.set_xlim(0, CX); ax.set_ylim(0, CY); ax.axis('off')

def hh(t): return TH/2 if t=='term' else BH/2

def box(x, y, w, h, text, fs=FS, round_r=0.07, lw=LW):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={round_r}",
        edgecolor=INK, facecolor=WHITE, linewidth=lw, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=INK,
            fontproperties=prop, zorder=4, linespacing=1.6,
            math_fontfamily='stix')

def terminal(x, y, text, fs=FS):
    box(x, y, BW, TH, text, fs=fs, round_r=0.30, lw=LW)

def arrow(p1, p2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>', mutation_scale=MS,
        color=INK, linewidth=ARROW_LW, zorder=2, shrinkA=0, shrinkB=0,
        joinstyle='miter', capstyle='butt'))

ys = [YTOP - i*GAP for i in range(len(MAIN))]
for i,(t,txt) in enumerate(MAIN):
    y = ys[i]
    terminal(XS, y, txt) if t=='term' else box(XS, y, BW, BH, txt)

for i in range(len(MAIN)-1):
    top = ys[i] - hh(MAIN[i][0])
    bot = ys[i+1] + hh(MAIN[i+1][0])
    arrow((XS, top), (XS, bot))

plt.subplots_adjust(left=0.004, right=0.996, top=0.996, bottom=0.004)
out = '/root/.openclaw/workspace/flowchart_q1/流程图_问题三_加粗版'
plt.savefig(out+'.png', dpi=220, bbox_inches='tight', facecolor='white', pad_inches=0.05)
plt.savefig(out+'.pdf', bbox_inches='tight', facecolor='white', pad_inches=0.05)
plt.savefig(out+'.svg', bbox_inches='tight', facecolor='white', pad_inches=0.05)
print('OK ->', out)
print('\n--- 自检 ---')
print('线宽=%.1f 箭头=%.1f 箭头头=%.0f 字号=%.1f' % (LW, ARROW_LW, MS, FS))
print('块宽=%.1f 块高=%.2f 净空=%.2f 画布 %.1f x %.1f' % (BW, BH, GAP-BH, CX, CY))
print('顶余量=%.2f 底余量=%.2f' % (CY-(ys[0]+hh(MAIN[0][0])), ys[-1]-hh(MAIN[-1][0])))
