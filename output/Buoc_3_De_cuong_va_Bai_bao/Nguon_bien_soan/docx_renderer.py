"""Local Word rendering helpers, adapted from the existing Step 2 authoring script."""
import mistune
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
MARKDOWN=mistune.create_markdown(renderer="ast",plugins=["table","url"])
NAVY, BLUE, GRAY="183A59","245F83","526575"
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
