"""把图 1 从「浮动锚定+四周环绕+behindDoc」改为「内嵌 inline」，让图与图注各占一行、不再互相压字。
   2026-11-06  图 2 / 图 3 保持原样不动。"""
import re, sys, zipfile

SRC = "孟浩楠-科研训练计划项目申报书-最终20261106.docx"
DST = "孟浩楠-科研训练计划项目申报书-终稿20261106.docx"

CX, CY = 5274310, 3163469

INLINE = (
    '<wp:inline distT="0" distB="0" distL="0" distR="0">'
    f'<wp:extent cx="{CX}" cy="{CY}"/>'
    '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
    '<wp:docPr id="255954245" name="图片 1"/>'
    '<wp:cNvGraphicFramePr><a:graphicFrameLocks '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
    '</wp:cNvGraphicFramePr>'
    '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
    '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
    '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
    '<pic:nvPicPr><pic:cNvPr id="255954245" name="图片 1"/>'
    '<pic:cNvPicPr><a:picLocks noChangeAspect="1"/></pic:cNvPicPr></pic:nvPicPr>'
    '<pic:blipFill><a:blip r:embed="rId7"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
    f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{CX}" cy="{CY}"/></a:xfrm>'
    '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
    '</pic:pic></a:graphicData></a:graphic></wp:inline>'
)

zin = zipfile.ZipFile(SRC)
items = zin.infolist()
data = {i.filename: zin.read(i.filename) for i in items}
zin.close()

doc = data["word/document.xml"].decode("utf-8")
i = doc.find('r:embed="rId7"')
if i < 0:
    sys.exit("找不到 rId7")
s = doc.rfind("<wp:anchor", 0, i)
e = doc.find("</wp:anchor>", i) + len("</wp:anchor>")
old = doc[s:e]
assert 'r:embed="rId7"' in old and 'r:embed="rId13"' not in old and 'r:embed="rId14"' not in old
print("替换 anchor -> inline，长度", len(old), "->", len(INLINE))
doc = doc[:s] + INLINE + doc[e:]

data["word/document.xml"] = doc.encode("utf-8")
zout = zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED)
for it in items:
    zout.writestr(it, data[it.filename])
zout.close()
print("已写出:", DST)
