"""把新的四行版图 1 替换进申报书 docx（替换 word/media/image1.png 字节 + 调整显示尺寸保持比例与宽度）。
原图 2230x996 RGBA，显示 5274310 x 2355850 EMU（=14.63cm x 6.53cm）。
新图 1889x1133，宽度不变，高度按比例 -> 5274310 * 1133/1889。
"""
import re, shutil, sys, zipfile

SRC = "孟浩楠-科研训练计划项目申报书-修订20261106.docx"
DST = "孟浩楠-科研训练计划项目申报书-图1已更新20261106.docx"
NEW_IMG = "figs/图1-本项目主要研究内容.png"

def main():
    from PIL import Image
    w, h = Image.open(NEW_IMG).size
    old_cx, old_cy = 5274310, 2355850
    new_cx = old_cx
    new_cy = int(old_cx * h / w)
    print(f"新图 {w}x{h} -> 显示 {new_cx} x {new_cy} EMU "
          f"({new_cx/360000:.2f}cm x {new_cy/360000:.2f}cm)")

    zin = zipfile.ZipFile(SRC)
    items = zin.infolist()
    data = {i.filename: zin.read(i.filename) for i in items}
    zin.close()

    # 1) 换图字节
    data["word/media/image1.png"] = open(NEW_IMG, "rb").read()

    # 2) 调整 document.xml 里的显示尺寸（只改围绕 rId7 的那一处）
    doc = data["word/document.xml"].decode("utf-8")
    i = doc.find('r:embed="rId7"')
    if i < 0:
        print("找不到 rId7"); sys.exit(1)
    # 向前找最近的 extent / ext
    start = doc.rfind("<wp:extent", 0, i)
    end = doc.find("/>", start) + 2
    seg = doc[start:end]
    new_seg = re.sub(r'cx="\d+"', f'cx="{new_cx}"', seg)
    new_seg = re.sub(r'cy="\d+"', f'cy="{new_cy}"', new_seg)
    doc = doc[:start] + new_seg + doc[end:]
    print("  wp:extent:", seg, "->", new_seg)

    # 之后再向后找 a:ext（同一个图片）
    start2 = doc.find("<a:ext", i)
    end2 = doc.find("/>", start2) + 2
    seg2 = doc[start2:end2]
    new_seg2 = re.sub(r'cx="\d+"', f'cx="{new_cx}"', seg2)
    new_seg2 = re.sub(r'cy="\d+"', f'cy="{new_cy}"', new_seg2)
    doc = doc[:start2] + new_seg2 + doc[end2:]
    print("  a:ext:", seg2, "->", new_seg2)

    data["word/document.xml"] = doc.encode("utf-8")

    zout = zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED)
    for it in items:
        zout.writestr(it, data[it.filename])
    zout.close()
    print("已写出:", DST)

if __name__ == "__main__":
    main()
