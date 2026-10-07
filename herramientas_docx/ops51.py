import re, html, zipfile, datetime
from xml.dom import minidom
from lib51 import all_paras, vis_text, nsdecl
from edit51 import Ctx, replace, del_mark, edits, tnodes
def balanced_end(x,start,tag):
    pat=re.compile(r'<%s(?=[\s>/])[^>]*?(/?)>|</%s>'%(re.escape(tag),re.escape(tag)))
    depth=0
    for m in pat.finditer(x,start):
        if m.group(0).startswith('</'):
            depth-=1
            if depth==0: return m.end()
        elif m.group(1)=='/':
            if depth==0: return m.end()
        else: depth+=1
    raise ValueError('sin cierre '+tag)
def ppr_span(px):
    m=re.match(r'<w:p\b[^>]*>',px)
    if not m or px.endswith('/>') and px.count('<')==1: return None
    a=m.end()
    if px.startswith('<w:pPr>',a) or px.startswith('<w:pPr ',a): return a,balanced_end(px,a,'w:pPr')
    return None
def mark_del(px):
    sp=ppr_span(px)
    if not sp: return False
    p=re.sub(r'<w:pPrChange\b.*?</w:pPrChange>','',px[sp[0]:sp[1]],flags=re.S)
    r=re.search(r'<w:rPr>(.*?)</w:rPr>',p,flags=re.S)
    return bool(r and re.search(r'<w:del\b',r.group(1)))
CONTENT=re.compile(r'<w:t[\s>]|<w:drawing|<w:pict|<w:object|<w:fldChar|<w:instrText|<w:sym\b|Reference\b|<w:br\b|<w:tab/>|<w:fldSimple')
def empty_after(px):
    sp=ppr_span(px); y=px[sp[1]:] if sp else px
    y=re.sub(r'<w:del\b[^>]*[^/]>.*?</w:del>','',y,flags=re.S)
    return not CONTENT.search(y)
def deleted_row_spans(x):
    out=[]
    for m in re.finditer(r'<w:tr(?=[\s>])',x):
        s=m.start(); head=x[s:s+4000]
        tp=re.match(r'<w:tr\b[^>]*>\s*(?:<w:tblPrEx>.*?</w:tblPrEx>\s*)?(<w:trPr>.*?</w:trPr>)?',head,flags=re.S)
        if tp and tp.group(1) and re.search(r'<w:del\b',tp.group(1)): out.append((s,balanced_end(x,s,'w:tr')))
    return out
def accepted_seq2(x):
    rows=deleted_row_spans(x); ps=all_paras(x); out=[]; buf=''
    def inrow(s): return any(a<=s<b for a,b in rows)
    nxt_gap={ps[i][0]:x[ps[i][1]:ps[i+1][0]].strip()!='' for i in range(len(ps)-1)}
    for s,e in ps:
        if inrow(s): continue
        px=x[s:e]; buf+=vis_text(px)
        if not mark_del(px): out.append(buf); buf=''
        elif nxt_gap.get(s) and buf=='' and empty_after(px): pass
        elif nxt_gap.get(s): out.append(buf); buf=''
    if buf: out.append(buf)
    return out
def accept_all(x):
    # 1) unir párrafos con marca borrada (de atrás hacia delante)
    ps=all_paras(x); nmerge=0; nfail=0
    for i in range(len(ps)-2,-1,-1):
        s,e=ps[i]; px=x[s:e]
        if not mark_del(px): continue
        s2=ps[i+1][0]
        if x[e:s2].strip()=='' and re.match(r'<w:p[\s>/]',x[s2:s2+5]):
            sp=ppr_span(px); body=px[(sp[1] if sp else re.match(r'<w:p\b[^>]*>',px).end()):-len('</w:p>')]
            e2=balanced_end(x,s2,'w:p'); p2=x[s2:e2]
            if p2.endswith('/>') and '</w:p>' not in p2:
                head=p2[:-2]+'>'; merged=head+body+'</w:p>'
            else:
                h=re.match(r'<w:p\b[^>]*>',p2).end(); sp2=ppr_span(p2); h=sp2[1] if sp2 else h
                merged=p2[:h]+body+p2[h:]
            x=x[:s]+merged+x[e2:]; nmerge+=1
        elif empty_after(px): x=x[:s]+x[e:]; nmerge+=1
        else: nfail+=1
    # 2) filas borradas y tablas vacías
    for s,e in sorted(deleted_row_spans(x),reverse=True):
        x=x[:s]+x[e:]
    for m in sorted(re.finditer(r'<w:tbl>',x),key=lambda m:-m.start()):
        e=balanced_end(x,m.start(),'w:tbl')
        if '<w:tr' not in x[m.start():e]: x=x[:m.start()]+x[e:]
    # 3) borrados, movidos, inserciones y cambios de formato
    x=re.sub(r'<w:del\b[^>]*[^/]>.*?</w:del>','',x,flags=re.S)
    x=re.sub(r'<w:del\b[^>]*/>','',x)
    x=re.sub(r'<w:moveFrom\b[^>]*[^/]>.*?</w:moveFrom>','',x,flags=re.S)
    x=re.sub(r'<w:move(?:From|To)Range(?:Start|End)\b[^>]*/>','',x)
    x=re.sub(r'<w:moveTo\b[^>]*[^/]>|</w:moveTo>','',x)
    x=re.sub(r'<w:ins\b[^>]*[^/]>|</w:ins>','',x)
    x=re.sub(r'<w:ins\b[^>]*/>','',x)
    for t in ('rPrChange','pPrChange','sectPrChange','tblPrChange','tblPrExChange','trPrChange','tcPrChange','tblGridChange'):
        x=re.sub(r'<w:%s\b[^>]*[^/]>.*?</w:%s>'%(t,t),'',x,flags=re.S)
    x=re.sub(r'<w:(?:numberingChange|cellIns|cellMerge)\b[^>]*/>','',x)
    assert '<w:cellDel' not in x and '<w:delText' not in x, 'restos de revisiones'
    return x,nmerge,nfail
def strip_comments(x):
    x=re.sub(r'<w:comment(?:RangeStart|RangeEnd)\b[^>]*/>','',x)
    x=re.sub(r'<w:r>(?:<w:rPr>(?:(?!</w:rPr>).)*</w:rPr>)?<w:commentReference\b[^>]*/></w:r>','',x,flags=re.S)
    return re.sub(r'<w:commentReference\b[^>]*/>','',x)
def write_docx(src,dst,parts,clean):
    zs=zipfile.ZipFile(src); names=zs.namelist()
    drop=set()
    if clean:
        drop={n for n in names if re.match(r'word/comments(Extended|Ids|Extensible)?\.xml$',n) or re.match(r'word/_rels/comments.*\.rels$',n)}
    with zipfile.ZipFile(dst,'w') as zo:
        for it in zs.infolist():
            if it.filename in drop: continue
            d=parts[it.filename].encode('utf8') if it.filename in parts else zs.read(it.filename)
            if clean and it.filename=='word/_rels/document.xml.rels':
                t=d.decode('utf8'); t=re.sub(r'<Relationship\b[^>]*Target="comments[^"]*"[^>]*/>','',t); d=t.encode('utf8')
            if clean and it.filename=='[Content_Types].xml':
                t=d.decode('utf8'); t=re.sub(r'<Override\b[^>]*PartName="/word/comments[^"]*"[^>]*/>','',t); d=t.encode('utf8')
            if it.filename=='word/settings.xml':
                t=d.decode('utf8'); t=re.sub(r'<w:trackRevisions\b[^>]*/>','',t)
                if not clean: t=re.sub(r'(<w:settings\b[^>]*>)',r'\1<w:trackRevisions/>',t,count=1)
                d=t.encode('utf8')
            zo.writestr(it,d,compress_type=it.compress_type)
