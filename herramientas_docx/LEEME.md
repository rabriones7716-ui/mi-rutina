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
