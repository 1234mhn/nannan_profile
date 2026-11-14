"""图 1 收尾：①删除图注前插入的空段落；②图注段落居中、去掉首行缩进、行距改单倍。
   2026-11-06"""
import re, sys, zipfile

SRC = "孟浩楠-科研训练计划项目申报书-终稿20261106.docx"
DST = "孟浩楠-科研训练计划项目申报书-终稿20261106b.docx"

EMPTY = ('<w:p w14:paraId="5A1B0001"><w:pPr><w:spacing w:line="240" w:lineRule="auto"/>'
         '<w:rPr><w:rFonts w:hint="eastAsia" w:eastAsia="仿宋_GB2312"/>'
         '<w:color w:val="000000"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr></w:p>')

zin = zipfile.ZipFile(SRC)
items = zin.infolist()
data = {i.filename: zin.read(i.filename) for i in items}
zin.close()

doc = data["word/document.xml"].decode("utf-8")

# 1) 删空段
if EMPTY in doc:
    doc = doc.replace(EMPTY, "")
    print("[OK] 删除多余空段")
else:
    print("[WARN] 未找到待删空段")

# 2) 图 1 图注段落：居中 + 去掉 firstLine 缩进 + 保留原行距
CAP = "图 1  本项目主要研究内容</w:t>"
i = doc.find(CAP)
if i < 0:
    sys.exit("找不到图 1 图注")
ps = doc.rfind("<w:p ", 0, i)
pe = doc.find("</w:p>", i) + len("</w:p>")
para = doc[ps:pe]
new = para.replace('<w:ind w:firstLine="480" w:firstLineChars="200"/>', "")
# 已经是居中 + 仍有 firstLine 缩进 -> 只删缩进
doc = doc[:ps] + new + doc[pe:]
print("[OK] 图 1 图注改为居中、无缩进")

data["word/document.xml"] = doc.encode("utf-8")
zout = zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED)
for it in items:
    zout.writestr(it, data[it.filename])
zout.close()
print("已写出:", DST)
