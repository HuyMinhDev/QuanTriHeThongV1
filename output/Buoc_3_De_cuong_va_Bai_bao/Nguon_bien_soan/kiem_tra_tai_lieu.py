"""Validate deliverable structure, provenance, citations, and template settings."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from docx import Document

BASE=Path(__file__).resolve().parent.parent
SRC=BASE/'Nguon_bien_soan'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
checks=[]


def check(name,condition,detail=None):
    if not condition:raise AssertionError(name+': '+str(detail))
    checks.append({'check':name,'passed':True,'detail':detail})


def citations(source):
    out=set()
    for match in re.finditer(r'\[(\d+(?:(?:,|–|-)\d+)*)\]',source):
        raw=match.group(1)
        # Numeric intervals used as equation domains are not citations.
        if raw=='0,1':continue
        for piece in raw.split(','):
            if '–' in piece or '-' in piece:
                a,b=re.split('[–-]',piece);out.update(range(int(a),int(b)+1))
            else:out.add(int(piece))
    return out


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    refs=json.loads((SRC/'references.json').read_text())
    check('37 distinct real-source records',len(refs)==37 and len({r['id'] for r in refs})==37)
    check('reference titles, authors and source URLs populated',all(r['title'] and r['authors'] and r['url'].startswith('https://') for r in refs))
    paper='\n'.join((SRC/f).read_text() for f in ['paper_intro.md','paper_method.md','paper_experiments.md'])
    pc=citations(paper)
    check('paper citations resolve and all bibliography records used',pc==set(range(1,38)),sorted(pc))
    pr=citations((SRC/'de_cuong.md').read_text())
    check('proposal citations resolve to local bibliography',pr==set(range(1,22)),sorted(pr))
    check('no unresolved work markers/internal web IDs in narrative',not re.search(r'TODO|FIXME|turn\d+(?:search|view)|cite',paper))
    manifest=json.loads((SRC/'manifest_14_word.json').read_text())
    check('fourteen ingested Word inputs',len(manifest)==14)
    for r in manifest:
        original=Path(r['file']);copied=BASE/'Tai_lieu_dau_vao_14_Word'/original.name
        check('input hash '+original.name,r['sha256']==sha(copied) and (not original.exists() or sha(original)==r['sha256']))
    template=Path('spec/Mau-trinh-bay-de-cuong-LV-PH-2022.doc')
    if template.exists():check('user template copied unchanged',sha(template)==sha(SRC/template.name))
    docs=[]
    for name in ['01_De_cuong_Luan_van_Thac_si.docx','02_Du_thao_Bai_bao_WCR.docx']:
        path=BASE/name
        with ZipFile(path) as z:
            check(name+' ZIP integrity',z.testzip() is None)
            xmls=[n for n in z.namelist() if n.endswith('.xml') or n.endswith('.rels')]
            for n in xmls:ET.fromstring(z.read(n))
            root=ET.fromstring(z.read('word/document.xml'))
            text=' '.join(t.text or '' for t in root.findall('.//w:t',NS)+root.findall('.//m:t',NS))
            links=[n for n in z.namelist() if n.endswith('.rels')]
            external=sum(z.read(n).count(b'TargetMode="External"') for n in links)
            check(name+' external paper/source links',external>=21,external)
            check(name+' substantial narrative',len(text.split())>1500,len(text.split()))
            if name.startswith('01'):
                mar=root.find('.//w:pgMar',NS)
                expected={'top':1984,'bottom':1701,'left':1984,'right':1134}
                check('template margins match within 1 twip',all(abs(int(mar.attrib['{'+NS['w']+'}'+k])-v)<=1 for k,v in expected.items()))
                st=ET.fromstring(z.read('word/styles.xml'))
                normal=st.find(".//w:style[@w:styleId='Normal']",NS)
                check('template TNR 13',normal.find('.//w:rFonts',NS).attrib['{'+NS['w']+'}ascii']=='Times New Roman' and normal.find('.//w:sz',NS).attrib['{'+NS['w']+'}val']=='26')
                check('template 1.5 line spacing',normal.find('.//w:spacing',NS).attrib['{'+NS['w']+'}line']=='360')
                head=ET.fromstring(z.read('word/header1.xml'))
                check('top-centred page number only',head.find('.//w:jc',NS).attrib['{'+NS['w']+'}val']=='center' and len(head.findall('.//w:fldSimple',NS))==1 and head.find('.//w:fldSimple',NS).attrib['{'+NS['w']+'}instr']=='PAGE')
                for entry in [n for n in z.namelist() if re.match(r'word/footer\d+.xml',n)]:
                    footer=ET.fromstring(z.read(entry));check('empty proposal footer '+entry,not footer.findall('.//w:t',NS))
                check('16 linked contents page fields',len([x for x in root.findall('.//w:fldSimple',NS) if x.attrib.get('{'+NS['w']+'}instr','').startswith('PAGEREF')])==16)
                check('cover body 14/title 16 present',root.find(".//w:sz[@w:val='32']",NS) is not None and root.find(".//w:sz[@w:val='28']",NS) is not None)
            else:
                math_text=' '.join(t.text or '' for t in root.findall('.//m:t',NS))
                eqnos={int(x) for x in re.findall(r'\((\d+)\)',math_text)}
                check('all fourteen numbered equations present as editable Word math',set(range(1,15))<=eqnos,{'numbers':sorted(eqnos),'math_objects':len(root.findall('.//m:oMath',NS))})
                check('executed-results figure embedded',any(n.startswith('word/media/') for n in z.namelist()))
                check('explicit real-data evidence boundary','not yet executed' in text.lower() and 'UNKNOWN' in text)
        result=subprocess.run(['textutil','-convert','txt','-stdout',str(path)],capture_output=True,text=True)
        check(name+' macOS textutil readable',result.returncode==0,result.stderr.strip())
        docs.append({'file':name,'bytes':path.stat().st_size,'sha256':sha(path),'words_including_references':len(text.split()),'tables':len(Document(path).tables)})
    sim=json.loads((BASE/'Kiem_tra/simulation_results.json').read_text())
    check('simulation forty instances no assertion failures',sim['summary']['instances']==40 and sim['summary']['assertion_failures']==0)
    for name,digest in sim['metadata']['source_sha256'].items():check('recorded simulation source hash '+name,sha(BASE/'Mo_phong'/name)==digest)
    report={'documents':docs,'checks':checks,'passed':len(checks),'limits':['No Microsoft Word visual pagination/render verification available; final page count must be checked in Word.','No real-data benchmark has been run; simulation evidence is finite and synthetic.']}
    (BASE/'Kiem_tra/kiem_tra_tai_lieu.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'checks_passed':len(checks),'documents':docs},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
