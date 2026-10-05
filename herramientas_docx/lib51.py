import zipfile,re
from xml.dom import minidom
def doc(n): return zipfile.ZipFile(n).read('word/document.xml').decode('utf8')
def nsdecl(x):
    root=re.search(r'<w:document\b[^>]*>',x).group()
    return ' '.join(re.findall(r'xmlns:\w+="[^"]*"',root))
def para_span(x,pos):
    starts=[m.start() for m in re.finditer(r'<w:p[ >]',x[:pos])]
    for s in reversed(starts):
        depth=0; e=None
        for m in re.finditer(r'<w:p[ >]|</w:p>',x[s:]):
            depth+= 1 if m.group().startswith('<w:p') else -1
            if depth==0: e=s+m.end(); break
        if e and e>pos: return s,e
def parse_frag(x,px):
    d=minidom.parseString('<root '+nsdecl(x)+'>'+px+'</root>')
    return d,d.documentElement.firstChild
def run_text(r):
    return ''.join(n.firstChild.data if n.firstChild else '' for n in r.childNodes if n.nodeType==1 and n.tagName in('w:t','w:delText'))
def runs_summary(p):
    out=[]
    for r in p.getElementsByTagName('w:r'):
        par=r.parentNode; cont=par.tagName; auth=par.getAttribute('w:author') if cont in('w:ins','w:del') else ''
        if cont=='w:del' and par.parentNode.tagName=='w:ins': cont='ins>del'
        rpr=r.getElementsByTagName('w:rPr'); fl=''
        if rpr:
            for tag in ('w:b','w:i','w:vertAlign','w:rStyle'):
                if rpr[0].getElementsByTagName(tag): fl+=tag[2:]+' '
        other=[n.tagName for n in r.childNodes if n.nodeType==1 and n.tagName not in('w:rPr','w:t','w:delText')]
        txt=run_text(r)
        out.append(f"{cont}{('('+auth[:22]+')') if auth else ''} [{fl.strip()}] {other if other else ''} «{txt[:80]}{'…' if len(txt)>80 else ''}» ({len(txt)})")
    return out
import html
def all_paras(x):
    """(inicio, fin) de los w:p de nivel superior; admite párrafos vacíos autocerrados <w:p .../>."""
    out=[]; depth=0; s=None
    for m in re.finditer(r'<w:p(?=[\s/>])[^>]*>|</w:p>',x):
        g=m.group()
        if g.startswith('</'):
            depth-=1
            if depth==0: out.append((s,m.end()))
        elif g.endswith('/>'):
            if depth==0: out.append((m.start(),m.end()))
        else:
            if depth==0: s=m.start()
            depth+=1
    return out
def vis_text(px):
    y=re.sub(r'<w:del\b[^>]*/>','',px)
    y=re.sub(r'<w:del\b[^>]*[^/]>.*?</w:del>','',y,flags=re.S)
    return html.unescape(''.join(re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>',y)))
def mark_deleted(px):
    m=re.search(r'<w:pPr>.*?</w:pPr>',px,flags=re.S)
    if not m: return False
    rp=re.search(r'<w:rPr>.*?</w:rPr>',m.group(),flags=re.S)
    return bool(rp and re.search(r'<w:del\b',rp.group()))
def accepted_seq(x):
    """Texto de párrafos tras aceptar todo: une los párrafos cuya marca está borrada. Devuelve [(texto, [índices originales])]."""
    ps=all_paras(x); out=[]; buf=''; idx=[]
    for i,(s,e) in enumerate(ps):
        px=x[s:e]; buf+=vis_text(px); idx.append(i)
        if not mark_deleted(px): out.append((buf,idx)); buf=''; idx=[]
    if idx: out.append((buf,idx))
    return out
