# A题 Q3 复现 —— 使用说明

## 文件清单

| 文件 | 作用 |
|---|---|
| `step1_数据与损伤模型.py` | 模拟数据 + 损伤模型（真实版替换这里） |
| `step2_优化模型.py` | 三零件 + 加权求和 + SLSQP 求解 |
| `step3_实时性验证.py` | 计时器 + 每秒一次 + 动图（题目要求） |
| `step4_对比与灵敏度.py` | 优化前后对比图 + 灵敏度分析 |
| `run_all.py` | 一键跑全部 |

## 跑法
```bash
cd /root/.openclaw/workspace/MCM_2026/A题Q3_复现
python3 run_all.py
```

## 输出
- `out/Q3_优化结果_功率分配.csv`
- `out/Q3_对比图.png`
- `out/Q3_灵敏度分析.png`
- `out/Q3_实时性动图.gif`
- `out/Q3_计时统计.txt`
