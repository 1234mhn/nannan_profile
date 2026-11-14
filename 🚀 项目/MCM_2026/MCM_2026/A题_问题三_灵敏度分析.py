#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2024 A题 Q3 灵敏度分析
================================================================
三个灵敏度维度：
  ① 权重 w1 灵敏度    → 展示双目标权衡（论文必写）
  ② 总功率 P_agc 灵敏度 → 展示负荷影响
  ③ 偏离限制 DELTA 灵敏度 → 展示约束松紧对优化空间的影响（最有价值）
================================================================
"""
import numpy as np
from scipy.optimize import minimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 中文字体
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

N = 100
P_RATED = 5.0
np.random.seed(42)
V = np.random.uniform(11.2, 15.0, N)


def damage_spindle(P, v):
    return 1e-3 * np.power(P, 3) * (11.2 / v) ** 2


def damage_tower(P, v):
    return 8e-4 * np.power(P, 2.5) * (v / 11.2) ** 1.5


def solve(P_AGC, w1, w2, DELTA):
    """求解给定参数下的最优分配"""
    def obj(P):
        return w1 * np.mean(damage_spindle(P, V)) + w2 * np.mean(damage_tower(P, V))

    def cons_sum(P):
        return np.sum(P) - P_AGC

    def cons_dev(P):
        Pbar = P_AGC / N
        return np.concatenate([(Pbar + DELTA) - P, P - (Pbar - DELTA)])

    res = minimize(obj, np.full(N, P_AGC / N), method='SLSQP',
                   bounds=[(0, P_RATED)] * N,
                   constraints=[{'type': 'eq', 'fun': cons_sum},
                                {'type': 'ineq', 'fun': cons_dev}],
                   options={'maxiter': 500, 'ftol': 1e-10})
    f1 = np.mean(damage_spindle(res.x, V))
    f2 = np.mean(damage_tower(res.x, V))
    return res.x, f1, f2


# ============ ① 权重灵敏度 ============
print("【① 权重灵敏度分析】")
ws = np.linspace(0, 1, 11)
f1_list, f2_list = [], []
for w1 in ws:
    _, f1, f2 = solve(300.0, w1, 1 - w1, 1.0)
    f1_list.append(f1); f2_list.append(f2)
    print(f"  w1={w1:.1f} 主轴损伤={f1:.6f} 塔架损伤={f2:.6f}")

# ============ ② 总功率灵敏度 ============
print("\n【② 总功率灵敏度分析】")
pagcs = np.linspace(100, 480, 12)
f1_p, f2_p = [], []
for pa in pagcs:
    _, f1, f2 = solve(pa, 0.5, 0.5, 1.0)
    f1_p.append(f1); f2_p.append(f2)
    print(f"  P_agc={pa:.0f}MW 主轴={f1:.6f} 塔架={f2:.6f}")

# ============ ③ 偏离限制灵敏度 ============
print("\n【③ 偏离限制 DELTA 灵敏度分析】")
deltas = [0.1, 0.2, 0.5, 1.0, 2.0, 3.0, 5.0]
f1_d, f2_d, impr = [], [], []
_, f1_base, f2_base = solve(300.0, 0.5, 0.5, 1.0)  # 基准
for d in deltas:
    _, f1, f2 = solve(300.0, 0.5, 0.5, d)
    f1_d.append(f1); f2_d.append(f2)
    impr.append((f1_base - f1) / f1_base * 100)   # 主轴改善率
    print(f"  DELTA={d:.1f}MW 主轴={f1:.6f} 塔架={f2:.6f}")

# ============ 画图 ============
fig, axes = plt.subplots(1, 3, figsize=(17, 4.5))

ax = axes[0]
ax.plot(ws, f1_list, 'o-', label='主轴损伤', color='#d62728')
ax.plot(ws, f2_list, 's-', label='塔架损伤', color='#1f77b4')
ax.set_xlabel('权重 w1 (主轴权重)'); ax.set_ylabel('平均疲劳损伤')
ax.set_title('① 权重灵敏度：双目标权衡')
ax.legend(); ax.grid(alpha=0.3)

ax = axes[1]
ax.plot(pagcs, f1_p, 'o-', label='主轴损伤', color='#d62728')
ax.plot(pagcs, f2_p, 's-', label='塔架损伤', color='#1f77b4')
ax.set_xlabel('电网调度总功率 P_agc (MW)'); ax.set_ylabel('平均疲劳损伤')
ax.set_title('② 总功率灵敏度')
ax.legend(); ax.grid(alpha=0.3)

ax = axes[2]
ax.plot(deltas, impr, 'o-', color='#2ca02c', lw=2)
ax.set_xlabel('偏离限制 DELTA (MW)'); ax.set_ylabel('主轴损伤改善率 (%)')
ax.set_title('③ 约束松紧灵敏度（优化空间）')
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('Q3_灵敏度分析图.png', dpi=150)
print("\n✅ 已保存：Q3_灵敏度分析图.png")
