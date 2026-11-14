"""按 2026-11-06 清单修改申报书：
顺序 4 → 2 → 5 → 3 → 8
（1 图1 需重绘，另行处理；9 文献年份待用户核实，不改）
"""
import re, shutil, sys, zipfile

SRC = "孟浩楠-科研训练计划项目申报书-图3已插入20261105.docx"
DST = "孟浩楠-科研训练计划项目申报书-修订20261106.docx"

CASES = []  # (说明, old, new, 期望命中次数)

# ---- 4. 第五部分预期成果首句 ----
CASES.append((
    "4-预期成果首句",
    "围绕报告弱监督条件下的医学图像细粒度对齐与疾病分类开展研究",
    "围绕报告弱监督条件下的医学图像分类方法开展研究",
    1,
))

# ---- 2. 可行性分析「项目名称中的细粒度对齐」 ----
CASES.append((
    "2-可行性项目名称自指",
    '项目名称中的"细粒度对齐"在 30 个月周期内不宜承诺覆盖所有模态和全部疾病类别',
    '项目名称中的"分类方法"在 30 个月周期内不宜承诺覆盖所有模态和全部疾病类别',
    1,
))

# ---- 5. 进度表 2027.12 断裂 ----
CASES.append((
    "5-第六阶段起始时间",
    "（6）第六阶段（2028 年 12 月—2029 年 3 月）",
    "（6）第六阶段（2027 年 12 月—2029 年 3 月）",
    1,
))
CASES.append((
    "5-第六阶段第一小条",
    "2028 年 12 月—2029 年 1 月：根据评审或阶段反馈补充实验",
    "2027 年 12 月—2028 年 6 月：根据评审或阶段反馈补充实验",
    1,
))
CASES.append((
    "5-第六阶段第二小条",
    "2029 年 1 月—3 月：完成论文修改或转投",
    "2028 年 7 月—2029 年 3 月：完成论文修改或转投",
    1,
))

# ---- 3. 研究目标 / 总体目标 口径对齐新标题 ----
CASES.append((
    "3-研究目标首句",
    "本项目围绕影像报告弱监督条件下的医学图像疾病分类开展研究",
    "本项目围绕影像报告弱监督条件下的医学图像分类方法开展研究",
    1,
))
CASES.append((
    "3-总体目标",
    "本项目的总体目标是形成一种对人工标注依赖较低",
    "本项目的总体目标是形成一种对人工标注依赖较低",
    1,
))

# ---- 8. 3.1 节末 Relation Modeling 断句 ----
CASES.append((
    "8-Relation Modeling 断句",
    " Relation Modeling 等则从匹配之间的关系入手",
    "Inter-Matching Relation Modeling 等工作则从匹配之间的关系入手",
    1,
))


def run():
    shutil.copyfile(SRC, DST)
    zin = zipfile.ZipFile(SRC)
    items = zin.infolist()
    data = {i.filename: zin.read(i.filename) for i in items}
    zin.close()

    doc = data["word/document.xml"].decode("utf-8")
    ok = True
    for desc, old, new, expect in CASES:
        n = doc.count(old)
        if n != expect:
            print(f"[FAIL] {desc}: 命中 {n} 次，期望 {expect}")
            ok = False
            continue
        doc = doc.replace(old, new)
        print(f"[OK]   {desc}")

    if not ok:
        print("\n有替换未命中，已中止，未写文件。")
        sys.exit(1)

    data["word/document.xml"] = doc.encode("utf-8")

    zout = zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED)
    for i in items:
        zout.writestr(i, data[i.filename])
    zout.close()
    print(f"\n已写出：{DST}")


if __name__ == "__main__":
    run()
