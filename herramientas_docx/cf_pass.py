import zipfile,re,json,os,hashlib,html,xml.parsers.expat
from xml.dom import minidom
from lib51 import all_paras,vis_text
from edit51 import Ctx
from ops51 import accept_all,accepted_seq2,strip_comments,balanced_end,deleted_row_spans
from fin51 import set_text,del_para,del_row,add_tr_rev,cell_text,mark_ins_row,wrap_all,ins_mark
AUT='Revisión 2026-10 – versión final'
SRC='CF_cc.docx'; z=zipfile.ZipFile(SRC); x=z.read('word/document.xml').decode('utf8'); ctx=Ctx(z,x)
y0,_,_=accept_all(x); A=[vis_text(y0[a:b]) for a,b in all_paras(y0)]
log=[]
def raw_index_by_text(x,t,occ=None):
    ps=all_paras(x); cands=[j for j,(a,b) in enumerate(ps) if vis_text(x[a:b])==t]
    if occ is not None and len(cands)>occ: return cands[occ]
    if len(cands)==1: return cands[0]
    if len(cands)>1: raise Exception('texto repetido: '+t[:60])
    key=t[:60]; cands=[j for j,(a,b) in enumerate(ps) if vis_text(x[a:b]).startswith(key)]
    if len(cands)==1: return cands[0]
    raise Exception(f'no encontrado ({len(cands)}): '+t[:80])
def full(i,new):
    global x
    j=raw_index_by_text(x,A[i]); old=vis_text(x[all_paras(x)[j][0]:all_paras(x)[j][1]]); log.append((i,old,new)); x=set_text(x,ctx,j,new,AUT)
def pairs(i,prs):
    global x
    j=raw_index_by_text(x,A[i]); ps=all_paras(x); old=vis_text(x[ps[j][0]:ps[j][1]]); new=old
    for o,n in prs:
        assert new.count(o)==1,(i,o[:50],new.count(o)); new=new.replace(o,n)
    log.append((i,old,new)); x=set_text(x,ctx,j,new,AUT)
# ---------- tablas (sobre el XML en bruto) ----------
def find_table(x,title_prefix,nth=0):
    ps=all_paras(x); hits=[j for j,(a,b) in enumerate(ps) if vis_text(x[a:b]).startswith(title_prefix)]
    assert hits,title_prefix; j=hits[nth]; pos=ps[j][1]
    while True:
        a=x.index('<w:tbl>',pos); b=balanced_end(x,a,'w:tbl')
        if live_rows(x,a,b): return a,b
        pos=b
def live_rows(x,a,b):
    dele=deleted_row_spans(x); out=[]
    for m in re.finditer(r'<w:tr[\s>]',x[a:b]):
        rs=a+m.start()
        if any(s<=rs<e for s,e in dele): continue
        if any(s<rs<e for s,e in out): continue
        out.append((rs,balanced_end(x,rs,'w:tr')))
    return out
def cell_spans(x,rs,re_):
    out=[]
    for m in re.finditer(r'<w:tc[\s>]',x[rs:re_]):
        cs=rs+m.start()
        if any(s<cs<e for s,e in out): continue
        out.append((cs,balanced_end(x,cs,'w:tc')))
    return out
def para_idx_in(x,s,e): return [j for j,(a,b) in enumerate(all_paras(x)) if s<=a<e]
def cell_set(title,row,col,new,nth=0,check=None):
    global x
    a,b=find_table(x,title,nth); rows=live_rows(x,a,b); cs=cell_spans(x,*rows[row]); s,e=cs[col]
    idx=para_idx_in(x,s,e); ps=all_paras(x); old=' / '.join(vis_text(x[ps[j][0]:ps[j][1]]) for j in idx)
    if check: assert check in old,(title,row,col,old[:80])
    for j in sorted(idx[1:],reverse=True): x=del_para(x,ctx,j,AUT)
    x=set_text(x,ctx,idx[0],new,AUT); log.append((f'{title[:25]} r{row}c{col}',old,new))
def cell_pairs(title,row,col,prs,nth=0):
    global x
    a,b=find_table(x,title,nth); rows=live_rows(x,a,b); cs=cell_spans(x,*rows[row]); s,e=cs[col]
    idx=para_idx_in(x,s,e); ps=all_paras(x)
    for j in sorted(idx,reverse=True):
        t=vis_text(x[ps[j][0]:ps[j][1]]); new=t
        for o,n in prs:
            if o in new: new=new.replace(o,n)
        if new!=t: log.append((f'{title[:25]} r{row}c{col}',t,new)); x=set_text(x,ctx,j,new,AUT)
def delete_row(title,row,nth=0):
    global x
    a,b=find_table(x,title,nth); rows=live_rows(x,a,b); idx=para_idx_in(x,*rows[row]); x=del_row(x,ctx,idx[0],AUT); log.append((f'{title[:25]} fila {row}','(fila eliminada)',''))
def rebuild_table(title,new_rows,keep_cols=None,merge_from=None,nth=0):
    """new_rows: lista de listas de textos. keep_cols: nº de columnas finales; merge_from: índice de la celda a partir de la cual se fusionan las restantes."""
    global x
    a,b=find_table(x,title,nth); rows=live_rows(x,a,b)
    grid=[int(v) for v in re.findall(r'<w:gridCol w:w="(\d+)"',x[a:b])]
    tmpl_rows=[]
    for k,(rs,re_) in enumerate(rows):
        row=accept_all(x[rs:re_])[0]; row=re.sub(r'\sw14:(?:paraId|textId)="[^"]*"','',row); tmpl_rows.append(row)
    def build(row_xml,texts):
        cs=[(m.start(),balanced_end(row_xml,m.start(),'w:tc')) for m in re.finditer(r'<w:tc[\s>]',row_xml)]
        cs=[c for c in cs if not any(s<c[0]<e for s,e in cs if (s,e)!=c)]
        cells=[row_xml[s:e] for s,e in cs]
        if merge_from is not None:
            w=sum(grid[merge_from:]); tc=cells[merge_from]
            tc=re.sub(r'<w:tcW w:w="\d+"',f'<w:tcW w:w="{w}"',tc,count=1); tc=re.sub(r'<w:gridSpan [^>]*/>','',tc); tc=re.sub(r'(<w:tcW\b[^>]*/>)',r'\1<w:gridSpan w:val="%d"/>'%len(grid[merge_from:]),tc,count=1)
            cells=cells[:merge_from]+[tc]
        assert len(cells)==len(texts),(len(cells),len(texts))
        cells=[cell_text(tc,t) for tc,t in zip(cells,texts)]
        return row_xml[:cs[0][0]]+''.join(cells)+row_xml[cs[-1][1]:]
    new_xml=''.join(mark_ins_row(build(tmpl_rows[0] if k==0 else tmpl_rows[min(k,len(tmpl_rows)-1)],t),ctx,AUT,ctx.ns) for k,t in enumerate(new_rows))
    for rs,re_ in reversed(rows): idx=para_idx_in(x,rs,re_); x=del_row(x,ctx,idx[0],AUT)
    assert x.startswith('<w:tbl>',a); b=balanced_end(x,a,'w:tbl'); x=x[:b-len('</w:tbl>')]+new_xml+x[b-len('</w:tbl>'):]
    log.append((f'{title[:25]} reconstruida','',' | '.join(' ; '.join(r) for r in new_rows)[:400]))
def table_cells_text(title,nth=0):
    a,b=find_table(x,title,nth); out=[]
    for rs,re_ in live_rows(x,a,b):
        cs=cell_spans(x,rs,re_); ps=all_paras(x)
        out.append([' / '.join(vis_text(x[ps[j][0]:ps[j][1]]) for j in para_idx_in(x,s,e)) for s,e in cs])
    return out
# ---------- valores ----------
OMv=206120.292278
def van_r(base,r): return base-sum(OMv/(1+r)**t for t in range(8,31))
v8=van_r(78956971,0.08); v16=van_r(9400633,0.16)
def M(v): return f'{v/1e6:,.2f}'.replace(',','_').replace('.',',').replace('_','.')
def U(v): return f'{round(v):,.0f}'.replace(',','.')
PUB=33101387.79; CONV=47725355.51
# plantilla de tabla (Montecarlo) tomada antes de cualquier edición
_a,_b=find_table(x,'Distribución del VAN en la simulación de Montecarlo con las decisiones adoptadas'); TPL41=re.sub(r'\sw14:(?:paraId|textId)="[^"]*"','',accept_all(x[_a:_b])[0])
def new_p(style,text):
    p=f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr><w:r><w:t xml:space="preserve">{html.escape(text,quote=False)}</w:t></w:r></w:p>'
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
    def mkrow(row,texts):
        cs=[]
        for m in re.finditer(r'<w:tc[\s>]',row):
            c=m.start()
            if any(s<c<e for s,e in cs): continue
            cs.append((c,balanced_end(row,c,'w:tc')))
        cells=[row[s:e] for s,e in cs]
        while len(cells)<len(texts): cells.append(cells[-1])
        out=[]
        for tc,t,w in zip(cells,texts,widths):
            tc=re.sub(r'<w:tcW [^>]*/>',f'<w:tcW w:w="{w}" w:type="dxa"/>',tc,count=1); tc=re.sub(r'<w:gridSpan [^>]*/>','',tc); out.append(cell_text(tc,t))
        return row[:cs[0][0]]+''.join(out)+row[cs[-1][1]:]
    grid='<w:tblGrid>'+''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)+'</w:tblGrid>'
    body=''.join(mark_ins_row(mkrow(rows[0] if k==0 else rows[1],t),ctx,AUT,ctx.ns) for k,t in enumerate(rows_texts))
    return '<w:tbl>'+tblpr+grid+body+'</w:tbl>'
def insert_after(i,block,text=None,occ=None):
    global x
    j=raw_index_by_text(x,text or A[i],occ); e=all_paras(x)[j][1]; x=x[:e]+block+x[e:]; log.append((f'inserción tras [{i}]','',vis_text(block)[:300]))
# ====================== TEXTOS ======================
full(11,'Anexo electrónico EEO2 del Informe de Terminación de Proyecto (PCR)')
full(23,'Fuente de cuadro: elaboración propia a partir del Libro de Confiabilidad y VAN (EEO5), hojas AMI_Regla (celdas D20 y D21, resultado publicado), VAN_Programa (celdas G18 y J18, convención de facturación) y Flujo_Anual (TIR en las celdas B24 y D24 y recuperación descontada en B34 y D34). Horizonte 2015-2045, dólares constantes de 2015 con 2015 = t₀ y tasa social de descuento del 12 %. Escenario adoptado: atribución del ∆TTIk igual a cero, medición inteligente en su escenario base focalizado (44,8 GWh/año; banda 26,4 a 97,1) con el ahorro operativo por gestión remota incluido y con su gasto de operación y mantenimiento al 2,5 % anual del CAPEX, y pérdidas de subtransmisión en su serie declarada. El Programa publica +33.101.387,79 dólares con la medición inteligente valorada como transferencia (resultado publicado) y declara +47.725.355,51 con la convención de facturación (apartado 8.4).')
pairs(127,[('o de una réplica externa no tienen celda viva en esos libros','o de fuentes ajenas a los libros no tienen celda viva en ellos')])
pairs(131,[('(salidas de las estimaciones econométricas y réplicas externas)','(salidas de las estimaciones econométricas y fuentes ajenas a los libros)')])
pairs(134,[('+13.112.347 dólares en la base focalizada (incl. ahorro C&R; banda +5,29 a +31,77 millones) en el marco del subcomponente C2.3 aislado y +7.123.045 dólares en el marco del objetivo específico II completo (base E3: +6.608.522 y +619.220).','+12.392.693 dólares en la base focalizada (incluido el ahorro operativo; banda +4,57 a +31,05 millones) en el marco del subcomponente C2.3 aislado y +6.403.391 dólares en el marco del objetivo específico II completo, ambos con la convención de facturación y con el gasto de operación y mantenimiento de la medición inteligente al 2,5 % anual de su CAPEX.')])
pairs(135,[('son 4,38 en el marco del subcomponente (incl. C&R) y 1,722 en el del objetivo','son 3,70 en el marco del subcomponente (incluido el ahorro operativo) y 1,605 en el del objetivo')])
pairs(138,[('El valor actual neto que este documento publica es de +33.821.041,83 dólares bajo la regla de transferencias del componente de medición inteligente (lectura B; razón beneficio/costo 1,4708; apartado 8.4), con +48.445.009,55 dólares bajo la convención de facturación, declarada como convención de referencia (lectura A; razón 1,6744). Ambas cifras incorporan, además de la energía adicional servida y las pérdidas de subtransmisión evitadas, los canales de confiabilidad por contribución (frecuencia y duración, apartado 8.4); sin ellos el valor actual neto de referencia es de +15.459.050 dólares (lectura A sin canales; banda +7,64 a +34,12 millones) o +835.082 dólares (lectura B sin canales), con la reestimación corregida de +731.265 dólares como piso metodológico y su cascada de conciliación de treinta y cuatro escalones agrupados en seis causas documentada en el libro.',
 'El valor actual neto que este documento publica es de +33.101.387,79 dólares con la medición inteligente valorada como transferencia (resultado publicado; razón beneficio/costo 1,4563; apartado 8.4), con +47.725.355,51 dólares bajo la convención de facturación, declarada como convención de referencia (razón 1,6578). Ambas cifras incorporan, además de la energía adicional servida y las pérdidas de subtransmisión evitadas, los beneficios de confiabilidad por contribución (frecuencia y duración, apartado 8.4) y el gasto de operación y mantenimiento de la medición inteligente al 2,5 % anual de su CAPEX; la reestimación corregida de +731.265 dólares queda como piso metodológico, con su cascada de conciliación de treinta y cuatro escalones agrupados en seis causas documentada en el libro.')])
pairs(143,[('la simulación del componente de medición de esta evaluación (semilla fija, moda del componente en la base focalizada, sin los canales de confiabilidad; memoria) da 83,5 %, con percentil 5 en −10,8 millones y percentil 95 en +62,4; la simulación del Programa completo con los canales de confiabilidad (apartado V.7 siguiente) sitúa la probabilidad de VAN negativo en 11,5 % bajo la lectura publicada y en 1,4 % bajo la convención declarada: la banda es positiva con alta probabilidad, no «enteramente».',
 'la simulación del Programa completo de esta evaluación, con los beneficios de confiabilidad (apartado V.7 siguiente), sitúa la probabilidad de VAN negativo del resultado publicado en 7,70 %, con percentil 5 en −3,35 millones y percentil 95 en +64,77: la banda es positiva con alta probabilidad, no «enteramente».')])
full(144,'Simulación de riesgo de esta evaluación. La simulación de Montecarlo del Programa completo, con las variables de riesgo declaradas —incluidos los beneficios de confiabilidad por frecuencia y duración del apartado 8.4—, corre en el propio Libro de Confiabilidad y VAN (EEO5, hoja MC_B): 10.000 simulaciones sobre nueve parámetros inciertos con distribuciones triangulares, PERT y discretas dentro de sus bandas de evidencia, correlación de 0,5 entre el excedente del consumidor y la utilización, y semilla 20260917. Da una probabilidad de valor actual neto negativo del 7,70 % para el resultado publicado (media 27,75 millones; mediana 26,14; percentil 5 en −3,35 y percentil 95 en 64,77). La simulación del componente de medición que acompañaba al análisis preliminar de este anexo (hoja MonteCarlo del Libro de Análisis) se conserva como memoria histórica y no es el riesgo del Programa.')
pairs(149,[('en la lectura B publicada (65,0 % en la lectura A sin canales, base focalizada; 70,2 % en la base E3; 78,2 % en la reestimación corregida)','en el resultado publicado'),('un canal monetizado de 44,8 GWh/año en la base focalizada (27,0 en la lectura prudente E3; 10,62 en la reestimación corregida), frente a','un canal monetizado de 44,8 GWh/año en la base focalizada, frente a')])
full(151,'E.4El resultado consolidado es positivo. Con las decisiones adoptadas y los beneficios de confiabilidad por contribución (frecuencia y duración, capítulo 8), el Programa presenta un valor actual neto de US$33,10 millones con la medición inteligente valorada como transferencia (resultado publicado; razón beneficio/costo 1,4563) y de US$47,73 millones bajo la convención de facturación declarada (razón 1,6578). La tasa interna de retorno es de 18,34 % en el resultado publicado (20,22 % en la convención); la recuperación descontada ocurre en 2027 (Libro de Confiabilidad y VAN, EEO5, hoja Flujo_Anual, celdas B24, D24, B34 y D34). El margen es material: el valor presente de los beneficios tendría que caer un 31,3 % para anular el resultado publicado. La sostenibilidad posterior al préstamo conserva el signo positivo incluso en la degradación severa: basta conservar el 29,6 % de los beneficios posteriores a 2025. La rejilla de escenarios método × comparador del modelo anterior abarca desde −12,35 millones hasta +124,65 millones, y la celda adoptada es la prudente dentro de ese rango, no la central.')
pairs(153,[('—US$33,82 millones publicados (lectura B) o US$48,45 millones bajo la convención declarada (lectura A); US$15,46 millones (lectura A sin canales) o US$0,84 millones (lectura B sin canales); TIR 18,45 % en la lectura B publicada, 12,18 % en la lectura B sin canales y 14,84 % en la lectura A sin canales—','—US$33,10 millones publicados o US$47,73 millones bajo la convención de facturación declarada; TIR de 18,34 % en el resultado publicado—')])
pairs(154,[('el Monte Carlo del componente de medición (memoria, sin los canales de confiabilidad) eleva la probabilidad de VAN positivo del componente a 83,5 % con la base focalizada —la simulación del Programa completo, con los canales de confiabilidad, se documenta en el apartado V.7—;','la simulación de Montecarlo del Programa completo, con los beneficios de confiabilidad, deja la probabilidad de VAN negativo del resultado publicado en 7,70 % (apartado V.7);'),('al nivel focalizado (+15,46 millones, lectura A sin canales); el resto','al nivel focalizado; el resto')])
pairs(347,[('en la lectura B publicada (88,62 % sin canales; 73,8 % en la lectura A sin canales, base focalizada; 79,7 % en la base E3; 88,8 % en la reestimación corregida; Libro de Confiabilidad y VAN, EEO5, hoja Mapa_Objetivos, celdas D36 a D38)','en el resultado publicado (Libro de Confiabilidad y VAN, EEO5, hoja Mapa_Objetivos, celda D36)')])
pairs(512,[('(EEO#4)','(EEO5)')])
pairs(791,[('en la lectura B publicada (65,0 % en la lectura A sin canales, base focalizada; 70,2 % en la base E3)','en el resultado publicado')])
pairs(927,[('y VAN del Programa (US$731.265 en la reestimación corregida, hoja Por_Componente, celda F16; US$15.459.050 en la base focalizada, lectura A sin canales, hoja Por_Objetivo, celda D8).','y VAN publicado del Programa (US$33.101.388; Libro de Confiabilidad y VAN, EEO5, hoja AMI_Regla, celda D20).'),('por construcción, el VAN del Programa es el central menos la parte no atribuida del canal.','por construcción, el VAN del Programa es el publicado menos la parte no atribuida del canal.')])
pairs(928,[('el valor actual neto del Programa sería de −US$13,45 millones.','el valor actual neto publicado del Programa sería de +US$18,92 millones, y con una del 50 %, de +US$4,73 millones; el signo se invierte por debajo del 42 % de atribución.')])
for i in (932,933,1290,2028,2029,2033): pairs(i,[('(EEO#4)','(EEO3)')])
pairs(988,[('Aporta 0,9 veces el valor actual neto del Programa completo en la base focalizada (1,5 en la base E3; 18,72 en la reestimación corregida, cuando los otros dos objetivos consumían casi todo su excedente).','Aporta 0,4 veces el valor actual neto publicado del Programa.'),('en la lectura B publicada (88,62 % sin canales; 73,8 % en la lectura A sin canales, base focalizada; 79,7 % en la base E3; 88,8 % en la reestimación corregida).','en el resultado publicado.')])
pairs(1030,[('(f_C = f_B = 0), a la espera del dato de campo por obra—','(f_C = f_B = 0), porque el dato de campo por obra no está disponible al cierre—'),('por lo que el canal permanece en memoria hasta contar con el dato de conexiones nuevas por obra que el apartado 10.5 ya solicita para este mismo componente.','por lo que el canal permanece en memoria: el dato de conexiones nuevas por obra no está disponible al cierre (apartado 10.5).')])
full(1285,'Fuente de cuadro: libro de análisis, hoja Escenarios_Componente (enlazada a Flujo_Programa). Dólares de 2015 descontados al 12 %. El VAN del componente incluye el ahorro operativo y el gasto de operación y mantenimiento de la medición inteligente al 2,5 % anual de su CAPEX. Las columnas del VAN, la TIR y la razón beneficio/costo del Programa por escenario se retiran de este cuadro: correspondían a una lectura interna sin los beneficios de confiabilidad. El resultado publicado del Programa, con la base focalizada, es un VAN de US$33.101.387,79, una TIR de 18,34 % y una razón beneficio/costo de 1,4563 (Libro de Confiabilidad y VAN, EEO5, hojas AMI_Regla, celdas D20 y D21, y Flujo_Anual, celda D24).')
pairs(1289,[('con la valoración (beneficio creciente más ahorro C&R) el objetivo alcanza VAN positivo ya con la lectura prudente de 27,0 GWh/año (+619.220) y llega a +7.123.045 con la base focalizada.','con la valoración (beneficio creciente más ahorro operativo) y el gasto de operación y mantenimiento de la medición inteligente al 2,5 %, el objetivo alcanza VAN positivo con la base focalizada (+6.403.391); con la lectura prudente de 27,0 GWh/año quedaría en −100.434, prácticamente en cero.')])
pairs(1333,[('verificarla exige el consumo mensual por usuario de las cuentas con medidor del Programa en CNEL (solicitud nº 7). Sin ese dato, la lectura conservadora es la cota E2 (26,4 GWh/año; VAN del Programa 7,64 millones) y la que el balance de red hace verosímil es el tope E1 (34,12 millones).','verificarla exigiría el consumo mensual por usuario de las cuentas con medidor del Programa en CNEL, dato que no está disponible al cierre (vacío nº 7 del apartado 10.5). Sin ese dato, la lectura conservadora es la cota E2 (26,4 GWh/año; VAN del componente 4,57 millones) y la que el balance de red hace verosímil es el tope E1 (31,05 millones).')])
pairs(1617,[('el valor presente del canal de medición inteligente es el 18,8 % de los beneficios del Programa en la base focalizada (19,5 % con el ahorro C&R, no expuesto a esta asimetría; base E3: 12,2 % y 13,0 %; reestimación corregida: 3,1 %).','el valor presente del canal de medición inteligente es el 14,1 % de los beneficios del Programa con la convención de facturación (16,99 de 120,27 millones) y el 2,2 % en el resultado publicado, donde la facturación recuperada se trata como transferencia.')])
pairs(1684,[('+US$13.112.347 con razón beneficio/costo de 4,38 (incl. ahorro C&R; base E3: +6.608.522). En el marco del objetivo completo es de +US$7.123.045 con razón de 1,722 (base E3: +619.220).','+US$12.392.693 con razón beneficio/costo de 3,70 (incluidos el ahorro operativo y el gasto de operación y mantenimiento al 2,5 %). En el marco del objetivo completo es de +US$6.403.391 con razón de 1,605.')])
pairs(1686,[('la convención de facturación (lectura A), que acredita','la convención de facturación, que acredita'),('la regla de transferencias (lectura B, recomendada por el auditor; f=1,2, λ=0,5)','la regla de transferencias (f=1,2, λ=0,5)'),('La regla de transferencias (lectura B) es la que se publica, por coherencia con la regla FERUM del EC-L1160 (EEO#8, apartado 12); la convención de facturación (lectura A) se declara como convención de referencia.','La regla de transferencias es la que se publica, por coherencia con la regla FERUM del EC-L1160 (EEO9, apartado 12); la convención de facturación se declara como convención de referencia.')])
pairs(2020,[('Con la base focalizada (44,8 GWh/año; lectura A sin canales) el escenario adoptado de atribución 0,00 es +15.459.050 y el de atribución 0,564 llevaría el VAN a ≈48,7 millones (Análisis Económico, Cuadro 19).','Los escenarios de esta rejilla se conservan como memoria del modelo de la reestimación corregida; el resultado publicado, con la base focalizada, los beneficios de confiabilidad y el gasto de operación de la medición inteligente, es de 33.101.387,79 dólares (Cuadro 23).')])
pairs(2199,[('celda C41 (lectura B; celda B41, +32.861.246 USD, en la lectura A)','celda C41 (resultado publicado; celda B41, +32.141.591 USD, con la convención de facturación)')])
pairs(2200,[('un valor actual neto de +18.237.278 dólares en la lectura B publicada (+32.861.246 en la lectura A; Cuadro 14 y apartado 8.4)','un valor actual neto de +17.517.624 dólares en el resultado publicado (+32.141.591 con la convención de facturación; Cuadro 14 y apartado 8.4)'),('sin los canales de contribución C2.1 y C2.2/C2.4— y no al OED II oficial','antes de los beneficios de confiabilidad por contribución— y no al OED II oficial')])
pairs(2399,[('Se solicita que el PMR final muestre 1.999.','El PMR vigente muestra 1.607 por su definición del universo; la cifra adoptada en todo el paquete es 1.999.')])
pairs(2477,[('La sensibilidad a la tasa de descuento se corre sobre la lectura B publicada: con el 8 % el VAN del Programa es de US$78.956.971 y con el 16 % de US$9.400.633 (con los canales de confiabilidad; sin ellos, US$28.739.140 y −US$13.307.676; Libro de Confiabilidad y VAN, EEO5, hoja Sostenibilidad_Tasa, celdas B81, B86, C81 y C86).',f'La sensibilidad a la tasa de descuento se corre sobre el resultado publicado: con el 8 % el VAN del Programa es de US${U(v8)} y con el 16 % de US${U(v16)} (con los beneficios de confiabilidad y el gasto de operación de la medición inteligente; Libro de Confiabilidad y VAN, EEO5, hoja Sostenibilidad_Tasa, celdas B81 y B86).'),('corresponden al modelo de la reestimación corregida, sin los canales de confiabilidad por contribución (que este documento valora aparte en el apartado 8.4); la lectura publicada es la B, con esos canales (Cuadro 23).','corresponden al modelo de la reestimación corregida, antes de los beneficios de confiabilidad por contribución (que este documento valora aparte en el apartado 8.4); el resultado publicado, con esos beneficios, está en el Cuadro 23.'),('cuyo VAN oficial en la lectura B publicada es de +16.203.286 y +18.237.278 USD','cuyo VAN oficial en el resultado publicado es de +16.203.286 y +17.517.624 USD')])
full(2486,'8.6Incluso el escenario adoptado debe leerse con cautela, y por dos razones que conviene enunciar juntas. La primera es aritmética: con el valor actual neto de la reestimación corregida de 731.265 dólares bastaba una caída del 1,01 % de los beneficios; en el resultado publicado, con los beneficios de confiabilidad, el umbral es del 31,3 % (EEO5, hoja Sostenibilidad_Tasa, celda B55). La segunda es probabilística: la simulación de esta evaluación (10.000 simulaciones, semilla 20260917) da una probabilidad de VAN negativo del 7,70 %, con mediana de US$26,14 millones y percentiles 5 y 95 en −US$3,35 y +US$64,77 millones; la de la reestimación corregida (51,49 % de VAN positivo) queda como referencia histórica.')
pairs(2487,[('(lectura A sin canales, base focalizada: 73,8 % y 65,0 %; base E3: 79,7 % y 70,2 %; reestimación corregida: 88,8 % y 78,2 %; EEO5, hoja Mapa_Objetivos, celdas D37 y H21)','(EEO5, hoja Mapa_Objetivos, celdas D37 y H21)'),('El análisis de tornado lo confirma: los tres primeros parámetros por rango de valor actual neto son el factor de excedente (US$75,65 millones de rango), la atribución del ∆TTIk sobre la serie del modelo anterior (US$71,73 millones) y el factor de confiabilidad (US$66,78 millones).','El análisis de tornado del resultado publicado lo confirma: los tres primeros parámetros por rango de valor actual neto son el factor de excedente del consumidor, la energía no suministrada evitada por MVA y la utilización de la capacidad nueva (EEO5, hoja Umbrales_B).')])
full(2518,'8.11La defensa de esta revisión no es de tamaño sino de calidad. Una tasa interna de retorno del 18,34 % y una razón beneficio/costo de 1,4563 (resultado publicado; Libro de Confiabilidad y VAN, EEO5, hoja Flujo_Anual, celdas D24 y D22), calculadas sobre contrafactuales medidos, con seis pruebas de robustez publicadas incluso cuando contradicen la hipótesis del Programa, valen más ante una revisión independiente que un resultado grande sostenido en una atribución fijada a mano y en una cantidad física que no se reproduce con el microdato. La corrección es el argumento de credibilidad.')
full(2520,'8.12La rejilla de escenarios es determinista: cada celda fija un valor de cada decisión. La simulación de Montecarlo hace lo contrario: sortea a la vez los nueve parámetros con banda declarada, diez mil veces con semilla fija (20260917), y devuelve la distribución del resultado publicado. Corre en la hoja MC_B del Libro de Confiabilidad y VAN y arroja los percentiles siguientes.')
full(2557,'Fuente de cuadro: Libro de Confiabilidad y VAN (EEO5), hoja MC_B (10.000 simulaciones, nueve parámetros inciertos, semilla 20260917; dólares de 2015 descontados al 12 %). Media 27.750.939 y desviación típica 20.610.434. La simulación histórica del componente de medición del Libro de Análisis (hoja MonteCarlo) y la de la reestimación corregida se conservan como memoria en el apéndice C del Análisis Económico.')
full(2558,'8.13La lectura es directa: el resultado publicado conserva VAN positivo en el 92,3 % de los mundos compatibles con las bandas; la mediana (26,14 millones) queda por debajo del caso central (33,10) por la asimetría de las bandas de valoración. Los resultados negativos se concentran en las simulaciones con excedente del consumidor y utilización bajos a la vez, los dos primeros parámetros del tornado.')
full(2559,'8.14El análisis de sostenibilidad posterior al préstamo completa el cuadro de riesgo. El modelo anterior declaraba sostenibles sus cuatro escenarios de degradación; la reestimación corregida invertía el signo ya con la degradación leve (−2,35 millones). Sobre el resultado publicado, con los beneficios de confiabilidad, el valor actual neto conserva el signo positivo en los tres escenarios de degradación: la leve (operación al 90 %) lo deja en +28,4 millones, la moderada (operación al 70 % y O&M un 20 % mayor) en +18,0 y la severa (50 % y O&M un 50 % mayor) en +7,0; el punto de quiebre es conservar el 29,6 % de los beneficios posteriores a 2025 (Libro de Confiabilidad y VAN, EEO5, hoja Sostenibilidad_Tasa, celdas B50 a B54; Análisis Económico, Cuadro 24).')
full(2560,'8.15Esa fragilidad no la produce el análisis de sostenibilidad: la produce el flujo base. El valor actual neto de la reestimación corregida de 731.265 dólares dejaba un margen del 1,01 %; en el resultado publicado, con los beneficios de confiabilidad, el margen es del 31,3 %. La consecuencia práctica para el Banco es que la sostenibilidad de este Programa depende por completo de que la capacidad instalada siga operando y utilizándose: el 53,71 % del valor presente de los beneficios es energía adicional servida, y esa energía se pierde si la capacidad se subutiliza.')
full(2562,'8.16El estudio de contribución de los beneficios de confiabilidad añade al valor actual neto del Programa dos canales que la reestimación corregida no incorporaba: 20.415.039 dólares por el canal de frecuencia (C2.1, apartado 4.6.1) y 12.570.921 dólares por el canal de duración (C2.2/C2.4, apartado 4.6.3). Con la convención de facturación del componente de medición inteligente, declarada como convención, el valor actual neto es de 47.725.355,51 dólares (razón beneficio/costo 1,6578). Aplicando en su lugar la regla de transferencias de la medición inteligente (f=1,2, λ=0,5), el componente resta 14.623.968 dólares de esa cifra y el valor actual neto publicado del Programa es de 33.101.387,79 dólares, con razón beneficio/costo de 1,4563. Ambas cifras cargan el gasto de operación y mantenimiento de la medición inteligente al 2,5 % anual de su CAPEX. La regla de transferencias es la lectura publicada; la convención de facturación queda declarada como convención de referencia (EEO9, apartado 12). Ninguna de las dos afecta el valor de los canales de frecuencia y duración, que son independientes de la regla de la medición inteligente. Las cantidades físicas de ambos canales, interrupciones evitadas y su duración, se estiman sobre el panel histórico de calidad de servicio por alimentador del regulador ecuatoriano (ARCONEL), con la frecuencia y la duración de las interrupciones observadas en la propia red del Ecuador entre 2008 y 2025, y no sobre parámetros importados (apartado 4.6).')
full(2624,'Fuente: elaboración propia a partir de VAN_Programa!A7:K18 y Mapa_Objetivos!C9:C12/F9:F12 del Libro de Confiabilidad y VAN (EEO5). Filas redondeadas a la unidad; pueden no sumar exactamente por redondeo (el total es 47.725.355,51 con la convención de facturación y 33.101.387,79 en el resultado publicado).')
full(2778,'9.3\tCon los beneficios de confiabilidad del estudio de ENS —contribución, no atribución—, el valor actual neto del Programa es de 47.725.355,51 dólares bajo la convención de facturación de la medición inteligente (razón beneficio/costo 1,6578) y de 33.101.387,79 dólares con la medición inteligente valorada como transferencia (resultado publicado; razón 1,4563). Las veinte dimensiones de la fila 1 a la 20 no cambian: los dos canales nuevos (frecuencia, +20.415.039; duración, +12.570.921) se documentan por separado en el apartado 4.6 y en el apartado 8.4, con su cascada y su banda.')
pairs(2794,[('con el valor coherente el valor actual neto del Programa —sin los canales de confiabilidad, lectura A— cae, en el escenario base, a −US$23,51 millones (reestimación corregida: −US$31,74).','con el valor coherente el valor actual neto publicado cae, en el escenario base, a cerca de +US$0,6 millones, al borde de su valor de cambio de 0,4166 (EEO5, hoja Umbrales_B).')])
pairs(2797,[('(agrupación interna, sin los canales C2 de contribución)','(agrupación interna, antes de los beneficios de confiabilidad por contribución)')])
pairs(2812,[('cuyo efecto está acotado al 18,8 % de los beneficios en la base focalizada (19,5 % con el ahorro C&R incluido; base E3: 12,2 % y 13,0 %; reestimación corregida: 3,1 %).','cuyo efecto está acotado al 14,1 % de los beneficios con la convención de facturación y al 2,2 % en el resultado publicado.')])
pairs(2814,[('Solicitudes de datos que se elevan a las distribuidoras. Las limitaciones declaradas en este documento se convierten en diez solicitudes concretas, consolidadas en la hoja Solicitudes_EED del libro de análisis:','Vacíos de dato declarados al cierre. Las limitaciones de este documento se cierran con la información recopilada y no se elevan nuevas solicitudes a las distribuidoras. Los diez vacíos, registrados en la hoja Solicitudes_EED del libro de análisis, son:'),('(habilita los canales de acceso y regularización del C1.2, hoy pro memoria)','(habilitaría los canales de acceso y regularización del C1.2, hoy pro memoria)'),('(fija la fracción de absorción del contrafactual físico)','(fijaría la fracción de absorción del contrafactual físico)'),('(afina la prima de consumo 1,79)','(afinaría la prima de consumo 1,79)'),('que verifica directamente la prima de consumo','que verificaría directamente la prima de consumo'),('que permitiría construir la dosis-respuesta','que permitiría construir la dosis-respuesta'),('Cada una cierra un frente abierto identificado en la evidencia del trabajo de campo.','Cada uno acota un frente abierto identificado en la evidencia del trabajo de campo; su cierre queda para las operaciones sucesoras.')])
pairs(2830,[('el anexo electrónico EEO#2','el anexo electrónico EEO2')])
pairs(3013,[('(EEO#4)','(EEO5)'),('los canales C2.1 y C2.2/C2.4','los beneficios de confiabilidad (C2.1 y C2.2/C2.4)')])
pairs(781,[('(EEO#4)','(EEO3)'),('que se solicita a las EED','no disponible al cierre (apartado 10.5)'),('el canal de acceso a la espera de dato','el canal de acceso sin dato al cierre')])
pairs(1319,[('(solicitud nº 7)','(vacío de dato nº 7, apartado 10.5)')])
pairs(1615,[('es de 18,83 % en la base focalizada (12,72 % en la base E3)','es de 18,23 % en la base focalizada, con el gasto de operación y mantenimiento de la medición inteligente al 2,5 % anual de su CAPEX; en la base E3 el VAN del objetivo queda en −100.434 dólares y la TIR por debajo del 12 %')])
pairs(1620,[('+US$7.123.045 en el marco del objetivo II (base E3: +619.220; reestimación corregida: −US$7.604.739)','+US$6.403.391 en el marco del objetivo II (base E3: −US$100.434; reestimación corregida: −US$7.604.739)')])
pairs(2414,[('(piso metodológico, superado por el escenario base focalizado: +15.459.050, lectura A sin canales)','(piso metodológico; el resultado publicado es +33.101.388, Cuadro 23)')])
pairs(2422,[('SÍ (reestimación corregida; referencia: la base focalizada, +15.459.050, lectura A sin canales; el VAN publicado es el de la lectura B, Cuadro 23)','SÍ (reestimación corregida; el resultado publicado es +33.101.388, Cuadro 23)')])
pairs(2515,[('y a la base focalizada de 15.459.050 (escalón +6.503.826: ajuste de focalización)','y a la base focalizada de 15.459.050 (escalón +6.503.826: ajuste de focalización), que el gasto de operación y mantenimiento de la medición inteligente al 2,5 % deja en 14.739.396 antes de los beneficios de confiabilidad (escalón −719.654)')])
# rótulos de figuras (índice y cuerpo): sustitución documento a documento al final
CAPS=[
 ('Figura 31. Sin los canales C2 el VAN sería de 15,46; C2.1 y C2.2/C2.4 lo llevan a 48,45 (valor presente, millones de dólares)','Figura 31. Del valor presente de los beneficios (120,27) al resultado publicado (33,10): los beneficios de confiabilidad aportan 32,99 y la transferencia de la medición inteligente resta 14,62 (millones de dólares de 2015)'),
 ('Figura 32. El valor actual neto es positivo en toda la banda de cada canal C2 y sin ellos (15,46); C2.1 va de 1,91 a 28,63, C2.2/C2.4 de 9,17 a 14,99 (millones de dólares)','Figura 32. El resultado publicado sigue positivo en toda la banda de cada beneficio de confiabilidad: de 14,6 a 41,3 millones con el canal de frecuencia y de 29,7 a 35,5 con el de duración (millones de dólares de 2015)'),
 ('Figura 34. Del TTIK observado al VAN: dos canales de contribución (frecuencia y duración) cierran en 48,45 millones de USD (esquema)','Figura 34. Del TTIK observado al VAN: dos canales de contribución (frecuencia y duración) cierran en 47,73 millones de USD con la convención de facturación y en 33,10 en el resultado publicado (esquema)'),
 ('Figura 43. Sin los canales C2 el VAN sería de 15,46; C2.1 y C2.2/C2.4 lo llevan a 48,45 (VP, millones de USD)','Figura 43. Del valor presente de los beneficios (120,27) al resultado publicado (33,10): los beneficios de confiabilidad aportan 32,99 y la transferencia de la medición inteligente resta 14,62 (VP, millones de USD)'),
 ('Figura 45. El VP acumulado del programa llega en 2045 a 48,45 con los dos canales C2 y a 15,46 sin ellos (millones de USD)','Figura 45. El VP acumulado del programa cruza cero en 2027 y llega en 2045 a 33,10 en el resultado publicado y a 47,73 en la convención de facturación (millones de USD)'),
 ('Figura 46. El VAN es positivo en toda la banda de cada canal C2 y sin ellos (15,46); C2.1 va de 1,91 a 28,63, C2.2/C2.4 de 9,17 a 14,99 (millones de USD)','Figura 46. El resultado publicado sigue positivo en toda la banda de cada beneficio de confiabilidad: de 14,6 a 41,3 millones con el canal de frecuencia y de 29,7 a 35,5 con el de duración (millones de USD)'),
 ('Figura 47. Con g = 0 % el VAN baja de 48,45 a 43,73; los tres canales de ENS crecen con la demanda (millones de USD)','Figura 47. Con g = 0 % el VAN publicado baja de 33,10 a 28,39 y la convención de facturación de 47,73 a 43,01; los tres canales de ENS crecen con la demanda (millones de USD)'),
 ('Figura 49. El VAN es negativo en una fracción pequeña de las simulaciones; sin el canal SCADA y sin los canales C2 esa fracción sube (millones de USD)','Figura 49. El VAN publicado es negativo en el 7,70 % de 10.000 simulaciones; mediana 26,14, percentiles 5 y 95 en −3,35 y 64,77 (millones de USD)'),
 ('Figura 44. Los canales C2 llevan el VAN de C2.1 de −4,17 a 16,25 y el de C2.2 de −5,90 a 6,56; el resto no se modifica (VAN, millones de USD)','Figura 44. Los beneficios de confiabilidad llevan el VAN publicado de 0,12 a 33,10 millones: C2.1 pasa de −4,17 a 16,25 y C2.2 de −5,90 a 6,56; el resto no se modifica (VAN, millones de USD)'),
 ('Figura 48. El excedente del consumidor explica buena parte de la varianza del VAN; las variables nuevas de los canales C2 aportan menos (millones de USD, %)','Figura 48. Ningún parámetro anula por sí solo el VAN publicado dentro de su banda de evidencia: valores de cambio frente a bandas (cambio respecto del valor central, %)'),
 ('Figura 50. El riesgo de VAN negativo se concentra en el grupo de capacidad y energía frente al programa completo (millones de USD)','Figura 50. El riesgo de VAN negativo crece al retirar los beneficios de confiabilidad: 7,70 % en el resultado publicado, 23,11 % sin el canal de duración y 54,32 % sin ambos canales (millones de USD)'),
 ('Cuadro — Valor actual neto por subcomponente, con y sin los canales de confiabilidad (contribución, no atribución; tabla auxiliar)','Cuadro — Valor actual neto por subcomponente y aporte de los beneficios de confiabilidad (contribución, no atribución; tabla auxiliar)'),
 ('Distribución del VAN en la simulación de Montecarlo con las decisiones adoptadas (tabla auxiliar)','Distribución del VAN publicado en la simulación de Montecarlo (tabla auxiliar)'),
]
# ====================== TABLAS ======================
# Ficha (T0)
cell_set('Ficha de resultados del análisis económico ex post al cierre',1,0,'Resultado publicado (medición inteligente valorada como transferencia): +33.101.387,79. Convención de facturación (declarada, no publicada como resultado central): +47.725.355,51',check='33.821.041,83')
cell_set('Ficha de resultados del análisis económico ex post al cierre',1,1,'1,4563 (resultado publicado) · 1,6578 (convención de facturación, declarada)',check='1,4708')
cell_set('Ficha de resultados del análisis económico ex post al cierre',1,2,'18,34 % (resultado publicado; recuperación descontada en 2027) · 20,22 % (convención de facturación, declarada; 2026)',check='18,45 %')
# T2 fila 5
cell_pairs('El anexo recorre cinco etapas encadenadas',5,3,[('→ VAN del Programa +33.821.042 (lectura B, publicada) / +48.445.010 (lectura A, declarada)','→ VAN del Programa +33.101.388 (resultado publicado) / +47.725.356 (convención de facturación, declarada)')])
# Cuadro 3 (T5)
cell_set('Cuadro 3. ¿Incluido en el análisis costo-beneficio?',3,3,'Canal monetizado principal: 53,71 % del valor presente de los beneficios en el resultado publicado. Único eslabón entre la capacidad física y el bienestar valorable',nth=1,check='53,71 %')
cell_set('Cuadro 3. ¿Incluido en el análisis costo-beneficio?',4,3,'Canal monetizado del OED II: 14,1 % del valor presente de los beneficios con la convención de facturación, ahorro operativo incluido, y 2,2 % en el resultado publicado, donde la facturación recuperada se trata como transferencia. Medido intra-medidor sobre panel balanceado',nth=1,check='18,8 %')
# T15 escenarios de atribución: columna VAN del Programa (publicado)
vp=[5674005,11348010,28370024,42555036,56740049]
for r,v in enumerate(vp,start=1):
    cell_set('R1.3 — Escenarios de porcentaje de atribución',r,4,U(PUB-(56740049-v)).replace('-','−'))
# T22 escenarios del componente: 10 → 6 columnas
old=table_cells_text('Cuadro — Escenarios del componente de medición',nth=1)
newrows=[old[0][:5]+['VAN del componente, incluidos el ahorro operativo y el O&M al 2,5 % (USD)']]
for r,v in zip(old[1:],[4569544,5888868,12392693,31054684]): newrows.append(r[:5]+[U(v)])
rebuild_table('Cuadro — Escenarios del componente de medición',newrows,merge_from=5,nth=1)
# Cuadro 14 (T27)
T='Cuadro 14. Resultado económico del OED II'; N=1
cell_set(T,2,1,'10.586.961 USD',nth=N,check='9.867.307'); cell_set(T,2,2,'CAPEX nominal 13.759.604 USD y OPEX nominal 13.651.147 USD, incluido el gasto de operación y mantenimiento de la medición inteligente al 2,5 % anual de su CAPEX',nth=N,check='8.910.380')
cell_set(T,3,1,'+6.403.391 USD',nth=N,check='7.123.045')
cell_set(T,3,2,'Positivo en el escenario base; con la lectura prudente E3 queda en −100.434 USD y en la reestimación corregida era negativo salvo con la ruta de 85,98 GWh. Cifra del objetivo específico II completo bajo la agrupación interna de este ejercicio, no del subcomponente C2.3 aislado (+12.392.693 USD, fila siguiente); el OED II oficial bajo la matriz del PCR se muestra en las dos filas finales.',nth=N,check='13.112.347')
cell_set(T,4,1,'18,23 % (agrupación interna)',nth=N,check='18,83 %'); cell_set(T,5,1,'1,605',nth=N,check='1,722')
cell_set(T,5,2,'Por cada dólar de costo el objetivo devuelve un dólar y sesenta centavos (lectura prudente E3: 0,99; reestimación corregida: veintitrés centavos)',nth=N,check='setenta')
cell_set(T,6,1,'2,24 % en el resultado publicado (EEO5, hoja Mapa_Objetivos, celda H24); 14,1 % con la convención de facturación',nth=N,check='2,24 %')
cell_set(T,7,1,'+12.392.693 USD (incluido el ahorro operativo)',nth=N,check='13.112.347'); cell_set(T,7,2,'Marco del subcomponente, con razón B/C de 3,70 (banda +4,57 a +31,05 M; lectura prudente E3: +5.888.868 y 2,28)',nth=N,check='4,38')
cell_set(T,9,0,'VAN oficial del OED II — con los beneficios de confiabilidad, convención de facturación',nth=N); cell_set(T,9,1,'+32.141.591 USD',nth=N,check='32.861.246')
cell_set(T,9,2,'Añade la contribución de C2.1 (frecuencia) y C2.2/C2.4 (duración), apartados 4.6.1 y 4.6.3; detalle por subcomponente en el apartado 8.4. Con la convención de facturación declarada de la medición inteligente. Mapa_Objetivos!F10',nth=N,check='lectura A')
cell_set(T,10,0,'VAN oficial del OED II — con los beneficios de confiabilidad, resultado publicado',nth=N); cell_set(T,10,1,'+17.517.624 USD',nth=N,check='18.237.278')
cell_set(T,10,2,'Añade la misma contribución de C2.1 y C2.2/C2.4 con la medición inteligente valorada como transferencia; AMI_Regla!C41',nth=N,check='lectura B')
delete_row(T,8,nth=N)
# Cuadro 19 (T35) fila 8
T='Cuadro 19. Resultado económico del objetivo de confiabilidad'
cell_set(T,8,0,'VAN oficial del OED II, resultado publicado',nth=1,check='lectura B'); cell_set(T,8,1,'+17.517.624 USD',nth=1,check='18.237.278')
cell_set(T,8,2,'OED II de la matriz del PCR (modernización, eficiencia y confiabilidad), con los beneficios de confiabilidad por contribución (Cuadro 14; Libro de Confiabilidad y VAN, EEO5, hoja AMI_Regla, celda C41). Los −5.352.419 USD de este cuadro son el resultado del objetivo de confiabilidad de la agrupación interna de este ejercicio, antes de esos beneficios, y no el del OED II oficial',nth=1,check='sin esos canales')
# Cascada por causa (T40) fila 6
cell_set('Cascada de conciliación por causa y escalones',6,2,'Operación y mantenimiento de la medición inteligente declarada vacía en la reestimación corregida, en lugar de imputar el 5 % anual del CAPEX del modelo anterior. Desde el 6-oct-2026 el titular carga el 2,5 % anual (tasa de las redes de distribución), un escalón posterior de la cadena (−719.654 USD)',check='declarada vacía')
# T41 Montecarlo
rebuild_table('Distribución del VAN en la simulación de Montecarlo con las decisiones adoptadas',[['Unidad de análisis','P5 (USD)','Mediana (USD)','P95 (USD)','P(VAN > 0)'],['Programa, resultado publicado','−3.350.331','26.136.709','64.768.868','92,30 %']])
# T42 VAN por subcomponente
rows42=[['Subcomponente','VAN, convención de facturación (USD)','VAN, resultado publicado (USD)','Aporte de los beneficios de confiabilidad (USD)'],
 ['C1.1 Subtransmisión','28.762.042','28.762.042','—'],['C1.2 Distribución','−10.823.160','−10.823.160','—'],['C1.3a Fiscalización subtransmisión','−985.387','−985.387','—'],['C1.3b Fiscalización distribución','−750.209','−750.209','—'],
 ['C2.1 Dispositivos inteligentes en alimentadores','16.247.497','16.247.497','+20.415.039'],['C2.2 Automatización y adecuación de subestaciones','6.556.977','6.556.977','+12.454.204'],['C2.3 Medición inteligente (AMI)','12.392.693','−2.231.275','—'],['C2.4 Centros de datos y de control','−2.995.414','−2.995.414','+116.717'],
 ['C2.5 Supervisión y fiscalización C2','−60.161','−60.161','—'],['C3.1 Estrategia de capacitación','−139.334','−139.334','—'],['C3.2 Fortalecimiento de procesos','−480.187','−480.187','—'],['Programa','47.725.356','33.101.388','+32.985.960']]
rebuild_table('Cuadro — Valor actual neto por subcomponente, con y sin los canales',rows42,nth=1)
# Cuadro 23 (T43) filas 9, 11, 12
T='Cuadro 23. Síntesis integral del contrafactual'; N=1
cell_set(T,9,2,'Resultado publicado (medición inteligente valorada como transferencia, con los beneficios de confiabilidad): US$+33.101.387,79 · convención de facturación, declarada: US$+47.725.355,51',nth=N,check='33.821.041,83')
cell_set(T,9,4,'+US$33.101.387,79 (resultado publicado) · +US$47.725.355,51 (convención de facturación, declarada)',nth=N,check='33.821.041,83'); cell_set(T,9,6,'EEO5 AMI_Regla!D20 (resultado publicado) · VAN_Programa!G18 (convención de facturación)',nth=N)
cell_set(T,11,2,'1,4563 (resultado publicado) · 1,6578 (convención de facturación, declarada)',nth=N,check='1,4708'); cell_set(T,11,6,'EEO5 AMI_Regla!D21 (resultado publicado) · VAN_Programa!J18 (convención de facturación)',nth=N)
cell_set(T,12,2,'18,34 % en el resultado publicado (20,22 % con la convención de facturación, declarada). Recuperación descontada: 2027 (resultado publicado) y 2026 (convención de facturación)',nth=N,check='18,45 %'); cell_set(T,12,6,'EEO5 Flujo_Anual!D24 (resultado publicado) y B24 (convención de facturación); recuperación en D34 y B34',nth=N)
# ====================== CUADRO DE SENSIBILIDAD (nuevo) ======================
TIT_S='Cuadro — Sensibilidad del valor actual neto del Programa a la convención de la medición inteligente y a los beneficios de confiabilidad (tabla auxiliar)'
INTRO_S='Dos decisiones de presentación separan las cifras de este capítulo: la convención con que se valora la energía recuperada por la medición inteligente y la inclusión de los beneficios de confiabilidad. El cuadro siguiente las cruza y muestra qué cambia con cada una; los costos son los mismos en los cuatro casos. Los beneficios de confiabilidad no proceden de parámetros importados: sus cantidades físicas se estiman sobre el panel histórico de calidad de servicio por alimentador del regulador ecuatoriano (ARCONEL), con la frecuencia y la duración de las interrupciones observadas en la propia red del Ecuador entre 2008 y 2025 (apartado 4.6).'
ROWS_S=[['Caso','VAN al 12 % (USD de 2015)','TIR','Razón beneficio/costo','Recuperación descontada','P(VAN < 0)'],
 ['Resultado publicado, con beneficios de confiabilidad ¹','+33.101.388','18,34 %','1,4563','2027','7,70 %'],
 ['Convención de facturación, con beneficios de confiabilidad ²','+47.725.356','20,22 %','1,6578','2026','no simulada ⁵'],
 ['Resultado publicado, sin beneficios de confiabilidad ³','+115.428','12,02 %','1,0016','2045','54,32 %'],
 ['Convención de facturación, sin beneficios de confiabilidad ⁴','+14.739.396','14,73 %','1,2032','2033','no simulada ⁵']]
NOTAS_S=['Notas de cuadro. (1) Resultado publicado: la facturación recuperada por la medición inteligente se trata como transferencia entre usuarios y distribuidoras y solo cuenta como beneficio su componente real (regla de transferencias, f = 1,2 y λ = 0,5; apartado 8.4); el flujo incluye los dos canales de confiabilidad del estudio de contribución, frecuencia (C2.1, apartado 4.6.1) y duración (C2.2/C2.4, apartado 4.6.3). Es la cifra que publica el PCR. (2) Convención de facturación: la energía recuperada se acredita a la tarifa como beneficio económico pleno, con los mismos canales de confiabilidad. Se declara como convención de referencia y no se publica como resultado central.',
 '(3) y (4) Sin beneficios de confiabilidad: los mismos dos casos retirando los canales de frecuencia y duración; se conserva la energía no suministrada evitada por el refuerzo de capacidad del C1.1. Son lecturas internas que muestran cuánto del resultado descansa en la confiabilidad. (5) La simulación de Montecarlo (10.000 corridas, semilla 20260917) se corre sobre el resultado publicado y sobre su variante sin beneficios de confiabilidad; la convención de facturación no se simula porque es una convención de referencia, no un resultado. En los cuatro casos: horizonte 2015-2045, dólares constantes de 2015, tasa social de descuento del 12 %, gasto de operación y mantenimiento de la medición inteligente al 2,5 % anual de su CAPEX y valor presente de los costos de 72.549.627 dólares.',
 'Fuente: Libro de Confiabilidad y VAN (EEO5), hoja Flujo_Anual, filas 15 (VAN), 22 (razón beneficio/costo), 24 (TIR) y 34 (recuperación descontada), columnas D y E (resultado publicado, con y sin beneficios de confiabilidad) y B y C (convención de facturación, con y sin); hoja MC_B, celdas G4 y G5 (probabilidad de VAN negativo). Elaboración propia.']
block=new_p('ParBID',INTRO_S)+new_p('TituloCuadro',TIT_S)+new_table(TPL41,ROWS_S,[3000,1500,1000,1200,1300,1200])+''.join(new_p('FuenteCuadro',t) for t in NOTAS_S)
insert_after(2624,block,text='Fuente: elaboración propia a partir de VAN_Programa!A7:K18 y Mapa_Objetivos!C9:C12/F9:F12 del Libro de Confiabilidad y VAN (EEO5). Filas redondeadas a la unidad; pueden no sumar exactamente por redondeo (el total es 47.725.355,51 con la convención de facturación y 33.101.387,79 en el resultado publicado).')
insert_after(69,new_p('IndiceBID',TIT_S),occ=0)
# ====================== PASE GENÉRICO ======================
GEN=CAPS+[('en la lectura B publicada','en el resultado publicado'),('la lectura B publicada','el resultado publicado'),('lectura B publicada','resultado publicado'),('la lectura publicada','el resultado publicado'),('lectura publicada','resultado publicado'),('(lectura B, publicada)','(resultado publicado)'),('(lectura B)','(resultado publicado)'),('lectura A, declarada','convención de facturación, declarada'),('(lectura A)','(convención de facturación)'),('EEO#2','EEO2'),('EEO#8','EEO9')]
ps=all_paras(x)
for j in range(len(ps)-1,-1,-1):
    s,e=ps[j]; t=vis_text(x[s:e]); new=t
    for o,n in GEN:
        if o in new: new=new.replace(o,n)
    if new!=t: log.append((f'gen {j}',t,new)); x=set_text(x,ctx,j,new,AUT)
# ====================== FIGURAS ======================
rels=z.read('word/_rels/document.xml.rels').decode('utf8'); rel={m.group(1):m.group(2) for m in re.finditer(r'<Relationship [^>]*Id="([^"]+)"[^>]*Target="([^"]+)"',rels)}
def media_after(cap_prefix,min_idx=200):
    ps=all_paras(x); T=[vis_text(x[a:b]) for a,b in ps]
    i=next(k for k,t in enumerate(T) if t.strip().startswith(cap_prefix) and k>min_idx)
    j=next(k for k in range(i+1,i+6) if '<w:drawing' in x[ps[k][0]:ps[k][1]]); rid=re.search(r'r:embed="([^"]+)"',x[ps[j][0]:ps[j][1]]).group(1); return 'word/'+rel[rid]
MEDIA={}
for cap,png in (('Figura 31.','cf_fig31.png'),('Figura 32.','cf_fig32.png'),('Figura 34.','cf_fig34.png'),('Figura 43.','cf_fig31.png'),('Figura 44.','cf_fig44.png'),('Figura 45.','cf_fig45.png'),('Figura 46.','cf_fig32.png'),('Figura 47.','cf_fig47.png'),('Figura 48.','cf_fig48.png'),('Figura 49.','cf_fig49.png'),('Figura 50.','cf_fig50.png')):
    m=media_after(cap); MEDIA[m]=open(png,'rb').read(); log.append((cap,m,png))
print('medios a sustituir:',{k:len(v) for k,v in MEDIA.items()})
# ====================== SALIDA ======================
xml.parsers.expat.ParserCreate().Parse(x.encode('utf8'),True)
y,nm,nf=accept_all(x); y=strip_comments(y); xml.parsers.expat.ParserCreate().Parse(y.encode('utf8'),True)
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
            elif n=='word/settings.xml':
                if clean: d=re.sub(rb'<w:trackRevisions\b[^>]*/>',b'',d)
            zo.writestr(it,d)
os.makedirs('salida_om',exist_ok=True)
cc='salida_om/Anexo_Analisis_Contrafactual_EC-L1147 (con control de cambios).docx'; cl='salida_om/Anexo_Analisis_Contrafactual_EC-L1147.docx'
save2(cc,x,False); save2(cl,y,True)
Aa=accepted_seq2(x); L=[vis_text(y[a:b]) for a,b in all_paras(y)]
sha=lambda f:hashlib.sha256(open(f,'rb').read()).hexdigest()[:8].upper()
print(dict(ediciones=len(log),revisiones={k[1]:v for k,v in ctx.count.items()},aceptado_igual_limpio=Aa==L,no_unibles=nf,sha_cc=sha(cc),sha_limpio=sha(cl),bytes=(os.path.getsize(cc),os.path.getsize(cl))))
RES=r'33\.821\.04|48\.445\.0|\b33,82\b|\b48,45\b|18,45 ?%|1,4708|1,6744|\b1,47\b|\b1,67\b|20,31 ?%|7,08 ?%|11,5 %|48,1 %|83,5|15\.459\.0|\b15,46\b|835\.08|\b0,84 millones|12,18 ?%|14,84 ?%|\b2044\b|lectura [AB]\b|lectura publicada|sin (los )?canales|EEO#|13\.112\.347|\b4,38\b|7\.123\.045|1,722|18,83|18\.237\.27|32\.861\.24|valor de referencia externo|solicitud|Solicitud|28,0 %|29,1 millones|\+18,8\b|\+8,0\b|−13,45|43,73|Montecarlo de referencia|100\.000 iteraciones'
for t in L:
    for m in re.finditer(RES,t): print('RESTO:',t[max(0,m.start()-70):m.end()+60].replace('\n',' '))
json.dump(log,open('salida_om/log_CF.json','w'),ensure_ascii=False,indent=0)
