# Herramientas de edición de Word con control de cambios

Estas cuatro piezas de Python editan archivos .docx con control de cambios, sin Word y sin lxml.
La versión limpia se genera aceptando todos los cambios, y se verifica que coincide con la versión con control de cambios aceptada.
No contienen texto de los documentos del BID.

| Archivo | Qué hace |
|---|---|
| `lib51.py` | Lee párrafos, texto visible y secuencia aceptada. |
| `edit51.py` | Reemplaza texto con `w:ins` y `w:del`, y borra marcas de párrafo. |
| `ops51.py` | Acepta todos los cambios, quita comentarios y escribe el .docx. |
| `fin51.py` | Edita párrafos por diferencia de palabras, borra párrafos y filas, e inserta filas nuevas. |

Uso básico:

```python
import zipfile
from edit51 import Ctx
from fin51 import set_text, del_para, del_row
from ops51 import accept_all
z = zipfile.ZipFile('documento.docx'); x = z.read('word/document.xml').decode('utf8'); ctx = Ctx(z, x)
x = set_text(x, ctx, 11, 'Texto nuevo del párrafo 11.')   # índice de párrafo en bruto
limpio, uniones, fallos = accept_all(x)
```

## Pases del 6-oct (PCR y anexo de flujos)

- `pcr_edit.py`: pase editorial del PCR (Tabla 1A, Tablas 3A a 3D, tabla de la sección IV, códigos en palabras). Insumo: la versión con control de cambios del pase mecánico.
- `eeo9_pass.py` y `eeo9_fig.py`: pase corto del anexo de flujos económicos y financieros (Figuras 3, 4 y 11; frase que lee juntos C2.2 y C2.4; celda de la tabla de canales).
- `passlib.py`: `save2` acepta en la versión limpia las revisiones que traigan notas al pie, notas finales, encabezados y pies; `accept_aux(ruta)` hace lo mismo sobre un docx ya guardado; `set_media(rótulo, png, min_idx)` admite documentos cortos.
- `xlsx_xml.py`: edición mínima de libros xlsx a nivel de XML (celda, fórmula, texto en línea; filas nuevas; `fullCalcOnLoad`), conserva gráficos y comentarios. `anexos_pass.py`: pase del 6-oct sobre EEO1, EEO6, Sustento_AMI y Escenario_Macro_C23 (verificación con copias recalculadas en LibreOffice).
