"""Create the template-aligned proposal and the research draft from recorded sources."""
from pathlib import Path
import importlib.util
import json
import re
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

SRC=Path(__file__).resolve().parent
BASE=SRC.parent
REFS=json.loads((SRC/'references.json').read_text())
spec=importlib.util.spec_from_file_location('docx_renderer',SRC/'docx_renderer.py')
old=importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def pagefield(p,instr,placeholder='…'):
    fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),instr)
    run=OxmlElement('w:r');t=OxmlElement('w:t');t.text=placeholder;run.append(t);fld.append(run)
    p._p.append(fld)


def common_styles(d,proposal=False):
    sec=d.sections[0]
    sec.page_width,sec.page_height=Cm(21),Cm(29.7)
    sec.top_margin,sec.bottom_margin=Cm(3.5 if proposal else 2),Cm(3 if proposal else 2)
    sec.left_margin,sec.right_margin=Cm(3.5 if proposal else 2),Cm(2)
    sec.header_distance,sec.footer_distance=Cm(1.5 if proposal else .8),Cm(.8)
    sec.different_first_page_header_footer=proposal
    n=d.styles['Normal'];n.font.name='Times New Roman';n.font.size=Pt(13 if proposal else 11.5)
    n.font.color.rgb=RGBColor.from_string('000000')
    n.paragraph_format.line_spacing=1.5 if proposal else 1.12
    n.paragraph_format.space_after=Pt(0 if proposal else 5)
    n.paragraph_format.widow_control=True
    for name,size in [('Heading 1',13 if proposal else 15),('Heading 2',13 if proposal else 13),('Heading 3',13 if proposal else 11.5)]:
        s=d.styles[name];s.font.name='Times New Roman';s.font.size=Pt(size);s.font.bold=True
        s.font.color.rgb=RGBColor.from_string('000000' if proposal else '183A59')
        s.paragraph_format.line_spacing=1.5 if proposal else 1.1
        s.paragraph_format.space_before=Pt(6 if proposal else 12)
        s.paragraph_format.space_after=Pt(3 if proposal else 6)
        s.paragraph_format.keep_with_next=True
    for name,size,font in [('TableText',13 if proposal else 9.5,'Times New Roman'),('CodeBlock',9,'Consolas'),('Equation',12,'Cambria Math'),('Caption',13 if proposal else 10,'Times New Roman'),('Reference',13 if proposal else 10.5,'Times New Roman')]:
        if name not in d.styles: s=d.styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH)
        else: s=d.styles[name]
        s.base_style=n;s.font.name=font;s.font.size=Pt(size)
        s.paragraph_format.line_spacing=1.5 if proposal else 1.05
        s.paragraph_format.space_after=Pt(0 if proposal else 4)
    d.styles['Reference'].paragraph_format.left_indent=Cm(.65)
    d.styles['Reference'].paragraph_format.first_line_indent=Cm(-.65)
    d.styles['CodeBlock'].paragraph_format.keep_together=False
    for st in d.styles:
        if st.type==WD_STYLE_TYPE.PARAGRAPH:
            rpr=st.element.get_or_add_rPr();fonts=rpr.find(qn('w:rFonts'))
            if fonts is None: fonts=OxmlElement('w:rFonts');rpr.append(fonts)
            for att in ['ascii','hAnsi','eastAsia','cs']:fonts.set(qn('w:'+att),st.font.name or 'Times New Roman')
    upd=OxmlElement('w:updateFields');upd.set(qn('w:val'),'true');d.settings.element.append(upd)
    # Restrict the proposal header to the required centred page number.
    h=sec.header.paragraphs[0];h.alignment=WD_ALIGN_PARAGRAPH.CENTER
    if not proposal:h.add_run('RESEARCH DRAFT • 15 NOVEMBER 2026 • REAL-DATA STUDY PENDING').font.size=Pt(8)
    else:pagefield(h,'PAGE','1')
    if not proposal:
        f=sec.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.CENTER
        pagefield(f,'PAGE','1');f.add_run(' / ');pagefield(f,'NUMPAGES','…')


def table(d,t,proposal):
    counter=len(d.tables)+1
    labels=['Synthesis of the fourteen studies.','Notation and domains.','Executed synthetic validation.','Planned real-data benchmarks.','Baseline comparison contract.','Evaluation dimensions and metrics.']
    label='Bảng 1. Tiến độ thực hiện dự kiến.' if proposal else f'Table {counter}. '+labels[counter-1]
    cap=d.add_paragraph(label,style='Caption')
    cap.paragraph_format.keep_with_next=True
    rows=[]
    for part in t['children']:
        if part['type']=='table_head':rows.append(part['children'])
        elif part['type']=='table_body':rows.extend(x['children'] for x in part['children'])
    if not rows:return
    n=len(rows[0]);tb=d.add_table(rows=0,cols=n);tb.style='Table Grid';tb.autofit=False
    width=15.5 if proposal else 17
    if n==2: widths=[width*.29,width*.71]
    elif n==3: widths=[width*.19,width*.41,width*.40]
    else:widths=[width/n]*n
    for c,w in enumerate(widths):tb.columns[c].width=Cm(w)
    for j,row in enumerate(rows):
        cells=tb.add_row().cells
        for c,tok in enumerate(row):
            cells[c].width=Cm(widths[c]);p=cells[c].paragraphs[0];p.style=d.styles['TableText']
            old.inline(p,tok.get('children',[]),bold=j==0)
            if j==0:old.shade(cells[c],'E6EDF3' if not proposal else 'EEEEEE')
        pr=tb.rows[-1]._tr.get_or_add_trPr()
        if j==0:pr.append(OxmlElement('w:tblHeader'))
        pr.append(OxmlElement('w:cantSplit'))


def render(d,source,proposal=False):
    for t in old.MARKDOWN(source):
        k=t['type']
        if k=='table':table(d,t,proposal)
        elif k=='block_code' and t.get('attrs',{}).get('info')=='math':
            # Editable native Word math; text notation mirrors the equations in source.
            for line in t['raw'].strip().splitlines():
                p=d.add_paragraph(style='Equation')
                if not line.strip():continue
                eq=OxmlElement('m:oMath');r=OxmlElement('m:r');text=OxmlElement('m:t');text.text=line
                r.append(text);eq.append(r);p._p.append(eq)
        else:old.render(d,[t])


def short_author(a):
    parts=a.split('; ')
    return '; '.join(parts[:2])+(' et al.' if len(parts)>2 else '')


def reference(d,ref,number=None,compact=False):
    p=d.add_paragraph(style='Reference')
    author=short_author(ref['authors']) if compact else ref['authors'].replace(';',',')
    p.add_run(f"[{number or ref['id']}] {author}. {ref['title']}. {ref['venue']}, {ref['year']}. ")
    if ref.get('doi'):old.link(p,'doi:'+ref['doi'],'https://doi.org/'+ref['doi'])
    else:old.link(p,'Nguồn chính / source',ref['url'])
    if not compact:
        p.add_run(' | ');old.link(p,'Full text / official source',ref['url'])
        p.add_run(' | Status: '+ref['status']+'.')
    return p


def cover_line(d,text,size=14,bold=False,space=0):
    p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before=Pt(space);p.paragraph_format.space_after=Pt(0)
    p.paragraph_format.line_spacing=1.5
    r=p.add_run(text);r.font.name='Times New Roman';r.font.size=Pt(size);r.bold=bold
    return p


def proposal():
    d=Document();common_styles(d,True)
    d.core_properties.title='Đề cương luận văn thạc sĩ – Tái xếp hạng gợi ý đa mục tiêu'
    d.core_properties.author='Nguyễn Minh Huy';d.core_properties.language='vi-VN'
    cover_line(d,'TRƯỜNG ĐẠI HỌC THỦY LỢI',14,True)
    cover_line(d,'--------o0o---------',14)
    cover_line(d,'ĐỀ CƯƠNG\nLUẬN VĂN THẠC SĨ',14,True,24)
    cover_line(d,'TÁI XẾP HẠNG GỢI Ý ĐA MỤC TIÊU\nVỚI KIỂM CHỨNG TÍNH KHẢ THI\nDƯỚI BẤT ĐỊNH ĐỘ PHỔ BIẾN',16,True,18)
    cover_line(d,'Học viên cao học: Nguyễn Minh Huy\nLớp: ………………………\nMã số học viên: ………………………\nNgành đào tạo: Công nghệ thông tin\nMã ngành: ………………………',14,False,18)
    cover_line(d,'NGƯỜI HƯỚNG DẪN:\n1. Người hướng dẫn chính: ………………………\n2. Người hướng dẫn phụ: ………………………',14,False,18)
    cover_line(d,'ĐƠN VỊ QUẢN LÝ:\nPHÂN HIỆU TRƯỜNG ĐẠI HỌC THỦY LỢI',14,True,18)
    cover_line(d,'Tp.HCM, năm …………',14,False,18)
    d.add_page_break();d.add_heading('MỤC LỤC',1)
    toc=[('PHẦN I. ĐĂNG KÝ ĐỀ TÀI LUẬN VĂN THẠC SĨ',0),('I. HỌC VIÊN',1),('II. NGƯỜI HƯỚNG DẪN',1),('III. THÔNG TIN VỀ ĐỀ TÀI',1),('PHẦN II. NỘI DUNG ĐỀ CƯƠNG CHI TIẾT',0),('1. MỞ ĐẦU',1),('1.1. Tính cấp thiết của đề tài',2),('1.2. Mục đích và nhiệm vụ nghiên cứu',2),('1.3. Đối tượng và phạm vi nghiên cứu',2),('1.4. Cách tiếp cận và phương pháp nghiên cứu',2),('1.5. Ý nghĩa khoa học và thực tiễn',2),('1.6. Kết quả dự kiến',2),('2. DỰ KIẾN BỐ CỤC LUẬN VĂN',1),('3. TIẾN ĐỘ THỰC HIỆN DỰ KIẾN',1),('Ý KIẾN CỦA CÁC ĐƠN VỊ VÀ NGƯỜI HƯỚNG DẪN',0),('TÀI LIỆU THAM KHẢO',0)]
    toc_pars=[]
    for label,level in toc:
        p=d.add_paragraph(label+'  ');p.paragraph_format.left_indent=Cm(.4*level)
        toc_pars.append(p)
    d.add_page_break();render(d,(SRC/'de_cuong.md').read_text(),True)
    d.add_page_break();d.add_heading('TÀI LIỆU THAM KHẢO',1)
    selected=list(range(1,15))+[19,20,22,30,32,33,35]
    # Proposal citations are local [1–21]; the paper preserves source IDs [1–37].
    for num,rid in enumerate(selected,1):
        if num==11:d.add_page_break();d.add_heading('TÀI LIỆU THAM KHẢO (tiếp)',1)
        reference(d,REFS[rid-1],num,compact=True)
    for idx,((label,_),p) in enumerate(zip(toc,toc_pars),1):
        match=next((q for q in d.paragraphs if q.style.name.startswith('Heading') and q.text==label),None)
        if match is None:raise ValueError('Missing template heading '+label)
        start=OxmlElement('w:bookmarkStart');start.set(qn('w:id'),str(idx));start.set(qn('w:name'),'Sec'+str(idx))
        end=OxmlElement('w:bookmarkEnd');end.set(qn('w:id'),str(idx))
        match._p.insert(0,start);match._p.append(end);pagefield(p,'PAGEREF Sec'+str(idx)+' \\h')
    path=BASE/'01_De_cuong_Luan_van_Thac_si.docx';d.save(path)
    return path


def paper():
    d=Document();common_styles(d)
    title='Scenario-Coupled Feasibility Audits for Multi-Objective Recommendation Re-ranking under Popularity Uncertainty'
    d.core_properties.title=title;d.core_properties.language='en-US';d.core_properties.author='Author information to be confirmed'
    source='\n\n'.join((SRC/f).read_text() for f in ['paper_intro.md','paper_method.md','paper_experiments.md'])
    render(d,source)
    # Place the empirical figure next to executed results, using recorded data only.
    fig=BASE/'Kiem_tra/bound_comparison.png'
    if fig.exists():
        anchor=next(p for p in d.paragraphs if p.text.startswith('The additional ten rejections'))
        pic=d.add_paragraph();pic.alignment=WD_ALIGN_PARAGRAPH.CENTER;pic.add_run().add_picture(str(fig),width=Cm(15.8))
        caption=d.add_paragraph('Figure 1. Structural minimum CVaR versus necessary lower bounds for 240 synthetic prefixes. The identity line indicates an exact bound; points below it reflect relaxation gaps. This figure measures bound strength, not speed.',style='Caption')
        anchor._p.addprevious(pic._p);pic._p.addnext(caption._p)
    d.add_page_break();d.add_heading('References',1)
    d.add_paragraph('Numeric references correspond to citations in this draft. Links and publication status were checked during preparation through 15 November 2026; preprint/workshop records are explicitly labeled. The first fourteen are the original synthesis corpus.')
    for r in REFS:reference(d,r)
    d.add_page_break();d.add_heading('Appendix A. Source-to-contribution and code map',1)
    d.add_paragraph('The following are external author/toolkit repositories from the source corpus. They are pointers, not a claim that every complete repository was downloaded or rerun. The delivered Step 3 simulation is our own finite-instance prototype. See the Step 2 SOURCE notes for inspected excerpts and missing files.')
    for r in REFS[:14]:
        p=d.add_paragraph();p.add_run(f"[{r['id']}] {r['title']} — ").bold=True
        if r.get('code'):old.link(p,'Author / official code',r['code'])
        else:p.add_run('No verified official code recorded.')
        p.add_run(' | ');old.link(p,'Paper',r['url'])
    d.add_heading('Appendix B. Artifact and implementation contract',1)
    d.add_paragraph('Input provenance: manifest_14_word.json records the fourteen ingested Word files and their SHA-256 hashes. Mathematical development and experiment design are in the editable Markdown sources. The synthetic study retains its seed, inputs, primal metrics, numerical solver evidence, and code hashes. No user-level benchmark interaction files or third-party full repositories are bundled in this Step 3 archive.')
    render(d,'```text\ncd Mo_phong\npython3 -m unittest test_core -v\npython3 run_study.py\n```')
    d.add_paragraph('Dependencies for executed simulation: Python 3.14.3, NumPy 2.4.4, SciPy 1.17.1. The code has enumeration and MILP backends. Full-data preprocessing, BPR/LightGCN training, original-baseline reproduction, deadline scheduling, and resource measurement remain implementation steps for the proposed real-data study.')
    d.add_paragraph('To use the MILP completion backend: import core; call core.wcr(instance, oracle=lambda prefix: core.milp_oracle(instance, prefix=prefix, time_limit=10)). A per-call limit is not a total batch deadline. Inspect and record UNKNOWN, infeasibility evidence and any feasible incumbent; never label a timed-out unverified ranking as certified.')
    path=BASE/'02_Du_thao_Bai_bao_WCR.docx';d.save(path)
    return path


if __name__=='__main__':
    for p in [proposal(),paper()]:print(p.name,p.stat().st_size)
