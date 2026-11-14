#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================
A题 Q3 复现 · 第2步：优化模型建立与求解
================================================================
【模型总览】

  决策变量：P = (P_1,...,P_N) ∈ R^N     每台风机功率参考值 (MW)

  目标函数（多目标 → 加权求和）：
      min  F(P) = w1*f1(P) + w2*f2(P)
      f1(P) = (1/N)*Σ a_i * P_i^3        主轴平均损伤
      f2(P) = (1/N)*Σ b_i * P_i^2.5      塔架平均损伤
      w1 + w2 = 1

  约束条件：
      ① Σ P_i = P_AGC                (等式：功率守恒)
      ② 0 <= P_i <= 5                (边界：额定上限)
      ③ |P_i - P_AGC/N| <= 1         (不等式：不偏离平均分配)

【为什么用加权求和法】
  - 多目标优化常用三种：加权求和 / ε-约束 / Pareto(NSGA-II)
  - 本题要求"每秒算一次"，速度优先 → 加权求和最快（转成单目标）
  - 且题目允许"给出目标权重值（如果有）并说明设计思路"
    → 说明出题人默认接受加权法

【为什么用 SLSQP】
  - 目标非线性、约束有等式 → 需要支持等式约束的 NLP 求解器
  - SLSQP (Sequential Least Squares Programming) 正是干这个的
  - scipy 自带，无需额外依赖
================================================================
"""

import numpy as np
import time
from scipy.optimize import minimize

from step1_数据与损伤模型 import (
    N, P_RATED, DELTA, gen_data, precompute_coeffs
)


# ============================================================
# 一、构建目标函数（闭包，把系数绑进去）
# ============================================================
def make_objective(a, b, w1=0.5, w2=0.5):
    """
    返回目标函数 F(P)。

    注意：这里用的是"解析简化版"——
    a_i, b_i 已预计算，每次求值只做幂运算，不做雨流计数。
    这是满足"每秒一次"实时性的关键。
    """
    def F(P):
        f1 = np.mean(a * P ** 3)        # 主轴平均损伤
        f2 = np.mean(b * P ** 2.5)      # 塔架平均损伤
        return w1 * f1 + w2 * f2
    return F


def make_grad(a, b, w1=0.5, w2=0.5):
    """解析梯度（可选，能显著加速 SLSQP 收敛）"""
    def G(P):
        g1 = a * 3.0 * P ** 2 / N       # d(f1)/dP_i
        g2 = b * 2.5 * P ** 1.5 / N     # d(f2)/dP_i
        return w1 * g1 + w2 * g2
    return G


# ============================================================
# 二、约束条件
# ============================================================
def make_constraints(P_AGC):
    Pbar = P_AGC / N

    def cons_eq(P):
        """① 功率守恒：ΣP_i - P_AGC = 0"""
        return np.sum(P) - P_AGC

    def cons_dev(P):
        """
        ③ |P_i - Pbar| <= 1
          scipy 的 'ineq' 要求返回 >= 0，所以：
            P_i <= Pbar + 1  →  (Pbar+1) - P_i >= 0
            P_i >= Pbar - 1  →  P_i - (Pbar-1) >= 0
        """
        upper = (Pbar + DELTA) - P
        lower = P - (Pbar - DELTA)
        return np.concatenate([upper, lower])

    return [
        {'type': 'eq',   'fun': cons_eq},
        {'type': 'ineq', 'fun': cons_dev},
    ]


# ============================================================
# 三、求解函数
# ============================================================
def solve_q3(V, P_AGC, w1=0.5, w2=0.5, x0=None, use_grad=True,
             maxiter=300):
    """
    求解 Q3 有功功率优化分配问题。

    参数
    ----
    V      : (N,) 风速
    P_AGC  : float 电网调度指令
    w1,w2  : 权重（w1+w2=1）
    x0     : 初值；None 则用平均分配
    use_grad : 是否用解析梯度（快很多）

    返回
    ----
    dict: P_opt, f1, f2, F, time_ms, success, message, ...
    """
    a, b = precompute_coeffs(V)
    obj = make_objective(a, b, w1, w2)
    jac = make_grad(a, b, w1, w2) if use_grad else None

    # ---- 初值策略：热启动 vs 平均分配 ----
    if x0 is None:
        x0 = np.full(N, P_AGC / N)

    bounds = [(0.0, P_RATED)] * N
    cons = make_constraints(P_AGC)

    t0 = time.perf_counter()
    res = minimize(
        obj, x0, jac=jac,
        method='SLSQP',
        bounds=bounds,
        constraints=cons,
        options={'maxiter': maxiter, 'ftol': 1e-12, 'disp': False}
    )
    t_ms = (time.perf_counter() - t0) * 1000

    P_opt = res.x
    f1 = np.mean(a * P_opt ** 3)
    f2 = np.mean(b * P_opt ** 2.5)

    return {
        'P_opt': P_opt,
        'f1': f1, 'f2': f2, 'F': obj(P_opt),
        'time_ms': t_ms,
        'success': res.success,
        'message': res.message,
        'nit': res.nit,
        'P_AGC': P_AGC,
        'w1': w1, 'w2': w2,
    }


# ============================================================
# 四、约束校验（题目要求"展示约束条件是否满足"）
# ============================================================
def check_constraints(P, P_AGC, verbose=True):
    Pbar = P_AGC / N
    ok_sum = abs(P.sum() - P_AGC) < 1e-6
    ok_range = (P.min() >= -1e-9) and (P.max() <= P_RATED + 1e-9)
    max_dev = np.max(np.abs(P - Pbar))
    ok_dev = max_dev <= DELTA + 1e-9

    if verbose:
        print("  【约束校验】")
        print(f"    ① ΣP = {P.sum():.6f} (目标 {P_AGC})  偏差 "
              f"{abs(P.sum()-P_AGC):.2e}  {'✅' if ok_sum else '❌'}")
        print(f"    ② P ∈ [{P.min():.4f}, {P.max():.4f}] "
              f"(要求 [0, {P_RATED}])  {'✅' if ok_range else '❌'}")
        print(f"    ③ 最大偏离均值 = {max_dev:.6f} "
              f"(要求 ≤ {DELTA})  {'✅' if ok_dev else '❌'}")

    return ok_sum and ok_range and ok_dev


# ============================================================
# 五、对比：优化前（平均分配） vs 优化后
# ============================================================
def compare(V, P_AGC, **kw):
    a, b = precompute_coeffs(V)

    # ---- 优化前：平均分配 ----
    P_avg = np.full(N, P_AGC / N)
    f1_avg = np.mean(a * P_avg ** 3)
    f2_avg = np.mean(b * P_avg ** 2.5)
    F_avg = 0.5 * f1_avg + 0.5 * f2_avg

    # ---- 优化后 ----
    r = solve_q3(V, P_AGC, **kw)

    print("=" * 66)
    print(f"优化前后对比  (P_AGC = {P_AGC} MW, w1={kw.get('w1',0.5)}, "
          f"w2={kw.get('w2',0.5)})")
    print("=" * 66)
    print(f"{'指标':<22}{'优化前(平均)':>14}{'优化后':>14}{'改善':>14}")
    print("-" * 66)

    def row(name, v0, v1):
        imp = (v0 - v1) / v0 * 100 if v0 != 0 else 0
        print(f"{name:<22}{v0:>14.6f}{v1:>14.6f}{imp:>13.2f}%")

    row("主轴平均损伤", f1_avg, r['f1'])
    row("塔架平均损伤", f2_avg, r['f2'])
    row("加权目标 F", F_avg, r['F'])
    print(f"{'功率方差':<22}{np.var(P_avg):>14.6f}"
          f"{np.var(r['P_opt']):>14.6f}")
    print(f"{'最大损伤(主轴)':<20}{np.max(a*P_avg**3):>14.6f}"
          f"{np.max(a*r['P_opt']**3):>14.6f}")
    print(f"{'损伤不均衡度(std)':<18}{np.std(a*P_avg**3):>14.6f}"
          f"{np.std(a*r['P_opt']**3):>14.6f}")

    print(f"\n【求解信息】{r['message']}")
    print(f"  耗时 {r['time_ms']:.2f} ms   迭代 {r['nit']} 次   "
          f"{'✅ 满足 <1000ms' if r['time_ms'] < 1000 else '❌ 超时'}")

    check_constraints(r['P_opt'], P_AGC)

    return P_avg, r


# ============================================================
# 六、主程序
# ============================================================
if __name__ == "__main__":
    V, P_AGC = gen_data()
    compare(V, P_AGC)
