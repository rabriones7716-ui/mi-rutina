"""Edición mínima de libros xlsx a nivel de XML: conserva gráficos, comentarios, estilos y todo lo que openpyxl perdería.
Celdas nuevas o cambiadas: texto en línea (inlineStr), número o fórmula sin valor en caché (Excel recalcula al abrir: fullCalcOnLoad)."""
import zipfile,re,html
def col_idx(col):
    n=0
    for ch in col: n=n*26+ord(ch)-64
    return n
def split_ref(ref):
    m=re.match(r'([A-Z]+)(\d+)$',ref); return m.group(1),int(m.group(2))
class Book:
    def __init__(self,path):
        z=zipfile.ZipFile(path); self.order=z.namelist(); self.files={n:z.read(n) for n in self.order}; z.close()
        wb=self.files['xl/workbook.xml'].decode(); rels=self.files['xl/_rels/workbook.xml.rels'].decode()
        rid={}
        for m in re.finditer(r'<Relationship\b[^>]*>',rels):
            t=m.group(0); i=re.search(r'\bId="([^"]+)"',t).group(1); tg=re.search(r'\bTarget="([^"]+)"',t).group(1); rid[i]=tg
        self.sheets={}
        for m in re.finditer(r'<sheet\b[^>]*>',wb):
            t=m.group(0); name=html.unescape(re.search(r'\bname="([^"]+)"',t).group(1)); r=re.search(r'r:id="([^"]+)"',t).group(1)
            tg=rid[r]; tg=tg.lstrip('/'); tg=tg if tg.startswith('xl/') else 'xl/'+tg; self.sheets[name]=tg
        ss=self.files.get('xl/sharedStrings.xml',b'').decode()
        self.ss=[html.unescape(re.sub(r'<[^>]+>','',m.group(1))) for m in re.finditer(r'<si>(.*?)</si>',ss,flags=re.S)]
        self.log=[]
    def _x(self,sheet): return self.files[self.sheets[sheet]].decode()
    def _w(self,sheet,x): self.files[self.sheets[sheet]]=x.encode()
    def _find(self,x,ref):
        return re.search(r'<c r="%s"(?P<attrs>[^>]*?)(?:/>|>(?P<body>.*?)</c>)'%ref,x,flags=re.S)
    def text(self,sheet,ref):
        m=self._find(self._x(sheet),ref)
        if not m: return None
        attrs=m.group('attrs') or ''; body=m.group('body') or ''
        t=re.search(r'\bt="([^"]+)"',attrs); t=t.group(1) if t else None
        f=re.search(r'<f[^>]*>(.*?)</f>',body,flags=re.S)
        if f: return '='+html.unescape(f.group(1))
        if t=='inlineStr': return html.unescape(re.sub(r'<[^>]+>','',body))
        v=re.search(r'<v>(.*?)</v>',body,flags=re.S); v=html.unescape(v.group(1)) if v else ''
        if t=='s': return self.ss[int(v)]
        return v
    def style(self,sheet,ref):
        m=self._find(self._x(sheet),ref)
        if not m: return None
        s=re.search(r'\bs="(\d+)"',m.group('attrs') or ''); return s.group(1) if s else None
    @staticmethod
    def _cell(ref,s,value,kind):
        sa=f' s="{s}"' if s else ''
        if kind=='f': return f'<c r="{ref}"{sa}><f>{html.escape(value[1:] if value.startswith("=") else value,quote=False)}</f></c>'
        if kind=='n': return f'<c r="{ref}"{sa}><v>{repr(float(value)) if not isinstance(value,int) else value}</v></c>'
        return f'<c r="{ref}"{sa} t="inlineStr"><is><t xml:space="preserve">{html.escape(str(value),quote=False)}</t></is></c>'
    def set(self,sheet,ref,value,kind=None,style=None,check=None,style_from=None):
        """kind: 'f' fórmula, 'n' número, 's' texto (por defecto según el valor). check: subcadena que debe estar en el texto anterior."""
        if kind is None: kind='f' if isinstance(value,str) and value.startswith('=') else ('n' if isinstance(value,(int,float)) else 's')
        x=self._x(sheet); old=self.text(sheet,ref)
        if check is not None: assert old is not None and check in old,(sheet,ref,check,old)
        m=self._find(x,ref)
        if m:
            s=style or self.style(sheet,ref); x=x[:m.start()]+self._cell(ref,s,value,kind)+x[m.end():]
        else:
            col,row=split_ref(ref); s=style or (self.style(sheet,style_from) if style_from else None)
            if s is None and row>1: s=self.style(sheet,f'{col}{row-1}')
            cell=self._cell(ref,s,value,kind)
            rm=re.search(r'<row r="%d"\b[^>]*?(?:/>|>(.*?)</row>)'%row,x,flags=re.S)
            if rm:
                if rm.group(0).endswith('/>'):
                    x=x[:rm.start()]+rm.group(0)[:-2]+'>'+cell+'</row>'+x[rm.end():]
                else:
                    body=rm.group(1); pos=0
                    for cm in re.finditer(r'<c r="([A-Z]+)%d"'%row,body):
                        if col_idx(cm.group(1))<col_idx(col): pos=cm.end()
                        else: break
                    if pos:  # colocar tras la celda anterior completa
                        cm2=re.compile(r'<c r="[A-Z]+%d"[^>]*?(?:/>|>.*?</c>)'%row,flags=re.S)
                        pos=0
                        for cm in cm2.finditer(body):
                            c0=re.match(r'<c r="([A-Z]+)',cm.group(0)).group(1)
                            if col_idx(c0)<col_idx(col): pos=cm.end()
                            else: break
                    body=body[:pos]+cell+body[pos:]
                    x=x[:rm.start(1)]+body+x[rm.end(1):]
            else:
                newrow=f'<row r="{row}">{cell}</row>'; ins=None
                for rm2 in re.finditer(r'<row r="(\d+)"',x):
                    if int(rm2.group(1))>row: ins=rm2.start(); break
                if ins is None: ins=x.index('</sheetData>')
                x=x[:ins]+newrow+x[ins:]
        self._w(sheet,x); self.log.append((sheet,ref,old,value)); return old
    def replace(self,sheet,ref,old_sub,new_sub):
        t=self.text(sheet,ref); assert t is not None and old_sub in t,(sheet,ref,old_sub,t); return self.set(sheet,ref,t.replace(old_sub,new_sub),kind='s')
    def save(self,dst):
        for name,path in self.sheets.items():
            x=self.files[path].decode()
            refs=re.findall(r'<c r="([A-Z]+)(\d+)"',x)
            if refs:
                mc=max(col_idx(c) for c,_ in refs); mr=max(int(r) for _,r in refs)
                def col_name(n):
                    s=''
                    while n: n,r=divmod(n-1,26); s=chr(65+r)+s
                    return s
                x=re.sub(r'<dimension ref="[^"]*"/>',f'<dimension ref="A1:{col_name(mc)}{mr}"/>',x,count=1)
            self.files[path]=x.encode()
        wb=self.files['xl/workbook.xml'].decode()
        if 'fullCalcOnLoad' not in wb:
            wb=re.sub(r'<calcPr\b',' <calcPr fullCalcOnLoad="1"',wb,count=1) if '<calcPr' in wb else wb.replace('</workbook>','<calcPr fullCalcOnLoad="1"/></workbook>')
            self.files['xl/workbook.xml']=wb.encode()
        with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED) as zo:
            for n in self.order: zo.writestr(n,self.files[n])
