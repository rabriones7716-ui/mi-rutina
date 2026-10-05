import re, zipfile, difflib, html
from xml.dom import minidom
from lib51 import all_paras, vis_text, accepted_seq
from edit51 import Ctx, del_mark, edit_para, apply_text, TOK, D_LOC, D_UTC
from ops51 import balanced_end, accept_all
AUT='Revisión 2026-10 – versión final'
def diff_eds(a,b,maxchunks=12):
    ta=TOK.findall(a); tb=TOK.findall(b); pa=[0]; pb=[0]
    for t in ta: pa.append(pa[-1]+len(t))
    for t in tb: pb.append(pb[-1]+len(t))
    ops=[(pa[i1],pa[i2],pb[j1],pb[j2]) for g,i1,i2,j1,j2 in difflib.SequenceMatcher(a=ta,b=tb,autojunk=False).get_opcodes() if g!='equal']
    m=[]
    for o in ops:
        if m and o[0]-m[-1][1]<=1 and o[2]-m[-1][3]<=1: m[-1]=(m[-1][0],o[1],m[-1][2],o[3])
        else: m.append(o)
    if len(m)>maxchunks: m=[(m[0][0],m[-1][1],m[0][2],m[-1][3])]
    return [(s,e,b[js:je]) for s,e,js,je in m]
def para_text(x,i):
    ps=all_paras(x); return vis_text(x[ps[i][0]:ps[i][1]])
def set_text(x,ctx,i,new,aut=AUT):
    old=para_text(x,i)
    return x if old==new else apply_text(x,ctx,i,diff_eds(old,new),aut,True)
def wrap_all(d,p,ctx,aut,tag):
    runs=[]
    def walk(n,inins):
        for c in list(n.childNodes):
            if c.nodeType!=1: continue
            if c.tagName=='w:r':
                if not (tag=='w:ins' and inins): runs.append(c)
            elif c.tagName in('w:del','w:moveFrom','w:pPr'): continue
            else: walk(c, inins or c.tagName=='w:ins')
    walk(p,False)
    for r in runs:
        w=ctx.rev(d,tag,aut); r.parentNode.insertBefore(w,r); r.parentNode.removeChild(r); w.appendChild(r)
        if tag=='w:del':
            for t in [c for c in r.childNodes if c.nodeType==1 and c.tagName in('w:t','w:instrText')]:
                nt=d.createElement('w:delText' if t.tagName=='w:t' else 'w:delInstrText')
                for a in list(t.attributes.keys()): nt.setAttribute(a,t.getAttribute(a))
                for ch in list(t.childNodes): nt.appendChild(ch)
                r.replaceChild(nt,t)
def ins_mark(d,p,ctx,aut):
    ppr=next((c for c in p.childNodes if c.nodeType==1 and c.tagName=='w:pPr'),None)
    if ppr is None: ppr=d.createElement('w:pPr'); p.insertBefore(ppr,p.firstChild)
    rpr=next((c for c in ppr.childNodes if c.nodeType==1 and c.tagName=='w:rPr'),None)
    if rpr is None:
        rpr=d.createElement('w:rPr'); stop=next((c for c in ppr.childNodes if c.nodeType==1 and c.tagName in('w:sectPr','w:pPrChange')),None); ppr.insertBefore(rpr,stop)
    rpr.insertBefore(ctx.rev(d,'w:ins',aut),rpr.firstChild)
def del_para(x,ctx,i,aut=AUT):
    def fn(d,p): wrap_all(d,p,ctx,aut,'w:del'); del_mark(d,p,ctx,aut)
    return edit_para(x,ctx,i,fn)
def rev_el(ctx,tag,aut):
    ctx.nid+=1; ctx.count[(aut,tag)]=ctx.count.get((aut,tag),0)+1
    return f'<{tag} w:id="{ctx.nid}" w:author="{aut}" w:date="{D_LOC}"'+(f' w16du:dateUtc="{D_UTC}"' if ctx.du else '')+'/>'
def add_tr_rev(row,ctx,tag,aut):
    pos=re.match(r'<w:tr\b[^>]*>(\s*<w:tblPrEx>.*?</w:tblPrEx>)?',row,flags=re.S).end()
    if row.startswith('<w:trPr>',pos):
        e=balanced_end(row,pos,'w:trPr'); ch=row.find('<w:trPrChange',pos,e); at=ch if ch!=-1 else e-len('</w:trPr>')
        return row[:at]+rev_el(ctx,tag,aut)+row[at:]
    assert not row.startswith('<w:trPr',pos), 'trPr raro'
    return row[:pos]+'<w:trPr>'+rev_el(ctx,tag,aut)+'</w:trPr>'+row[pos:]
def row_span(x,s):
    a=max(x.rfind('<w:tr ',0,s),x.rfind('<w:tr>',0,s)); return a,balanced_end(x,a,'w:tr')
def del_row(x,ctx,i,aut=AUT):
    ps=all_paras(x); a,b=row_span(x,ps[i][0])
    for j in sorted([j for j,(s,e) in enumerate(ps) if a<=s<b],reverse=True): x=del_para(x,ctx,j,aut)
    a,b=row_span(x,all_paras(x)[i][0]); return x[:a]+add_tr_rev(x[a:b],ctx,'w:del',aut)+x[b:]
def cell_text(tc,text):
    ps=[(m.start(),balanced_end(tc,m.start(),'w:p')) for m in re.finditer(r'<w:p[\s>]',tc)]
    p=tc[ps[0][0]:ps[0][1]]; h=re.match(r'<w:p\b[^>]*>',p).end(); ppr=''
    if p.startswith('<w:pPr>',h): ppr=p[h:balanced_end(p,h,'w:pPr')]
    m=re.search(r'<w:r\b[^>]*>\s*(<w:rPr>.*?</w:rPr>)?',p[h+len(ppr):],flags=re.S); rpr=(m.group(1) or '') if m else ''
    np=p[:h]+ppr+'<w:r>'+rpr+'<w:t xml:space="preserve">'+html.escape(text,quote=False)+'</w:t></w:r></w:p>'
    return tc[:ps[0][0]]+np+tc[ps[-1][1]:]
def mark_ins_row(row,ctx,aut,ns):
    d=minidom.parseString('<root '+ns+'>'+row+'</root>'); tr=d.documentElement.firstChild
    for p in tr.getElementsByTagName('w:p'): wrap_all(d,p,ctx,aut,'w:ins'); ins_mark(d,p,ctx,aut)
    return add_tr_rev(tr.toxml(),ctx,'w:ins',aut)
