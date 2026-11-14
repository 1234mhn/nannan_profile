import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib import font_manager as fm

# 中文字体
fp = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fb = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
fm.fontManager.addfont(fp)
name = fm.FontProperties(fname=fp).get_name()
plt.rcParams['font.family'] = name
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(14, 8.2), dpi=170)
ax.set_xlim(0, 14); ax.set_ylim(0, 8.2); ax.axis('off')

C_OLD = '#B8C4D4'; C_OLD_B = '#5A6B85'
C_NEW = '#A8D3B0'; C_NEW_B = '#2E7D5B'
C_BAD = '#D9534F'; C_BG1 = '#F4F6F9'; C_BG2 = '#F0F8F3'

def box(x, y, w, h, text, fc, ec, fs=13, bold=False, tc='#1F2937', r=0.12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.02,rounding_size={r}",
                                fc=fc, ec=ec, lw=2))
    ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=fs,
            fontweight='bold' if bold else 'normal', color=tc, linespacing=1.5)
    return (x, y, w, h)

def arrow(x1, y1, x2, y2, color='#4B5563', lw=2.2, style='-|>', ls='-'):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                 mutation_scale=22, color=color, lw=lw, linestyle=ls,
                                 shrinkA=2, shrinkB=2))

# ============ 背景两块 ============
ax.add_patch(FancyBboxPatch((0.35, 0.45), 6.35, 6.15, boxstyle="round,pad=0.02,rounding_size=0.18",
                            fc=C_BG1, ec=C_OLD_B, lw=2.5, ls='--', alpha=0.95))
ax.text(3.52, 6.15, '之前的方法（主流 / LLaVA 式两段拼）', ha='center', va='center',
        fontsize=16, fontweight='bold', color=C_OLD_B)

ax.add_patch(FancyBboxPatch((7.3, 0.45), 6.35, 6.15, boxstyle="round,pad=0.02,rounding_size=0.18",
                            fc=C_BG2, ec=C_NEW_B, lw=2.5, ls='--', alpha=0.95))
ax.text(10.47, 6.15, '现在的方法（CheXmix / 早期融合）', ha='center', va='center',
        fontsize=16, fontweight='bold', color=C_NEW_B)

# ============ 左：旧方法 ============
# 输入
box(0.75, 4.95, 1.85, 0.72, '胸片图像', '#FFFFFF', C_OLD_B, 13)
# 视觉编码器
box(3.05, 4.9, 1.75, 0.82, '视觉编码器\n(CLIP)', C_OLD, C_OLD_B, 12.5)
arrow(2.62, 5.31, 3.03, 5.31)

# 投影层 - 红色警示
box(5.15, 4.82, 1.35, 0.95, '投影层', '#FADBD8', C_BAD, 14, bold=True, tc='#922B21')
arrow(4.82, 5.31, 5.13, 5.31)

# 破裂符号
ax.text(5.82, 4.42, '⚠', ha='center', va='center', fontsize=26, color=C_BAD)
ax.text(5.82, 4.0, '视觉细节\n被压缩/扭曲', ha='center', va='center', fontsize=11.5,
        color=C_BAD, fontweight='bold', linespacing=1.4)

# 语言模型
box(3.05, 3.15, 1.75, 0.85, '语言模型\n(LLM)', C_OLD, C_OLD_B, 12.5)
arrow(5.82, 4.72, 4.2, 4.05, color=C_BAD, ls=(0,(4,3)))

# 文本输入
box(0.75, 3.2, 1.85, 0.72, '放射报告文本', '#FFFFFF', C_OLD_B, 13)
arrow(2.62, 3.56, 3.03, 3.56)

# 输出
box(0.9, 1.35, 5.1, 0.85, '分类 / 报告生成', '#FFFFFF', C_OLD_B, 14, bold=True)
arrow(3.92, 3.12, 3.45, 2.24)

ax.text(3.52, 0.95, '两套模块 + 中间翻译，信息在“翻译”这一步流失', ha='center', va='center',
        fontsize=12, color='#4A5568', style='italic')

# ============ 右：新方法 ============
box(7.7, 4.95, 1.75, 0.72, '胸片图像', '#FFFFFF', C_NEW_B, 13)
box(7.7, 3.35, 1.75, 0.72, '放射报告文本', '#FFFFFF', C_NEW_B, 13)

# token 化
box(9.85, 4.85, 1.6, 0.92, '图像切成\n1024 个块', C_NEW, C_NEW_B, 11.5)
box(9.85, 3.25, 1.6, 0.92, '文本分成\n词 token', C_NEW, C_NEW_B, 11.5)
arrow(9.47, 5.31, 9.83, 5.31)
arrow(9.47, 3.71, 9.83, 3.71)

# 统一个序列
ax.add_patch(FancyBboxPatch((11.75, 3.35), 1.55, 2.35, boxstyle="round,pad=0.02,rounding_size=0.12",
                            fc='#FFFFFF', ec=C_NEW_B, lw=2.5))
ax.text(12.52, 5.5, '统 一 序 列', ha='center', va='center', fontsize=12, fontweight='bold', color=C_NEW_B)
# 小方块
labels = ['图','图','图','文','文']
for i, lb in enumerate(labels):
    yy = 4.95 - i*0.34
    fc = '#D5EBDC' if lb == '图' else '#FFF3CD'
    ax.add_patch(Rectangle((11.95, yy), 1.15, 0.28, fc=fc, ec=C_NEW_B, lw=1.2))
    ax.text(12.52, yy+0.14, lb, ha='center', va='center', fontsize=10, color='#1F2937')

arrow(11.47, 5.31, 11.73, 5.05)
arrow(11.47, 3.71, 11.73, 3.95)

# 一个模型
box(8.6, 1.95, 2.9, 0.85, '一个 Transformer', C_NEW, C_NEW_B, 13.5, bold=True)
arrow(12.52, 3.33, 11.0, 2.82)

# 输出
box(8.35, 0.72, 3.4, 0.8, '分类 / 报告生成 / 补图', '#FFFFFF', C_NEW_B, 13.5, bold=True)
arrow(10.05, 1.93, 10.05, 1.54)

# 对勾
ax.text(13.0, 2.28, '✓', ha='center', va='center', fontsize=30, color=C_NEW_B, fontweight='bold')
ax.text(13.0, 1.75, '无需\n投影层', ha='center', va='center', fontsize=11, color=C_NEW_B,
        fontweight='bold', linespacing=1.3)

# ============ 底部对比条 ============
ax.add_patch(FancyBboxPatch((0.35, 0.05), 13.3, 0.32, boxstyle="round,pad=0.01,rounding_size=0.08",
                            fc='#2C3E50', ec='#2C3E50'))
ax.text(7.0, 0.21, '核心差别：左图用“翻译”连接两个模块（细节有损）    右图让图像和文本从一开始就是同一种 token（无翻译损耗）',
        ha='center', va='center', fontsize=12.5, color='#FFFFFF', fontweight='bold')

plt.tight_layout(pad=0.3)
out = '/root/.openclaw/workspace/figs/architecture_compare.png'
plt.savefig(out, bbox_inches='tight', facecolor='white')
print('saved', out)
