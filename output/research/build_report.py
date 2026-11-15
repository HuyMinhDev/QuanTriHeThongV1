from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent
PAPERS = json.loads((ROOT / "papers.json").read_text())
DOCX = OUT / "Tong_quan_14_bai_bao_MultiObjective_Recsys_2026.docx"
NAVY = "17365D"
BLUE = "245B81"
GRAY = "586575"


def shade(cell, color):
    el = OxmlElement("w:shd")
    el.set(qn("w:fill"), color)
    cell._tc.get_or_add_tcPr().append(el)


def lang(style, code="vi-VN"):
    rpr = style.element.get_or_add_rPr()
    item = OxmlElement("w:lang")
    item.set(qn("w:val"), code)
    rpr.append(item)


def hyperlink(p, text, url):
    link = OxmlElement("w:hyperlink")
    rel = p.part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    link.set(qn("r:id"), rel)
    run = OxmlElement("w:r")
    props = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), BLUE)
    props.append(color)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    props.append(underline)
    run.append(props)
    t = OxmlElement("w:t")
    t.text = text
    run.append(t)
    link.append(run)
    p._p.append(link)


INLINE = re.compile(r"(\[[^\]]+\]\([^\)]+\)|\*\*[^*]+\*\*|https?://[^\s]+)")


def inline(p, text):
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("[") and "](" in part and part.endswith(")"):
            label, url = part[1:-1].split("](", 1)
            hyperlink(p, label, url)
        elif part.startswith("**") and part.endswith("**"):
            p.add_run(part[2:-2]).bold = True
        elif part.startswith("http"):
            url = part.rstrip(".;,。")
            hyperlink(p, url, url)
            if url != part:
                p.add_run(part[len(url):])
        else:
            p.add_run(part)


def paragraph(text="", style=None):
    p = doc.add_paragraph(style=style)
    inline(p, text)
    return p


def table(rows):
    t = doc.add_table(rows=1, cols=len(rows[0]))
    t.style = "Table Grid"
    t.autofit = False
    widths = {
        2: [5.1, 11.9],
        3: [3.6, 5.8, 7.6],
        4: [1.2, 3.7, 6.2, 5.9],
    }.get(len(rows[0]), [17 / len(rows[0])] * len(rows[0]))
    for i, w in enumerate(widths):
        t.columns[i].width = Cm(w)
    for ri, values in enumerate(rows):
        cells = t.rows[0].cells if ri == 0 else t.add_row().cells
        for ci, value in enumerate(values):
            cells[ci].width = Cm(widths[ci])
            cells[ci].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cells[ci].paragraphs[0]
            p.style = doc.styles["TableText"]
            inline(p, value.strip())
            if ri == 0:
                shade(cells[ci], NAVY)
                for run in p.runs:
                    run.bold = True
                    run.font.color.rgb = RGBColor.from_string("FFFFFF")
            elif ri % 2 == 0:
                shade(cells[ci], "F1F5F8")
        trpr = t.rows[ri]._tr.get_or_add_trPr()
        no_split = OxmlElement("w:cantSplit")
        trpr.append(no_split)
        if ri == 0:
            header = OxmlElement("w:tblHeader")
            trpr.append(header)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def md(text):
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line == "<pagebreak>":
            doc.add_page_break()
            i += 1
            continue
        if line == "<mainrefs>":
            for a in PAPERS:
                ref = f"[{a['id']}] {a['authors'].replace(';', ',')}, “{a['title']},” {a['venue']}."
                p = paragraph(ref, "Reference")
                if a["doi"]:
                    p.add_run(" DOI: ")
                    hyperlink(p, a["doi"], "https://doi.org/" + a["doi"])
                    p.add_run(". ")
                else:
                    p.add_run(" ")
                hyperlink(p, "Bài/toàn văn", a["paper"])
                p.add_run(". ")
                hyperlink(p, "Code", a["code"])
                p.add_run(".")
            i += 1
            continue
        if line.startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                content = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"[:\- ]+", x or " ") for x in content):
                    block.append(content)
                i += 1
            if block:
                table(block)
            continue
        match = re.match(r"^(#{1,3})\s+(.*)", line)
        if match:
            doc.add_heading(match[2], level=len(match[1]))
            i += 1
            continue
        if line.startswith("- "):
            paragraph(line[2:], "List Bullet")
            i += 1
            continue
        chunk = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "- ", "<")):
            chunk.append(lines[i].strip())
            i += 1
        paragraph(" ".join(chunk), "Reference" if re.match(r"^\[\d+\]", line) else None)


doc = Document()
section = doc.sections[0]
section.page_width, section.page_height = Cm(21), Cm(29.7)
section.top_margin, section.bottom_margin = Cm(1.8), Cm(1.8)
section.left_margin, section.right_margin = Cm(2), Cm(2)
section.header_distance, section.footer_distance = Cm(0.65), Cm(0.7)

normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(11.5)
normal.font.color.rgb = RGBColor.from_string("202A35")
normal.paragraph_format.line_spacing = 1.10
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.widow_control = True
lang(normal)

for name, size, color in [("Heading 1", 16, NAVY), ("Heading 2", 13, BLUE), ("Heading 3", 12, BLUE)]:
    style = doc.styles[name]
    style.font.name = "Times New Roman"
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor.from_string(color)
    style.paragraph_format.space_before = Pt(11)
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.keep_with_next = True
    lang(style)

for name, size in [("CardText", 11), ("TableText", 10), ("Reference", 10.5), ("Meta", 10), ("PaperTitle", 13)]:
    style = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    style.base_style = normal
    style.font.size = Pt(size)
    style.paragraph_format.line_spacing = 1.04 if name == "CardText" else 1.08
    style.paragraph_format.space_after = Pt(5 if name != "TableText" else 3)
    lang(style)
doc.styles["PaperTitle"].font.bold = True
doc.styles["PaperTitle"].font.color.rgb = RGBColor.from_string(NAVY)
doc.styles["PaperTitle"].paragraph_format.keep_with_next = True
doc.styles["Meta"].font.color.rgb = RGBColor.from_string(GRAY)
doc.styles["Reference"].paragraph_format.space_after = Pt(7)

header = section.header.paragraphs[0]
header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = header.add_run("CSE631 • ĐỀ TÀI 07 • KHẢO SÁT VÀ THIẾT KẾ NGHIÊN CỨU")
r.font.name = "Arial"
r.font.size = Pt(8)
r.font.color.rgb = RGBColor.from_string(GRAY)
footer = section.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = footer.add_run("Rà soát 15/11/2026  •  ")
r.font.size = Pt(9)
field = OxmlElement("w:fldSimple")
field.set(qn("w:instr"), "PAGE")
footer._p.append(field)
section.different_first_page_header_footer = True

doc.core_properties.title = "Khảo sát 14 bài báo và định hướng luận văn hệ gợi ý đa mục tiêu"
doc.core_properties.subject = "Accuracy–Diversity–Exposure Balanced Re-ranking"
doc.core_properties.author = "Tài liệu nghiên cứu hỗ trợ người học"
doc.core_properties.keywords = "recommender systems, reranking, diversity, exposure fairness, multi-objective, CSE631"
doc.core_properties.language = "vi-VN"

paragraph("CSE631  |  ĐỀ TÀI 07", "Meta")
doc.add_paragraph().paragraph_format.space_after = Pt(25)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(12)
for line in ["KHẢO SÁT BÀI BÁO", "VÀ ĐỊNH HƯỚNG LUẬN VĂN"]:
    r = p.add_run(line + "\n")
    r.font.name = "Arial"
    r.font.size = Pt(23)
    r.bold = True
    r.font.color.rgb = RGBColor.from_string(NAVY)
paragraph("Hệ gợi ý đa mục tiêu cân bằng độ chính xác, đa dạng và công bằng hiển thị sản phẩm", "PaperTitle")
paragraph("Accuracy–Diversity–Exposure Balanced Re-ranking", "Meta")
doc.add_paragraph().paragraph_format.space_after = Pt(14)
p = paragraph("14 công trình trọng tâm 2025–2026", "PaperTitle")
paragraph("Bài gốc và mã nguồn • Thiết lập thực nghiệm • Kết quả và hạn chế\nHướng đóng góp mới • Giao thức đánh giá • Tài liệu tham khảo")
doc.add_paragraph().paragraph_format.space_after = Pt(12)
table([
    ["Phạm vi", "Thông tin"],
    ["Tài liệu đầu vào", "CSE631_DeTai_07_MultiObjective_Recsys.pdf, 11 trang"],
    ["Điều kiện nghiên cứu", "Máy 16 GB RAM; MovieLens và dữ liệu sản phẩm bổ sung"],
    ["Ngày rà soát", "15/11/2026"],
    ["Trạng thái", "Khảo sát có kiểm tra nguồn; chưa chạy tái lập mã nguồn"],
])
paragraph("Tài liệu phục vụ chọn hướng luận văn cao học và chuẩn bị nghiên cứu có thể phát triển thành paper. Tính mới và hiệu quả của hướng đề xuất cần được xác lập bằng đối sánh và thực nghiệm.", "Meta")

doc.add_page_break()
md((ROOT / "report_intro.md").read_text())

labels = [
    ("problem", "Bài toán và phương pháp"),
    ("data", "Dữ liệu và protocol"),
    ("baselines", "Baselines"),
    ("metrics", "Phép đo"),
    ("result", "Kết quả đã công bố"),
    ("environment", "Ngôn ngữ, code và môi trường"),
    ("limit", "Hạn chế và phạm vi kết luận"),
    ("extension", "Hướng cải tiến đề xuất"),
    ("audit", "Điểm cần kiểm tra khi tái lập"),
]
card_markdown = []
for a in PAPERS:
    doc.add_page_break()
    doc.add_heading(f"3.{a['id']}. [{a['id']}] {a['short']}", level=2)
    paragraph(a["title"], "PaperTitle")
    paragraph(a["authors"], "Meta")
    paragraph(a["venue"], "Meta")
    p = doc.add_paragraph(style="Meta")
    if a["doi"]:
        hyperlink(p, "DOI: " + a["doi"], "https://doi.org/" + a["doi"])
        p.add_run("  |  ")
    hyperlink(p, "Bài/toàn văn", a["paper"])
    p.add_run("  |  ")
    hyperlink(p, "Code chính thức", a["code"])
    paragraph("**Vai trò:** " + a["role"], "CardText")
    for key, label in labels:
        paragraph(f"**{label}:** {a[key]}", "CardText")
    card_markdown.extend([
        "<pagebreak>", f"## 3.{a['id']}. [{a['id']}] {a['short']}",
        "**" + a["title"] + "**", a["authors"], a["venue"],
        f"[Bài/toàn văn]({a['paper']}) | [Code]({a['code']})",
        *[f"**{label}:** {a[key]}" for key, label in labels],
    ])

for name in ["report_methods.md", "report_directions.md", "report_references.md"]:
    md((ROOT / name).read_text())

settings = doc.settings.element
update = OxmlElement("w:updateFields")
update.set(qn("w:val"), "true")
settings.append(update)
doc.save(DOCX)

with (ROOT / "danh_muc_bai_bao.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(PAPERS[0]))
    writer.writeheader()
    writer.writerows(PAPERS)

source = (ROOT / "report_intro.md").read_text() + "\n\n" + "\n\n".join(card_markdown)
source += "\n\n" + (ROOT / "report_methods.md").read_text()
source += "\n\n" + (ROOT / "report_directions.md").read_text()
refs = (ROOT / "report_references.md").read_text()
main_refs = []
for a in PAPERS:
    main_refs.append(f"[{a['id']}] {a['authors']}. {a['title']}. {a['venue']}. DOI: {a['doi'] or 'không gán DOI'}. [Bài]({a['paper']}). [Code]({a['code']}).")
source += "\n\n" + refs.replace("<mainrefs>", "\n\n".join(main_refs))
(ROOT / "bao_cao_nguon.md").write_text(source)

print(json.dumps({"file": str(DOCX), "bytes": DOCX.stat().st_size,
                  "papers": len(PAPERS), "words_source": len(source.split()),
                  "tables": len(doc.tables), "paragraphs": len(doc.paragraphs)}, ensure_ascii=False, indent=2))
