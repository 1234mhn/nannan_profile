# -*- coding: utf-8 -*-
"""
生成《中国研究生数学建模竞赛 论文骨架模板》Word 文档
严格遵循官方《论文格式规范》：
- 论文题目：三号黑体，居中
- 一级标题：四号黑体，居中
- 其他汉字：小四号宋体
- 行距：单倍行距
- 页脚中部：阿拉伯数字页码
- 无页眉
- 无任何身份标识信息
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ---------- 全局默认样式：小四号宋体，单倍行距 ----------
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)  # 小四
style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
pf = style.paragraph_format
pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
pf.space_before = Pt(0)
pf.space_after = Pt(0)

# ---------- 页边距（常规） ----------
sec = doc.sections[0]
sec.top_margin = Cm(2.54)
sec.bottom_margin = Cm(2.54)
sec.left_margin = Cm(3.17)
sec.right_margin = Cm(3.17)

# ---------- 页脚中部页码 ----------
def add_page_number(paragraph):
    run = paragraph.add_run()
    fld1 = OxmlElement('w:fldChar'); fld1.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'), 'preserve'); instr.text = 'PAGE'
    fld2 = OxmlElement('w:fldChar'); fld2.set(qn('w:fldCharType'), 'end')
    run._r.append(fld1); run._r.append(instr); run._r.append(fld2)
    run.font.size = Pt(10.5)
    run.font.name = 'Times New Roman'

footer = sec.footer
footer.is_linked_to_previous = False
fp = footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_page_number(fp)

# 确保无页眉内容
hdr = sec.header
hdr.is_linked_to_previous = False
for p in hdr.paragraphs:
    p.text = ''

# ---------- 辅助函数 ----------
def set_run(run, font_cn='宋体', font_en='Times New Roman', size=12, bold=False):
    run.font.name = font_en
    run.font.size = Pt(size)
    run.bold = bold
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_cn)

def add_para(text, font_cn='宋体', size=12, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT,
             first_indent=True, space_before=0, space_after=0):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if first_indent:
        p.paragraph_format.first_line_indent = Pt(size * 2)
    r = p.add_run(text)
    set_run(r, font_cn=font_cn, size=size, bold=bold)
    return p

def h1(text):
    """一级标题：四号黑体，居中；设置 outline level 1 供目录抓取"""
    p = add_para(text, font_cn='黑体', size=14, align=WD_ALIGN_PARAGRAPH.CENTER,
                 first_indent=False, space_before=12, space_after=6)
    _set_outline(p, 1)
    return p

def h2(text):
    """二级标题：小四号黑体，左对齐；设置 outline level 2"""
    p = add_para(text, font_cn='黑体', size=12, align=WD_ALIGN_PARAGRAPH.LEFT,
                 first_indent=False, space_before=6, space_after=3)
    _set_outline(p, 2)
    return p

def _set_outline(p, level):
    """写入 w:outlineLvl，使 Word 目录域能识别标题层级"""
    pPr = p._p.get_or_add_pPr()
    ol = OxmlElement('w:outlineLvl')
    ol.set(qn('w:val'), str(level - 1))
    pPr.append(ol)

def body(text):
    return add_para(text, font_cn='宋体', size=12)

def placeholder(tip):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p.paragraph_format.first_line_indent = Pt(24)
    r = p.add_run(tip)
    set_run(r, font_cn='宋体', size=12)
    r.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    return p

# ==================== 封面页 ====================
add_para('中国研究生创新实践系列大赛', font_cn='黑体', size=16, bold=False,
         align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=False, space_before=60, space_after=6)
add_para('第二十三届中国研究生数学建模竞赛', font_cn='黑体', size=16,
         align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=False, space_after=60)

add_para('学    校：____________________（按规范要求填写/遮蔽）', font_cn='宋体', size=12,
         align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=False, space_after=120)

# ==================== 摘要页 ====================
doc.add_page_break()

# 论文题目：三号黑体居中
add_para('基于XXXXXX的XXXXXX模型', font_cn='黑体', size=16,
         align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=False, space_before=6, space_after=12)

# 摘要标题（小四黑体）
add_para('摘  要', font_cn='黑体', size=12, align=WD_ALIGN_PARAGRAPH.CENTER,
         first_indent=False, space_after=6)

placeholder('【摘要写作要点】简明扼要，篇幅一般不超过两页，无需译成英文。必须包含：')
placeholder('① 建模思路  ② 主要方法  ③ 模型  ④ 结果与结论  ⑤ 创新点')
placeholder('')
placeholder('建议四段式：')
placeholder('第1段：问题背景与本文要解决的问题；')
placeholder('第2段：针对问题一/二/三分别采用了什么方法、建立了什么模型；')
placeholder('第3段：求解得到的具体结果（要有具体数字结论，不要空话）；')
placeholder('第4段：模型的创新点、优点与推广价值。')
placeholder('')
placeholder('（在此处撰写摘要正文，替换以上灰色提示文字）')

# 关键词
p = doc.add_paragraph()
p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
p.paragraph_format.space_before = Pt(12)
r = p.add_run('关键词：')
set_run(r, font_cn='黑体', size=12)
r2 = p.add_run('关键词1；关键词2；关键词3；关键词4')
set_run(r2, font_cn='宋体', size=12)

# ==================== 目录页 ====================
doc.add_page_break()

add_para('目  录', font_cn='黑体', size=14, align=WD_ALIGN_PARAGRAPH.CENTER,
         first_indent=False, space_after=12)

# 目录域：自动生成（打开后需按 F9 更新域）
def add_toc_field():
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    run = p.add_run()
    fld_begin = OxmlElement('w:fldChar'); fld_begin.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'), 'preserve')
    instr.text = r'TOC \o "1-3" \h \z \u'
    fld_sep = OxmlElement('w:fldChar'); fld_sep.set(qn('w:fldCharType'), 'separate')
    placeholder_run = OxmlElement('w:t'); placeholder_run.text = '（右键此处 → 更新域，即可自动生成目录）'
    fld_end = OxmlElement('w:fldChar'); fld_end.set(qn('w:fldCharType'), 'end')
    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_sep)
    run._r.append(placeholder_run)
    run._r.append(fld_end)
    set_run(run, font_cn='宋体', size=12)

add_toc_field()

# ==================== 正文 ====================
doc.add_page_break()

h1('一、问题重述')
h2('1.1 问题背景')
placeholder('（结合赛题，用2-3段交代问题背景，说明该问题的现实意义。）')
h2('1.2 问题提出')
placeholder('（将赛题要求拆解为若干个子问题，分点列出，例如：')
placeholder('问题一：……；问题二：……；问题三：……）')

h1('二、问题分析')
h2('2.1 对问题一的分析')
placeholder('（说明该问题的本质是什么数学问题，准备用什么思路/方法解决。）')
h2('2.2 对问题二的分析')
placeholder('（同上。建议配一张总体思路流程图，很加分。）')

h1('三、模型假设')
placeholder('（列出3-6条合理假设，每条单独一行，用编号列示。假设要与后文模型对应。）')
placeholder('假设1：……')
placeholder('假设2：……')

h1('四、符号说明')
placeholder('（用表格列出全文符号及其含义、单位。表格字体可用五号。）')

# 符号说明表格
table = doc.add_table(rows=1, cols=3)
table.style = 'Table Grid'
hdr_cells = table.rows[0].cells
for i, t in enumerate(['符号', '含义', '单位']):
    hdr_cells[i].text = ''
    rr = hdr_cells[i].paragraphs[0].add_run(t)
    set_run(rr, font_cn='黑体', size=10.5)
    hdr_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
for _ in range(4):
    row = table.add_row().cells
    for c in row:
        c.text = ''

h1('五、模型建立与求解')
h2('5.1 问题一模型的建立与求解')
placeholder('5.1.1 模型建立：说明建模思想，给出数学表达式（公式需编号）。')
placeholder('5.1.2 模型求解：说明求解算法与工具，给出求解结果（配图表）。')
h2('5.2 问题二模型的建立与求解')
placeholder('（结构同上。）')

h1('六、模型检验与灵敏度分析')
placeholder('（对关键参数做灵敏度分析，给出参数变化对结果的影响曲线/表格。）')
placeholder('这是「参与奖 vs 获奖」的分水岭，务必写。')

h1('七、模型评价与推广')
h2('7.1 模型优点')
h2('7.2 模型缺点')
h2('7.3 模型推广')

h1('八、参考文献')
placeholder('[1] 作者，书名，出版地：出版社，起止页码，出版年。')
placeholder('[2] 作者，论文名，杂志名，卷期号：起止页码，出版年。')
placeholder('[3] 作者，资源标题，网址，访问时间（年月日）。')

h1('附录')
placeholder('附录1：程序代码（如赛题要求上传源程序，按规定时间内上传竞赛系统）')
placeholder('附录2：其他支撑材料')

doc.save('/root/.openclaw/workspace/MCM_2026/数模论文骨架模板_2026.docx')
print('OK saved')
