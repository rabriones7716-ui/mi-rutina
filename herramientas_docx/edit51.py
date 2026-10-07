import zipfile, re, datetime, difflib, sys
from xml.dom import minidom
from lib51 import doc, nsdecl, all_paras, vis_text, mark_deleted, accepted_seq
AUT_SYNC='Revisión 2026-10 – sincronización con la versión limpia'
AUT_51='Revisión 2026-10 – residuos de la conciliación'
now=datetime.datetime.utcnow().replace(second=0,microsecond=0)
D_UTC=now.strftime('%Y-%m-%dT%H:%M:00Z'); D_LOC=(now-datetime.timedelta(hours=5)).strftime('%Y-%m-%dT%H:%M:00Z')
class Ctx:
    def __init__(s,zf,x):
        s.ns=nsdecl(x); s.du='xmlns:w16du=' in s.ns
        ids=[int(v) for n in zf.namelist() if n.endswith('.xml') for v in re.findall(r'w:id="(\d+)"',zf.read(n).decode('utf8','ignore'))]
        s.nid=max(ids)+100; s.count={}
    def rev(s,d,tag,aut):
        s.nid+=1; el=d.createElement(tag); el.setAttribute('w:id',str(s.nid)); el.setAttribute('w:author',aut); el.setAttribute('w:date',D_LOC)
        if s.du: el.setAttribute('w16du:dateUtc',D_UTC)
        s.count[(aut,tag)]=s.count.get((aut,tag),0)+1; return el
def under(n,tag,stop):
    n=n.parentNode
    while n is not None and n is not stop:
        if n.nodeType==1 and n.tagName==tag: return True
        n=n.parentNode
    return False
def tnodes(p):
    out=[];pos=0
    for t in p.getElementsByTagName('w:t'):
        if under(t,'w:del',p): continue
        L=len(t.firstChild.data) if t.firstChild else 0; out.append((t,pos,pos+L)); pos+=L
    return out
def split_at(p,off):
    for t,a,b in tnodes(p):
        if a<off<b:
            r=t.parentNode; assert r.tagName=='w:r',r.tagName
            k=off-a; txt=t.firstChild.data; r2=r.cloneNode(True)
            kids=list(r.childNodes); kids2=list(r2.childNodes); i=kids.index(t); t2=kids2[i]
            for c in kids[i+1:]: r.removeChild(c)
            for c in kids2[:i]:
                if not(c.nodeType==1 and c.tagName=='w:rPr'): r2.removeChild(c)
            t.firstChild.data=txt[:k]; t2.firstChild.data=txt[k:]
            t.setAttribute('xml:space','preserve'); t2.setAttribute('xml:space','preserve')
            r.parentNode.insertBefore(r2,r.nextSibling); return
def runs_in(p,s,e):
    runs=[]
    for t,a,b in tnodes(p):
        if s<=a and b<=e and b>a:
            if t.parentNode not in runs: runs.append(t.parentNode)
        elif a<e and b>s: raise Exception('frontera sin partir')
    for r in runs:
        for t,a,b in tnodes(p):
            if t.parentNode is r and not(s<=a and b<=e) and b>a: raise Exception('run con varios w:t a ambos lados')
    return runs
def new_run(d,tmpl,text):
    nr=d.createElement('w:r')
    if tmpl is not None:
        rp=[c for c in tmpl.childNodes if c.nodeType==1 and c.tagName=='w:rPr']
        if rp:
            rc=rp[0].cloneNode(True)
            for ch in [c for c in rc.childNodes if c.nodeType==1 and c.tagName in('w:rPrChange','w:ins','w:del')]: rc.removeChild(ch)
            nr.appendChild(rc)
    t=d.createElement('w:t'); t.setAttribute('xml:space','preserve'); t.appendChild(d.createTextNode(text)); nr.appendChild(t); return nr
def place_after(p,node,el,ctx):
    par=node.parentNode
    if par is p: p.insertBefore(el,node.nextSibling); return
    if par.tagName=='w:ins' and par.parentNode is p:
        foll=[]; n=node.nextSibling
        while n is not None: foll.append(n); n=n.nextSibling
        p.insertBefore(el,par.nextSibling)
        if any(f.nodeType==1 for f in foll):
            c2=par.cloneNode(False); ctx.nid+=1; c2.setAttribute('w:id',str(ctx.nid))
            for f in foll: par.removeChild(f); c2.appendChild(f)
            p.insertBefore(c2,el.nextSibling)
        return
    raise Exception('contenedor no previsto '+par.tagName)
def place_before(p,node,el,ctx):
    par=node.parentNode
    if par is p: p.insertBefore(el,node); return
    if par.tagName=='w:ins' and par.parentNode is p:
        prev=[]; n=par.firstChild
        while n is not None and n is not node: prev.append(n); n=n.nextSibling
        if any(f.nodeType==1 for f in prev):
            c0=par.cloneNode(False); ctx.nid+=1; c0.setAttribute('w:id',str(ctx.nid))
            for f in prev: par.removeChild(f); c0.appendChild(f)
            p.insertBefore(c0,par)
        p.insertBefore(el,par); return
    raise Exception('contenedor no previsto '+par.tagName)
def replace(d,p,s,e,new,ctx,aut,tracked):
    if e>s: split_at(p,e); split_at(p,s); runs=runs_in(p,s,e)
    else: split_at(p,s); runs=[]
    tn=tnodes(p)
    tmpl=runs[0] if runs else next((t.parentNode for t,a,b in tn if b==s and b>a), next((t.parentNode for t,a,b in tn if a==s), None))
    nr=new_run(d,tmpl,new) if new else None
    if not tracked:
        if nr is not None:
            if runs: runs[0].parentNode.insertBefore(nr,runs[0])
            else:
                prev=next((t.parentNode for t,a,b in tn if b==s and b>a),None)
                if prev is not None: prev.parentNode.insertBefore(nr,prev.nextSibling)
                else: tmpl.parentNode.insertBefore(nr,tmpl)
        for r in runs: r.parentNode.removeChild(r)
        return
    last=None; groups=[]
    for r in runs:
        if groups and groups[-1][-1].nextSibling is r: groups[-1].append(r)
        else: groups.append([r])
    for g in groups:
        par=g[0].parentNode
        if par.tagName not in('w:p','w:ins'): raise Exception('contenedor '+par.tagName)
        w=ctx.rev(d,'w:del',aut); par.insertBefore(w,g[0])
        for r in g:
            par.removeChild(r)
            for t in [c for c in r.childNodes if c.nodeType==1 and c.tagName=='w:t']:
                dt=d.createElement('w:delText'); dt.setAttribute('xml:space','preserve'); dt.appendChild(d.createTextNode(t.firstChild.data if t.firstChild else '')); r.replaceChild(dt,t)
            w.appendChild(r)
        last=w
    if nr is None: return
    ins=ctx.rev(d,'w:ins',aut); ins.appendChild(nr)
    if last is not None: place_after(p,last,ins,ctx)
    else:
        prev=next((t.parentNode for t,a,b in tn if b==s and b>a),None)
        if prev is not None: place_after(p,prev,ins,ctx)
        else: place_before(p,tmpl,ins,ctx)
def del_mark(d,p,ctx,aut):
    ppr=next((c for c in p.childNodes if c.nodeType==1 and c.tagName=='w:pPr'),None)
    if ppr is None: ppr=d.createElement('w:pPr'); p.insertBefore(ppr,p.firstChild)
    rpr=next((c for c in ppr.childNodes if c.nodeType==1 and c.tagName=='w:rPr'),None)
    if rpr is None:
        rpr=d.createElement('w:rPr'); stop=next((c for c in ppr.childNodes if c.nodeType==1 and c.tagName in('w:sectPr','w:pPrChange')),None); ppr.insertBefore(rpr,stop)
    if any(c.nodeType==1 and c.tagName=='w:del' for c in rpr.childNodes): return
    dl=ctx.rev(d,'w:del',aut); ins_=[c for c in rpr.childNodes if c.nodeType==1 and c.tagName=='w:ins']
    rpr.insertBefore(dl, ins_[0].nextSibling if ins_ else rpr.firstChild)
TOK=re.compile(r'\w+|\s+|[^\w\s]')
def edits(a,b):
    ta=TOK.findall(a); tb=TOK.findall(b); off=[0]
    for t in ta: off.append(off[-1]+len(t))
    sm=difflib.SequenceMatcher(a=ta,b=tb,autojunk=False)
    return [(off[i1],off[i2],''.join(tb[j1:j2])) for t,i1,i2,j1,j2 in sm.get_opcodes() if t!='equal']
def edit_para(x,ctx,i,fn):
    ps=all_paras(x); s,e=ps[i]
    d=minidom.parseString('<root '+ctx.ns+'>'+x[s:e]+'</root>'); p=d.documentElement.firstChild
    assert p.tagName=='w:p'
    assert ''.join(t.firstChild.data if t.firstChild else '' for t,_,_ in [(t,0,0) for t,_,_ in tnodes(p)])==vis_text(x[s:e]), 'mapa de texto distinto'
    fn(d,p); return x[:s]+p.toxml()+x[e:]
def apply_text(x,ctx,i,eds,aut,tracked):
    def fn(d,p):
        for s_,e_,n_ in sorted(eds,key=lambda z:-z[0]): replace(d,p,s_,e_,n_,ctx,aut,tracked)
    return edit_para(x,ctx,i,fn)
