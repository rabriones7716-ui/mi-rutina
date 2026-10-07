import passlib as L
from passlib import full,pairs,set_media,gen_pass
AUT='Revisión 2026-10 – versión final'
A=L.init('salida_om/Anexo_Flujos_Economicos_Financieros_EC-L1147 (con control de cambios).docx',AUT)
pairs(172,[('con un VAN de -3,00 M US$ en la configuración central (VP beneficios 0,12 M US$ frente a VP costos 3,11 M US$): su costo excede la contribución que se le puede acreditar por esta vía.','con un VAN de -3,00 M US$ en la configuración central (VP beneficios 0,12 M US$ frente a VP costos 3,11 M US$): su costo excede la contribución que se le puede acreditar por esta vía. Leídos juntos, C2.2 y C2.4, los dos subcomponentes del canal de duración, suman +3,56 M US$ (6,56 − 3,00): el canal cubre el costo de ambos.')])
for cap,png,new in (('Figura 3.','eeo9_fig3.png','Figura 3. C1.1 Subtransmisión — beneficios y costos económicos (VP 2015-2045 al 12 %; el módulo satélite de pérdidas técnicas se cita en memoria).'),
                    ('Figura 4.','eeo9_fig4.png','Figura 4. C1.2 Distribución — beneficios y costos económicos (VP 2015-2045 al 12 %; los módulos satélite se citan en memoria; canal de acceso y regularización = 0, ver texto).'),
                    ('Figura 11.','eeo9_fig11.png','Figura 11. Aporte de cada canal al Objetivo General de Desarrollo: resultado publicado y convención de facturación.')):
    set_media(cap,png,min_idx=50)
    i=next(k for k,t in enumerate(A) if t.strip().startswith(cap) and k>50); full(i,new)
print('medios:',list(L.MEDIA))
L.cell_set('Canales de aporte al Objetivo General de Desarrollo',6,3,'Resultado publicado; suma de las filas anteriores, con diferencias de 1 USD por redondeo',nth=0,check='Lectura B')
L.finish('salida_fin/Anexo_Flujos_Economicos_Financieros_EC-L1147 (con control de cambios).docx','salida_fin/Anexo_Flujos_Economicos_Financieros_EC-L1147.docx',r'lectura [AB]\b|EEO#|33\.821|48\.445',"salida_fin/log_EEO9_v2.json")
