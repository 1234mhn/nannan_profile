# 方案 — 2026 研赛 D题

用户偏好（未指定的项在门禁 A 一并确认）：
- 排版引擎：LaTeX（默认，xelatex 可用）
- 竞赛类型：华为杯（中国研究生数学建模竞赛）
- 论文语言：中文
- 实际问题清单：
  - Q1：单点往返运输能力与货箱组批方案（45组载荷反解 + 15服务区组批优化 + 多目标权衡 + 返航余量灵敏度）
  - Q2：异构无人机多点多架次运输调度（VRPTW + 共享电池周转 + 时限约束，多目标）
  - Q3：通信约束下运输与中继联合调度（LOS/链路预算 + 中继悬停选址 + 联合调度）
  - Q4：救援任务分区与资源配置优化（2组/3组划分 + 资源核算 + 缺口分析）

workflow:
1. 赛题分析与建模设计          → ANALYSIS_MODELING_REPORT.md
2. [门禁A] 方案质询            → MODEL_GRILL_REPORT.md
3. 编程实现与数据图表          → RESULTS_REPORT.md、results/、figures/
4. 结构图绘制（按需）          → DRAWIO_REPORT.md
5. 论文内容计划                → PAPER_CONTENT_PLAN.md
6. [门禁B] 论证计划质询        → 更新 PAPER_GRILL_REPORT.md
7. 正文撰写与摘要              → paper/
8. [门禁C] 成稿质询            → 更新 PAPER_GRILL_REPORT.md
9. 编译与验收                  → VERIFY_REPORT.md
