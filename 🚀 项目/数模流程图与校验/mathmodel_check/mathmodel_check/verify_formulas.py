#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国研究生数学建模竞赛论文公式验算脚本
"""

import numpy as np
from scipy.optimize import fsolve

# ============ 问题一参数 ============
print("=" * 60)
print("问题一：熵权法与配比模型验算")
print("=" * 60)

# 测试熵权法公式（简化示例）
# 假设有 n=3 个样本，某组 G_s,g 如下
n = 3
G_sg = np.array([0.5, 0.7, 0.8])

# 公式 2: P_s,g = G_s,g / Σ G_s,g
P_sg = G_sg / np.sum(G_sg)
print(f"\n熵权法占比 P_s,g: {P_sg}")
print(f"占比之和 = {np.sum(P_sg):.6f} (应为1)")

# 公式 3: E_g = -Σ P_s,g·ln(P_s,g) / ln(n)
# 处理 0*ln0 = 0 的约定
P_sg_safe = np.where(P_sg > 0, P_sg, 1)  # 避免 log(0)
E_g = -np.sum(P_sg * np.log(P_sg_safe)) / np.log(n)
print(f"归一化熵 E_g = {E_g:.6f}")

# ============ 问题二参数（论文给定值）============
print("\n" + "=" * 60)
print("问题二：广义标度律验算")
print("=" * 60)

E = 1.689870
A_N = 0.353956
A_D = 1.240274
alpha = 0.339995
beta = 0.279906
kappa = 0.150040
mu = 0.991719

print(f"\n经典标度律参数:")
print(f"  E = {E}")
print(f"  A_N = {A_N}, α = {alpha}")
print(f"  A_D = {A_D}, β = {beta}")
print(f"\n乘性质量参数:")
print(f"  κ = {kappa}, μ = {mu}")

# 定义 L_0 和 L_2
def L_0(N, D):
    """经典标度律 公式11"""
    return E + A_N * N**(-alpha) + A_D * D**(-beta)

def L_2(N, D, Q):
    """乘性质量标度律 公式15"""
    L_p = L_0(N, D)  # 假设 m(p)=1 在参考配比处
    F_Q = 1 + kappa * (1 - Q)**mu
    return L_p * F_Q

# 验算公式17-19的求导
def verify_derivatives(N, D, Q):
    """验算公式17-19的偏导数"""
    L_p = L_0(N, D)
    F_Q = 1 + kappa * (1 - Q)**mu

    # 公式17: ∂L_2/∂N = -F·α·A_N·N^(-α-1)
    dL2_dN_formula = -F_Q * alpha * A_N * N**(-alpha - 1)

    # 公式18: ∂L_2/∂D = -F·β·A_D·D^(-β-1)
    dL2_dD_formula = -F_Q * beta * A_D * D**(-beta - 1)

    # 公式19: ∂L_2/∂Q = -L_0·κμ(1-Q)^(μ-1)
    # 注意：这里应该是 L_p 还是 L_0？论文写的是 L_0
    dL2_dQ_formula = -L_p * kappa * mu * (1 - Q)**(mu - 1)

    # 数值验证（用有限差分）
    h = 1e-6
    dL2_dN_numeric = (L_2(N + h, D, Q) - L_2(N - h, D, Q)) / (2 * h)
    dL2_dD_numeric = (L_2(N, D + h, Q) - L_2(N, D - h, Q)) / (2 * h)
    dL2_dQ_numeric = (L_2(N, D, Q + h) - L_2(N, D, Q - h)) / (2 * h)

    print(f"\n在 N={N}, D={D}, Q={Q} 处的偏导数验算:")
    print(f"  ∂L_2/∂N: 公式={dL2_dN_formula:.6e}, 数值={dL2_dN_numeric:.6e}, 差={abs(dL2_dN_formula - dL2_dN_numeric):.2e}")
    print(f"  ∂L_2/∂D: 公式={dL2_dD_formula:.6e}, 数值={dL2_dD_numeric:.6e}, 差={abs(dL2_dD_formula - dL2_dD_numeric):.2e}")
    print(f"  ∂L_2/∂Q: 公式={dL2_dQ_formula:.6e}, 数值={dL2_dQ_numeric:.6e}, 差={abs(dL2_dQ_formula - dL2_dQ_numeric):.2e}")

    return dL2_dN_formula, dL2_dD_formula, dL2_dQ_formula

# 测试点
N_test, D_test, Q_test = 10, 1000, 0.8
dL_dN, dL_dD, dL_dQ = verify_derivatives(N_test, D_test, Q_test)

# 验算公式20: MRC = -∂L_2/∂C
# C = 0.006 * N * D
# dL/dC = (dL/dN)·(dN/dC) + (dL/dD)·(dD/dC)
# 如果 D/N 保持恒定，则 N ∝ √C, D ∝ √C
# dN/dC = dN/d(6ND) * 10^18 = ...
#
# 论文写: MRC = -[N(∂L/∂N) + D(∂L/∂D)] / (2C)
# 验证这个公式是否正确

print(f"\n公式20 MRC 验算:")
C = 0.006 * N_test * D_test * 1e18  # FLOPs
MRC_formula = -(N_test * dL_dN + D_test * dL_dD) / (2 * C / 1e18)
print(f"  C = {C:.2e} FLOPs")
print(f"  MRC (公式) = {MRC_formula:.6e}")

# 数值验证：如果 N 和 D 都按 √C 缩放
# N(C) = N_test * √(C/C_test), D(C) = D_test * √(C/C_test)
def L_2_from_C(C_val):
    ratio = np.sqrt(C_val / C)
    N_new = N_test * ratio
    D_new = D_test * ratio
    return L_2(N_new, D_new, Q_test)

h_C = C * 1e-6
dL_dC_numeric = (L_2_from_C(C + h_C) - L_2_from_C(C - h_C)) / (2 * h_C)
MRC_numeric = -dL_dC_numeric

print(f"  dL/dC (数值) = {dL_dC_numeric:.6e}")
print(f"  MRC (数值) = {MRC_numeric:.6e}")
print(f"  差值 = {abs(MRC_formula - MRC_numeric):.2e}")

# ============ 公式22：质量等效参数验算 ============
print("\n" + "=" * 60)
print("公式22：质量提升的等效参数规模验算")
print("=" * 60)

# 论文声称：质量提高0.1，D=1000，N=10 → N_equiv=17.788
# 即 L_2(17.788, 1000, Q) = L_2(10, 1000, Q+0.1)
D_fix = 1000
N_original = 10
delta_Q = 0.1

# 假设当前质量 Q=0.5（论文未明确说，这里假设一个值）
# 或者用 Q=0.8（中等质量）
for Q_base in [0.5, 0.8]:
    Q_new = Q_base + delta_Q

    # 求解 L_2(N_equiv, D_fix, Q_base) = L_2(N_original, D_fix, Q_new)
    def equation(N_equiv):
        return L_2(N_equiv, D_fix, Q_base) - L_2(N_original, D_fix, Q_new)

    N_equiv_solution = fsolve(equation, N_original * 2)[0]
    multiplier = N_equiv_solution / N_original

    print(f"\n质量从 {Q_base} 提升到 {Q_new} (Δ={delta_Q}):")
    print(f"  N_original = {N_original}, D = {D_fix}")
    print(f"  N_equiv = {N_equiv_solution:.3f}")
    print(f"  倍数 = {multiplier:.3f}")
    print(f"  论文值 = 17.788 (1.779倍)")
    if Q_base == 0.5:
        print(f"  → 若论文用 Q=0.5，差异 = {abs(N_equiv_solution - 17.788):.3f}")

# 对 N=100 的情况
N_original_100 = 100
for Q_base in [0.5, 0.8]:
    Q_new = Q_base + delta_Q

    def equation(N_equiv):
        return L_2(N_equiv, D_fix, Q_base) - L_2(N_original_100, D_fix, Q_new)

    N_equiv_solution = fsolve(equation, N_original_100 * 4)[0]
    multiplier = N_equiv_solution / N_original_100

    print(f"\n质量从 {Q_base} 提升到 {Q_new}, N_original = {N_original_100}:")
    print(f"  N_equiv = {N_equiv_solution:.3f}")
    print(f"  倍数 = {multiplier:.3f}")
    print(f"  论文值 = 393.302 (3.933倍)")
    if Q_base == 0.5:
        print(f"  → 若论文用 Q=0.5，差异 = {abs(N_equiv_solution - 393.302):.3f}")

# ============ 问题三参数 ============
print("\n" + "=" * 60)
print("问题三：算力配置验算")
print("=" * 60)

# 公式24: L_ctx_crit = 6/η_attn
eta_attn = 2e-4
L_ctx_crit_formula = 6 / eta_attn
print(f"\n公式24验算:")
print(f"  η_attn = {eta_attn}")
print(f"  L_ctx_crit = 6/η_attn = {L_ctx_crit_formula}")
print(f"  论文值 = 30000")
print(f"  一致性: {'✓' if abs(L_ctx_crit_formula - 30000) < 1 else '✗'}")

# 公式30：预算等式验算
# C = C_train + C_quality + C_attn
# C = 6e18·N·D + 10^9·D·Δg(Q) + η_attn·10^18·N·D·L_ctx
# = 10^18·N·D·(6 + η_attn·L_ctx) + 10^9·D·Δg(Q)
# 消元得 D_B = C / {10^18(6+η_attn·L_ctx)N_B + 10^9·Δg(Q)}

print("\n公式30预算消元验算:")
C_budget = 1e19
L_ctx = 32768
N_B = 0.4911
D_B = 1.1433
Q = 0.9484
Q_0 = 0.605095  # 论文中问题三的基准质量

# 假设指数型质量成本 g(Q) = a·[exp(b(Q-Q_0))-1]
# 论文未给出 a, b 的具体值，这里无法验算具体的 Δg(Q)
# 但可以验算成本等式的结构

C_train = 6e18 * N_B * D_B
C_attn = eta_attn * 1e18 * N_B * D_B * L_ctx
# C_quality 无法验算（缺 a, b）

print(f"  预算 C = {C_budget:.2e}")
print(f"  N_B = {N_B}, D_B = {D_B}, Q = {Q}, L_ctx = {L_ctx}")
print(f"  C_train = {C_train:.2e} ({C_train/C_budget*100:.1f}%)")
print(f"  C_attn = {C_attn:.2e} ({C_attn/C_budget*100:.1f}%)")
print(f"  C_train + C_attn = {(C_train + C_attn):.2e}")
print(f"  (需要 C_quality 补齐到 {C_budget:.2e})")

# ============ 问题四参数 ============
print("\n" + "=" * 60)
print("问题四：能力预测验算")
print("=" * 60)

# 公式33: g_N,slow = g_C,slow / (1 + g_D/g_C·r_D)
g_C = 0.5264
g_D = 0.4793
g_C_slow = 0.5 * g_C
data_growth_share = g_D / g_C  # 论文另处写法

print(f"\n公式33验算:")
print(f"  g_C = {g_C}/年, g_D = {g_D}/年")
print(f"  g_C,slow = 0.5·g_C = {g_C_slow}/年")
print(f"  论文值 = 0.2632/年, 差异 = {abs(g_C_slow - 0.2632):.4f}")

# 论文说 data_growth_share = g_D/g_C 且 r_D 也等于这个值
r_D = data_growth_share  # 假设
g_N_slow_formula = g_C_slow / (1 + (g_D/g_C) * r_D)
print(f"  data_growth_share = g_D/g_C = {data_growth_share:.4f}")
print(f"  g_N,slow = g_C,slow / (1 + g_D/g_C·r_D)")
print(f"           = {g_C_slow} / (1 + {g_D/g_C}·{r_D})")
print(f"           = {g_C_slow} / (1 + {g_D/g_C * r_D:.4f})")
print(f"           = {g_N_slow_formula:.6f}/年")
print(f"  论文值 = 0.0236/年, 差异 = {abs(g_N_slow_formula - 0.0236):.6f}")

# 另一种写法：g_N,slow = (1 - data_growth_share)·g_C,slow
g_N_slow_alt = (1 - data_growth_share) * g_C_slow
print(f"\n  替代写法: g_N,slow = (1 - data_growth_share)·g_C,slow")
print(f"           = (1 - {data_growth_share:.4f})·{g_C_slow}")
print(f"           = {g_N_slow_alt:.6f}/年")

# 公式35: B_hat = 61.995352 - 20.855488·L
a_0 = 61.995352
a_1 = -20.855488
L_test = 2.9406
B_hat = a_0 + a_1 * L_test
print(f"\n公式35验算:")
print(f"  Loss = {L_test}")
print(f"  B_hat = {a_0} + {a_1}·{L_test}")
print(f"       = {B_hat:.6f}")
print(f"  论文说第三问 Loss=2.9406 映射得分约 0.667")
print(f"  0.667 换算到 0-100: {0.667 * 100:.2f}")
print(f"  验算结果差异: {abs(B_hat - 0.667*100):.2f}")

# 公式37: 参数前沿预测
# log10 N(t+h) = log10 N(t) + g_N,slow·h
N_frontier_0 = 10.344  # log10 尺度
h_12 = 1  # 12个月 = 1年
h_24 = 2  # 24个月 = 2年
g_N_slow = 0.0236

log10_N_12 = N_frontier_0 + g_N_slow * h_12
log10_N_24 = N_frontier_0 + g_N_slow * h_24

print(f"\n公式37参数前沿预测:")
print(f"  初始 log10(N) = {N_frontier_0}")
print(f"  g_N,slow = {g_N_slow}/年")
print(f"  12个月后: log10(N) = {N_frontier_0} + {g_N_slow}·1 = {log10_N_12:.6f}")
print(f"  论文值 = 10.921, 差异 = {abs(log10_N_12 - 10.921):.6f}")
print(f"  24个月后: log10(N) = {N_frontier_0} + {g_N_slow}·2 = {log10_N_24:.6f}")
print(f"  论文值 = 11.530, 差异 = {abs(log10_N_24 - 11.530):.6f}")

# ============ Shapley 分解验算（公式32）============
print("\n" + "=" * 60)
print("公式32：Shapley 分解验算")
print("=" * 60)

# 假设函数 F(N, t) = β_0 + β_logN·log10(N) + β_time·t
# 简化示例（忽略 chat 交互项）
beta_0 = 10
beta_logN = 5
beta_time = 2

def F(N, t):
    return beta_0 + beta_logN * np.log10(N) + beta_time * t

N_0, t_0 = 10, 0    # 起点
N_1, t_1 = 100, 1   # 终点

# 论文公式32
Delta_scale = 0.5 * ((F(N_1, t_1) - F(N_0, t_1)) + (F(N_1, t_0) - F(N_0, t_0)))
Delta_tech = 0.5 * ((F(N_1, t_1) - F(N_1, t_0)) + (F(N_0, t_1) - F(N_0, t_0)))

total_change = F(N_1, t_1) - F(N_0, t_0)

print(f"  F(N_0={N_0}, t_0={t_0}) = {F(N_0, t_0):.2f}")
print(f"  F(N_1={N_1}, t_1={t_1}) = {F(N_1, t_1):.2f}")
print(f"  总变化 = {total_change:.2f}")
print(f"\n  Δ_scale = 0.5·[(F(N_1,t_1)-F(N_0,t_1)) + (F(N_1,t_0)-F(N_0,t_0))]")
print(f"          = 0.5·[({F(N_1,t_1):.2f}-{F(N_0,t_1):.2f}) + ({F(N_1,t_0):.2f}-{F(N_0,t_0):.2f})]")
print(f"          = {Delta_scale:.2f}")
print(f"  Δ_tech  = 0.5·[(F(N_1,t_1)-F(N_1,t_0)) + (F(N_0,t_1)-F(N_0,t_0))]")
print(f"          = 0.5·[({F(N_1,t_1):.2f}-{F(N_1,t_0):.2f}) + ({F(N_0,t_1):.2f}-{F(N_0,t_0):.2f})]")
print(f"          = {Delta_tech:.2f}")
print(f"  Δ_scale + Δ_tech = {Delta_scale + Delta_tech:.2f}")
print(f"  验证: 等于总变化? {'✓' if abs(Delta_scale + Delta_tech - total_change) < 1e-10 else '✗'}")

print("\n" + "=" * 60)
print("验算完成")
print("=" * 60)
