# EC-L1147 · Anexo de Flujos Económicos y Financieros en versión final · 6-oct-2026

Pase corto del anexo de flujos (anexo electrónico de flujos por subcomponente) con el titular del 6-oct (O&M de la medición inteligente al 2,5 % anual del CAPEX): tres figuras regeneradas, una frase que lee juntos los subcomponentes C2.2 y C2.4 y el último código de lectura en palabras.
El documento va en versión limpia y con control de cambios; la limpia es exactamente la otra con todo aceptado (verificado párrafo a párrafo).

## Archivos y dónde van

| Archivo | Carpeta de destino en «Entrega Final v4» | SHA-256 (8) | Bytes |
|---|---|---|---|
| `Anexo_Flujos_Economicos_Financieros_EC-L1147.docx` | raíz (reemplaza) | `B3E4EA0F` | 1.574.424 |
| `Anexo_Flujos_Economicos_Financieros_EC-L1147 (con control de cambios).docx` | `Soporte\con control de cambios` | `44947E1E` | 1.584.894 |

Insumo: la versión con control de cambios del pase mecánico del 6-oct. Autor de las revisiones: «Revisión 2026-10 – versión final». 8 ediciones (10 inserciones y 9 eliminaciones de Word).
Los Word no se suben al repositorio porque son de uso interno del BID. Se entregaron en la conversación.

## Qué cambió

- **Figura 3** (C1.1 Subtransmisión: beneficios y costos económicos, VP 2015-2045 al 12 %; VAN 34,66 M US$) y **Figura 4** (C1.2 Distribución, con el canal de acceso y regularización en cero) regeneradas con los flujos del libro vigente; los módulos satélite se muestran aparte y se citan en memoria. Rótulos actualizados.
- **Figura 11** (aporte de cada canal al Objetivo General de Desarrollo) regenerada con las dos series del libro: resultado publicado (105,65 M US$: 56,7 capacidad y cobertura; 44,3 calidad y continuidad; 2,4 gestión comercial y medición; 2,3 pérdidas técnicas) y convención de facturación (120,27 M US$). Rótulo actualizado.
- **C2.2 y C2.4 leídos juntos.** Frase nueva en el apartado de centros de datos y de control: los dos subcomponentes del canal de duración suman +3,56 M US$ (6,56 − 3,00), igual en el resultado publicado y en la convención.
- **Códigos en palabras.** La fila de total de la tabla de canales de aporte decía «Lectura B; suma de las filas anteriores…»; pasa a «Resultado publicado; suma…». Sin «lectura A/B» en cuerpo ni notas al pie; «las dos lecturas» se conserva como sustantivo común donde remite al apartado 2.
- **Sin cambio de titular** (ya aplicado en el pase mecánico): VAN publicado 33.101.388 USD de 2015 al 12 %; convención 47.725.356.

## Verificación

- XML válido en ambas versiones; aceptar todo sobre la versión con control de cambios reproduce la limpia; 0 revisiones sin cerrar; las notas al pie no traían revisiones.
- Render con LibreOffice: 18 páginas; revisadas las páginas de las Figuras 3 (p. 6) y 11 (p. 15) y la tabla de canales.

## Pendientes que tocan a este anexo

- Renumeración EEO# cuando se confirme la tabla (este anexo era el EEO#8 y pasa a EEO9).
- El resaltado amarillo es la convención de texto revisado del paquete; decidir si se retira en la versión final.

## Entrada para el registro de revisión

```
2026-10-06 · Anexo_Flujos_Economicos_Financieros_EC-L1147.docx · versión final (pase corto: figuras y lectura conjunta C2.2+C2.4)
Insumo: versión con control de cambios del pase mecánico del 6-oct. Salidas: limpio B3E4EA0F; con control de cambios 44947E1E.
Figuras 3, 4 y 11 regeneradas con el libro vigente; frase C2.2+C2.4 = +3,56 M US$; fila de total de la tabla de canales en palabras (resultado publicado).
Titular sin cambio: VAN 33.101.388 (convención 47.725.356).
Herramientas: herramientas_docx/passlib.py, eeo9_pass.py y eeo9_fig.py (repositorio, commit del 6-oct).
```
