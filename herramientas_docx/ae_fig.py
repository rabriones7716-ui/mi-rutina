import json,matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
GREEN='#2E8B57'; RED='#C0392B'; BLUE='#1F4E79'; LBLUE='#5DADE2'; GRAY='#9E9E9E'; ORANGE='#E59400'; DK='#333333'; MG='#777777'; OR='#C55A11'; LO='#F4B183'
def fmt(v,d=2): return f'{v:,.{d}f}'.replace(',','_').replace('.',',').replace('_','.')
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
R=json.load(open('flujo_anual_B.json')); yrs=sorted(int(k) for k in R)
def f(r,c):
    try: return float(R[str(r)].get(c,'0') or 0)
    except: return 0.0
Y=[int(f(r,'A')) for r in yrs]; P=[f(r,'P')/1e6 for r in yrs]; T=[f(r,'T')/1e6 for r in yrs]
# estadísticos para el texto 6.3 y 6.5
imin=int(np.argmin(T)); print('mínimo VP acumulado',round(T[imin],2),'en',Y[imin]); print('primer año de flujo neto positivo sostenido',next(Y[i] for i in range(len(P)) if all(p>0 for p in P[i:])))
print('flujo neto medio 2026-2045 (M nominal)',round(np.mean([P[i] for i in range(len(P)) if Y[i]>=2026]),2),'; 2024-2045',round(np.mean([P[i] for i in range(len(P)) if Y[i]>=2024]),2))
cross=next(Y[i] for i in range(len(T)) if all(t>=0 for t in T[i:])); print('cruce',cross,'cierre',round(T[-1],2))
ben=[sum(f(r,c) for c in 'CDEFGHJK') for r in yrs]; cost=[f(r,'L')+f(r,'M') for r in yrs]
print('benef nominal',round(sum(ben)),'costo nominal',round(sum(cost)),'neto',round(sum(ben)-sum(cost)),'razón',round(sum(ben)/sum(cost),2))
print('costo 2015-2018 %',round(100*sum(c for c,y in zip(cost,Y) if y<=2018)/sum(cost),1),'; beneficio >2025 %',round(100*sum(b for b,y in zip(ben,Y) if y>2025)/sum(ben),1))
print('factor descuento 2018',round(f(42,'B'),3),'2026',round(f(50,'B'),3))
# ---------- Figura 3 ----------
fig,ax=plt.subplots(figsize=(9.6,5.81),dpi=200)
ax.bar(Y,P,color=[RED if p<0 else GREEN for p in P],width=0.8)
ax.axhline(0,color='black',lw=0.8); ax.set_ylabel('Flujo neto anual (MUS$)'); ax.set_xlabel('')
ax2=ax.twinx(); ax2.plot(Y,T,color=BLUE,lw=2.2); ax2.axhline(0,color=BLUE,lw=0.6,ls=':'); ax2.set_ylabel('VP acumulado @ 12 % (MUS$)'); ax2.spines['top'].set_visible(False)
ax2.annotate(f'cruza cero en {cross}\nVAN 2045 = {fmt(T[-1])} M',xy=(cross,0),xytext=(cross+4,-22),color=BLUE,arrowprops=dict(arrowstyle='->',color=BLUE,lw=1),fontsize=9)
ax.set_title('Figura 3. Flujo neto anual y valor presente acumulado del Programa, 2015-2045 (resultado publicado)',fontsize=10)
ax.legend(handles=[Patch(color=GREEN,label='Flujo neto anual (barras, eje izq.)'),Line2D([],[],color=BLUE,lw=2.2,label='Valor presente acumulado (línea, eje der.)')],loc='lower right',frameon=False,fontsize=8)
ax.grid(axis='y',alpha=0.3); plt.tight_layout(); plt.savefig('ae_fig3.png'); plt.close()
# ---------- Figura 4: descomposición del VAN (cascada) ----------
steps=[('Energía\nadicional',56.740049),('Continuidad\npor capacidad',11.277501),('Pérdidas de\nsubtransm.',2.281120),('Medición\ninteligente\n(convención)',16.990352),('Frecuencia\n(C2.1)',20.415039),('Duración\n(C2.2, C2.4)',12.570921)]
fig,ax=plt.subplots(figsize=(9.6,6.05),dpi=200)
run=0; xs=[]; k=0
for n,v in steps:
    ax.bar(k,v,bottom=run,color=GREEN,width=0.7); ax.text(k,run+v+1.2,f'+{fmt(v)}',ha='center',fontsize=8); run+=v; xs.append(n); k+=1
ax.bar(k,run,color=BLUE,width=0.7); ax.text(k,run+1.2,fmt(run),ha='center',fontsize=8,fontweight='bold'); xs.append('Beneficios,\nvalor\npresente'); k+=1
for n,v in (('CAPEX',-58.678253),('Operación y\nmanteni-\nmiento',-13.871374)):
    ax.bar(k,v,bottom=run,color=RED,width=0.7); ax.text(k,run+v-3.5,fmt(v),ha='center',fontsize=8); run+=v; xs.append(n); k+=1
ax.bar(k,run,color=LBLUE,width=0.7); ax.text(k,run+1.2,fmt(run),ha='center',fontsize=8,fontweight='bold'); xs.append('VAN,\nconvención de\nfacturación'); k+=1
ax.bar(k,-14.623968,bottom=run,color=ORANGE,width=0.7); ax.text(k,run-14.623968-3.5,'−14,62',ha='center',fontsize=8); run-=14.623968; xs.append('Transferencia\nmedición\ninteligente'); k+=1
ax.bar(k,run,color=BLUE,width=0.7); ax.text(k,run+1.2,fmt(run),ha='center',fontsize=8,fontweight='bold'); xs.append('VAN,\nresultado\npublicado')
ax.set_xticks(range(len(xs))); ax.set_xticklabels(xs,fontsize=7); ax.set_ylabel('Millones de USD de 2015, valor presente al 12 %'); ax.set_ylim(0,135); ax.grid(axis='y',alpha=0.3)
ax.set_title('Figura 4. Del valor presente de los beneficios (120,27) al VAN publicado (33,10):\ncostos y transferencia de la medición inteligente',fontsize=10,loc='left')
plt.tight_layout(); plt.savefig('ae_fig4.png'); plt.close()
# ---------- Figura 5: concentración por subcomponente ----------
sub=[('C1.1 Subtransmisión',64.398979),('C2.1 Dispositivos inteligentes en alimentadores',20.415039),('C2.2 Automatización de subestaciones',12.454204),('C1.2 Distribución',5.899691),('C2.3 Medición inteligente (transferencia)',2.366384),('C2.4 Centros de datos y de control',0.116717),('C1.3a, C1.3b, C2.5, C3.1, C3.2 (habilitantes)',0.0)]
tot=sum(v for _,v in sub)
fig,ax=plt.subplots(figsize=(9.6,4.57),dpi=200)
yy=np.arange(len(sub))[::-1]
ax.barh(yy,[v for _,v in sub],color=[BLUE]+[GREEN]*5+[GRAY],height=0.6)
for y,(n,v) in zip(yy,sub): ax.text(v+0.8,y,f'{fmt(v)}  ({fmt(100*v/tot,1)} %)',va='center',fontsize=8.5)
ax.set_yticks(yy); ax.set_yticklabels([n for n,_ in sub],fontsize=8.5); ax.set_xlim(0,80); ax.set_xlabel('Valor presente de los beneficios, millones de USD de 2015 (resultado publicado; total 105,65)')
ax.set_title('Figura 5. Concentración del valor presente de los beneficios por subcomponente\n(resultado publicado): C1.1 aporta el 61,0 %',fontsize=10,loc='left'); ax.grid(axis='x',alpha=0.3)
plt.tight_layout(); plt.savefig('ae_fig5.png'); plt.close()
# ---------- Figura 6: cascada por causa y por cambio ----------
items=[('Estimación\nprevia',40.17,'tot',BLUE),('Defectos\ncorregidos',-52.97,'d',RED),('Decisiones\nde diseño',-9.70,'d',RED),('Cambio de\nperímetro',-2.09,'d',RED),('Supuesto →\nobservado',18.82,'d',GREEN),('Convención\nde descuento',4.74,'d',GREEN),('Vacío de\ndato',1.77,'d',GREEN),('Reestimación\ncorregida',0.73,'tot',BLUE),
 ('Δ 117,24\n(→26,4 GWh)',3.36,'d',GREEN),('sin ×0,70',2.41,'d',GREEN),('E3 sostenido\n+ crecimiento',1.85,'d',GREEN),('+ C&R',0.61,'d',GREEN),('prima 1,79\n(solo CNEL)',6.50,'d',GREEN),('O&M de la\nmedición 2,5 %',-0.72,'d',RED),('Base del\ncomponente',14.74,'tot',BLUE),
 ('Canal de\nfrecuencia',20.42,'d',GREEN),('Canal de\nduración',12.57,'d',GREEN),('Convención de\nfacturación',47.73,'tot',LBLUE),('Transferencia\nmedición int.',-14.62,'d',ORANGE),('Resultado\npublicado',33.10,'tot',BLUE)]
fig,ax=plt.subplots(figsize=(9.6,5.74),dpi=200)
run=0
for k,(n,v,kind,c) in enumerate(items):
    if kind=='tot': ax.bar(k,v,color=c,width=0.7); ax.text(k,v+1.5 if v>=0 else v-3,fmt(v),ha='center',fontsize=7.5,fontweight='bold'); run=v
    else:
        ax.bar(k,v,bottom=run,color=c,width=0.7); ax.text(k,run+v+1.5 if v>=0 else run+v-3,('+' if v>0 else '')+fmt(v,1),ha='center',fontsize=7.2); run+=v
ax.axhline(0,color='black',lw=0.8); ax.set_xticks(range(len(items))); ax.set_xticklabels([i[0].replace('\n',' ') for i in items],fontsize=7,rotation=45,ha='right'); ax.set_ylabel('VAN del Programa (MUS$)'); ax.grid(axis='y',alpha=0.3); ax.set_ylim(-70,60)
ax.set_title('Figura 6. Cascada del VAN: de la estimación previa a la reestimación corregida,\na la base del componente y al resultado publicado (millones de USD)',fontsize=9.5,loc='left')
plt.tight_layout(); plt.savefig('ae_fig6.png'); plt.close()
# ---------- Figura 7: valores de cambio (Umbrales_B) ----------
V=[('Excedente del consumidor sobre la energía adicional',0.15,0.10,0.30,0.062492),('Energía no suministrada evitada por MVA (MWh/MVA-año)',4.302,0.335,25.809,-8.3251),('Utilización de la capacidad nueva',1.0,0.4278,1.0,0.416613),('Costo de la energía no suministrada (USD/MWh)',1533,789.4,1762,386.58),('Escala del canal de frecuencia',1.0,0.093558,1.40239,-0.62142),('Tarifa (USD/kWh)',0.092,0.070,0.110,0.035736),('Energía por capacidad (GWh/MVA-año)',2.67,2.358,3.234,1.11236),('Tendencia del canal de frecuencia',0.13794,0.0,0.35334,0.98101),('Transferencia de carga',1.0,0.5,1.5,-1.93517),('Cuota del canal de duración',1.0,0.5,1.2,-1.63317)]
def fig_umbrales(fname,size,title):
    fig,ax=plt.subplots(figsize=size,dpi=200); yy=np.arange(len(V))[::-1]
    for y,(n,c,lo,hi,sw) in zip(yy,V):
        bl=(lo/c-1)*100; bh=(hi/c-1)*100
        ax.barh(y,bh-bl,left=bl,height=0.5,color='#E5E5E5',edgecolor='none'); ax.plot([0,0],[y-0.25,y+0.25],color=DK,lw=1.2)
        req=(sw/c-1)*100
        if sw<=0: ax.text(bl,y-0.36,'no anula: el VAN sigue positivo aunque el parámetro caiga a cero',va='top',ha='left',fontsize=7,color=OR,fontweight='bold')
        elif req>170: ax.annotate('',xy=(170,y),xytext=(150,y),arrowprops=dict(arrowstyle='->',color=OR,lw=1.5)); ax.text(bl,y-0.36,f'anula en {fmt(sw,3)} (+{fmt(req,0)} %), muy por encima del máximo de la banda',fontsize=7,color=OR,ha='left',va='top')
        else: ax.plot(req,y,marker='D',color=OR,ms=7,zorder=5); ax.text(req,y-0.36,f'anula en {fmt(sw,3 if c<10 else 0)} ({fmt(req,0)} %)',fontsize=7,color=OR,ha='center',va='top')
        ax.text(bl-2,y+0.02,fmt(lo,3 if c<10 else 0),fontsize=6.6,color=MG,ha='right',va='center'); ax.text(min(bh,165)+2,y+0.02,fmt(hi,3 if c<10 else 0),fontsize=6.6,color=MG,ha='left',va='center')
    ax.set_yticks(yy); ax.set_yticklabels([f'{n}\ncentral {fmt(c,3 if c<10 else 0)}' for n,c,*_ in V],fontsize=7.5)
    ax.set_xlim(-102,172); ax.set_xlabel('Cambio del parámetro respecto de su valor central (%)')
    ax.legend(handles=[Patch(color='#E5E5E5',label='Banda de evidencia del parámetro'),Line2D([],[],color=DK,lw=1.2,label='Valor central adoptado'),Line2D([],[],marker='D',color=OR,ls='none',label='Valor que anula el VAN publicado')],loc='upper right',frameon=False,fontsize=7.5)
    ax.set_title(title,loc='left',fontsize=9.5); ax.set_ylim(-0.8,len(V)-0.3); plt.tight_layout(rect=(0,0.05,1,1))
    fig.text(0.01,0.01,'Fuente: Libro de Confiabilidad y VAN (EEO5), hoja Umbrales_B, filas 40 a 49. Las diez variables se ordenan por su rango en el tornado del resultado publicado.',fontsize=6.8,color=MG,va='bottom'); plt.savefig(fname); plt.close()
fig_umbrales('ae_fig7.png',(9.6,4.96),'Figura 7. Ningún parámetro anula por sí solo el VAN publicado dentro de su banda de evidencia (valores de cambio frente a bandas)')
# ---------- Figura 8: riesgo al retirar los beneficios de confiabilidad (MC_B) ----------
M=[('Resultado publicado',-3.35,26.14,64.77,7.70),('Sin el canal de duración (C2.2/C2.4)',-14.06,14.74,53.04,23.11),('Sin los beneficios de confiabilidad\n(frecuencia y duración)',-29.18,-2.49,35.33,54.32)]
def fig_mc(fname,size,title):
    fig,ax=plt.subplots(figsize=size,dpi=200); yy=np.arange(len(M))[::-1]
    for y,(n,p5,p50,p95,pn) in zip(yy,M):
        ax.barh(y,p95-p5,left=p5,height=0.45,color=LO,edgecolor='none')
        if p5<0: ax.barh(y,min(0,p95)-p5,left=p5,height=0.45,color=OR,edgecolor='none')
        ax.plot([p50,p50],[y-0.3,y+0.3],color=DK,lw=2)
        ax.text(p5-1,y,f'P5 {fmt(p5)}',ha='right',va='center',fontsize=8,color=MG); ax.text(p95+1,y,f'P95 {fmt(p95)}',ha='left',va='center',fontsize=8,color=MG)
        ax.text(p50,y+0.3,f'mediana {fmt(p50)}',ha='center',va='bottom',fontsize=8,color=DK)
        ax.text(84,y,f'P(VAN < 0) = {fmt(pn)} %',ha='left',va='center',fontsize=9.5,color=OR if pn>20 else DK,fontweight='bold')
    ax.axvline(0,color=DK,lw=0.8,ls='--'); ax.set_yticks(yy); ax.set_yticklabels([m[0] for m in M],fontsize=8.5)
    ax.set_xlim(-45,118); ax.set_xlabel('VAN del Programa, millones de USD de 2015 (intervalo P5 a P95; 10.000 corridas, semilla 20260917)')
    ax.set_title(title,loc='left',fontsize=9.5); ax.set_ylim(-0.6,len(M)-0.3); plt.tight_layout(rect=(0,0.05,1,1))
    fig.text(0.01,0.01,'Fuente: Libro de Confiabilidad y VAN (EEO5), hoja MC_B, filas 4 a 6. Naranja oscuro: tramo negativo del intervalo.',fontsize=7,color=MG,va='bottom'); plt.savefig(fname); plt.close()
fig_mc('ae_fig8.png',(9.6,6.35),'Figura 8. El riesgo de VAN negativo crece al retirar los beneficios de confiabilidad:\ndel 7,70 % al 54,32 % de las simulaciones')
# ---------- Figura 14: sostenibilidad S0-S3 ----------
S=[('S0\nBase',33.101388,1.4563),('S1\nDegradación leve',28.401479,1.3915),('S2\nDegradación moderada',17.968938,1.2442),('S3\nDegradación severa',7.020038,1.0934)]
fig,ax=plt.subplots(figsize=(9.6,4.9),dpi=200)
ax.bar(range(4),[s[1] for s in S],color=GREEN,width=0.55)
for k,s in enumerate(S): ax.text(k,s[1]/2,fmt(s[1],1),ha='center',va='center',fontweight='bold',fontsize=10,color='white')
ax.set_xticks(range(4)); ax.set_xticklabels([s[0] for s in S]); ax.set_ylabel('VAN (MUS$)'); ax.set_ylim(0,40); ax.axhline(0,color='black',lw=0.8); ax.grid(axis='y',alpha=0.3)
ax2=ax.twinx(); ax2.plot(range(4),[s[2] for s in S],color=BLUE,marker='o',lw=2); ax2.axhline(1.0,color=BLUE,ls=':',lw=0.8); ax2.set_ylim(0.9,1.55); ax2.set_ylabel('Razón B/C'); ax2.spines['top'].set_visible(False)
for k,s in enumerate(S): ax2.text(k+0.12,s[2],fmt(s[2],3),color=BLUE,fontsize=8,va='bottom')
ax.set_title('Figura 14. VAN y razón B/C por escenario de sostenibilidad posterior al cierre (resultado publicado):\nlos tres escenarios de degradación conservan el signo',fontsize=9.5,loc='left')
plt.tight_layout(); plt.savefig('ae_fig14.png'); plt.close()
# ---------- Figura 15: escalera de lecturas ----------
E=[('Estimación previa\n(histórica)',40.17,GRAY),('Reestimación\ncorregida',0.73,GRAY),('Lectura prudente E3\n(memoria)',8.96,GRAY),('Base del componente\n(antes de la confiabilidad)',14.74,BLUE),('Convención de\nfacturación (declarada)',47.73,LBLUE),('Resultado\npublicado',33.10,ORANGE)]
fig,ax=plt.subplots(figsize=(9.6,4.8),dpi=200)
ax.bar(range(len(E)),[e[1] for e in E],color=[e[2] for e in E],width=0.6)
for k,e in enumerate(E): ax.text(k,e[1]+0.8,fmt(e[1],1),ha='center',fontweight='bold',fontsize=9)
ax.set_xticks(range(len(E))); ax.set_xticklabels([e[0] for e in E],fontsize=8); ax.set_ylabel('VAN del Programa (millones de USD)'); ax.set_ylim(0,55); ax.grid(axis='y',alpha=0.3)
ax.set_title('Figura 15. Lecturas del VAN del Programa: de la reestimación corregida (0,73) al resultado publicado (33,10),\ncon la convención de facturación declarada (47,73)',fontsize=9.5,loc='left')
plt.tight_layout(); plt.savefig('ae_fig15.png'); plt.close()
print('figuras ok')
