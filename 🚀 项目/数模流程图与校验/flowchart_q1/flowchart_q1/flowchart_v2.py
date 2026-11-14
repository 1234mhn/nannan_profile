#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题一流程图 v2：学术极简风格，真正的流程图
从上到下布局，明确的步骤顺序和分支
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
import matplotlib.font_manager as fm

# 设置中文字体
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['font.size'] = 10

# 配色方案：学术极简（低饱和）
COLOR_INPUT = '#E8EAF6'      # 浅蓝灰（输入）
COLOR_PROCESS = '#F5F5F5'    # 浅灰（处理）
COLOR_DECISION = '#FFF9E6'   # 浅米黄（判断/分支）
COLOR_OUTPUT = '#E8F5E9'     # 浅绿（输出）
COLOR_BORDER = '#37474F'     # 深蓝灰（边框）
COLOR_ARROW = '#546E7A'      # 中蓝灰（箭头）
COLOR_TEXT = '#212121'       # 深灰（文字）

# 创建画布（竖版，3:4比例）
fig, ax = plt.subplots(figsize=(12, 16), dpi=200)
ax.set_xlim(0, 12)
ax.set_ylim(0, 16)
ax.axis('off')

# 辅助函数：绘制矩形框
def draw_box(x, y, w, h, text, color, fontsize=10, fontweight='normal'):
    box = FancyBboxPatch((x-w/2, y-h/2), w, h,
                         boxstyle="round,pad=0.05",
                         edgecolor=COLOR_BORDER,
                         facecolor=color,
                         linewidth=1.2)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center',
            fontsize=fontsize, fontweight=fontweight,
            color=COLOR_TEXT, fontproperties=prop)

# 辅助函数：绘制菱形（判断节点）
def draw_diamond(x, y, w, h, text, fontsize=9):
    vertices = [(x, y+h/2), (x+w/2, y), (x, y-h/2), (x-w/2, y)]
    diamond = Polygon(vertices, closed=True,
                     edgecolor=COLOR_BORDER,
                     facecolor=COLOR_DECISION,
                     linewidth=1.2)
    ax.add_patch(diamond)
    ax.text(x, y, text, ha='center', va='center',
            fontsize=fontsize, color=COLOR_TEXT, fontproperties=prop)

# 辅助函数：绘制箭头
def draw_arrow(x1, y1, x2, y2, label='', label_pos=0.5, label_offset=0.15):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle='->',
                           mutation_scale=20,
                           linewidth=2,
                           color=COLOR_ARROW)
    ax.add_patch(arrow)
    if label:
        mid_x = x1 + (x2 - x1) * label_pos
        mid_y = y1 + (y2 - y1) * label_pos
        ax.text(mid_x + label_offset, mid_y, label,
                fontsize=8, color=COLOR_ARROW,
                fontproperties=prop, ha='left')

# ===== 流程图主体 =====

# 1. 输入数据（顶部）
draw_box(6, 15, 4, 0.6, '输入 A1—A3\n272505条·7领域·22指标', COLOR_INPUT, 10, 'bold')

# 箭头向下
draw_arrow(6, 14.7, 6, 14.2)

# 2. 预处理
draw_box(6, 13.8, 3.5, 0.5, '指标预处理\n方向统一+归一化', COLOR_PROCESS)

# 箭头向下到分叉点
draw_arrow(6, 13.55, 6, 13.0)

# 3. 分叉点（用菱形标记）
draw_diamond(6, 12.5, 1.8, 0.6, '并行\n双路径')

# 左支路 A：质量评分
draw_arrow(6, 12.2, 3.5, 11.5, '路径A')
draw_box(3.5, 11.0, 2.8, 0.5, '六类语义分组\n22指标→6组', COLOR_PROCESS, 9)
draw_arrow(3.5, 10.75, 3.5, 10.3)
draw_box(3.5, 9.9, 2.8, 0.5, '组内中位数聚合', COLOR_PROCESS, 9)
draw_arrow(3.5, 9.65, 3.5, 9.2)
draw_box(3.5, 8.8, 2.8, 0.5, '熵权加权 w(g)', COLOR_PROCESS, 9)
draw_arrow(3.5, 8.55, 3.5, 8.1)
draw_box(3.5, 7.7, 2.8, 0.5, '综合质量 S(s)', COLOR_OUTPUT, 9, 'bold')

# 右支路 B：冲突稳健评分
draw_arrow(6, 12.2, 8.5, 11.5, '路径B')
draw_box(8.5, 11.0, 2.8, 0.5, '同域秩变换\n各领域独立排秩', COLOR_PROCESS, 9)
draw_arrow(8.5, 10.75, 8.5, 10.3)
draw_box(8.5, 9.9, 2.8, 0.5, '冲突强度 c(s)\n跨域秩方差', COLOR_PROCESS, 9)
draw_arrow(8.5, 9.65, 8.5, 9.2)
draw_box(8.5, 8.8, 2.8, 0.5, '90%阈值标记\nc(s)>τ 冲突样本', COLOR_DECISION, 9)
draw_arrow(8.5, 8.55, 8.5, 8.1)
draw_box(8.5, 7.7, 2.8, 0.5, '稳健评分 S*(s)\n加权中位数', COLOR_OUTPUT, 9, 'bold')

# 两路汇合
draw_arrow(3.5, 7.45, 6, 7.0)
draw_arrow(8.5, 7.45, 6, 7.0)

# 4. 质量模块验证
draw_box(6, 6.6, 3.5, 0.5, '质量模块验证\nBootstrap 200次·95%区间', COLOR_PROCESS)

draw_arrow(6, 6.35, 6, 5.9)

# 5. 输出1（子任务一/二完成）
draw_box(6, 5.5, 4.5, 0.6, '输出1：质量评分+冲突标记+稳健评分', COLOR_OUTPUT, 10, 'bold')

# ===== 分隔线（表示进入子任务三） =====
ax.plot([1, 11], [5.0, 5.0], 'k--', linewidth=1, alpha=0.3)
ax.text(6, 4.8, '子任务三：配比建模', ha='center', fontsize=9,
        color='#757575', fontproperties=prop, style='italic')

# 箭头向下
draw_arrow(6, 4.6, 6, 4.2)

# 6. 输入配比数据
draw_box(6, 3.9, 4, 0.5, '输入 A4—A15\n17维配比+验证Loss', COLOR_INPUT, 10, 'bold')

draw_arrow(6, 3.65, 6, 3.2)

# 7. 特征构造
draw_box(6, 2.9, 3.5, 0.5, '单纯形约束\n+特征构造', COLOR_PROCESS)

draw_arrow(6, 2.65, 6, 2.2)

# 8. 模型分叉
draw_diamond(6, 1.8, 1.8, 0.6, '模型\n选择')

# 左支：线性基线
draw_arrow(6, 1.5, 3.5, 1.0, '线性')
draw_box(3.5, 0.6, 2.5, 0.4, '线性岭回归\n基线模型', COLOR_PROCESS, 9)

# 右支：二阶交互
draw_arrow(6, 1.5, 8.5, 1.0, '二阶')
draw_box(8.5, 0.6, 2.5, 0.4, '二阶岭回归\n组合效应', COLOR_PROCESS, 9)

# 两路汇合到训练
draw_arrow(3.5, 0.4, 6, 0.0)
draw_arrow(8.5, 0.4, 6, 0.0)

# 9. 模型训练与选择（绘制在负Y区域，继续向下）
ax.set_ylim(-4, 16)  # 扩展Y轴范围

draw_box(6, -0.5, 3.8, 0.5, '五折交叉验证\nR²/RMSE/配对Bootstrap', COLOR_PROCESS)

draw_arrow(6, -0.75, 6, -1.2)

# 10. 独立验证
draw_box(6, -1.6, 3.8, 0.5, '独立验证\n1M同尺度+1B跨尺度', COLOR_PROCESS)

draw_arrow(6, -1.85, 6, -2.3)

# 11. 输出2
draw_box(6, -2.7, 4.5, 0.6, '输出2：局部配比效应+适用边界', COLOR_OUTPUT, 10, 'bold')

draw_arrow(6, -2.95, 6, -3.4)

# 12. 最终输出（底部）
draw_box(6, -3.8, 5, 0.7, '最终输出\n质量评分+不确定性\n冲突评价+配比效应+边界',
         COLOR_OUTPUT, 10, 'bold')

# 添加标题
ax.text(6, 15.8, '问题一 数据质量评价与建模流程',
        ha='center', fontsize=14, fontweight='bold',
        color=COLOR_TEXT, fontproperties=prop)

# 调整布局
plt.tight_layout()

# 保存
output_dir = '/root/.openclaw/workspace/flowchart_q1'
png_path = f'{output_dir}/流程图_问题一_v2.png'
pdf_path = f'{output_dir}/流程图_问题一_v2.pdf'

plt.savefig(png_path, dpi=200, bbox_inches='tight', facecolor='white')
plt.savefig(pdf_path, bbox_inches='tight', facecolor='white')

print(f"✓ PNG: {png_path}")
print(f"✓ PDF: {pdf_path}")
print("\n布局思路：从上到下主干，双路径并行（质量评分+冲突稳健），")
print("分隔后进入配比建模，模型分叉后汇合，最终输出。")
