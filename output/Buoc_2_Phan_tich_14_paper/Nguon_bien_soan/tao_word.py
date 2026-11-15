"""Build the separate Vietnamese study guides; no research code is executed."""
from __future__ import annotations

import json
import re
from pathlib import Path

import mistune
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

BASE = Path(__file__).resolve().parent.parent
PAPERS = json.loads((BASE / "danh_muc_nguon.json").read_text())
MARKDOWN = mistune.create_markdown(renderer="ast", plugins=["table", "url"])
NAVY, BLUE, GRAY = "183A59", "245F83", "526575"


def field(paragraph, instruction):
    el = OxmlElement("w:fldSimple")
    el.set(qn("w:instr"), instruction)
    paragraph._p.append(el)


def link(p, label, url):
    el = OxmlElement("w:hyperlink")
    rel = p.part.relate_to(url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True)
    el.set(qn("r:id"), rel)
    run = OxmlElement("w:r")
    pr = OxmlElement("w:rPr")
    c = OxmlElement("w:color")
    c.set(qn("w:val"), BLUE)
    pr.append(c)
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    pr.append(u)
    run.append(pr)
    t = OxmlElement("w:t")
    t.text = label
    run.append(t)
    el.append(run)
    p._p.append(el)


def plain(tokens):
    return "".join(t.get("raw", "") if "raw" in t else plain(t.get("children", [])) for t in tokens)


def inline(p, tokens, bold=False, italic=False):
    for t in tokens:
        kind = t["type"]
        if kind in ["strong", "emphasis"]:
            inline(p, t.get("children", []), bold or kind == "strong", italic or kind == "emphasis")
        elif kind == "link":
            link(p, plain(t.get("children", [])), t["attrs"]["url"])
        elif kind in ["softbreak", "linebreak"]:
            p.add_run(" " if kind == "softbreak" else "\n")
        elif kind == "codespan":
            r = p.add_run(t["raw"])
            r.font.name = "Consolas"
            r.font.size = Pt(10)
            r.bold = bold
        elif kind in ["text", "inline_html"]:
            r = p.add_run(t.get("raw", ""))
            r.bold, r.italic = bold, italic
        elif "children" in t:
            inline(p, t["children"], bold, italic)
        else:
            p.add_run(t.get("raw", ""))


def shade(element, color):
    target = element._tc.get_or_add_tcPr() if hasattr(element, "_tc") else element._p.get_or_add_pPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:fill"), color)
    target.append(sh)


def render_table(doc, token):
    rows = []
    for part in token["children"]:
        if part["type"] == "table_head":
            rows.append(part["children"])
        elif part["type"] == "table_body":
            rows.extend(row["children"] for row in part["children"])
    if not rows:
        return
    n = len(rows[0])
    table = doc.add_table(rows=0, cols=n)
    table.style, table.autofit = "Table Grid", False
    lengths = [max(len(plain(row[c].get("children", []))) for row in rows) for c in range(n)]
    weights = [max(12, min(75, x)) ** .5 for x in lengths]
    widths = [17*w/sum(weights) for w in weights]
    for c, w in enumerate(widths):
        table.columns[c].width = Cm(w)
    for ri, values in enumerate(rows):
        cells = table.add_row().cells
        for ci, value in enumerate(values):
            cells[ci].width = Cm(widths[ci])
            cells[ci].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cells[ci].paragraphs[0]
            p.style = doc.styles["TableText"]
            inline(p, value.get("children", []), bold=ri == 0)
            if ri == 0:
                shade(cells[ci], NAVY)
                for r in p.runs:
                    r.font.color.rgb = RGBColor.from_string("FFFFFF")
            elif ri % 2 == 0:
                shade(cells[ci], "F0F5F8")
        pr = table.rows[-1]._tr.get_or_add_trPr()
        if ri == 0:
            repeat = OxmlElement("w:tblHeader")
            pr.append(repeat)
        no_split = OxmlElement("w:cantSplit")
        pr.append(no_split)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def render(doc, tokens, shift=0, depth=0):
    for t in tokens:
        kind = t["type"]
        if kind == "heading":
            level = max(1, min(3, t["attrs"]["level"]-shift))
            p = doc.add_heading(level=level)
            inline(p, t["children"])
        elif kind in ["paragraph", "block_text"]:
            p = doc.add_paragraph()
            inline(p, t.get("children", []))
        elif kind == "list":
            ordered = t.get("attrs", {}).get("ordered", False)
            for item in t.get("children", []):
                children = item.get("children", [])
                for j, child in enumerate(children):
                    if child["type"] in ["paragraph", "block_text"]:
                        p = doc.add_paragraph(style="List Number" if ordered else "List Bullet")
                        p.paragraph_format.left_indent = Cm(.5+.35*depth)
                        inline(p, child.get("children", []))
                    else:
                        render(doc, [child], shift, depth+1)
        elif kind == "block_code":
            p = doc.add_paragraph(style="CodeBlock")
            content = t.get("raw", "").rstrip("\n")
            p.add_run(content)
            p.paragraph_format.keep_together = len(content.splitlines()) <= 20
            shade(p, "F1F4F7")
        elif kind == "table":
            render_table(doc, t)
        elif kind == "block_quote":
            start = len(doc.paragraphs)
            render(doc, t.get("children", []), shift, depth)
            for p in doc.paragraphs[start:]:
                p.paragraph_format.left_indent = Cm(.5)
                shade(p, "F1F5F8")
        elif kind == "thematic_break":
            doc.add_paragraph("────────────────────────────────")
        elif kind == "block_html":
            raw = t.get("raw", "")
            if "pagebreak" in raw:
                doc.add_page_break()
            else:
                doc.add_paragraph(raw)
        elif kind != "blank_line":
            if "children" in t:
                render(doc, t["children"], shift, depth)
            elif t.get("raw"):
                doc.add_paragraph(t["raw"])


def styles(doc):
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.top_margin, s.bottom_margin = Cm(1.8), Cm(1.8)
    s.left_margin, s.right_margin = Cm(2), Cm(2)
    s.header_distance, s.footer_distance = Cm(.65), Cm(.65)
    s.different_first_page_header_footer = True
    n = doc.styles["Normal"]
    n.font.name, n.font.size = "Times New Roman", Pt(11.5)
    n.font.color.rgb = RGBColor.from_string("202D38")
    n.paragraph_format.line_spacing, n.paragraph_format.space_after = 1.1, Pt(6)
    n.paragraph_format.widow_control = True
    for name, size in [("Heading 1", 14), ("Heading 2", 12.5), ("Heading 3", 11.5)]:
        st = doc.styles[name]
        st.font.name, st.font.size, st.font.bold = "Times New Roman", Pt(size), True
        st.font.color.rgb = RGBColor.from_string(NAVY)
        st.paragraph_format.keep_with_next = True
        st.paragraph_format.space_before, st.paragraph_format.space_after = Pt(12), Pt(6)
    for name, size, font in [("Meta", 10, "Arial"), ("TableText", 10, "Times New Roman"),
                             ("CodeBlock", 9, "Consolas"), ("CoverTitle", 19, "Arial")]:
        st = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        st.base_style = n
        st.font.name, st.font.size = font, Pt(size)
        st.paragraph_format.line_spacing = 1.05
        st.paragraph_format.space_after = Pt(5)
    doc.styles["CoverTitle"].font.bold = True
    doc.styles["CoverTitle"].font.color.rgb = RGBColor.from_string(NAVY)
    doc.styles["Meta"].font.color.rgb = RGBColor.from_string(GRAY)
    for st in doc.styles:
        if st.type == WD_STYLE_TYPE.PARAGRAPH:
            prop = st.element.get_or_add_rPr()
            lang = OxmlElement("w:lang")
            lang.set(qn("w:val"), "vi-VN")
            prop.append(lang)


def build(paper, path):
    doc = Document()
    styles(doc)
    doc.core_properties.title = paper["title"] + " — Hướng dẫn đọc và tái lập"
    doc.core_properties.subject = "Bước 2 / CSE631 / Multi-objective recommendation reranking"
    doc.core_properties.author = "Tài liệu học tập CSE631 – Hỗ trợ phân tích bài báo"
    doc.core_properties.language = "vi-VN"
    doc.core_properties.keywords = "paper analysis, beginner tutorial, recommender systems, reranking"
    h = doc.sections[0].header.paragraphs[0]
    h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = h.add_run(f"CSE631 • BƯỚC 2 • PAPER {paper['id']:02d} • {paper['short']}")
    r.font.name, r.font.size = "Arial", Pt(8)
    r.font.color.rgb = RGBColor.from_string(GRAY)
    f = doc.sections[0].footer.paragraphs[0]
    f.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f.add_run(f"Paper {paper['id']:02d}  •  ")
    field(f, "PAGE")
    f.add_run(" / ")
    field(f, "NUMPAGES")
    f.add_run("  •  Biên soạn 15/11/2026")
    for r in f.runs:
        r.font.size = Pt(9)
    p = doc.add_paragraph("CSE631  |  ĐỀ TÀI 07  |  BƯỚC 2", style="Meta")
    p.paragraph_format.space_after = Pt(25)
    doc.add_paragraph(f"PAPER {paper['id']:02d}\nĐỌC, HIỂU VÀ PHÂN TÍCH", style="CoverTitle")
    p = doc.add_paragraph(paper["title"], style="CoverTitle")
    p.paragraph_format.space_before = Pt(12)
    doc.add_paragraph(paper["authors"], style="Meta")
    doc.add_paragraph(paper["venue"], style="Meta")
    p = doc.add_paragraph(style="Meta")
    if paper.get("doi"):
        link(p, "DOI: "+paper["doi"], "https://doi.org/"+paper["doi"])
        p.add_run("  |  ")
    link(p, "Bài/toàn văn", paper["paper"])
    p.add_run("  |  ")
    link(p, "Code chính thức", paper["code"])
    p = doc.add_paragraph("Hướng dẫn tiếng Việt cho người mới bắt đầu")
    p.paragraph_format.space_before = Pt(25)
    p.runs[0].bold = True
    doc.add_paragraph("Từ bài toán, định nghĩa và công thức đến mã giả, ví dụ số, đọc code, thực nghiệm và hướng phát triển luận văn.")
    doc.add_paragraph("Ngữ cảnh: accuracy–diversity–exposure balanced reranking; điều kiện dự kiến máy 16 GB RAM.", style="Meta")
    p = doc.add_paragraph("Phạm vi kiểm chứng", style="Heading 2")
    doc.add_paragraph("Đọc tài liệu và mã nguồn truy cập được; chạy các ví dụ giảng giải nhỏ. Chưa huấn luyện lại hoặc tái lập đầy đủ benchmark gốc. Ví dụ tự xây dựng và nhận xét độc lập được ghi nhãn trong nội dung.", style="Meta")
    doc.add_paragraph("Các tệp mã kèm theo là phần đã đọc/trích xuất qua web; xem SOURCE.md để biết phần thiếu và link repo đầy đủ. Tài liệu không thay thế bài gốc và điều kiện sử dụng dữ liệu/mã nguồn.", style="Meta")
    doc.add_page_break()
    source = path.read_text()
    ast = MARKDOWN(source)
    shift = 0
    if ast and ast[0]["type"] == "heading" and re.match(r"^\d{2}\.", plain(ast[0].get("children", []))):
        ast = ast[1:]
        shift = 1
    render(doc, ast, shift)
    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    doc.settings.element.append(update)
    target = BASE / (path.stem + ".docx")
    doc.save(target)
    return {"id":paper["id"], "file":target.name, "words":len(source.split()),
            "tables":len(doc.tables), "bytes":target.stat().st_size,
            "headings":sum(1 for p in doc.paragraphs if p.style.name.startswith("Heading"))}


if __name__ == "__main__":
    result = []
    for paper in PAPERS:
        paths = list((BASE / "Nguon_bien_soan").glob(f"{paper['id']:02d}_*.md"))
        if len(paths) != 1:
            raise RuntimeError(f"Expected one guide for paper {paper['id']}, found {paths}")
        result.append(build(paper, paths[0]))
    (BASE / "thong_ke_tai_lieu.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
