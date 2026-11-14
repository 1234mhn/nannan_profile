"""图 1 图注单独成行：在图注段落前插入空段落。
   原因：图片是 anchor(wrapTight, behindDoc) 浮在段落里，与「图 1」标签同段，导致底部文字被压。
   2026-11-06"""
import sys, zipfile

SRC = "孟浩楠-科研训练计划项目申报书-图1已更新20261106.docx"
DST = "孟浩楠-科研训练计划项目申报书-最终20261106.docx"

CAP = '图 1  本项目主要研究内容</w:t></w:r></w:p>'
EMPTY = ('<w:p w14:paraId="5A1B0001"><w:pPr><w:spacing w:line="240" w:lineRule="auto"/>'
         '<w:rPr><w:rFonts w:hint="eastAsia" w:eastAsia="仿宋_GB2312"/>'
         '<w:color w:val="000000"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr></w:p>')

zin = zipfile.ZipFile(SRC)
items = zin.infolist()
data = {i.filename: zin.read(i.filename) for i in items}
zin.close()

doc = data["word/document.xml"].decode("utf-8")
n = doc.count(CAP)
print("图注命中:", n)
if n != 1:
    sys.exit("未按预期命中，中止")
doc = doc.replace(CAP, CAP + EMPTY)

data["word/document.xml"] = doc.encode("utf-8")
zout = zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED)
for it in items:
    zout.writestr(it, data[it.filename])
zout.close()
print("已写出:", DST)
