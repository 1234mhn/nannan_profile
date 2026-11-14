import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib import font_manager as fm

fp = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(fp)
plt.rcParams['font.family'] = fm.FontProperties(fname=fp).get_name()
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(16.2, 10.4), dpi=165)
ax.set_xlim(0, 16.2)
ax.set_ylim(0, 10.4)
ax.axis('off')

C_OLD = '#C3CFDE'; C_OLD_B = '#4A5F7A'
C_NEW = '#AFD9BA'; C_NEW_B = '#2E7D5B'
C_BAD = '#C0392B'; C_BG1 = '#F5F7FA'; C_BG2 = '#F1F9F4'
C_HOT_B = '#B9770E'; C_BORROW_B = '#4A6FA5'


def box(x, y, w, h, main, sub='', fc='#fff', ec='#333', fs=12.5, fs2=9.6,
        tc='#1F2937', tc2='#5A6572', lw=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.10",
                                fc=fc, ec=ec, lw=lw))
    if sub:
        ax.text(x+w/2, y+h*0.68, main, ha='center', va='center',
                fontsize=fs, fontweight='bold', color=tc)
        ax.text(x+w/2, y+h*0.28, sub, ha='center', va='center',
                fontsize=fs2, color=tc2, style='italic')
    else:
        ax.text(x+w/2, y+h/2, main, ha='center', va='center',
                fontsize=fs, fontweight='bold', color=tc, linespacing=1.45)


def arrow(x1, y1, x2, y2, color='#4B5563', lw=2.3, ls='-'):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
                                 mutation_scale=20, color=color, lw=lw,
                                 linestyle=ls, shrinkA=0, shrinkB=0))


# ===== 两栏背景 =====
ax.add_patch(FancyBboxPatch((0.25, 0.55), 6.55, 9.05,
                            boxstyle="round,pad=0.02,rounding_size=0.18",
                            fc=C_BG1, ec=C_OLD_B, lw=2.5, ls='--'))
ax.add_patch(FancyBboxPatch((7.10, 0.55), 8.85, 9.05,
                            boxstyle="round,pad=0.02,rounding_size=0.18",
                            fc=C_BG2, ec=C_NEW_B, lw=2.5, ls='--'))
ax.text(3.52, 10.12, '【旧】主流 LLaVA 式：两段拼接', ha='center', va='center',
        fontsize=15.5, fontweight='bold', color=C_OLD_B)
ax.text(11.52, 10.12, '【新】CheXmix：早期融合 + 两阶段训练', ha='center', va='center',
        fontsize=15.5, fontweight='bold', color=C_NEW_B)

# ==================== 左：旧方法 ====================
box(0.50, 8.40, 1.85, 0.82, '胸片图像', '', fs=12.5)
box(2.80, 8.33, 1.95, 0.96, '看图专家', '（视觉编码器 CLIP）', fc=C_OLD, ec=C_OLD_B, fs=12.5)
arrow(2.37, 8.81, 2.74, 8.81)

box(5.18, 8.25, 1.45, 1.12, '翻译', '（投影层）', fc='#FADBD8', ec=C_BAD,
    fs=13.5, tc='#922B21', tc2='#B03A2E')
arrow(4.77, 8.81, 5.14, 8.81)

box(2.80, 6.45, 1.95, 0.96, '说话的人', '（语言模型 LLM）', fc=C_OLD, ec=C_OLD_B, fs=12.5)

arrow(5.90, 8.21, 5.90, 6.18, color=C_BAD, ls=(0, (4.5, 3.5)))
ax.plot([5.90, 3.78], [6.18, 6.18], color=C_BAD, lw=2.3, linestyle=(0, (4.5, 3.5)))
arrow(3.78, 6.18, 3.78, 6.41, color=C_BAD)

ax.text(5.90, 5.72, '⚠ 细节被压掉', ha='center', va='center', fontsize=11.2,
        color=C_BAD, fontweight='bold')

box(0.50, 6.52, 1.85, 0.82, '放射报告', '', fs=12.5)
arrow(2.37, 6.93, 2.74, 6.93)

box(0.72, 4.45, 4.80, 0.88, '分类 / 报告生成', '', fs=13.5)
arrow(3.78, 6.43, 3.78, 5.39)

ax.add_patch(FancyBboxPatch((0.72, 3.50), 4.80, 0.70,
                            boxstyle="round,pad=0.02,rounding_size=0.10",
                            fc='#fff', ec=C_OLD_B, lw=1.8, ls=':'))
ax.text(3.12, 3.98, '训练：只有一步（两段分开训）', ha='center', va='center',
        fontsize=11.5, fontweight='bold', color=C_OLD_B)
ax.text(3.12, 3.70, '先训视觉编码器，再训投影层', ha='center', va='center',
        fontsize=9.6, color='#5A6572', style='italic')
arrow(3.12, 4.20, 3.12, 4.41, color=C_OLD_B, ls=(0, (3, 3)))

ax.text(3.52, 2.45, '两个专家靠「翻译」对话，翻译必失真', ha='center', va='center',
        fontsize=12.2, color='#3E4C5E', style='italic', fontweight='bold')

# ==================== 右：新方法 ====================
box(7.45, 8.40, 1.65, 0.82, '胸片图像', '', fs=12.5)
box(7.45, 6.75, 1.65, 0.82, '放射报告', '', fs=12.5)

box(9.47, 8.32, 1.95, 1.05, '切成 1024 小块', '（图像 token）', fc=C_NEW, ec=C_NEW_B, fs=11.8, fs2=9.3)
box(9.47, 6.68, 1.95, 1.05, '切成一个个词', '（文本 token）', fc=C_NEW, ec=C_NEW_B, fs=11.8, fs2=9.3)
arrow(9.12, 8.81, 9.43, 8.81)
arrow(9.12, 7.16, 9.43, 7.16)

# ===== 统一序列（框 6.60 ~ 9.52）=====
ax.add_patch(FancyBboxPatch((11.80, 6.60), 1.90, 2.92,
                            boxstyle="round,pad=0.02,rounding_size=0.12",
                            fc='#fff', ec=C_NEW_B, lw=2.4))
ax.text(12.75, 9.22, '同一种语言', ha='center', va='center',
        fontsize=11.5, fontweight='bold', color=C_NEW_B)
ax.text(12.75, 8.93, '（统一 token 序列）', ha='center', va='center',
        fontsize=8.8, color='#5A6572', style='italic')
for i, lb in enumerate(['图', '图', '图', '文', '文']):
    yy = 8.48 - i * 0.34
    fcc = '#D5EBDC' if lb == '图' else '#FFF3CD'
    ax.add_patch(Rectangle((12.00, yy), 1.50, 0.28, fc=fcc, ec=C_NEW_B, lw=1.1))
    ax.text(12.75, yy + 0.14, lb, ha='center', va='center', fontsize=10, color='#1F2937')
arrow(11.42, 8.81, 11.76, 8.45)
arrow(11.42, 7.16, 11.76, 7.52)

# ===== S1（框 4.85 ~ 6.30）=====
ax.add_patch(FancyBboxPatch((7.45, 4.85), 3.40, 1.45,
                            boxstyle="round,pad=0.02,rounding_size=0.12",
                            fc='#E8F0FA', ec=C_BORROW_B, lw=2.4))
ax.text(9.15, 5.97, '训练阶段 S1：自回归', ha='center', va='center',
        fontsize=12.5, fontweight='bold', color='#2C4A73')
ax.text(9.15, 5.60, '顺着往下写 · 学会生成表达', ha='center', va='center',
        fontsize=10.2, color='#3D5A80')
ax.text(9.15, 5.18, '← 继承自变色龙', ha='center', va='center', fontsize=10,
        color=C_BORROW_B, fontweight='bold', style='italic')

# 统一序列框底(6.60) → 下行 6.48 → 左拐 → S1 框顶(6.30)上方留 0.10
arrow(12.75, 6.52, 12.75, 6.48)
ax.plot([12.75, 9.15], [6.48, 6.48], color='#4B5563', lw=2.3)
arrow(9.15, 6.48, 9.15, 6.40)

# ===== S2（框 4.85 ~ 6.30）=====
ax.add_patch(FancyBboxPatch((11.25, 4.85), 3.40, 1.45,
                            boxstyle="round,pad=0.02,rounding_size=0.12",
                            fc='#FFF4E5', ec=C_HOT_B, lw=2.9))
ax.text(12.95, 5.97, '训练阶段 S2：掩码重建', ha='center', va='center',
        fontsize=12.5, fontweight='bold', color='#7E5109')
ax.text(12.95, 5.60, '遮住 50% 再补回来 · 学会看细节', ha='center', va='center',
        fontsize=10.2, color='#8A6023')
ax.text(12.95, 5.18, '← CheXmix 新增（原创）', ha='center', va='center',
        fontsize=10, color=C_HOT_B, fontweight='bold', style='italic')

arrow(10.88, 5.57, 11.20, 5.57, color=C_HOT_B, lw=2.9)

# ===== Transformer（框 3.30 ~ 4.20）=====
box(8.55, 3.30, 4.40, 0.90, '一个 Transformer 就够了', '', fc=C_NEW, ec=C_NEW_B, fs=13.5, lw=2.4)

# S2 框底(4.85) → 下行 4.62 → 左拐 → 竖直下行 → Transformer 框顶(4.20)上方留 0.10
arrow(12.95, 4.77, 12.95, 4.62, color='#4B5563', lw=2.3)
ax.plot([12.95, 11.10], [4.62, 4.62], color='#4B5563', lw=2.3)
arrow(11.10, 4.62, 11.10, 4.30)

box(8.55, 2.00, 1.95, 0.80, '分类 / 判别', '', fs=12.5)
box(11.00, 2.00, 1.95, 0.80, '报告 / 补图', '', fs=12.5)
arrow(9.52, 3.26, 9.52, 2.85)
arrow(11.97, 3.26, 11.97, 2.85)

ax.text(15.05, 4.55, '✓ 不需要\n投影层', ha='center', va='center',
        fontsize=12.5, color=C_NEW_B, fontweight='bold', linespacing=1.4)

ax.text(11.52, 1.30, 'S1 学会「写」  +  S2 逼它「真看懂」  =  判别和生成都会',
        ha='center', va='center', fontsize=12, color='#2E7D5B', fontweight='bold')

# ===== 底部条 =====
ax.add_patch(FancyBboxPatch((0.25, 0.06), 15.70, 0.36,
                            boxstyle="round,pad=0.01,rounding_size=0.08",
                            fc='#2C3E50', ec='#2C3E50'))
ax.text(8.10, 0.24, '架构：取消投影层（借自变色龙）    ｜    训练：多了一个掩码重建阶段（CheXmix 原创）',
        ha='center', va='center', fontsize=12.5, color='#fff', fontweight='bold')

plt.tight_layout(pad=0.3)
out = '/root/.openclaw/workspace/figs/architecture_compare_v13.png'
plt.savefig(out, bbox_inches='tight', facecolor='white')
print('saved', out)
