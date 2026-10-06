import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from matplotlib.patches import Patch
BLUE='#1F4E79'; LB='#7FA7C9'; GREEN='#2E8B57'; RED='#C0392B'; GRAY='#9E9E9E'; MG='#777777'
def fmt(v,d=2): return f'{v:,.{d}f}'.replace(',','_').replace('.',',').replace('_','.')
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
def sub(fname,title,items,van,note):
    fig,ax=plt.subplots(figsize=(9.6,4.68),dpi=200); yy=np.arange(len(items))[::-1]
    ax.barh(yy,[v for _,v in items],color=[BLUE if v>0 else LB for _,v in items],height=0.55)
    for y,(n,v) in zip(yy,items): ax.text(v+(0.8 if v>=0 else -0.8),y,fmt(v),va='center',ha='left' if v>=0 else 'right',fontsize=9)
    ax.set_yticks(yy); ax.set_yticklabels([n for n,_ in items],fontsize=9); ax.axvline(0,color='black',lw=0.8); ax.grid(axis='x',alpha=0.3)
    lo=min(0,min(v for _,v in items))-12; hi=max(v for _,v in items)+14; ax.set_xlim(lo,hi); ax.set_xlabel('Millones de USD de 2015, valor presente 2015-2045 al 12 %')
    ax.set_title(title,loc='left',fontsize=10,fontweight='bold'); ax.text(0.99,0.04,f'VAN económico = {fmt(van)} M US$',transform=ax.transAxes,ha='right',va='bottom',fontsize=11,fontweight='bold',color=GREEN if van>0 else RED)
    plt.tight_layout(rect=(0,0.06,1,1)); fig.text(0.01,0.01,note,fontsize=7.5,color=MG,va='bottom'); plt.savefig(fname); plt.close()
sub('eeo9_fig3.png','C1.1 Subtransmisión: beneficios y costos económicos\n(igual en las dos convenciones)',[('Canales compartidos con C1.2 asignados a C1.1:\nenergía adicional servida y ENS evitada por capacidad',62.12),('Pérdidas de subtransmisión evitadas',2.28),('CAPEX y O&M de C1.1',-35.64)],28.76,'Fuente: Libro de Confiabilidad y VAN (EEO5), hojas VAN_Programa y AMI_Regla (B34). VP de beneficios 64,40; VP de costos 35,64; B/C 1,81. El módulo satélite de pérdidas técnicas de C1.1 valida el canal de pérdidas (memoria, no entra al VAN).')
sub('eeo9_fig4.png','C1.2 Distribución: beneficios y costos económicos\n(igual en las dos convenciones)',[('Parte del canal de energía adicional\ny del pool N-1 asignada a C1.2',5.90),('CAPEX y O&M de C1.2',-16.72)],-10.82,'Fuente: Libro de Confiabilidad y VAN (EEO5), hojas VAN_Programa y AMI_Regla (B35). VP de beneficios 5,90; VP de costos 16,72; B/C 0,35. Los módulos satélite de pérdidas técnicas y de C1.2 con red y sin red se citan en memoria (acceso y regularización: canal central = 0, sin dato de conexiones nuevas por obra).')
# Figura 11: aporte de cada canal al OGD, resultado publicado (y convención)
ch=[('Capacidad y cobertura (energía adicional servida)',56.74,56.74),('Calidad y continuidad del servicio (ENS evitada:\ncapacidad, frecuencia y duración)',44.26,44.26),('Gestión comercial y medición',2.37,16.99),('Pérdidas técnicas evitadas',2.28,2.28),('Fortalecimiento institucional',0.0,0.0)]
totB=sum(c[1] for c in ch); totA=sum(c[2] for c in ch)
fig,ax=plt.subplots(figsize=(9.6,5.16),dpi=200); yy=np.arange(len(ch))[::-1]; h=0.36
ax.barh(yy+h/2,[c[1] for c in ch],height=h,color=BLUE); ax.barh(yy-h/2,[c[2] for c in ch],height=h,color=LB)
for y,(n,b,a) in zip(yy,ch):
    ax.text(b+0.8,y+h/2,f'{fmt(b,1)} M US$ ({fmt(100*b/totB,1)} %)',va='center',fontsize=8.5); ax.text(a+0.8,y-h/2,f'{fmt(a,1)} M US$ ({fmt(100*a/totA,1)} %)',va='center',fontsize=8.5,color=MG)
ax.set_yticks(yy); ax.set_yticklabels([c[0] for c in ch],fontsize=9); ax.set_xlim(0,80); ax.grid(axis='x',alpha=0.3); ax.set_xlabel('Millones de USD de 2015 (valor presente de los beneficios económicos, 2015-2045 al 12 %)')
ax.legend(handles=[Patch(color=BLUE,label=f'Resultado publicado (total {fmt(totB)})'),Patch(color=LB,label=f'Convención de facturación (total {fmt(totA)})')],loc='lower right',frameon=False,fontsize=9)
ax.set_title('Aporte de cada canal al Objetivo General de Desarrollo',loc='left',fontsize=10.5,fontweight='bold')
plt.tight_layout(rect=(0,0.05,1,1)); fig.text(0.01,0.01,'Fuente: Libro de Confiabilidad y VAN (EEO5), hoja Mapa_Objetivos: resultado publicado G21:H26; convención de facturación C21:D26.',fontsize=7.5,color=MG,va='bottom'); plt.savefig('eeo9_fig11.png'); plt.close()
from PIL import Image
for f,t in (('eeo9_fig3.png',5762625/2809875),('eeo9_fig4.png',5762625/2809875),('eeo9_fig11.png',5762625/3095625)):
    im=Image.open(f); print(f,im.size,round(im.size[0]/im.size[1],3),'objetivo',round(t,3))
