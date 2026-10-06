import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
OR='#C55A11'; LO='#F4B183'; DK='#333333'; GR='#BBBBBB'; MG='#777777'
def fmt(v,d=2): return f'{v:,.{d}f}'.replace(',','_').replace('.',',').replace('_','.')
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
# ---------- Figura 44: VAN por subcomponente antes y después de los beneficios de confiabilidad (resultado publicado) ----------
rows=[('TOTAL PROGRAMA (resultado publicado)',0.12,33.10),('C1.1 Subtransmisión',28.76,28.76),('C1.2 Distribución',-10.82,-10.82),('C1.3a Fiscalización subtransmisión',-0.99,-0.99),('C1.3b Fiscalización distribución',-0.75,-0.75),
 ('C2.1 Dispositivos inteligentes en alimentadores',-4.17,16.25),('C2.2 Automatización de subestaciones',-5.90,6.56),('C2.3 Medición inteligente (transferencia)',-2.23,-2.23),('C2.4 Centros de datos y de control',-3.11,-3.00),('C2.5 Supervisión y fiscalización C2',-0.06,-0.06),('C3.1 Estrategia de capacitación',-0.14,-0.14),('C3.2 Fortalecimiento de procesos',-0.48,-0.48)]
fig,ax=plt.subplots(figsize=(9.6,6.03),dpi=200)
yy=np.arange(len(rows))[::-1]; h=0.38
for y,(n,a,b) in zip(yy,rows):
    tot=n.startswith('TOTAL'); chg=abs(b-a)>0.005
    ax.barh(y+h/2,a,height=h,color=GR,edgecolor='none')
    ax.barh(y-h/2,b,height=h,color=(DK if tot else (OR if chg else MG)),edgecolor='none')
    ax.text((a if a>=0 else a)+(0.4 if a>=0 else -0.4),y+h/2,fmt(a),va='center',ha='left' if a>=0 else 'right',fontsize=7.5,color=MG)
    ax.text(b+(0.4 if b>=0 else -0.4),y-h/2,fmt(b),va='center',ha='left' if b>=0 else 'right',fontsize=7.5,color=DK,fontweight='bold' if (tot or chg) else 'normal')
ax.set_yticks(yy); ax.set_yticklabels([r[0] for r in rows],fontsize=8)
ax.axvline(0,color=DK,lw=0.8); ax.set_xlim(-17,40); ax.set_xlabel('Valor actual neto al 12 %, millones de USD de 2015')
ax.legend(handles=[Patch(color=GR,label='Antes de los beneficios de confiabilidad'),Patch(color=OR,label='Después: subcomponentes que cambian (C2.1, C2.2, C2.4)'),Patch(color=DK,label='Después: total del Programa')],loc='lower right',frameon=False,fontsize=8)
ax.set_title('Los beneficios de confiabilidad llevan el VAN publicado de 0,12 a 33,10 millones;\nsolo C2.1, C2.2 y C2.4 cambian',loc='left',fontsize=10,fontweight='bold')
ax.set_ylim(-0.6,len(rows)-0.4); plt.tight_layout(rect=(0,0.07,1,1)); fig.text(0.01,0.012,'Resultado publicado: medición inteligente valorada como transferencia (C2.3 = −2,23). Con la convención de facturación, C2.3 = +12,39 y el total pasa de 14,74 a 47,73.\nFuente: Libro de Confiabilidad y VAN (EEO5), hojas VAN_Programa y Mapa_Objetivos. Dólares de 2015 descontados al 12 %.',fontsize=7,color=MG,va='bottom'); plt.savefig('cf_fig44.png'); plt.close()
# ---------- Figura 48: valores de cambio frente a bandas de evidencia (Umbrales_B) ----------
V=[('Excedente del consumidor sobre la energía adicional',0.15,0.10,0.30,0.062492),
   ('Energía no suministrada evitada por MVA (MWh/MVA-año)',4.302,0.335,25.809,-8.3251),
   ('Utilización de la capacidad nueva',1.0,0.4278,1.0,0.416613),
   ('Costo de la energía no suministrada (USD/MWh)',1533,789.4,1762,386.58),
   ('Escala del canal de frecuencia',1.0,0.093558,1.40239,-0.62142),
   ('Tarifa (USD/kWh)',0.092,0.070,0.110,0.035736),
   ('Energía por capacidad (GWh/MVA-año)',2.67,2.358,3.234,1.11236),
   ('Tendencia del canal de frecuencia',0.13794,0.0,0.35334,0.98101),
   ('Transferencia de carga',1.0,0.5,1.5,-1.93517),
   ('Cuota del canal de duración',1.0,0.5,1.2,-1.63317)]
fig,ax=plt.subplots(figsize=(9.6,6.35),dpi=200)
yy=np.arange(len(V))[::-1]
for y,(n,c,lo,hi,sw) in zip(yy,V):
    bl=(lo/c-1)*100; bh=(hi/c-1)*100
    ax.barh(y,bh-bl,left=bl,height=0.5,color='#E5E5E5',edgecolor='none')
    ax.plot([0,0],[y-0.25,y+0.25],color=DK,lw=1.2)
    req=(sw/c-1)*100
    if sw<=0: ax.text(min(bh,165)+2,y-0.36,'no anula: el VAN sigue positivo aunque el parámetro caiga a cero',va='top',ha='left' if bh<60 else 'right',fontsize=7.2,color=OR,fontweight='bold') if bh<60 else ax.text(bl,y-0.36,'no anula: el VAN sigue positivo aunque el parámetro caiga a cero',va='top',ha='left',fontsize=7.2,color=OR,fontweight='bold')
    elif req>170: ax.annotate('',xy=(170,y),xytext=(150,y),arrowprops=dict(arrowstyle='->',color=OR,lw=1.5)); ax.text(bl,y-0.36,f'anula en {fmt(sw,3)} (+{fmt(req,0)} %), muy por encima del máximo de la banda',fontsize=7.2,color=OR,ha='left',va='top')
    else:
        ax.plot(req,y,marker='D',color=OR,ms=7,zorder=5); ax.text(req,y-0.36,f'anula en {fmt(sw,3 if c<10 else 0)} ({fmt(req,0)} %)',fontsize=7.2,color=OR,ha='center',va='top')
    ax.text(bl-2,y+0.02,fmt(lo,3 if c<10 else 0),fontsize=6.8,color=MG,ha='right',va='center'); ax.text(min(bh,165)+2,y+0.02,fmt(hi,3 if c<10 else 0),fontsize=6.8,color=MG,ha='left',va='center')
ax.set_yticks(yy); ax.set_yticklabels([f'{n}\ncentral {fmt(c,3 if c<10 else 0)}' for n,c,*_ in V],fontsize=7.8)
ax.set_xlim(-102,172); ax.set_xlabel('Cambio del parámetro respecto de su valor central (%)')
ax.legend(handles=[Patch(color='#E5E5E5',label='Banda de evidencia del parámetro'),Line2D([],[],color=DK,lw=1.2,label='Valor central adoptado'),Line2D([],[],marker='D',color=OR,ls='none',label='Valor que anula el VAN publicado')],loc='upper right',bbox_to_anchor=(1,1.0),frameon=False,fontsize=8)
ax.set_title('Ningún parámetro anula por sí solo el VAN publicado dentro de su banda de evidencia',loc='left',fontsize=10,fontweight='bold')
ax.set_ylim(-0.8,len(V)-0.3); plt.tight_layout(rect=(0,0.05,1,1)); fig.text(0.01,0.01,'Fuente: Libro de Confiabilidad y VAN (EEO5), hoja Umbrales_B, filas 40 a 49 (valor que anula el VAN del resultado publicado). Las diez variables se ordenan por su rango en el tornado.',fontsize=7,color=MG,va='bottom'); plt.savefig('cf_fig48.png'); plt.close()
# ---------- Figura 50: el riesgo crece al retirar los beneficios de confiabilidad (MC_B) ----------
M=[('Resultado publicado',-3.35,26.14,64.77,7.70),('Sin el canal de duración (C2.2/C2.4)',-14.06,14.74,53.04,23.11),('Sin los beneficios de confiabilidad\n(frecuencia y duración)',-29.18,-2.49,35.33,54.32)]
fig,ax=plt.subplots(figsize=(9.6,4.78),dpi=200)
yy=np.arange(len(M))[::-1]
for y,(n,p5,p50,p95,pn) in zip(yy,M):
    ax.barh(y,p95-p5,left=p5,height=0.45,color=LO,edgecolor='none')
    if p5<0: ax.barh(y,min(0,p95)-p5,left=p5,height=0.45,color=OR,edgecolor='none')
    ax.plot([p50,p50],[y-0.3,y+0.3],color=DK,lw=2)
    ax.text(p5-1,y,f'P5 {fmt(p5)}',ha='right',va='center',fontsize=8,color=MG); ax.text(p95+1,y,f'P95 {fmt(p95)}',ha='left',va='center',fontsize=8,color=MG)
    ax.text(p50,y+0.3,f'mediana {fmt(p50)}',ha='center',va='bottom',fontsize=8,color=DK)
    ax.text(84,y,f'P(VAN < 0) = {fmt(pn)} %',ha='left',va='center',fontsize=9.5,color=OR if pn>20 else DK,fontweight='bold')
ax.axvline(0,color=DK,lw=0.8,ls='--'); ax.set_yticks(yy); ax.set_yticklabels([m[0] for m in M],fontsize=8.5)
ax.set_xlim(-45,118); ax.set_xlabel('VAN del Programa, millones de USD de 2015 (intervalo P5 a P95; 10.000 simulaciones, semilla 20260917)')
ax.set_title('El riesgo de VAN negativo crece al retirar los beneficios de confiabilidad:\ndel 7,70 % al 54,32 % de las simulaciones',loc='left',fontsize=10,fontweight='bold')
ax.set_ylim(-0.6,len(M)-0.3); plt.tight_layout(rect=(0,0.05,1,1)); fig.text(0.01,0.01,'Fuente: Libro de Confiabilidad y VAN (EEO5), hoja MC_B, filas 4 a 6. Naranja oscuro: tramo negativo del intervalo.',fontsize=7,color=MG,va='bottom'); plt.savefig('cf_fig50.png'); plt.close()
print('ok')
