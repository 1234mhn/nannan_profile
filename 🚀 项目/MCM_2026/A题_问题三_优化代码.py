#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2024研赛 A题 问题三：风电场有功功率优化分配
================================================================
三零件（圈出来的）：
  变量：P[0..N-1] 每台风机功率参考值，连续，∈[0, 5] MW
  目标：min w1*f_主轴(P) + w2*f_塔架(P)     ← 双目标加权求和
  约束：① sum(P) = P_agc          （功率守恒，等式）
        ② 0 <= P_i <= 5           （单机上下限）
        ③ |P_i - P_agc/N| <= 1    （不偏离平均分配）

模型：多目标非线性规划 → 加权求和法 → SLSQP 求解
================================================================
⚠️ 注意：下面的损伤函数是【占位版】，用物理直觉构造 D ∝ P^3。
   真实版需接入 Q1（雨流近似损伤模型）+ Q2（风速→载荷估算）。
   替换 damage_spindle / damage_tower 的函数体即可，其余代码不用改。
"""

import numpy as np
from scipy.optimize import minimize
import time

# ============ 参数设置 ============
N = 100                 # 风机台数
P_RATED = 5.0           # 单机额定功率 (MW)
DELTA = 1.0             # 偏离平均分配的最大差值 (MW)
P_AGC = 300.0           # 电网调度指令：全场总功率 (MW)
W1, W2 = 0.5, 0.5       # 主轴/塔架 目标权重

# 模拟风速（真实版应从附件2读取）
np.random.seed(42)
V = np.random.uniform(11.2, 15.0, N)   # 轮毂处风速 m/s（风能过剩场景）


# ============ 1. 损伤函数（占位版，待替换）============
def damage_spindle(P, v):
    """
    主轴疲劳损伤：占位模型
    物理逻辑：
      - 风电过剩场景下，风速越接近额定(11.2m/s)，同样的功率对应的扭矩越小
      - 风速越高（可用风能越多），发同样功率越"轻松"，损伤越小
    真实版：应使用 Q1 的雨流近似损伤模型 + Q2 的扭矩估算
    """
    k = 1e-3
    # 风速有效因子：风速越大，单位功率的损伤越小
    v_eff = (11.2 / v) ** 2      # 以额定风速11.2为基准
    return k * np.power(P, 3) * v_eff


def damage_tower(P, v):
    """
    塔架疲劳损伤：占位模型
    物理逻辑：塔架推力随功率增加而增加，且风速越高推力越大
    真实版：应使用 Q1 的雨流近似损伤模型 + Q2 的推力估算
    """
    k2 = 8e-4
    v_eff = (v / 11.2) ** 1.5     # 风速越大，塔架受力越大
    return k2 * np.power(P, 2.5) * v_eff


# ============ 2. 目标函数 ============
def objective(P):
    """加权求和：min w1*mean(主轴损伤) + w2*mean(塔架损伤)"""
    f1 = np.mean(damage_spindle(P, V))   # 主轴总体损伤
    f2 = np.mean(damage_tower(P, V))     # 塔架总体损伤
    return W1 * f1 + W2 * f2


# ============ 3. 约束条件 ============
def cons_sum(P):
    """① 功率守恒：sum(P) - P_agc = 0"""
    return np.sum(P) - P_AGC


def cons_dev(P):
    """③ |P_i - P̄| <= 1  拆成两个不等式，都要 >= 0"""
    Pbar = P_AGC / N
    upper = (Pbar + DELTA) - P     # P_i <= P̄ + 1  →  >= 0
    lower = P - (Pbar - DELTA)     # P_i >= P̄ - 1  →  >= 0
    return np.concatenate([upper, lower])


# ============ 4. 求解 ============
def solve():
    x0 = np.full(N, P_AGC / N)                  # 初始解：平均分配
    bounds = [(0.0, P_RATED)] * N               # ② 0 <= P_i <= 5

    t0 = time.time()
    res = minimize(
        objective, x0,
        method='SLSQP',
        bounds=bounds,
        constraints=[
            {'type': 'eq',   'fun': cons_sum},
            {'type': 'ineq', 'fun': cons_dev},
        ],
        options={'maxiter': 500, 'ftol': 1e-10, 'disp': False}
    )
    elapsed = time.time() - t0
    return res, elapsed


# ============ 5. 主程序：求解 + 对比 + 输出 ============
if __name__ == '__main__':
    print("=" * 62)
    print("2024 A题 Q3  风电场有功功率优化分配")
    print("=" * 62)

    # ---- 优化前：平均分配 ----
    P_avg = np.full(N, P_AGC / N)
    f1_avg = np.mean(damage_spindle(P_avg, V))
    f2_avg = np.mean(damage_tower(P_avg, V))

    # ---- 优化后 ----
    res, elapsed = solve()
    P_opt = res.x
    f1_opt = np.mean(damage_spindle(P_opt, V))
    f2_opt = np.mean(damage_tower(P_opt, V))

    # ---- 输出结果 ----
    print(f"\n【求解状态】{res.message}")
    print(f"【求解耗时】{elapsed*1000:.2f} ms  (要求 < 1000 ms)")
    print(f"\n{'':14s}{'优化前(平均)':>14s}{'优化后':>14s}{'改善':>12s}")
    print("-" * 62)
    print(f"{'主轴总损伤':14s}{f1_avg:14.6f}{f1_opt:14.6f}{(f1_avg-f1_opt)/f1_avg*100:11.2f}%")
    print(f"{'塔架总损伤':14s}{f2_avg:14.6f}{f2_opt:14.6f}{(f2_avg-f2_opt)/f2_avg*100:11.2f}%")
    print(f"{'功率方差':14s}{np.var(P_avg):14.6f}{np.var(P_opt):14.6f}{'':>12s}")

    # ---- 约束校验 ----
    print("\n【约束校验】")
    print(f"  ① 总功率 = {P_opt.sum():.6f}  (目标 {P_AGC})  偏差 {abs(P_opt.sum()-P_AGC):.2e}")
    print(f"  ② 功率范围 [{P_opt.min():.4f}, {P_opt.max():.4f}]  (要求 [0, 5])")
    Pbar = P_AGC / N
    print(f"  ③ 最大偏离 = {np.max(np.abs(P_opt - Pbar)):.6f}  (要求 <= 1.0)")

    # ---- 保存结果 ----
    np.savetxt("Q3_优化结果_功率分配.csv",
               np.column_stack([np.arange(1, N + 1), P_opt]),
               header="风机编号,功率(MW)", delimiter=",", fmt="%d,%.6f",
               comments="")
    print("\n✅ 结果已保存：Q3_优化结果_功率分配.csv")

    # ---- 画图 ----
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))

        # 图1：功率分配对比
        axes[0].bar(np.arange(N) - 0.2, P_avg, width=0.4, label='平均分配', alpha=0.8)
        axes[0].bar(np.arange(N) + 0.2, P_opt, width=0.4, label='优化分配', alpha=0.8)
        axes[0].axhline(P_RATED, color='r', ls='--', lw=1, label='额定5MW')
        axes[0].set_xlabel('风机编号'); axes[0].set_ylabel('功率 (MW)')
        axes[0].set_title('优化前后功率分配对比'); axes[0].legend()

        # 图2：主轴/塔架损伤对比
        labels = ['主轴损伤', '塔架损伤']
        avg_v = [f1_avg, f2_avg]
        opt_v = [f1_opt, f2_opt]
        x = np.arange(2)
        axes[1].bar(x - 0.2, avg_v, width=0.4, label='优化前', alpha=0.8)
        axes[1].bar(x + 0.2, opt_v, width=0.4, label='优化后', alpha=0.8)
        axes[1].set_xticks(x); axes[1].set_xticklabels(labels)
        axes[1].set_title('疲劳损伤对比'); axes[1].legend()

        # 图3：散点-风速 vs 优化后功率
        axes[2].scatter(V, P_opt, alpha=0.7)
        axes[2].set_xlabel('风速 (m/s)'); axes[2].set_ylabel('优化后功率 (MW)')
        axes[2].set_title('风速 vs 分配功率')

        plt.tight_layout()
        plt.savefig("Q3_结果图.png", dpi=150)
        print("✅ 结果图已保存：Q3_结果图.png")
    except ImportError:
        print("⚠️ 未安装 matplotlib，跳过画图")
