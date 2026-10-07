# EC-L1147 · Anexos electrónicos en Excel al titular del 6-oct · 6-oct-2026

Pase sobre los cuatro libros de apoyo (EEO1 correspondencia PMR, EEO6 riesgos y sostenibilidad, Sustento_AMI y Escenario_Macro_C23) para alinearlos con el titular del 6-oct (O&M de la medición inteligente al 2,5 % anual del CAPEX), los códigos en palabras, las lecturas sin confiabilidad como sensibilidad y la Tabla 1A del PCR. Edición a nivel de XML (`herramientas_docx/xlsx_xml.py`): gráficos, comentarios, estilos y anchos intactos; celdas nuevas o cambiadas sin valor en caché (Excel recalcula al abrir, como ya hacían los libros).

## Archivos y dónde van

| Archivo | Carpeta de destino en «Entrega Final v4» | SHA-256 (8) | Bytes |
|---|---|---|---|
| `EEO1_Correspondencia_PMR_EC-L1147.xlsx` | raíz (reemplaza) | `6BDF08C3` | 44.734 |
| `EEO6_Riesgos_Sostenibilidad_EC-L1147.xlsx` | raíz (reemplaza) | `681E7AB7` | 19.081 |
| `Sustento_AMI_EC-L1147.xlsx` | raíz (reemplaza) | `87080819` | 22.992 |
| `Escenario_Macro_C23_EC-L1147.xlsx` | raíz (reemplaza) | `0A62734F` | 40.617 |
| `LEEME_ENTREGA_FINAL.md` | raíz (reemplaza; copia en este repositorio como `LEEME_ENTREGA_FINAL_06102026.md`) | — | — |

Los libros no se suben al repositorio (uso interno del BID); se entregaron en la conversación. Registro completo de celdas (hoja, celda, valor anterior, valor nuevo) en `salida/log_anexos_xlsx.json` del pase; en EEO1 queda además en su hoja `Control_Cambios` (filas 58 a 77).

## Qué cambió

- **EEO1 (correspondencia PMR).** Cuadro de VAN por OED (hoja 01_Numeracion_OED, filas 9 a 16): columnas «resultado publicado» y «convención de facturación» en lugar de «sin canales / con canales, lectura A»; valores de AMI_Regla!B40:C43 con los totales por fórmula (33,10 y 47,73 M USD; diferencia 14,62 en el OED II); control y fuente reescritos; nota G6 sin código. «Figura 4 del PCR» pasa a «Tabla 1A del PCR» (Leame y 02_Indicadores_PMR). Control_Cambios con las 20 celdas del 6-oct.
- **EEO6 (riesgos y sostenibilidad).** Montecarlo (02_Riesgos_Evaluacion, filas 20 a 29) con la hoja MC_B del libro: 7,70 % (resultado publicado), 54,32 % (sin beneficios de confiabilidad), 23,11 % (sin duración), 6,63 % y 98,33 % (variantes con excedente fijo), convención no simulada; el AMI queda como memoria con su VAN actual (+12,39 / −2,23 M). Escenarios S0-S3 (03) con Sostenibilidad_Tasa (33,10; 28,40; 17,97; 7,02 M; TIR 18,34/17,72/16,13/13,94 %; todos sostenibles) y los avisos de «no recalculado» sustituidos por la nota de recálculo. Umbrales (04) con Umbrales_B, Sostenibilidad_Tasa, Retraso_B y Brecha_Tarifaria: conservación mínima 29,6 % (antes 63,0 %), caída 31,3 %, excedente 6,25 %, utilización 41,66 %, tarifa 3,57 ¢/kWh, ratio 1,11 GWh/MVA-año, CENS 387 USD/MWh, retraso 0,17 M (cota 48,1 M; se retira 32,08 M), brecha 0,81 ¢/kWh (1,16), fracción de crisis 24,2 % (34,9 %), fracción con la brecha regulada de 2026 por fórmula (36,3 %). Condiciones (05) con los umbrales nuevos y las fuentes del EEO5. R-13: umbral 0,81 ¢/kWh. Leame: EEO6, EEO5, 29,6 %.
- **Sustento_AMI.** Parámetro nuevo 02_Parametros!B42 = VP del O&M (719.654,04 USD; Flujo_Anual!V70); VAN AMI, B/C y VAN del programa de los escenarios E0-E5 lo restan (fórmulas de 03_Escenarios, filas 11 a 14, y control de la fila 19). Nota de actualización en 00_RESUMEN!A3; «acciones de datos» reescritas como vacíos declarados al cierre; la referencia a la banda oficial pasa de +8,96 a +8,24 M.
- **Escenario_Macro_C23.** Parámetro nuevo 00_RESUMEN!B19 = VP del O&M; E1, E2, E3 y la sensibilización de E3 (filas 80 a 86) lo restan; B/C del AMI con el costo total (4.597.659). Con el ahorro de corte y lectura, E1, E2 y E3 dan 31.054.684, 4.569.544 y 5.888.868 USD: exactamente los VAN del subcomponente del cuadro de escenarios del Análisis Económico. Nota en Limites_Inversion_AMI!J6 (12 USD/med·año ≈ 2,7 % del CAPEX por medidor).

## Verificación

- Copias recalculadas con LibreOffice: EEO1, EEO6 y Sustento_AMI sin ningún error de fórmula; Escenario_Macro con los mismos 16 `#N/A` que el original (hoja Diagnostico_Grafico, anteriores al pase).
- Controles: EEO1 totales 33,1013877905 y 47,7253555078 M; EEO6 B15 = 0,3626; Sustento E0 «OK — reproduce v16 con O&M»; Escenario_Macro E1/E2/E3 con C&R = 31.054.684 / 4.569.544 / 5.888.868.
- Barrido: sin «lectura A/B» ni cifras retiradas en los cuatro libros (en EEO1, Control_Cambios conserva los textos anteriores como historial).

## Pendientes

- Renumeración EEO# cuando se confirme la tabla; `Coincidencia_Docs` del EEO5 con las celdas nuevas (MC_B G4:G8 y B4:F8; Umbrales_B F40:F46; Sostenibilidad_Tasa B50:F55; Retraso_B B46, B50, B53; Brecha_Tarifaria D43:D44 y B52:B53; AMI_Regla B40:D43; Flujo_Anual V70).
- EEO6: la hoja 01_Riesgos_PCR reproduce la Tabla 4 del PCR, sin cambios.

## Entrada para el registro de revisión

```
2026-10-06 · EEO1, EEO6, Sustento_AMI y Escenario_Macro_C23 (xlsx) · titular del 6-oct
Salidas: EEO1 6BDF08C3; EEO6 681E7AB7; Sustento_AMI 87080819; Escenario_Macro 0A62734F. LEEME_ENTREGA_FINAL.md reescrito al 6-oct.
EEO1: VAN por OED en resultado publicado y convención (AMI_Regla B40:C43); Tabla 1A del PCR. EEO6: MC_B, Sostenibilidad_Tasa, Umbrales_B, Retraso_B, Brecha_Tarifaria; avisos retirados.
Sustento_AMI y Escenario_Macro: parámetro VP O&M 719.654,04 (Flujo_Anual!V70) restado en VAN AMI y del programa; E1/E2/E3 = 31,05/4,57/5,89 M.
Herramientas: herramientas_docx/xlsx_xml.py y anexos_pass.py (repositorio, commit del 6-oct).
```
