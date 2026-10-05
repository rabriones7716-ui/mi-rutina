# Residuos del PCR de EC-L1147 (sección 5.1 del traspaso) · 6-oct-2026

**Qué se decide.** Si se instalan en `G:\Mi unidad\EC_L1147\Estudio\Entrega Final v4\` las dos versiones corregidas del PCR de EC-L1147.
**Qué cambia.** La conciliación del VAN ya no parte de una cifra retirada. Desaparecen las dos últimas menciones a «los canales de confiabilidad». La versión con control de cambios vuelve a dar exactamente la limpia al aceptar todo.
**Qué no cambia.** Ningún titular: VAN de 33.821.041,83 USD de 2015 al 12 %, TIR de 18,45 %, beneficio/costo de 1,4708, recuperación en 2027 y probabilidad de VAN negativo de 7,08 %.

**Glosario.**
- *Versión limpia*: `PCR_EC-L1147.docx`, sin revisiones; es la que lee el revisor del Banco.
- *Versión con control de cambios*: `PCR_EC-L1147 (con control de cambios).docx`; al aceptar todas sus revisiones debe dar la limpia.
- *Convención de facturación*: contar como beneficio toda la energía medida por la medición inteligente. Se declara y no se publica.

## 1. Archivos entregados

| Archivo | Base usada (Drive, «Entrega Final v4») | Resultado | Revisiones nuevas |
|---|---|---|---|
| `PCR_EC-L1147 (con control de cambios).docx` | SHA-256 3872D877…2C0F724C, la del traspaso | SHA-256 E8BE0ABB…7D77397A | 66: 58 de sincronización y 8 de la conciliación |
| `PCR_EC-L1147.docx` | SHA-256 86B86EAB…801F31D7, modificada 2 h después de la otra | SHA-256 75AAC1A7…758D65DB | Ninguna: es la versión limpia |

Los dos archivos van por la aplicación, no al repositorio, porque el PCR es de uso interno del Banco.

## 2. Cambios aplicados

### 2.1 Conciliación (sección II.3, párrafo que empezaba «Conciliación con el resultado ya publicado»)

| | Texto |
|---|---|
| **Antes** | Conciliación con el resultado ya publicado. El valor de USD 15.459.049,58, ya publicado, es el punto de partida: la contribución del canal de frecuencia (C2.1, dispositivos inteligentes en alimentadores, reconectadores) añade USD 20.415.038,67, y la del canal de duración (C2.2/C2.4, automatización y centros de control) añade USD 12.570.921,28, para un total de USD 48.445.009,55 con la convención de facturación de la medición inteligente (declarada). Con la medición inteligente valorada como transferencia (resultado publicado), el resultado baja en USD 14.623.967,71 hasta USD 33.821.041,83. |
| **Después** | Conciliación con la convención de facturación. Si toda la energía medida por la medición inteligente se contara como beneficio (convención de facturación del expediente, que se declara y no se publica), el VAN sería de USD 48.445.009,55 (dólares de 2015, al 12 %). La facturación recuperada por la medición inteligente es una transferencia de los usuarios a la distribuidora y no un beneficio, por lo que se restan USD 14.623.967,72. El resultado publicado es, por tanto, USD 48.445.009,55 − USD 14.623.967,72 = USD 33.821.041,83. Ese resultado incluye USD 32.985.959,95 de beneficios de confiabilidad en valor presente: USD 20.415.038,67 por la menor frecuencia de las interrupciones (C2.1, dispositivos inteligentes en alimentadores y reconectadores) y USD 12.570.921,28 por su menor duración (C2.2 y C2.4, automatización de subestaciones y centros de control). |

El resto del párrafo («Los dos beneficios de confiabilidad se valoran por contribución, no por atribución…») no cambia. Los 32.985.959,95 son el 31,2 % del valor presente de los beneficios del programa (105.651.015), como en `Mapa_Objetivos!H23`.

### 2.2 «Los canales de confiabilidad» → «los beneficios de confiabilidad»

| Lugar | Frase resultante |
|---|---|
| Sección II.3, párrafo de la descomposición por subcomponente | «…y, por contribución (no atribución), los beneficios de confiabilidad: frecuencia (C2.1, USD 20.415.039), automatización de subestaciones…» |
| Sección IV, fila «Incidencia distributiva» del cuadro de hallazgos | «…reparto no recalculado con los beneficios de confiabilidad.» |

En la versión con control de cambios cada frase aparecía dos veces: una en texto ya borrado por revisiones anteriores y otra visible. Por eso el traspaso hablaba de una «segunda aparición». Solo se cambió la visible.

### 2.3 Sincronización de la versión con control de cambios con la limpia

La limpia del Drive no es la que cita el traspaso y tenía cambios que no estaban registrados como revisiones: 27 párrafos distintos. Se tomó la limpia como texto final, porque es la más reciente y la que lee el revisor. Esos cambios se añadieron como revisiones a la otra versión. Son de cuatro tipos:
- referencias a hojas y celdas del libro retiradas del cuerpo, por ejemplo «Libro de Confiabilidad y VAN, Flujo_Anual, celda D24» o «AMI_Regla!C41»;
- en la sección final, «Datos a pedir a… distribuidoras… a la Unidad de Gestión del Programa» pasa a «Registro progresivo de datos conforme se entregan», en línea con la decisión de no enviar más pedidos;
- tres párrafos vacíos retirados tras la lista de enlaces electrónicos;
- dos párrafos unidos en la sección II.2, en el contrafactual físico del C1.1.

Van con el autor «Revisión 2026-10 – sincronización con la versión limpia». Los dos cambios de 2.1 y 2.2 van con el autor «Revisión 2026-10 – residuos de la conciliación». Para rechazar un grupo en Word: Revisar › Mostrar marcas › Personas, dejar marcado solo ese autor, y luego Rechazar › Rechazar todos los cambios mostrados.

## 3. Verificación y correcciones

| Comprobación | Resultado |
|---|---|
| XML de los dos documentos | Válido |
| Versión con control de cambios con todo aceptado frente a la limpia, párrafo por párrafo (1.403 párrafos) | Idénticas |
| Restos retirados en la limpia: 15.459.049, 14.623.967,71, «canales de confiabilidad», «resultado ya publicado», «lectura A/B», «sin canales», 12,18, 14,84, 53,09, 21,95, «B pleno», «B observado», referencias de celda | Cero |
| «0,84» en la limpia | Una vez: es el estadístico t (−0,84) del análisis contrafactual, no la lectura retirada |
| Resta y suma de la conciliación | 48.445.009,55 − 14.623.967,72 = 33.821.041,83; 20.415.038,67 + 12.570.921,28 = 32.985.959,95 |

Correcciones encontradas al trabajar, todas aplicadas:
1. El PCR restaba 14.623.967,71. Con las cifras mostradas la resta da 14.623.967,72, y ese es el valor que queda.
2. La limpia del Drive (86B86EAB…) no coincide con la del traspaso (2CD810D9…) y difería de la versión con control de cambios en 27 párrafos. Quedó sincronizada como se explica en 2.3.
3. Buscar las frases en el XML devolvía texto ya borrado por revisiones anteriores. La búsqueda se hizo sobre el texto visible.

## 4. Cómo instalarlo en tu PC

1. Copia los dos archivos actuales de la raíz de «Entrega Final v4» a `Soporte\Revisión 29092026\agentes\copias previas\PCR_antes_de_residuos_51_06102026\`. El Drive también guarda la versión anterior.
2. Sustitúyelos por los dos archivos entregados, con el mismo nombre.
3. Abre la versión con control de cambios en Word. Comprueba que abre sin avisos y revisa las revisiones de los dos autores nuevos.
4. Pega el bloque de la sección 5 al final de `Soporte\Registro de revisión 29092026.md`, en UTF-8 sin BOM.

## 5. Entrada para el registro

```
## 6-oct-2026 · PCR EC-L1147 · residuos de la conciliación y sincronización de versiones
- Conciliación (II.3): parte de la convención de facturación 48.445.009,55 y resta la facturación recuperada como transferencia 14.623.967,72 = 33.821.041,83 (USD de 2015, 12 %). Se retira 15.459.049,58. La resta antes decía 14.623.967,71.
- «los canales de confiabilidad» → «los beneficios de confiabilidad» en la descomposición por subcomponente (II.3) y en la fila «Incidencia distributiva» (IV).
- La versión limpia del Drive (SHA-256 86B86EAB…801F31D7) difería de la de control de cambios (3872D877…2C0F724C) en 27 párrafos sin revisión: referencias de hoja y celda retiradas del cuerpo, «Datos a pedir» → «Registro progresivo de datos», 3 párrafos vacíos y 2 párrafos unidos. Se añadieron como revisiones con el autor «Revisión 2026-10 – sincronización con la versión limpia».
- Autores nuevos: «Revisión 2026-10 – residuos de la conciliación» (8 revisiones) y el de sincronización (58). Marca de fecha de las revisiones: 2026-10-05 15:08, hora de Ecuador.
- Resultado: con control de cambios E8BE0ABB…7D77397A; limpio 75AAC1A7…758D65DB. Aceptado todo = limpio; restos retirados = 0. Ningún titular cambia.
```

## 6. Lo que queda de la sección 5.1

| Punto del traspaso | Estado | Qué hace falta |
|---|---|---|
| 1. Conciliación | Hecho | Revisar el texto de 2.1 |
| 2. «canales» → «beneficios» | Hecho | Nada |
| 3. Autoría de diez eliminaciones antiguas | No hecho | Solo si quieres rechazar por separado lo del 5-6 oct; requiere la copia `PCR_antes_de_B4_urgente_06102026` |
| 4. Segunda verificación | Hecha para esta ronda (sección 3) | Nada |
| 5. Pendientes de la ola 4 (renumeración ×48, costo del retraso, textos de método, figuras) | No hecho | La tabla de correspondencia de la renumeración y los textos de `agentes\B3_*` |
| 6. O&M de la medición inteligente | No hecho | Recalcular el Libro de Confiabilidad y VAN en Excel; cambia VAN, TIR y B/C en todo el paquete |

## 7. Sección 5.2 (anexos): supera el límite de 30 turnos

Hacer los anexos completos con las reglas de redacción no cabe en 30 turnos. Este trabajo usó unos 20 turnos para un solo documento en dos versiones, incluida la puesta a punto. Opciones:

| Opción | Qué incluye | Turnos estimados |
|---|---|---|
| **A. Coherencia numérica primero** | En los cinco anexos de Word, solo lo que contradice cifras: NOT1 (precio del canal: 0,0485 USD/kWh y 2,28 M, no 73,9), EEO9 (7,08 %), anexo económico (columna del Cuadro 24 y cita de `Léeme!B36/B37` en los cuadros 7.7 y D.1), anexo contrafactual («hoja hoja», 83,5 %, cuadros 10, 11 y 20). Además se comprueba en cada uno que la versión limpia coincide con la de control de cambios. EEO3 y EEO5 como guion de PowerShell para tu PC, porque hay que recalcular en Excel | 15-20 |
| B. Todo el punto 5.2 | A más las reglas de redacción en todos los anexos: apertura de tres frases, glosario y códigos fuera del cuerpo | 40 o más, en dos o tres sesiones |
| C. Solo diagnóstico | Comprobar en todos los anexos si la limpia y la de control de cambios coinciden, y listar los restos retirados sin corregir nada | 5 |

**Recomendación.** La opción A, en una sesión nueva que empiece con el traspaso y este archivo, porque esta conversación arrastra mucho contexto y encarece cada turno. Lo que A deja fuera (redacción) cambia la forma, no las cifras que mira el revisor.
