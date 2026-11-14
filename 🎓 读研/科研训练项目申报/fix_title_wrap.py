"""封面项目名称断行优化：原来断在「医学|图像」，改为「的|医学图像」。保持单下划线连续。"""
import shutil, sys, zipfile

SRC = "孟浩楠-科研训练计划项目申报书-修订20261106.docx"
DST = "孟浩楠-科研训练计划项目申报书-修订20261106b.docx"

OLD_TAIL = "<w:t>面向医学报告弱监督的医学</w:t>"
NEW_TAIL = "<w:t>面向医学报告弱监督的</w:t>"
OLD_NEXT_IND = '<w:ind w:firstLine="2880" w:firstLineChars="900"/>'
NEW_NEXT_IND = '<w:ind w:firstLine="2560" w:firstLineChars="800"/>'

zin = zipfile.ZipFile(SRC)
items = zin.infolist()
data = {i.filename: zin.read(i.filename) for i in items}
zin.close()

doc = data["word/document.xml"].decode("utf-8")

n1 = doc.count(OLD_TAIL)
n2 = doc.count(OLD_NEXT_IND)
print("命中:", n1, n2)
if n1 != 1 or n2 != 1:
    print("未按预期命中，中止")
    sys.exit(1)

doc = doc.replace(OLD_TAIL, NEW_TAIL)
doc = doc.replace(OLD_NEXT_IND, NEW_NEXT_IND)

data["word/document.xml"] = doc.encode("utf-8")
zout = zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED)
for i in items:
    zout.writestr(i, data[i.filename])
zout.close()
print("已写出:", DST)
