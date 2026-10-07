# Pase del 6-oct-2026 sobre los cuatro anexos electrónicos en Excel: titular con O&M de la medición inteligente al 2,5 % anual del CAPEX,
# códigos de lectura en palabras, lecturas sin confiabilidad solo como sensibilidad, Figura 4 del PCR → Tabla 1A, vacíos declarados.
import sys,json; sys.path.insert(0,'.')
from xlsx_xml import Book
OM=719654.0419955999            # EEO5, Flujo_Anual!V70: VP del O&M de la medición inteligente (2,5 % del CAPEX desde 2023), USD de 2015 al 12 %
OUT='out/'; LOGS={}
# ---------- Sustento_AMI ----------
b=Book('in/13fb5f44-Sustento_AMI_EC-L1147.xlsx')
b.set('00_RESUMEN','A3','Actualización 6-oct-2026 (titular del PCR): el VP de costos del AMI incluye el O&M al 2,5 % anual del CAPEX desde 2023 (719.654,04 USD de VP a 2015 al 12 %; EEO5, Flujo_Anual!V70). El VAN AMI y el VAN del programa de cada escenario bajan en esa cifra y el B/C usa el costo total. Las rutas E0-E5 siguen siendo internas (sustento de la prima CNEL); la banda oficial E1-E3 con el O&M vive en Escenario_Macro_C23_EC-L1147.xlsx y en el cuadro de escenarios del Análisis Económico.',style_from='A2')
b.replace('00_RESUMEN','A2','VAN +8,96 M incl. C&R)','VAN +8,24 M incl. C&R con el O&M del 6-oct-2026)')
b.set('00_RESUMEN','A16','VACÍOS DE DATO DECLARADOS AL CIERRE (sin nuevas solicitudes a las distribuidoras; moverían el central si se cerraran en operaciones sucesoras)',check='ACCIONES DE DATOS')
b.set('00_RESUMEN','A17','1. Centrosur: no consta si los 128 medidores sin línea base son conexiones clandestinas regularizadas (si lo fueran, el Δ del piso subiría hacia 111,65).',check='Consulta formal')
b.set('00_RESUMEN','A18','2. Los Ríos, Manabí, Guayas L.R. y Guayaquil (11.949 medidores, 64 % del parque): el hurto detectado o regularizado no se reportó.',check='Pedir a')
b.set('00_RESUMEN','A19','3. Sustento documental de la regla de focalización de los sitios AMI (OE/MEER): convertiría el supuesto de la prima en evidencia de diseño.',check='Sustento documental')
b.set('02_Parametros','A37','VP costos AMI C2.3 sin O&M (USD)',check='VP costos AMI C2.3')
b.replace('02_Parametros','C37','fila C2.3','fila C2.3 · solo CAPEX; el O&M va en la fila 42')
b.set('02_Parametros','A42','VP del O&M de la medición inteligente: 2,5 % anual del CAPEX desde 2023 (USD, VP a 2015, 12 %)',style_from='A41')
b.set('02_Parametros','B42',OM,style_from='B41')
b.set('02_Parametros','C42','Decisión del 6-oct-2026 (titular del PCR). EEO5, hoja Flujo_Anual, V70: vector 2,5 % × CAPEX AMI × (año ≥ 2023). Se suma al VP de costos del AMI (B37) y del programa (B40).',style_from='C41')
for c in 'BCDEFG':
    b.set('03_Escenarios',f'{c}11',f"={c}10-('02_Parametros'!$B$37+'02_Parametros'!$B$42)")
    b.set('03_Escenarios',f'{c}12',f"={c}10/('02_Parametros'!$B$37+'02_Parametros'!$B$42)")
    b.set('03_Escenarios',f'{c}13',f"='02_Parametros'!$B$38+({c}10-'02_Parametros'!$B$36)-'02_Parametros'!$B$42")
    b.set('03_Escenarios',f'{c}14',f"=('02_Parametros'!$B$39+({c}10-'02_Parametros'!$B$36))/('02_Parametros'!$B$40+'02_Parametros'!$B$42)")
b.set('03_Escenarios','H11','VP beneficios − VP costos AMI con O&M (3,878 + 0,720 = 4,598 M).',check='3,878 M')
b.set('03_Escenarios','H13','VAN v16 (0,731 M) + Δ del VP de beneficios AMI − VP del O&M del AMI (0,720 M).',check='VAN v16')
b.set('03_Escenarios','A19','Control: E0 debe reproducir el VAN del programa v16 (+731.265 USD) menos el O&M del AMI (−719.654 USD): +11.611 USD.',check='Control: E0')
b.set('03_Escenarios','B19','=IF(ABS(B13-(\'02_Parametros\'!$B$38-\'02_Parametros\'!$B$42))<2000,"OK — reproduce v16 con O&M","REVISAR")')
b.save(OUT+'Sustento_AMI_EC-L1147.xlsx'); LOGS['Sustento_AMI']=b.log
# ---------- Escenario_Macro ----------
b=Book('in/dfe2c0ff-Escenario_Macro_C23_EC-L1147.xlsx')
b.set('00_RESUMEN','A3','Actualización 6-oct-2026 (titular del PCR): el VAN AMI y el VAN del programa de E1, E2, E3 y de la sensibilización restan el VP del O&M de la medición inteligente al 2,5 % anual del CAPEX desde 2023 (fila 19; 719.654,04 USD; EEO5, Flujo_Anual!V70); el B/C del AMI usa el costo total (4.597.658,85 USD).',style_from='A2')
b.set('00_RESUMEN','A19','VP del O&M de la medición inteligente: 2,5 % anual del CAPEX desde 2023 (USD, VP a 2015, 12 %)',style_from='A11')
b.set('00_RESUMEN','B19',OM,style_from='B11')
b.set('00_RESUMEN','E19','Decisión del 6-oct-2026; EEO5, Flujo_Anual!V70. Se resta del VAN AMI y del VAN del programa en E1, E2, E3 y en la sensibilización de E3.',style_from='E11')
for sh,r in [('E1_Tope_Macro',63),('E2_Centrosur_Media',69),('E3_Parametrico',71)]:
    b.set(sh,f'B{r}',f"=B{r-1}-3878004.81-'00_RESUMEN'!$B$19",check='3878004.81')
    b.set(sh,f'B{r+1}',f"=B{r-1}/(3878004.81+'00_RESUMEN'!$B$19)",check='3878004.81')
    b.set(sh,f'B{r+2}',f"=731265.17+(B{r-1}-2262567.67)-'00_RESUMEN'!$B$19",check='731265.17')
    b.replace(sh,f'A{r}','VP costos AMI (3.878.005)','VP costos AMI (3.878.005 + O&M 719.654 = 4.597.659)')
    if sh!='E3_Parametrico': b.replace(sh,f'I{r+2}','Δ del VP de beneficios AMI;','Δ del VP de beneficios AMI − O&M del AMI (0,720 M; 00_RESUMEN!B19);')
for r in range(80,87):
    for c in 'BCD':
        t=b.text('E3_Parametrico',f'{c}{r}'); assert t.endswith("-2262567.67)/1000000"),t
        b.set('E3_Parametrico',f'{c}{r}',t.replace("-2262567.67)/1000000","-2262567.67-'00_RESUMEN'!$B$19)/1000000"))
b.replace('E3_Parametrico','A88','(motor v16 intacto en lo demás;','menos el O&M del AMI (0,720 M; 00_RESUMEN!B19) (motor v16 intacto en lo demás;')
b.set('Limites_Inversion_AMI','J6','Fuente 2·B65 (MDM, headend, mantenimiento): 12 USD/med·año ≈ 2,7 % del CAPEX por medidor, coherente con el O&M del 2,5 % anual adoptado el 6-oct-2026 para la valoración del programa.',check='Fuente 2')
b.save(OUT+'Escenario_Macro_C23_EC-L1147.xlsx'); LOGS['Escenario_Macro']=b.log
# ---------- EEO1 ----------
b=Book('in/25589e27-EEO1_Correspondencia_PMR_EC-L1147.xlsx')
b.replace('00_Leame','A4','(Figura 4 del PCR)','(Tabla 1A del PCR)')
b.replace('02_Indicadores_PMR','E3','(Figura 4 del PCR)','(Tabla 1A del PCR)')
b.replace('01_Numeracion_OED','G6','(lectura A)','(convención de facturación)')
b.set('01_Numeracion_OED','A9','OED según la matriz de resultados y el PMR · VAN por OED en el resultado publicado (regla de transferencias de la medición inteligente) y en la convención de facturación (declarada, no publicada)',check='lectura A')
b.set('01_Numeracion_OED','B10','VAN resultado publicado (M USD)',check='sin canales')
b.set('01_Numeracion_OED','C10','VAN convención de facturación (M USD)',check='con canales')
V={'11':(16203285.619080879,16203285.619080879),'12':(17517623.741424486,32141591.458765395),'13':(-619521.57,-619521.57)}
for r,(pb,ca) in V.items():
    b.set('01_Numeracion_OED',f'B{r}',pb/1e6); b.set('01_Numeracion_OED',f'C{r}',ca/1e6); b.set('01_Numeracion_OED',f'D{r}',f'=C{r}-B{r}')
b.set('01_Numeracion_OED','B14','=SUM(B11:B13)'); b.set('01_Numeracion_OED','C14','=SUM(C11:C13)'); b.set('01_Numeracion_OED','D14','=C14-B14')
b.set('01_Numeracion_OED','A15','Control: el total del resultado publicado coincide con 33.101.387,79 USD (EEO5, hoja AMI_Regla, C43; VAN publicado del programa) y el de la convención de facturación con 47.725.355,51 USD (AMI_Regla, B43). La diferencia, 14.623.967,72 USD, es la facturación recuperada por la medición inteligente que la regla de transferencias no acredita (toda en el OED II). Por OED: I 16.203.285,62; II 17.517.623,74 (32.141.591,46 con la convención); III −619.521,57 (AMI_Regla, B40:C42). Las cifras del cuadro están en millones de USD con dos decimales; los totales se calculan sobre los valores sin redondear. Las lecturas sin beneficios de confiabilidad se muestran solo en el cuadro de sensibilidad del Análisis Económico.',check='Control:')
b.set('01_Numeracion_OED','A16','Fuente: EEO5 (Libro de Confiabilidad y VAN), hoja AMI_Regla (B40:D43) y hoja Mapa_Objetivos. Valores con el O&M de la medición inteligente al 2,5 % anual del CAPEX (6-oct-2026).',check='Fuente:')
r0=58
for i,(sh,ref,old,new) in enumerate(list(b.log)):
    r=r0+i
    for c,v in zip('ABCDE',['2026-10-06',f'{sh}!{ref}',str(old) if old is not None else '—',str(new),'Titular del 6-oct-2026 (O&M de la medición inteligente al 2,5 %; resultado publicado y convención de facturación; códigos en palabras; Figura 4 del PCR convertida en Tabla 1A)']):
        b.set('Control_Cambios',f'{c}{r}',v,kind='s',style_from=f'{c}57')
b.save(OUT+'EEO1_Correspondencia_PMR_EC-L1147.xlsx'); LOGS['EEO1']=b.log
# ---------- EEO6 ----------
b=Book('in/9fa8ea6c-EEO6_Riesgos_Sostenibilidad_EC-L1147.xlsx')
b.replace('00_Leame','A1','EEO#6 ·','EEO6 ·')
b.replace('00_Leame','A4','sobre la base del Libro de Analisis (EEO#4), con fórmulas','sobre el resultado publicado (Libro de Confiabilidad y VAN, EEO5, hoja Sostenibilidad_Tasa; cifras')
b.replace('00_Leame','A5','vivas en Libro_Analisis!Sostenibilidad)','recalculadas el 6-oct-2026 con el O&M de la medición inteligente al 2,5 % anual del CAPEX)')
b.replace('00_Leame','A9','63,0 %','29,6 %')
b.replace('02_Riesgos_Evaluacion','G17','0,82 ¢/kWh de brecha media (lectura B)','0,81 ¢/kWh de brecha media (resultado publicado; 1,16 con la convención de facturación)')
b.set('02_Riesgos_Evaluacion','A20','Probabilidad de VAN negativo (EEO5, hoja MC_B: 10.000 corridas, nueve variables inciertas, semilla 20260917; VP en USD de 2015 al 12 %)',check='Probabilidad de VAN negativo')
MC=[('Resultado publicado (regla de transferencias de la medición inteligente), con los beneficios de confiabilidad',0.077,'Riesgo bajo. Media 27,75 M USD; P5 −3,35; mediana 26,14; P95 64,77. Es la cifra que publica el PCR (II.3, Tabla 3A).'),
    ('Resultado publicado sin los beneficios de confiabilidad (C2.1 frecuencia; C2.2/C2.4 duración)',0.5432,'Sensibilidad: el VAN queda casi nulo (115.428 USD) y más de la mitad de las corridas son negativas. Media −0,47 M USD; P5 −29,18; mediana −2,49; P95 35,33.'),
    ('Resultado publicado sin el canal de duración (C2.2/C2.4)',0.2311,'Sensibilidad: sin el canal de duración el riesgo sube, aunque menos que al retirar también la frecuencia. Media 16,39 M USD; P5 −14,06; mediana 14,74; P95 53,04.'),
    ('Resultado publicado con el excedente del consumidor fijo en su valor central (15 %)',0.0663,'Variante N2b: el excedente explica la mayor parte de la dispersión; fijo, el riesgo baja poco porque el signo depende también de la utilización y la tarifa.'),
    ('Resultado publicado sin beneficios de confiabilidad y con el excedente fijo (15 %)',0.9833,'Variante N2b sin confiabilidad: casi todas las corridas son negativas.'),
    ('Convención de facturación (toda la facturación recuperada como beneficio)','no simulada','Se declara y no se publica (VAN 47.725.355,51 USD; Análisis Económico, cuadro de sensibilidad).')]
for i,(a,p,c) in enumerate(MC):
    r=22+i; b.set('02_Riesgos_Evaluacion',f'A{r}',a); b.set('02_Riesgos_Evaluacion',f'B{r}',p); b.set('02_Riesgos_Evaluacion',f'C{r}',c)
b.set('02_Riesgos_Evaluacion','A28','AMI (C2.3) — P(VAN > 0) del subcomponente en su propio Montecarlo (memoria: simulación anterior a la decisión del O&M del 2,5 %, fuera del Montecarlo del programa)',check='AMI (C2.3)')
b.set('02_Riesgos_Evaluacion','C28','Se conserva como memoria por comparación. Con el O&M del 2,5 % el subcomponente vale +12.392.693 USD con la convención y −2.231.275 USD en el resultado publicado (EEO5, AMI_Regla!B38:C38).',check='Se reporta')
b.set('02_Riesgos_Evaluacion','A29','Fuente: EEO5 (Libro de Confiabilidad y VAN), hoja MC_B, filas 4 a 8 (G: P(VAN<0); B a F: media, desviación, P5, P50, P95). Sustituye a la réplica de referencia de 100.000 iteraciones de la entrega anterior (11,5 % sobre la base previa).',check='Fuente:')
b.set('03_Sostenibilidad_E3F','A1','Escenarios de sostenibilidad posterior al cierre sobre el resultado publicado (EEO5, hoja Sostenibilidad_Tasa; beneficios × E y OPEX × F desde 2026; CAPEX intacto)',check='Escenarios de sostenibilidad')
S=[(33101387.790650919,1.4562585528622674,0.18342054596736412,2027),(28401478.546682719,1.3914765623367047,0.17721468005914032,2028),(17968938.435987238,1.2442017520652753,0.16127241090639344,2028),(7020037.5139122326,1.0934367603856376,0.13939378563945115,2031)]
for i,(v,bc,tir,yr) in enumerate(S):
    r=4+i; b.set('03_Sostenibilidad_E3F',f'D{r}',v); b.set('03_Sostenibilidad_E3F',f'E{r}',bc); b.set('03_Sostenibilidad_E3F',f'F{r}',tir); b.set('03_Sostenibilidad_E3F',f'G{r}',yr); b.set('03_Sostenibilidad_E3F',f'H{r}','Sostenible (VAN > 0)')
b.set('03_Sostenibilidad_E3F','A9','Nota: escenarios recalculados el 6-oct-2026 sobre el resultado publicado (VAN 33.101.387,79 USD de 2015 al 12 %, con el O&M de la medición inteligente al 2,5 % anual del CAPEX); definiciones S1 (beneficios 90 %), S2 (70 %, OPEX 120 %) y S3 (50 %, OPEX 150 %) sin cambio. El VAN sigue positivo en los tres escenarios de degradación; conservar el 29,6 % de los beneficios posteriores a 2025 deja el VAN en cero. Fuente: EEO5, Sostenibilidad_Tasa!B50:F55.',check='AVISO')
U={4:('Factor de degradación de beneficios que anula el VAN (OPEX intacto, desde 2026)',0.29570155353249039,'Conservar el 29,6 % de los beneficios posteriores a 2025 mantiene el VAN en cero (sobre la base anterior era el 63,0 %). Fuente: EEO5, Sostenibilidad_Tasa!B54.'),
   5:('Costo del retraso histórico (cierre 2023 frente a 2019) con la regla por componente (USD)',172283.354154192,'Cada beneficio se adelanta solo junto con el activo que lo produce: el cierre en 2019 habría dejado el VAN en 33.273.671 USD, 0,17 M por encima del publicado. Fuente: EEO5, Retraso_B!B53 − B46.'),
   6:('Caída del VP de todos los beneficios que anula el VAN',0.31330875411203157,'Umbral de reversión del signo: 31,3 %. Fuente: EEO5, Sostenibilidad_Tasa!B55.'),
   7:('Factor de excedente de equilibrio',0.062492000159355784,'Fuera de la banda [0,10; 0,30] (central 0,15): no anula el VAN dentro de su banda. Fuente: EEO5, Umbrales_B!F40.'),
   8:('Factor de utilización de equilibrio',0.41661333439570469,'Por debajo de la banda [0,4278; 1,00] (central 1,00): no anula el VAN dentro de su banda. Fuente: EEO5, Umbrales_B!F42.'),
   9:('Tarifa media de equilibrio (USD/kWh)',0.035736228993243455,'Fuera de la banda [0,07; 0,11] (central 0,092): no anula el VAN dentro de su banda. Fuente: EEO5, Umbrales_B!F45.'),
   10:('Ratio energía/capacidad de equilibrio (GWh/MVA-año)',1.1123576028365292,'Por debajo de la banda observada [2,358; 3,234] (central 2,67): no puede anular el VAN. Fuente: EEO5, Umbrales_B!F46.'),
   11:('Costo de la energía no suministrada de equilibrio (CENS, USD/MWh)',386.58202936974249,'Por debajo de la banda [789,4; 1.762] (central 1.533): no anula el VAN. Fuente: EEO5, Umbrales_B!F43. La energía recuperada por la medición inteligente no es frente de quiebre: en el resultado publicado solo cuenta su componente real.'),
   12:('Costo del retraso histórico, cota superior (todos los beneficios adelantados por igual, USD)',48071037.024622604,'Cota que no se publica: supone adelantar beneficios de activos que aún no existían. Fuente: EEO5, Retraso_B!B50 − B46. Sustituye a los 32.082.628 USD de la base anterior.'),
   13:('Brecha media costo-tarifa que anula el VAN publicado (¢/kWh)',0.80507359853038718,'Resultado publicado; convención de facturación = 1,16 ¢/kWh. Fuente: EEO5, Brecha_Tarifaria!D43:D44.'),
   14:('Fracción de años de crisis de generación que anula el VAN publicado',0.24230364849424038,'Resultado publicado; convención de facturación = 34,9 %. Fuente: EEO5, Brecha_Tarifaria!B52:B53.'),
   15:('Fracción de años con la brecha regulada de 2026 que anula el VAN publicado','=B13/2.22','Resultado publicado (= brecha de cambio / brecha regulada de 2026, 2,22 ¢/kWh; ARCERNNR); convención de facturación = 52,3 %. Fuente: EEO5, Brecha_Tarifaria!D43 y Precio_Equilibrio_Oficial.')}
for r,(a,v,c) in U.items():
    b.set('04_Umbrales',f'A{r}',a); b.set('04_Umbrales',f'B{r}',v); b.set('04_Umbrales',f'C{r}',c)
b.set('04_Umbrales','A1','Umbrales de sostenibilidad del resultado económico publicado (EEO5, Libro de Confiabilidad y VAN: hojas Umbrales_B, Sostenibilidad_Tasa, Retraso_B y Brecha_Tarifaria)',check='Umbrales de sostenibilidad')
b.set('04_Umbrales','A16','Nota: umbrales recalculados el 6-oct-2026 sobre el resultado publicado (VAN 33.101.387,79 USD de 2015 al 12 %; O&M de la medición inteligente al 2,5 % anual del CAPEX). Ningún parámetro de precio o cantidad anula el VAN dentro de su banda de evidencia; el riesgo del signo está en la brecha entre el costo de suministro y la tarifa (filas 13 a 15).',check='AVISO')
b.set('05_Condiciones','C4','≥ 1,11 GWh/MVA-año (valor de cambio 1,1124); observado 2,67 (banda 2,36-3,23) y creciente',check='1,9425')
b.set('05_Condiciones','E4','EEO5, hoja Umbrales_B (fila «ratio»)',check='Switching_Values')
b.set('05_Condiciones','C5','≥ 2,5 % anual del CAPEX (paramétrico; es el O&M adoptado para la medición inteligente desde 2023); referencia ARCONEL por añadas 0,165/0,50/0,65 %',check='2,5 %')
b.set('05_Condiciones','E5','Libro_Analisis!OM_ARCONEL · EEO5, hojas Flujo_Anual (V70) y Sostenibilidad_Tasa',check='OM_ARCONEL')
b.set('05_Condiciones','C6','VAN del subcomponente a 44,8 GWh/año: +12,39 M USD con la convención de facturación y −2,23 M en el resultado publicado (O&M al 2,5 %); con la convención cubre su costo desde ≈12,1 GWh/año (44,8 × 4,60 / 16,99)',check='GWh/año')
b.set('05_Condiciones','E6','EEO5, AMI_Regla!B38:C38 · Análisis Económico, cuadro de escenarios de la medición inteligente',check='AE 5.3')
b.save(OUT+'EEO6_Riesgos_Sostenibilidad_EC-L1147.xlsx'); LOGS['EEO6']=b.log
json.dump(LOGS,open(OUT+'log_anexos_xlsx.json','w'),ensure_ascii=False,indent=0)
print({k:len(v) for k,v in LOGS.items()})
