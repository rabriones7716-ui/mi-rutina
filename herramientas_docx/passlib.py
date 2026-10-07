"""Ayudantes del pase con control de cambios (extraídos de cf_pass.py). Estado en variables de módulo."""
import zipfile,re,json,os,hashlib,html,xml.parsers.expat
from xml.dom import minidom
from lib51 import all_paras,vis_text
from edit51 import Ctx
from ops51 import accept_all,accepted_seq2,strip_comments,balanced_end,deleted_row_spans
from fin51 import set_text,del_para,del_row,cell_text,mark_ins_row,wrap_all,ins_mark
x=None; ctx=None; A=None; log=[]; AUT=None; SRC=None; MEDIA={}
def init(src,aut):
    global x,ctx,A,log,AUT,SRC,MEDIA
    SRC=src; AUT=aut; z=zipfile.ZipFile(src); x=z.read('word/document.xml').decode('utf8'); ctx=Ctx(z,x)
    y0,_,_=accept_all(x); A=[vis_text(y0[a:b]) for a,b in all_paras(y0)]; log=[]; MEDIA={}
    return A
def raw_index_by_text(t,occ=None):
    ps=all_paras(x); cands=[j for j,(a,b) in enumerate(ps) if vis_text(x[a:b])==t]
    if occ is not None and len(cands)>occ: return cands[occ]
    if len(cands)==1: return cands[0]
    if len(cands)>1: raise Exception('texto repetido: '+t[:60])
    key=t[:60]; cands=[j for j,(a,b) in enumerate(ps) if vis_text(x[a:b]).startswith(key)]
    if len(cands)==1: return cands[0]
    raise Exception(f'no encontrado ({len(cands)}): '+t[:80])
def cur_text(i,occ=None):
    j=raw_index_by_text(A[i],occ); ps=all_paras(x); return vis_text(x[ps[j][0]:ps[j][1]])
def full(i,new,occ=None):
    global x
    j=raw_index_by_text(A[i],occ); ps=all_paras(x); old=vis_text(x[ps[j][0]:ps[j][1]]); log.append((i,old,new)); x=set_text(x,ctx,j,new,AUT)
def pairs(i,prs,occ=None,strict=True):
    global x
    j=raw_index_by_text(A[i],occ); ps=all_paras(x); old=vis_text(x[ps[j][0]:ps[j][1]]); new=old
    for o,n in prs:
        c=new.count(o)
        if strict: assert c==1,(i,o[:60],c)
        if c: new=new.replace(o,n)
    if new!=old: log.append((i,old,new)); x=set_text(x,ctx,j,new,AUT)
def live_rows(a,b):
    dele=deleted_row_spans(x); out=[]
    for m in re.finditer(r'<w:tr[\s>]',x[a:b]):
        rs=a+m.start()
        if any(s<=rs<e for s,e in dele): continue
        if any(s<rs<e for s,e in out): continue
        out.append((rs,balanced_end(x,rs,'w:tr')))
    return out
def find_table(title_prefix,nth=0):
    ps=all_paras(x); hits=[j for j,(a,b) in enumerate(ps) if vis_text(x[a:b]).startswith(title_prefix)]
    assert hits,title_prefix; j=hits[nth]; pos=ps[j][1]
    while True:
        a=x.index('<w:tbl>',pos); b=balanced_end(x,a,'w:tbl')
        if live_rows(a,b): return a,b
        pos=b
def cell_spans(rs,re_):
    out=[]
    for m in re.finditer(r'<w:tc[\s>]',x[rs:re_]):
        cs=rs+m.start()
        if any(s<cs<e for s,e in out): continue
        out.append((cs,balanced_end(x,cs,'w:tc')))
    return out
def para_idx_in(s,e): return [j for j,(a,b) in enumerate(all_paras(x)) if s<=a<e]
def table_cells_text(title,nth=0):
    a,b=find_table(title,nth); out=[]
    for rs,re_ in live_rows(a,b):
        cs=cell_spans(rs,re_); ps=all_paras(x)
        out.append([' / '.join(vis_text(x[ps[j][0]:ps[j][1]]) for j in para_idx_in(s,e)) for s,e in cs])
    return out
def cell_set(title,row,col,new,nth=0,check=None):
    global x
    a,b=find_table(title,nth); rows=live_rows(a,b); cs=cell_spans(*rows[row]); s,e=cs[col]
    idx=para_idx_in(s,e); ps=all_paras(x); old=' / '.join(vis_text(x[ps[j][0]:ps[j][1]]) for j in idx)
    if check: assert check in old,(title[:30],row,col,old[:90])
    if old==new: return
    for j in sorted(idx[1:],reverse=True): x=del_para(x,ctx,j,AUT)
    x=set_text(x,ctx,idx[0],new,AUT); log.append((f'{title[:25]} r{row}c{col}',old,new))
def cell_pairs(title,row,col,prs,nth=0):
    global x
    a,b=find_table(title,nth); rows=live_rows(a,b); cs=cell_spans(*rows[row]); s,e=cs[col]
    idx=para_idx_in(s,e); ps=all_paras(x)
    for j in sorted(idx,reverse=True):
        t=vis_text(x[ps[j][0]:ps[j][1]]); new=t
        for o,n in prs:
            if o in new: new=new.replace(o,n)
        if new!=t: log.append((f'{title[:25]} r{row}c{col}',t,new)); x=set_text(x,ctx,j,new,AUT)
def row_pairs(title,prs,nth=0,rows=None):
    """pares aplicados a todas las celdas de la tabla (o de las filas indicadas)"""
    a,b=find_table(title,nth); R=live_rows(a,b)
    for r in range(len(R)):
        if rows is not None and r not in rows: continue
        cs=cell_spans(*R[r])
        for c in range(len(cs)): cell_pairs(title,r,c,prs,nth)
def delete_row(title,row,nth=0):
    global x
    a,b=find_table(title,nth); rows=live_rows(a,b); idx=para_idx_in(*rows[row]); x=del_row(x,ctx,idx[0],AUT); log.append((f'{title[:25]} fila {row}','(fila eliminada)',''))
def _top_cells(row_xml):
    cs=[]
    for m in re.finditer(r'<w:tc[\s>]',row_xml):
        c=m.start()
        if any(s<c<e for s,e in cs): continue
        cs.append((c,balanced_end(row_xml,c,'w:tc')))
    return cs
def _clean(frag): return re.sub(r'\sw14:(?:paraId|textId)="[^"]*"','',accept_all(frag)[0])
def _mkrow(row_xml,texts,widths=None,merge_from=None,grid=None):
    cs=_top_cells(row_xml); cells=[row_xml[s:e] for s,e in cs]
    if merge_from is not None:
        w=sum(grid[merge_from:]); tc=cells[merge_from]
        tc=re.sub(r'<w:tcW w:w="\d+"',f'<w:tcW w:w="{w}"',tc,count=1); tc=re.sub(r'<w:gridSpan [^>]*/>','',tc); tc=re.sub(r'(<w:tcW\b[^>]*/>)',r'\1<w:gridSpan w:val="%d"/>'%len(grid[merge_from:]),tc,count=1)
        cells=cells[:merge_from]+[tc]
    while len(cells)<len(texts): cells.append(cells[-1])
    cells=cells[:len(texts)]
    out=[]
    for k,(tc,t) in enumerate(zip(cells,texts)):
        if widths: tc=re.sub(r'<w:tcW [^>]*/>',f'<w:tcW w:w="{widths[k]}" w:type="dxa"/>',tc,count=1); tc=re.sub(r'<w:gridSpan [^>]*/>','',tc)
        out.append(cell_text(tc,t))
    return row_xml[:cs[0][0]]+''.join(out)+row_xml[cs[-1][1]:]
def rebuild_table(title,new_rows,merge_from=None,nth=0,tmpl_body=1,widths=None):
    """Sustituye todas las filas vivas por new_rows (marcadas como insertadas). tmpl_body: índice de la fila plantilla del cuerpo. widths: anchos nuevos (reescribe la rejilla)."""
    global x
    a,b=find_table(title,nth); rows=live_rows(a,b)
    grid=[int(v) for v in re.findall(r'<w:gridCol w:w="(\d+)"',x[a:b])]
    if widths=='auto':
        tot=sum(grid); n=len(new_rows[0]); widths=[tot//n]*n
    elif widths and sum(widths)<=100:
        tot=sum(grid); widths=[int(tot*w/sum(widths)) for w in widths]
    tmpl=[_clean(x[rs:re_]) for rs,re_ in rows]
    new_xml=''.join(mark_ins_row(_mkrow(tmpl[0] if k==0 else tmpl[min(tmpl_body if k<=tmpl_body else k,len(tmpl)-1)],t,merge_from=None if widths else merge_from,grid=grid,widths=widths),ctx,AUT,ctx.ns) for k,t in enumerate(new_rows))
    for rs,re_ in reversed(rows): idx=para_idx_in(rs,re_); x=del_row(x,ctx,idx[0],AUT)
    assert x.startswith('<w:tbl>',a); b=balanced_end(x,a,'w:tbl')
    if widths:
        g='<w:tblGrid>'+''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)+'</w:tblGrid>'
        seg=re.sub(r'<w:tblGrid>.*?</w:tblGrid>',g,x[a:b],count=1,flags=re.S); x=x[:a]+seg+x[b:]; b=balanced_end(x,a,'w:tbl')
    x=x[:b-len('</w:tbl>')]+new_xml+x[b-len('</w:tbl>'):]
    log.append((f'{title[:25]} reconstruida','',' | '.join(' ; '.join(r) for r in new_rows)[:400]))
def add_rows(title,rows_texts,nth=0,tmpl_row=-1):
    """Añade filas al final de la tabla, clonando una fila plantilla."""
    global x
    a,b=find_table(title,nth); rows=live_rows(a,b); tmpl=_clean(x[rows[tmpl_row][0]:rows[tmpl_row][1]])
    new_xml=''.join(mark_ins_row(_mkrow(tmpl,t),ctx,AUT,ctx.ns) for t in rows_texts)
    x=x[:b-len('</w:tbl>')]+new_xml+x[b-len('</w:tbl>'):]; log.append((f'{title[:25]} filas añadidas','',' | '.join(' ; '.join(r) for r in rows_texts)[:300]))
def new_p(style,text,bold_prefix=None):
    runs=''
    if bold_prefix: runs+=f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{html.escape(bold_prefix,quote=False)}</w:t></w:r><w:r><w:rPr><w:b/></w:rPr><w:tab/></w:r>'
    runs+=f'<w:r><w:t xml:space="preserve">{html.escape(text,quote=False)}</w:t></w:r>'
    p=f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{runs}</w:p>'
    d=minidom.parseString('<root '+ctx.ns+'>'+p+'</root>'); pe=d.documentElement.firstChild
    wrap_all(d,pe,ctx,AUT,'w:ins'); ins_mark(d,pe,ctx,AUT); return pe.toxml()
def new_table(tpl,rows_texts,widths):
    i0=tpl.index('<w:tblPr'); tblpr=tpl[i0:balanced_end(tpl,i0,'w:tblPr')]
    rows=[]
    for m in re.finditer(r'<w:tr[\s>]',tpl):
        rs=m.start()
        if any(s<rs<e for s,e in rows): continue
        rows.append((rs,balanced_end(tpl,rs,'w:tr')))
    rows=[tpl[s:e] for s,e in rows]
    grid='<w:tblGrid>'+''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)+'</w:tblGrid>'
    body=''.join(mark_ins_row(_mkrow(rows[0] if k==0 else rows[min(1,len(rows)-1)],t,widths=widths),ctx,AUT,ctx.ns) for k,t in enumerate(rows_texts))
    return '<w:tbl>'+tblpr+grid+body+'</w:tbl>'
def table_template(title,nth=0):
    a,b=find_table(title,nth); return _clean(x[a:b])
def insert_after(i,block,text=None,occ=None):
    global x
    j=raw_index_by_text(text or A[i],occ); e=all_paras(x)[j][1]; x=x[:e]+block+x[e:]; log.append((f'inserción tras [{i}]','',vis_text(block)[:300]))
def insert_before(i,block,text=None,occ=None):
    global x
    j=raw_index_by_text(text or A[i],occ); s=all_paras(x)[j][0]; x=x[:s]+block+x[s:]; log.append((f'inserción antes de [{i}]','',vis_text(block)[:300]))
def gen_pass(GEN):
    global x
    ps=all_paras(x); n=0
    for j in range(len(ps)-1,-1,-1):
        s,e=ps[j]; t=vis_text(x[s:e]); new=t
        for o,nw in GEN:
            if o in new: new=new.replace(o,nw)
        if new!=t:
            if '<w:hyperlink' in x[s:e]: SKIPPED.append((j,t[:120],new[:120])); continue
            log.append((f'gen {j}',t,new)); x=set_text(x,ctx,j,new,AUT); n+=1
    return n
SKIPPED=[]
def media_map():
    rels=zipfile.ZipFile(SRC).read('word/_rels/document.xml.rels').decode('utf8')
    return {m.group(1):m.group(2) for m in re.finditer(r'<Relationship [^>]*Id="([^"]+)"[^>]*Target="([^"]+)"',rels)}
def media_after(cap_prefix,min_idx=200):
    rel=media_map(); ps=all_paras(x); T=[vis_text(x[a:b]) for a,b in ps]
    for i in [k for k,t in enumerate(T) if t.strip().startswith(cap_prefix) and k>min_idx]:
        for k in list(range(i+1,min(i+6,len(ps))))+list(range(i-1,max(i-4,0),-1)):
            if '<w:drawing' in x[ps[k][0]:ps[k][1]]:
                rid=re.search(r'r:embed="([^"]+)"',x[ps[k][0]:ps[k][1]]).group(1); return 'word/'+rel[rid]
    raise Exception('sin imagen para '+cap_prefix)
def set_media(cap_prefix,png,min_idx=200):
    m=media_after(cap_prefix,min_idx); MEDIA[m]=open(png,'rb').read(); log.append((cap_prefix,m,png))
def save2(dst,doc,clean):
    zs=zipfile.ZipFile(SRC)
    drop={n for n in zs.namelist() if clean and (re.match(r'word/comments(Extended|Ids|Extensible)?\.xml$',n) or re.match(r'word/_rels/comments',n))}
    with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED) as zo:
        for it in zs.infolist():
            n=it.filename
            if n in drop: continue
            if n in MEDIA: zo.writestr(it,MEDIA[n]); continue
            d=zs.read(n)
            if n=='word/document.xml': d=doc.encode('utf8')
            elif n=='word/_rels/document.xml.rels' and clean: d=re.sub(rb'<Relationship\b[^>]*Target="comments[^"]*"[^>]*/>',b'',d)
            elif n=='[Content_Types].xml' and clean: d=re.sub(rb'<Override\b[^>]*PartName="/word/comments[^"]*"[^>]*/>',b'',d)
            elif n=='word/settings.xml' and clean: d=re.sub(rb'<w:trackRevisions\b[^>]*/>',b'',d)
            elif clean and re.match(r'word/(footnotes|endnotes|header\d*|footer\d*)\.xml$',n) and (b'<w:ins ' in d or b'<w:del ' in d):
                d=strip_comments(accept_all(d.decode('utf8'))[0]).encode('utf8')
            zo.writestr(it,d)
def finish(cc,cl,RES,logfile):
    xml.parsers.expat.ParserCreate().Parse(x.encode('utf8'),True)
    y,nm,nf=accept_all(x); y=strip_comments(y); xml.parsers.expat.ParserCreate().Parse(y.encode('utf8'),True)
    os.makedirs(os.path.dirname(cc),exist_ok=True); save2(cc,x,False); save2(cl,y,True)
    Aa=accepted_seq2(x); L=[vis_text(y[a:b]) for a,b in all_paras(y)]
    sha=lambda f:hashlib.sha256(open(f,'rb').read()).hexdigest()[:8].upper()
    print(dict(ediciones=len(log),revisiones={k[1]:v for k,v in ctx.count.items()},aceptado_igual_limpio=Aa==L,no_unibles=nf,sha_cc=sha(cc),sha_limpio=sha(cl),bytes=(os.path.getsize(cc),os.path.getsize(cl))))
    for t in L:
        for m in re.finditer(RES,t): print('RESTO:',t[max(0,m.start()-70):m.end()+60].replace('\n',' '))
    json.dump(log,open(logfile,'w'),ensure_ascii=False,indent=0); return L
def insert_after_contains(substr,block):
    global x
    ps=all_paras(x); c=[j for j,(a,b) in enumerate(ps) if substr in vis_text(x[a:b])]
    assert len(c)==1,(substr[:50],len(c)); e=ps[c[0]][1]; x=x[:e]+block+x[e:]; log.append((f'inserción tras «{substr[:40]}»','',vis_text(block)[:300]))
def delete_para(i,occ=None):
    global x
    j=raw_index_by_text(A[i],occ); x=del_para(x,ctx,j,AUT); log.append((i,A[i][:80],'(párrafo eliminado)'))
def new_p_from(i,text,bold_prefix=None,occ=None,keep_highlight=False):
    """Párrafo nuevo (insertado) con el pPr y el rPr del primer run del párrafo A[i]."""
    j=raw_index_by_text(A[i],occ); ps=all_paras(x); p=_clean(x[ps[j][0]:ps[j][1]])
    h=re.match(r'<w:p\b[^>]*>',p).end(); ppr=''
    if p.startswith('<w:pPr>',h): ppr=p[h:balanced_end(p,h,'w:pPr')]
    m=re.search(r'<w:r\b[^>]*>\s*(<w:rPr>.*?</w:rPr>)?',p[h+len(ppr):],flags=re.S); rpr=(m.group(1) or '') if m else ''
    if not keep_highlight: rpr=re.sub(r'<w:highlight [^>]*/>','',rpr)
    runs=''
    if bold_prefix:
        brpr=rpr.replace('</w:rPr>','<w:b/></w:rPr>') if rpr else '<w:rPr><w:b/></w:rPr>'
        runs+=f'<w:r>{brpr}<w:t xml:space="preserve">{html.escape(bold_prefix,quote=False)}</w:t></w:r>'
    runs+=f'<w:r>{rpr}<w:t xml:space="preserve">{html.escape(text,quote=False)}</w:t></w:r>'
    np_='<w:p>'+ppr+runs+'</w:p>'
    d=minidom.parseString('<root '+ctx.ns+'>'+np_+'</root>'); pe=d.documentElement.firstChild
    wrap_all(d,pe,ctx,AUT,'w:ins'); ins_mark(d,pe,ctx,AUT); return pe.toxml()
def words(lo,hi):
    return sum(len(A[i].split()) for i in range(lo,hi))
def delete_drawing_near(i,occ=None):
    """Elimina (con control de cambios) el párrafo con imagen contiguo al párrafo A[i] (antes o después)."""
    global x
    j=raw_index_by_text(A[i],occ); ps=all_paras(x)
    for k in (j-1,j+1,j-2,j+2):
        if 0<=k<len(ps) and '<w:drawing' in x[ps[k][0]:ps[k][1]]:
            x=del_para(x,ctx,k,AUT); log.append((f'imagen junto a [{i}]','','(párrafo con imagen eliminado)')); return
    raise Exception('sin imagen junto a '+A[i][:40])

def accept_aux(path):
    """Acepta las revisiones de notas al pie, notas finales, encabezados y pies en un docx ya limpio (reescribe el archivo)."""
    import shutil,tempfile
    zs=zipfile.ZipFile(path); tmp=path+'.tmp'; n_fix=[]
    with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as zo:
        for it in zs.infolist():
            d=zs.read(it.filename)
            if re.match(r'word/(footnotes|endnotes|header\d*|footer\d*)\.xml$',it.filename) and (b'<w:ins ' in d or b'<w:del ' in d):
                y=strip_comments(accept_all(d.decode('utf8'))[0]); xml.parsers.expat.ParserCreate().Parse(y.encode('utf8'),True); d=y.encode('utf8'); n_fix.append(it.filename)
            zo.writestr(it,d)
    zs.close(); shutil.move(tmp,path)
    return n_fix,hashlib.sha256(open(path,'rb').read()).hexdigest()[:8].upper(),os.path.getsize(path)
