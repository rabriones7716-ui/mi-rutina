# ENTREGA FINAL · Programa EC-L1147 — versión para el BID (6-oct-2026)

Carpeta autocontenida. Sustituye a la entrega del 24-sep-2026 (que queda intacta en `..\Entrega Final v3\`). Todos los documentos
finales están en la raíz; el soporte reproducible, en `Soporte\`; los controles de calidad, en `QA\`; las versiones con control
de cambios, en `Soporte\con control de cambios\`.

Qué cambia respecto del 24-sep: un solo cambio de titular (el O&M de la medición inteligente entra al 2,5 % anual de su CAPEX
desde 2023) y una reorganización de la presentación: caso base único (resultado publicado), cuadro de sensibilidad de cuatro
casos con notas al pie, Montecarlo del Libro de Confiabilidad y VAN, códigos de lectura en palabras y capas históricas rotuladas
como memoria. El PCR recorta II.3 y IV a cerca de la mitad de su prosa y lo compensa con tablas.

## 1. Contenido y enlaces electrónicos

| Enlace | Archivo | Contenido |
|---|---|---|
| — | `PCR_EC-L1147.docx` (limpio) · `PCR_EC-L1147 (con control de cambios).docx` | Informe de Terminación de Proyecto; Tabla 1A (lógica vertical verificada, antes Figura 4), Tablas 3A a 3D (resultado y sensibilidad, por objetivo y subcomponente, riesgo y umbrales, eficiencia operativa), sección IV en tabla |
| EEO#1 | `EEO1_Correspondencia_PMR_EC-L1147.xlsx` | Correspondencia PMR ↔ lógica vertical; VAN por OED en el resultado publicado y en la convención de facturación; registro de cambios |
| EEO#2 | `Anexo_Analisis_Contrafactual_EC-L1147.docx` | Análisis contrafactual: método de tres líneas y banda, física del C1.1, C1.2 y regularización, AMI, canal de frecuencia (reconectadores, estudio de eventos por cohorte), canal de duración (SCADA), dosis-respuesta, contribución al VAN, cuadro de sensibilidad, apéndice de figuras |
| EEO#3 | `Anexo_Analisis_Economico_EC-L1147.docx` | Evaluación económica: resultado publicado, VAN por componente y por OED oficial, habilitantes, cascada única, cuadro de sensibilidad de cuatro casos, Montecarlo (hoja MC_B), sostenibilidad, retraso con regla por componente, memoria histórica rotulada |
| EEO#4 | `Libro_Analisis_EC-L1147.xlsx` · `Libro_Confiabilidad_VAN_EC-L1147.xlsx` | Libro de Análisis (modelo CF&AE, memoria) y Libro de Confiabilidad y VAN del programa (Flujo_Anual, AMI_Regla, MC_B, Umbrales_B, Sostenibilidad_Tasa, Retraso_B, Brecha_Tarifaria, VAN_Financiero, Mapa_Flujos, Mapa_Objetivos, Coincidencia_Docs, Leyenda_Flujos) |
| EEO#5 | `Sustento_AMI_EC-L1147.xlsx` · `Escenario_Macro_C23_EC-L1147.xlsx` | Sustento de la medición inteligente y banda de escenarios; el VP de costos del AMI incluye el O&M al 2,5 % (fila nueva de parámetro); E1, E2 y E3 reproducen los VAN del subcomponente del EEO#3 (31,05; 4,57; 5,89 M USD con el ahorro de corte y lectura) |
| EEO#6 | `EEO6_Riesgos_Sostenibilidad_EC-L1147.xlsx` | Riesgos y sostenibilidad: Montecarlo MC_B, escenarios S0-S3 y umbrales recalculados sobre el resultado publicado; condiciones de sostenibilidad |
| EEO#7 | — | Permisos ambientales: pendiente de confirmación del Banco |
| EEO#8 | `Anexo_Flujos_Economicos_Financieros_EC-L1147.docx` | Qué entra al VAN y qué es transferencia, por componente; mapa de flujos; vista por objetivos; regla de la medición inteligente; figuras con el titular del 6-oct |
| EEO#9 | `Modulos_Satelite\` | Pérdidas técnicas de las obras del C1.1 y C1.2 (`1__…`) y C1.2 con red y sin red (`2__…`), con sus notas metodológicas; memoria, fuera del VAN |

La numeración EEO# es la que imprime el PCR. Los anexos en Excel ya usan la numeración del formato de EC-L1160 (EEO3 Libro de
Análisis, EEO5 Libro de Confiabilidad y VAN, EEO6 riesgos, EEO10 correspondencia PMR); la renumeración del PCR y de los anexos
en Word queda pendiente de confirmar la tabla (apartado 4).

Colores de los libros (hoja `Leyenda_Flujos` en cada uno): azul económico (entra al VAN), naranja transferencias entre
hogares, Estado y BID, violeta perspectiva de las empresas distribuidoras, verde/rojo resultados, gris base física, gris
claro en cursiva memoria.

## 2. Cifras publicadas (VP en USD de 2015, 12 %, 2015-2045)
- **Resultado publicado (regla de transferencias de la medición inteligente: f = 1,2, λ = 0,5, gross-up a bornes de generación;
  O&M de la medición inteligente al 2,5 % anual de su CAPEX desde 2023):** VAN del programa **33.101.387,79 USD**, B/C 1,4563,
  TIR 18,34 %, recuperación descontada en 2027; VP de beneficios 105.651.014,71 y VP de costos 72.549.626,92. Montecarlo del
  Libro de Confiabilidad y VAN (hoja MC_B, 10.000 corridas, nueve variables, semilla documentada): media 27,75 M, P50 26,14 M,
  P5 −3,35 M, P95 64,77 M, P(VAN<0) 7,70 %.
- **Convención de facturación, declarada y no publicada:** 47.725.355,51 USD, B/C 1,6578, TIR 20,22 %, recuperación en 2026;
  no se simula. La diferencia con el resultado publicado (14.623.967,72) es la facturación recuperada que la regla de
  transferencias no acredita.
- **Sensibilidad sin beneficios de confiabilidad** (solo en el cuadro de sensibilidad de cada documento): 115.427,83 USD
  (TIR 12,02 %; B/C 1,0016; 2045; P(VAN<0) 54,32 %) y 14.739.395,55 con la convención (14,73 %; 1,2032; 2033). Sin el canal de
  duración, P(VAN<0) 23,11 %.
- **Canales de contribución (no atribución), estimados sobre el panel histórico de calidad de servicio por alimentador del
  regulador (2008-2025):** C2.1 frecuencia 20.415.038,67 (banda 1,91-28,63 M); C2.2/C2.4 duración 12.570.921,28 (banda
  9,17-14,99 M). Escenarios de demanda (convención): g 0 % 43,01 M; 3 % 45,82 M; 4,62 % 47,73 M (0,72 M por debajo de los
  del 24-sep por el O&M).
- Por OED oficial: I +16,20 M; II +17,52 M en el resultado publicado (+32,14 M con la convención); III −0,62 M (capacitación,
  habilitante). Por subcomponente: C1.1 +28,76; C1.2 −10,82; C2.1 +16,25; C2.2 +6,56; C2.3 −2,23 (+12,39 con la convención;
  VP de costos 4,60 M con el O&M); C2.4 −3,00; habilitantes −2,42 (0,62 M el C3).
- C1.2: VAN −10,82 M; el canal de regularización vale 0 en el caso central y haría positivo el componente con 33.896
  hogares regularizados (10,55 % de los beneficiarios), vacío declarado al cierre. Acceso nuevo no plausible.
- Satélites (memoria): pérdidas técnicas ascendentes C1.1 1,56/0,99 M (sustituye al canal sellado, no se suma); C1.2 0,32 M.
- **Riesgo del signo (hoja `Umbrales_B`):** ningún parámetro anula el VAN publicado dentro de su banda de evidencia: tarifa
  media de cambio 3,57 ¢/kWh (banda 7-11), excedente 6,25 % (banda 10-30), utilización 41,66 % (banda 42,78-100), energía por
  capacidad 1,11 GWh/MVA-año (banda 2,36-3,23), CENS 387 USD/MWh (banda 789-1.762). Tres fragilidades declaradas con su valor
  de cambio: carbono (con la senda baja del Banco Mundial el VAN pasaría a −21,12 M y la TIR a 5,50 %; el 61 % de esa senda lo
  anula; el titular va sin carbono), costo marginal de los fondos públicos (el signo se invierte en 1,277, dentro de la banda
  1,2-1,3) y conversión de horas de interrupción a energía no suministrada (con el factor 0,4145 el VAN baja a 14,41 M y la
  TIR a 14,95 %).
- **Tarifas y costos (hoja `Brecha_Tarifaria`):** el canal de energía adicional servida (56,74 M; 53,7 % de los beneficios)
  supone que la tarifa cubre el costo marginal de suministro: se cumple en año normal (9,08 ¢ frente a 9,2) y no en año de
  crisis de generación (12,52 ¢; brecha 3,32 ¢). Cada centavo de brecha resta 41,12 M; la brecha media que anula el VAN
  publicado es de 0,81 ¢/kWh (1,16 con la convención), es decir, uno de cada cuatro (tres) años de crisis (24,2 % / 34,9 %).
  Transferencia implícita por subsidio tarifario sobre esa energía (brecha del costo medio del servicio, 2,14 ¢ normal /
  5,58 crisis): 87,98 M de VP en año normal (2,66 veces el VAN publicado) y 229,46 M en crisis, Estado → usuarios,
  proporcional al consumo y por ello concentrada en los usuarios de mayor consumo; no entra al VAN. Recalcado en el PCR
  (II.3, II.4 y IV), en EEO#3, en EEO#8 y en EEO#6 (R-13, R-14, umbrales).
- **Precio de equilibrio con fuentes oficiales (EEO#3; hojas `Precio_Equilibrio_Oficial` y `Fuentes_Tarifas`):** determinación
  anual de costos del SPEE del regulador: 9,028 ¢/kWh (2024, previa a la crisis); 11,92 frente a una tarifa media de 9,65
  (2025, reforma de mayo; resultado tarifario −603,11 MUS$); 12,83 frente a 10,61 (2026; −598,29 MUS$), cubierto por el Estado
  (art. 59 LOSPEE). Brecha regulada 2,27/2,22 ¢/kWh frente a 2,14 de la estimación propia. Cotas: la brecha de 2026 sostenida
  en todo el horizonte dejaría el VAN publicado en ≈ −58 M (33,10 − 2,22 × 41,12); el valor de cambio de 0,81 ¢/kWh equivale
  al 36,3 % de los años con esa brecha (24,2 % con la brecha marginal de crisis; episodios observados 2015-2025 ≈ 18 %).
  Incidencia por grupo (energía 2023): residencial 36,6 %, industrial 26,1 %, comercial 18,7 %. Anualidad del CAPEX del
  programa 9,64 MUS$/año = 0,036 ¢/kWh (0,28 % del costo del servicio). Ficha de 142 fuentes con URL
  (`Soporte\tarifas\fuentes_tarifas.csv`).
- **VAN financiero por actor (hoja `VAN_Financiero`; EEO#3; PCR II.4; EEO#8):** distribuidoras (sector) +147,66 M; generación
  pública a costo sin subsidio −136,04; Transelectric 0,00; Estado central −58,68; sector público consolidado −47,06 (+11,61
  antes del CAPEX); usuarios (memoria) −397,31. Conciliación con el VAN económico: −47,06 + 56,74 + 44,26 − 4,90 − 1,31 =
  47,73 (convención); −14,62 → 33,10 (publicado).
- **Retraso (hoja `Retraso_B`):** con la regla por componente (cada beneficio se adelanta solo con el activo que lo produce)
  el cierre en 2019 habría dejado el VAN en 33,27 M, 0,17 M por encima del publicado; cota superior 48,1 M si todos los
  beneficios se adelantaran por igual. La cifra de 32,1 M de la entrega anterior se retira.
- **Sostenibilidad (hoja `Sostenibilidad_Tasa`):** S1 leve +28,40 M (TIR 17,72 %), S2 moderada +17,97 M (16,13 %), S3 severa
  +7,02 M (13,94 %); conservar el 29,6 % de los beneficios posteriores a 2025 deja el VAN en cero.
- **Aportes del coordinador (G. Durán) integrados en el PCR:** Introducción, Relevancia (metas del PND, potencia instalada y
  demanda con dos figuras, componentes-OED, montos por componente 62,72/24,64/2,09 M más 1,15 M no asignados) y Efectividad
  (energía recuperada sin meta numérica), como pasada con control de cambios y autor «Integración aportes G. Durán». FMIk
  132 % con el R3 (134 % con la matriz técnica), TTIk 134 % con el R3 (126 % con la matriz técnica). Figuras 1 a 4 (la
  lógica vertical verificada pasa a la Tabla 1A). Los siete comentarios de Gabriel sobre la tabla de hallazgos quedan para la
  reunión del equipo (`Soporte\aportes_GD\DIFF_GD_vs_v3.md`).

## 3. Decisiones adoptadas (todas reversibles en los libros)
1. Resultado publicado = regla de transferencias de la medición inteligente (antes «lectura B»), por coherencia con el
   programa hermano y con la regla «las transferencias no suman al VAN»; la convención de facturación (antes «lectura A») se
   declara y no se publica. Selector en `Libro_Confiabilidad_VAN!AMI_Regla`. Códigos de lectura en palabras en todos los
   documentos y anexos.
2. O&M de la medición inteligente al 2,5 % anual de su CAPEX desde 2023 (VP 719.654,04 USD; `Flujo_Anual!V70`): único cambio
   de titular respecto del 24-sep.
3. Caso base único y cuadro de sensibilidad de cuatro casos (resultado publicado y convención, con y sin beneficios de
   confiabilidad) con notas al pie que explican cada escenario; las lecturas sin confiabilidad no aparecen en otro lugar.
4. OED por la matriz oficial del PCR, con nota de cruce a la agrupación interna del modelo.
5. FMIk/TTIk y capacitación con la cifra oficial de cierre (matriz R3) en el cuerpo y las otras lecturas en nota.
6. Módulos satélite y estudio de eventos fuera del VAN; dosis-respuesta descriptiva; el delta de TTIk del estimador de
   diferencias en diferencias se fija en cero (no significativo, sin grupo de control).
7. Sostenibilidad S1-S3, umbrales y Montecarlo recalculados sobre el resultado publicado (EEO#6); calificación por criterio
   (Tabla 6) sin recalcular.
8. La brecha entre tarifa y costo de suministro se presenta como el principal riesgo del signo del VAN y como transferencia
   distributiva, sin alterar el VAN publicado.
9. Costo del retraso con la regla por componente (0,17 M; cota 48,1 M).
10. Sin nuevas solicitudes de datos a las distribuidoras: las brechas se declaran como vacíos al cierre (siete en el PCR).
11. PCR: II.3 y IV a cerca de la mitad de su prosa, compensadas con la Tabla 1A y las Tablas 3A a 3D.

## 4. Pendientes del consultor y del Banco
- Vacíos declarados al cierre (sin nuevas solicitudes): conexiones nuevas por obra; holgura SCADA de las subestaciones
  vecinas; 128 medidores sin línea base; O&M por activo; costos de corte y lectura previos al AMI; pérdidas no técnicas de
  cuatro unidades de CNEL; consumo por usuario de las cuentas con medidor del Programa; precio de equilibrio (tarifa media y
  resultado tarifario 2024; determinación original 2025; serie 2019-2023; facturación por grupo de consumo 2023; costo
  marginal CENACE 2022-2025); beneficiarios del subsidio por categoría tarifaria.
- Renumeración de los anexos electrónicos al formato de EC-L1160 (tabla por confirmar); EEO#7; calificación por criterio;
  contrapartida local y cancelación formal; escenario de emergencia 15/35 % (pase propio, sin tocar en esta entrega).
- Al abrir los Word, «Actualizar campos» (tablas de contenido, índices de tablas y figuras). El resaltado amarillo es la
  convención de texto revisado del paquete: decidir si se retira.
- Registrar en `Coincidencia_Docs` del Libro de Confiabilidad y VAN las celdas nuevas que citan los anexos (lista en las notas
  de entrega del repositorio).

## 5. Controles de calidad (`QA\`)
Cada versión limpia es exactamente su versión con control de cambios con todo aceptado (verificado párrafo a párrafo, cuerpo y
notas al pie; corrección del 6-oct: las notas al pie traían revisiones del insumo sin aceptar). Barrido de restos en los
limpios: sin «lectura A/B», sin cifras retiradas (33.821.041,83; 48.445.009,55; 18,45 %; 1,4708; 11,5 %; 48,1 %; 15.459.050;
32,1 M salvo la frase que lo retira); quedan solo usos de memoria rotulados. Cifras clave y coincidencia con las celdas vivas
del Libro de Confiabilidad y VAN: titular del 6-oct en todos los documentos. Anexos en Excel editados a nivel de XML
(gráficos, comentarios y estilos intactos) y recalculados con LibreOffice sin errores de fórmula nuevos (los 16 `#N/A` de
`Diagnostico_Grafico` del Escenario Macro son anteriores y propios de LibreOffice). Renders de LibreOffice revisados página
a página en las secciones tocadas.

## 6. Reproducción
`Soporte\` contiene el plan, el inventario de la entrega anterior, los scripts de edición de cada documento, el motor de
documentos y las QA, los constructores de los libros, la analítica (tres líneas, estudio de eventos, dosis-respuesta,
duración por subestación) con sus figuras, las cifras canónicas y las bitácoras. Los pases del 6-oct están en el repositorio
(`herramientas_docx\`: `passlib.py`, `cf_pass.py`, `ae_pass.py`, `pcr_edit.py`, `eeo9_pass.py`, `xlsx_xml.py`,
`anexos_pass.py`), una corrida desde la versión con control de cambios del pase mecánico; sus notas de entrega llevan las
huellas SHA-256 de cada archivo.
