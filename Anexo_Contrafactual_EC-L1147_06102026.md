# EC-L1147 · Anexo de Análisis Contrafactual en versión final · 6-oct-2026

Pase mecánico del anexo contrafactual con el titular del 6-oct (O&M de la medición inteligente al 2,5 % anual del CAPEX) y la estructura acordada: caso base único, cuadro de sensibilidad, Montecarlo y memoria histórica.
El documento va en versión limpia y con control de cambios; la limpia es exactamente la otra con todo aceptado (verificado párrafo a párrafo).

## Archivos y dónde van

| Archivo | Carpeta de destino en «Entrega Final v4» | SHA-256 (8) | Bytes |
|---|---|---|---|
| `Anexo_Analisis_Contrafactual_EC-L1147.docx` | raíz (reemplaza) | `3037ECC1` | 8.296.975 |
| `Anexo_Analisis_Contrafactual_EC-L1147 (con control de cambios).docx` | `Soporte\con control de cambios` | `1AA9636B` | 8.348.089 |
| `Libro_Analisis_EC-L1147_v2.xlsx` | raíz, renombrado a `Libro_Analisis_EC-L1147.xlsx` (reemplaza al `3AB4C505`) | `EF3E91B4` | — |

Insumo: la versión con control de cambios subida el 6-oct (SHA `BCFBBDD7`). Autor de las revisiones: «Revisión 2026-10 – versión final». 143 ediciones (778 eliminaciones y 679 inserciones de Word).
Los Word y el Excel no se suben al repositorio porque son de uso interno del BID. Se entregaron en la conversación.

## Decisión registrada

Ajuste del retiro del 6-oct. Las lecturas sin beneficios de confiabilidad desaparecen de la prosa dispersa y reaparecen en un único cuadro de sensibilidad por documento, con las cifras nuevas del libro (no las viejas de 15,46 M, 0,84 M, 12,18 %, 14,84 %, 2044 y 2033).
El cuadro cruza las dos decisiones de presentación: convención de la medición inteligente (resultado publicado o convención de facturación) y beneficios de confiabilidad (con o sin). Lleva notas al pie que explican cada caso.

| Caso | VAN al 12 % (USD 2015) | TIR | B/C | Recuperación | P(VAN<0) | Celdas EEO5 |
|---|---|---|---|---|---|---|
| Resultado publicado, con confiabilidad | +33.101.388 | 18,34 % | 1,4563 | 2027 | 7,70 % | Flujo_Anual D15, D24, D22, D34; MC_B G4 |
| Convención de facturación, con confiabilidad | +47.725.356 | 20,22 % | 1,6578 | 2026 | no simulada | Flujo_Anual B15, B24, B22, B34 |
| Resultado publicado, sin confiabilidad | +115.428 | 12,02 % | 1,0016 | 2045 | 54,32 % | Flujo_Anual E15, E24, E22, E34; MC_B G5 |
| Convención de facturación, sin confiabilidad | +14.739.396 | 14,73 % | 1,2032 | 2033 | no simulada | Flujo_Anual C15, C24, C22, C34 |

El mismo cuadro irá al Análisis Económico (versión completa) y al PCR (cuadro y una frase).

## Qué cambió en el anexo

- **Titular.** Ficha, Cuadro 23 (filas 9, 11 y 12), ficha de etapas, E.4, 8.11, 8.16, 9.3 y las fuentes: VAN publicado 33.101.387,79 (B/C 1,4563; TIR 18,34 %; recuperación 2027); convención 47.725.355,51 (1,6578; 20,22 %; 2026); transferencia 14.623.968. Todo con el O&M de la medición inteligente al 2,5 %.
- **Códigos en palabras.** «Lectura A» pasa a «convención de facturación» y «lectura B» a «resultado publicado» en texto, cuadros y rótulos.
- **Retiro de las lecturas sin confiabilidad dispersas.** Cuadro 3, 8.6, 8.14, 8.15, 8.17, 9.3, Cuadro 14 (fila «sin canales» eliminada), Cuadro 22 (celdas de la columna de escenarios), cascada por causa y matriz de escenarios del componente (columnas del Programa retiradas; VAN del componente con O&M: E2 4.569.544, E3 5.888.868, base 12.392.693, E1 31.054.684).
- **Objetivo II y C2.3.** VP costos 10.586.961; VAN +6.403.391 (E3 −100.434); TIR 18,23 %; B/C 1,605; participación 2,24 % publicado y 14,1 % convención; C2.3 aislado +12.392.693 (B/C 3,70; banda +4,57 a +31,05); OED II oficial +32.141.591 (convención) y +17.517.624 (publicado). Puente 4.29 y fuentes 4.28 y 4.31 actualizados.
- **Montecarlo.** La simulación del Programa es la hoja MC_B: 7,70 %, media 27,75, mediana 26,14, P5 −3,35, P95 64,77, 10.000 corridas, nueve parámetros, semilla 20260917. El Montecarlo del componente queda como memoria. Cuadro de percentiles con una sola fila (92,30 % positivo).
- **Sensibilidad.** Tasa de descuento: 77,71 M al 8 % y 8,96 M al 16 % (cálculo propio sobre B81 y B86 restando el VP del O&M; confirmar con la segunda exportación). Sostenibilidad S1-S3: +28,4, +18,0, +7,0; umbral 29,6 %; margen 31,3 %. Tornado del resultado publicado: excedente, ENS por MVA, utilización (Umbrales_B). Atribución del canal de energía: 75 % → +18,92 M; 50 % → +4,73 M; signo se invierte bajo 42 % (cuadro R1.3 recalculado).
- **Cuadro nuevo** de sensibilidad (apartado 8.4, tras el cuadro auxiliar por subcomponente) con notas al pie y entrada en el índice de cuadros. El cuadro auxiliar por subcomponente pasa a cuatro columnas: convención, publicado y aporte de los beneficios de confiabilidad.
- **Datos históricos de calidad.** 8.16 y la introducción del cuadro nuevo dejan constancia de que las cantidades físicas de los dos canales de confiabilidad se estiman sobre el panel histórico de calidad de servicio por alimentador del regulador (ARCONEL), 2008-2025, y no sobre parámetros importados.
- **Figuras regeneradas** con las cifras nuevas: 31 y 43 (cascada del VP de beneficios al resultado publicado), 32 y 46 (bandas de los canales), 34 (esquema), 44 (VAN por subcomponente antes y después de la confiabilidad), 45 (VP acumulado, recuperación 2027), 47 (g = 0), 48 (valores de cambio frente a bandas, hoja Umbrales_B), 49 (histograma MC_B), 50 (riesgo al retirar los beneficios de confiabilidad). Se conservan los tamaños en el documento.
- **Anexos electrónicos.** EEO#2 → EEO2; EEO#4 → EEO3 (Libro de Análisis) o EEO5 (Libro de Confiabilidad y VAN) según el libro citado; EEO#8 → EEO9.
- **Solicitudes de datos.** El apartado 10.5 pasa de «solicitudes que se elevan» a «vacíos de dato declarados al cierre»; las remisiones del texto se reescriben en el mismo sentido. El PMR vigente muestra 1.607 y la cifra adoptada en el paquete es 1.999.

## Verificación

- XML válido en ambas versiones; aceptar todo sobre la versión con control de cambios reproduce la limpia; 0 revisiones sin cerrar.
- Barrido de restos sobre el limpio: sin «lectura A/B», «sin canales», 33.821, 48.445, 18,45 %, 1,4708, 1,6744, 15.459, 835.08, 83,5, 11,5 %, 48,1 %, 7,08, EEO#. Quedan solo usos legítimos: «2044» como año del valor residual del modelo anterior, «1,67 kWh», «1,47 millones de cocinas», la etiqueta «valor de referencia externo» para fuentes ajenas a los libros y la hoja Solicitudes_EED.
- Render con LibreOffice: 111 páginas (120 con marcas). Revisadas las páginas de la ficha, el cuadro R1.3, la matriz de escenarios, el Cuadro 14, la cascada, el Montecarlo, el cuadro auxiliar, el cuadro nuevo y las figuras 31 a 50.

## Pendientes que tocan a este anexo

- El resaltado amarillo es la convención de texto revisado del paquete. Decidir si se retira en la versión final (se puede hacer con un pase sin control de cambios).
- Registrar en `Coincidencia_Docs` del EEO5 las celdas que ahora cita el anexo: Flujo_Anual B15:E15, B22:E22, B24:E24, B34:E34; MC_B G4:G6; Umbrales_B F40:F49; Mapa_Objetivos F10 y H24; AMI_Regla C41, D20, D21; VAN_Programa G18, J18; Sostenibilidad_Tasa B50:B55, B81, B86.
- La Figura 30 (rejilla del modelo anterior) se conserva como memoria; su texto ya lo dice.
- Segunda exportación del EEO5: confirmar Sostenibilidad_Tasa B81 y B86 con el O&M del AMI.

## Entrada para el registro de revisión

```
2026-10-06 · Anexo_Analisis_Contrafactual_EC-L1147.docx · versión final (pase mecánico + cuadro de sensibilidad)
Insumo: versión con control de cambios del 6-oct (SHA BCFBBDD7). Salidas: limpio 3037ECC1; con control de cambios 1AA9636B.
Titular con O&M de la medición inteligente al 2,5 %: VAN publicado 33.101.387,79 (B/C 1,4563; TIR 18,34 %; 2027); convención 47.725.355,51 (1,6578; 20,22 %; 2026).
Decisión: las lecturas sin beneficios de confiabilidad se muestran solo en el cuadro de sensibilidad (115.428 y 14.739.396 USD; 12,02 % y 14,73 %; 2045 y 2033; P(VAN<0) 54,32 %), con notas al pie.
Montecarlo MC_B 7,70 %; códigos en palabras; EEO# renumerados; solicitudes → vacíos declarados; figuras 31, 32, 34, 43-50 regeneradas.
Herramienta: herramientas_docx/cf_pass.py y cf_fig3.py (repositorio, commit del 6-oct).
```
