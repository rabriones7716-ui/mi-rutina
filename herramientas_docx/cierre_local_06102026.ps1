# cierre_local_06102026.ps1 · EC-L1147 · cierre local del 6-oct-2026
# Hace cuatro cosas, sin Excel, sin Word y sin inteligencia artificial:
#   1. Huellas SHA-256 de los tres libros y aviso si hay otra copia del Libro de Confiabilidad y VAN modificada hoy.
#   2. Barrido de cifras viejas en los demás Excel de la entrega (solo lista; no cambia nada).
#   3. Entradas del 6-oct en Soporte\Registro de revisión 29092026.md (UTF-8 sin BOM; no duplica las que ya existan).
#   4. Memo de armonización: sustituye las cifras del EEO5 que cambiaron y añade una nota fechada.
# Ejecutar:  powershell -ExecutionPolicy Bypass -File "<ruta>\cierre_local_06102026.ps1"
# Opciones:  -SinRegistro  -SinMemo  (para omitir los puntos 3 o 4)
# Antes de cambiar el registro o el memo guarda una copia en Soporte\copias previas\.
param(
  [string]$Raiz = 'G:\Mi unidad\EC_L1147\Estudio\Entrega Final v4',
  [switch]$SinRegistro,
  [switch]$SinMemo
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
$utf8sinBom = New-Object System.Text.UTF8Encoding($false)
$hoy = '2026-10-06'
$dirRev = Join-Path $Raiz 'Soporte\Revisión 29092026'
$dirInf = Join-Path $dirRev 'agentes'
if (-not (Test-Path $dirInf)) { $dirInf = $Raiz }
$dirCopias = Join-Path $Raiz 'Soporte\copias previas'
if (-not (Test-Path $dirCopias)) { New-Item -ItemType Directory -Path $dirCopias | Out-Null }
$informe = Join-Path $dirInf 'cierre_local_20261006.txt'
$csv     = Join-Path $dirInf 'barrido_cifras_viejas_20261006.csv'
$L = New-Object System.Collections.Generic.List[string]
function Out([string]$s) { $script:L.Add($s); Write-Host $s }
function Hash-Compartido([string]$p) {
  $fs = [System.IO.File]::Open($p, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
  try { $sha = [System.Security.Cryptography.SHA256]::Create(); (($sha.ComputeHash($fs)) | ForEach-Object { $_.ToString('X2') }) -join '' }
  finally { $fs.Dispose() }
}
function Leer-Entrada($zip, [string]$nombre) {
  $e = $zip.GetEntry($nombre); if ($null -eq $e) { return '' }
  $sr = New-Object System.IO.StreamReader($e.Open()); try { $sr.ReadToEnd() } finally { $sr.Dispose() }
}
function Decodificar([string]$s) { [System.Net.WebUtility]::HtmlDecode($s) }
function Fin-De-Linea([string]$t) { if ($t.Contains("`r`n")) { "`r`n" } else { "`n" } }

Out "EC-L1147 · cierre local · $hoy"
Out "Raíz: $Raiz"
Out ''
# ---------------------------------------------------------------- 1. Huellas
Out '1. HUELLAS SHA-256 (los libros deben estar guardados en Excel)'
$libros = @('Libro_Confiabilidad_VAN_EC-L1147.xlsx', 'Libro_Analisis_EC-L1147.xlsx', 'Modulos_Satelite\Modulo_Perdidas_Tecnicas_C1.1_C1.2_EC-L1147.xlsx')
$rutaEEO5 = ''; $hashEEO5 = ''; $fechaEEO5 = ''
foreach ($rel in $libros) {
  $p = Join-Path $Raiz $rel
  if (Test-Path $p) {
    $fi = Get-Item $p; $h = Hash-Compartido $p
    Out ('   {0}' -f $rel)
    Out ('      {0} bytes · modificado {1} · SHA-256 {2}' -f $fi.Length, $fi.LastWriteTime.ToString('yyyy-MM-dd HH:mm'), $h)
    if ($rel -like 'Libro_Confiabilidad*') { $rutaEEO5 = $p; $hashEEO5 = $h; $fechaEEO5 = $fi.LastWriteTime.ToString('yyyy-MM-dd HH:mm') }
  } else { Out "   NO ENCONTRADO: $rel" }
}
Out '   Otras copias del Libro de Confiabilidad y VAN modificadas hoy (si la sesión de Excel editó una copia, hay que instalarla con _scripts\swap_eeo5_eeo12.ps1):'
$otras = Get-ChildItem -Path $Raiz -Recurse -Filter 'Libro_Confiabilidad_VAN_EC-L1147*.xlsx' -ErrorAction SilentlyContinue |
  Where-Object { $_.FullName -ne $rutaEEO5 -and $_.LastWriteTime.Date -eq (Get-Date).Date }
if ($otras) { foreach ($o in $otras) { Out ('   · {0} · {1} · {2}' -f $o.FullName.Substring($Raiz.Length + 1), $o.LastWriteTime.ToString('HH:mm'), (Hash-Compartido $o.FullName).Substring(0, 8)) } }
else { Out '   · ninguna: el libro editado es el de la raíz' }

# ---------------------------------------------------------------- 2. Barrido
Out ''
Out '2. BARRIDO DE CIFRAS VIEJAS EN LOS DEMÁS LIBROS (solo lista; no cambia nada)'
$patTexto   = '33\.821\.04\d|33,82\d? ?M|33,82 millones|18,45 ?%|18,4456|1,4708|48\.445\.0\d\d|48,45 ?M|15\.459\.0\d\d|15,46 ?M|835\.08\d|7,08 ?%|3,45 ?[¢c]|6,06 ?%|40,39|20,40|5,85 ?%|1,283|15,13 ?M|15,07 ?%|0,82 ?[¢c]|29,1 ?M|18,8 ?M|0,6238|62,4 ?%'
$patFormula = '33821041|15459049|48445009|835081\.8|20400784'
$numObj = @(
  @(33821041.83, 0.5, 'VAN publicado'), @(15459049.58, 0.5, 'convención sin beneficios de confiabilidad'),
  @(48445009.55, 0.5, 'convención de facturación'), @(835081.88, 0.5, 'publicado sin beneficios de confiabilidad'),
  @(20400784.91, 0.5, 'carbono'), @(1.4708486, 0.00005, 'B/C'), @(0.184456, 0.00005, 'TIR'), @(0.0708, 0.00005, 'P(VAN<0)'), @(1.283, 0.0005, 'MCPF')
)
$archivos = @()
$archivos += Get-ChildItem -Path $Raiz -Filter '*.xlsx' | Where-Object { $_.Name -notlike 'Libro_Confiabilidad*' -and $_.Name -notlike '~$*' }
$dirSat = Join-Path $Raiz 'Modulos_Satelite'
if (Test-Path $dirSat) { $archivos += Get-ChildItem -Path $dirSat -Filter '*.xlsx' | Where-Object { $_.Name -notlike '~$*' } }
$b8 = Join-Path $dirRev 'Bloque8b\Bloque8b_Cierre_LecturaUnificada.xlsx'
if (Test-Path $b8) { $archivos += Get-Item $b8 }
$filas = New-Object System.Collections.Generic.List[string]; $filas.Add('archivo;hoja;celda;tipo;contenido')
$SL = [System.Text.RegularExpressions.RegexOptions]::Singleline
foreach ($f in $archivos) {
  $n = 0
  $zip = [System.IO.Compression.ZipFile]::OpenRead($f.FullName)
  try {
    $wb = Leer-Entrada $zip 'xl/workbook.xml'; $rels = Leer-Entrada $zip 'xl/_rels/workbook.xml.rels'
    $mapa = @{}
    foreach ($m in [regex]::Matches($wb, '<sheet\b[^>]*?name="([^"]*)"[^>]*?r:id="([^"]*)"')) {
      $rid = $m.Groups[2].Value; $nombre = Decodificar $m.Groups[1].Value
      $r = [regex]::Match($rels, '<Relationship\b[^>]*?Id="' + [regex]::Escape($rid) + '"[^>]*?Target="([^"]*)"')
      if (-not $r.Success) { $r = [regex]::Match($rels, '<Relationship\b[^>]*?Target="([^"]*)"[^>]*?Id="' + [regex]::Escape($rid) + '"') }
      if ($r.Success) { $t = $r.Groups[1].Value; if ($t.StartsWith('/')) { $t = $t.Substring(1) } else { $t = 'xl/' + $t }; $mapa[$t] = $nombre }
    }
    $ss = @(); $xs = Leer-Entrada $zip 'xl/sharedStrings.xml'
    if ($xs -ne '') { $ss = @([regex]::Matches($xs, '<si>(.*?)</si>', $SL) | ForEach-Object { Decodificar ([regex]::Replace($_.Groups[1].Value, '<[^>]+>', '')) }) }
    $idxHit = @{}; for ($i = 0; $i -lt $ss.Count; $i++) { if ($ss[$i] -match $patTexto) { $idxHit[$i] = $true } }
    foreach ($e in $zip.Entries) {
      if ($e.FullName -notlike 'xl/worksheets/sheet*.xml') { continue }
      $hoja = if ($mapa.ContainsKey($e.FullName)) { $mapa[$e.FullName] } else { $e.FullName }
      $x = Leer-Entrada $zip $e.FullName
      foreach ($c in [regex]::Matches($x, '<c r="([A-Z]+\d+)"([^>]*?)(?:/>|>(.*?)</c>)', $SL)) {
        $cuerpo = $c.Groups[3].Value; if ($cuerpo -eq '') { continue }
        $ref = $c.Groups[1].Value; $attr = $c.Groups[2].Value; $tipo = ''; $texto = ''
        if ($attr -match '\bt="s"') {
          $v = [regex]::Match($cuerpo, '<v>(\d+)</v>')
          if ($v.Success -and $idxHit.ContainsKey([int]$v.Groups[1].Value)) { $tipo = 'texto'; $texto = $ss[[int]$v.Groups[1].Value] }
        } elseif ($attr -match '\bt="inlineStr"' -or $attr -match '\bt="str"') {
          $t = Decodificar ([regex]::Replace($cuerpo, '<[^>]+>', ''))
          if ($t -match $patTexto) { $tipo = 'texto'; $texto = $t }
        } else {
          $fm = [regex]::Match($cuerpo, '<f[^>]*>(.*?)</f>', $SL); $vm = [regex]::Match($cuerpo, '<v>(.*?)</v>')
          if ($fm.Success -and $fm.Groups[1].Value -match $patFormula) { $tipo = 'fórmula con literal'; $texto = '=' + (Decodificar $fm.Groups[1].Value) }
          elseif ($vm.Success) {
            $d = 0.0
            if ([double]::TryParse($vm.Groups[1].Value, [System.Globalization.NumberStyles]::Float, [System.Globalization.CultureInfo]::InvariantCulture, [ref]$d)) {
              foreach ($o in $numObj) { if ([math]::Abs($d - $o[0]) -le $o[1]) { $tipo = 'número (' + $o[2] + ')'; $texto = $vm.Groups[1].Value; break } }
            }
          }
        }
        if ($tipo -ne '') {
          $n++; $t2 = ($texto -replace '[\r\n;]', ' '); if ($t2.Length -gt 160) { $t2 = $t2.Substring(0, 160) + '…' }
          $filas.Add(('{0};{1};{2};{3};{4}' -f $f.Name, $hoja, $ref, $tipo, $t2))
        }
      }
    }
  } finally { $zip.Dispose() }
  Out ('   {0}: {1} celdas' -f $f.Name, $n)
}
[System.IO.File]::WriteAllLines($csv, $filas, $utf8sinBom)
Out "   Detalle por celda: $csv"

# ---------------------------------------------------------------- 3. Registro
Out ''
Out '3. REGISTRO DE REVISIÓN'
$reg = Join-Path $Raiz 'Soporte\Registro de revisión 29092026.md'
if ($SinRegistro -or -not (Test-Path $reg)) { Out "   omitido ($reg)" }
else {
  Copy-Item $reg (Join-Path $dirCopias 'Registro de revisión 29092026_antes_cierre_20261006.md') -Force
  $txt = [System.IO.File]::ReadAllText($reg, [System.Text.Encoding]::UTF8); $eol = Fin-De-Linea $txt
  $entradas = @(
    @('## 6-oct-2026 · PCR EC-L1147 · residuos de la conciliación y sincronización de versiones', @'
## 6-oct-2026 · PCR EC-L1147 · residuos de la conciliación y sincronización de versiones
- Conciliación (II.3): parte de la convención de facturación 48.445.009,55 y resta la facturación recuperada como transferencia 14.623.967,72 = 33.821.041,83 (USD de 2015, 12 %). Se retira 15.459.049,58. La resta antes decía 14.623.967,71.
- «los canales de confiabilidad» → «los beneficios de confiabilidad» en la descomposición por subcomponente (II.3) y en la fila «Incidencia distributiva» (IV).
- La versión limpia del Drive (SHA-256 86B86EAB…801F31D7) difería de la de control de cambios (3872D877…2C0F724C) en 27 párrafos sin revisión. Se añadieron como revisiones con el autor «Revisión 2026-10 – sincronización con la versión limpia».
- Autores nuevos: «Revisión 2026-10 – residuos de la conciliación» (8 revisiones) y el de sincronización (58).
- Resultado: con control de cambios E8BE0ABB…7D77397A; limpio 75AAC1A7…758D65DB. Aceptado todo = limpio. Ningún titular cambia.
'@),
    @('## 2026-10-05 · Lote 1 de anexos de EC-L1147 en versión final', @'
## 2026-10-05 · Lote 1 de anexos de EC-L1147 en versión final
Autor de las revisiones: «Revisión 2026-10 – versión final». Ninguna cifra titular cambia.
- Anexo_Flujos_Economicos_Financieros_EC-L1147: 38 párrafos; 110 inserciones y 168 eliminaciones. Lecturas en palabras; Montecarlo de MC_B (7,08 %); tres fragilidades y frase de la medición inteligente en el resumen; conciliación 48.445.009,55 − 14.623.967,72 = 33.821.041,83 USD; columnas sin beneficios de confiabilidad retiradas de la tabla por objetivo; Figura 2 sustituida; rango del tope térmico en el satélite del C1.1; dos comentarios internos resueltos. Limpio 9088C6F6, con control de cambios B0CDF225.
- Nota_Metodologica_Perdidas_Tecnicas_C1.1_C1.2_EC-L1147: precio del canal sellado a 0,0485 USD/kWh (2,28 MUS$); comparación económica 1.907.981 frente a 1.559.394 USD (−18,3 %); tope térmico como rango; supuestos del C1.2 como rango declarado. Limpio 94294BA8, con control de cambios AFB1B8A7.
- Nota_Metodologica_C1.2_Con_Red_y_Sin_Red_EC-L1147: sección 6 de solicitud de datos retirada; Limitaciones pasa a ser la sección 6; cinco remisiones cerradas con «no disponible al cierre». Limpio 53287FF6, con control de cambios 0EBB4355.
'@),
    @('## 2026-10-06 · Libros de Excel de EC-L1147', @'
## 2026-10-06 · Libros de Excel de EC-L1147
- Libro_Analisis_EC-L1147: C3_Capacitación!C23:C24 a 1.999 y 22 %, con sus notas D23:D24; Flujo_Programa!A38, A39, A42 y A43 rotulados «lectura interna, no publicada». VAN del modelo histórico 37.149.045,26 (antes 36.903.956,23). SHA 3AB4C505.
- Modulo_Perdidas_Tecnicas_C1.1_C1.2_EC-L1147: Puente!A2 y K5 con el precio de 0,0485 USD/kWh; E5 =D5 (1.907.981,44); J5 =(G5/E5-1)*100 (−18,27). SHA 96F2DDF3.
'@),
    @('## 2026-10-06 · Libro de Confiabilidad y VAN (EEO5): O&M de la medición inteligente en el titular', @'
## 2026-10-06 · Libro de Confiabilidad y VAN (EEO5): O&M de la medición inteligente en el titular
Decisión del usuario del 5-oct-2026, aplicada desde la sesión de Excel el 6-oct-2026. Primer cambio del titular.
- Regla: 2,5 % anual del CAPEX total del C2.3 desde 2023 (tasa de las redes de distribución); el piloto de 2017 no se cobra en 2017-2022 (omisión declarada, unos 0,03 M). Parámetro Motor_B!B43; vector Motor_B!B50:B80; VP −719.654,04. Entra por MC_Riesgo!F32:F62 y llega por fórmula a Flujo_Anual, MB_OPEX, MC_B y VAN_Financiero. Parámetros!D7 sin cambio.
- Titular: VAN 33.821.041,83 → 33.101.387,79 USD de 2015 al 12 %; B/C 1,4708 → 1,4563; TIR 18,45 % → 18,34 %; recuperación 2027. Convención de facturación 48.445.009,55 → 47.725.355,51. Lecturas internas sin beneficios de confiabilidad: 15.459.049,58 → 14.739.395,54 y 835.081,88 → 115.427,84.
- Montecarlo: 9.900 de las 10.000 filas de MC_B y MC_B_Replica eran valores pegados; se reanimaron con las fórmulas del motor (con el parámetro en cero se reproducen la media y el 7,08 % anteriores). Resultado publicado: P(VAN<0) 7,08 % → 7,70 %; media 27.750.938,52; P5 −3.350.330,90; P50 26.136.708,54; P95 64.768.867,88.
- Fragilidades y umbrales: carbono −21.120.438,95 y TIR 5,50 %, el 61,05 % de la senda lo anula; MCPF 1,2770; factor 0,4145: 14.410.321,66 y 14,95 %; umbrales 3,57 ¢/kWh, 6,25 %, 41,66 %, 1,1124 GWh/MVA-año. Sostenibilidad S0 a S3: 33,10 / 28,40 / 17,97 / 7,02 M.
- VAN_Financiero: O&M de las distribuidoras −13.871.373,83; la identidad contable cierra.
- Controles con literales sustituidos por referencias vivas (VAN_Programa!G19:G20, Parámetros!B92); controles rebasados según Control_Cambios!A497 en adelante. Rótulos: AMI_Regla!A48 (frase de la medición inteligente) y A1 restituido; VAN_Programa!A112 (C2.2 y C2.4 se leen juntos: 3.561.563); Coincidencia_Docs!A8 y F8 «lectura interna, no publicada», E15 «PCR, EEO4, EEO9».
- Archivo: {RUTA_EEO5}; SHA-256 {HASH_EEO5}; modificado {FECHA_EEO5}.
- Pendiente: pase de cifras en el PCR y los anexos; Coincidencia_Docs!B15 y demás citas de los documentos después de ese pase.
'@)
  )
  foreach ($e in $entradas) {
    if ($txt.Contains($e[0])) { Out ('   ya estaba: ' + $e[0]); continue }
    $bloque = $e[1].Replace('{RUTA_EEO5}', $rutaEEO5).Replace('{HASH_EEO5}', $hashEEO5).Replace('{FECHA_EEO5}', $fechaEEO5)
    $bloque = [regex]::Replace($bloque.Trim(), "`r?`n", $eol)
    if (-not $txt.EndsWith("`n")) { $txt += $eol }
    $txt += $eol + $bloque + $eol
    Out ('   añadida: ' + $e[0])
  }
  [System.IO.File]::WriteAllText($reg, $txt, $utf8sinBom)
  Out '   guardado en UTF-8 sin BOM; copia previa en Soporte\copias previas\'
}

# ---------------------------------------------------------------- 4. Memo
Out ''
Out '4. MEMO DE ARMONIZACIÓN'
$memo = Join-Path $Raiz 'Soporte\Memo de armonización EC-L1147 y EC-L1160_29092026.md'
if ($SinMemo -or -not (Test-Path $memo)) { Out "   omitido ($memo)" }
else {
  Copy-Item $memo (Join-Path $dirCopias 'Memo de armonización_antes_cierre_20261006.md') -Force
  $t = [System.IO.File]::ReadAllText($memo, [System.Text.Encoding]::UTF8); $eol = Fin-De-Linea $t
  if ($t.Contains('## Nota del 6-oct-2026')) { Out '   la nota del 6-oct ya estaba; no se repite nada' }
  else {
    $cambios = [ordered]@{
      '33.821.041,83' = '33.101.387,79'; '33,82 M' = '33,10 M'; '18,4456 %' = '18,3421 %'; '18,45 %' = '18,34 %'; '1,4708' = '1,4563'
      '48.445.009,55' = '47.725.355,51'; '48,45 M' = '47,73 M'; '7,08 %' = '7,70 %'
      '1,2830' = '1,2770'; '1,283' = '1,277'
      '−20.400.784,91' = '−21.120.438,95'; '-20.400.784,91' = '-21.120.438,95'; '−20,40 M' = '−21,12 M'; '-20,40 M' = '-21,12 M'
      '5,85 %' = '5,50 %'; '0,6238' = '0,6105'; '62,4 %' = '61,1 %'
      '15,13 M' = '14,41 M'; '15,07 %' = '14,95 %'; '15.459.049,58' = '14.739.395,54'; '835.081,88' = '115.427,84'
    }
    $lineas = $t -split "`r?`n"
    foreach ($k in $cambios.Keys) {
      $hits = @(); for ($i = 0; $i -lt $lineas.Count; $i++) { if ($lineas[$i].Contains($k)) { $hits += ($i + 1) } }
      if ($hits.Count -gt 0) { Out ('   «{0}» → «{1}» en las líneas {2}' -f $k, $cambios[$k], ($hits -join ', ')); $t = $t.Replace($k, $cambios[$k]) }
    }
    $nota = @'
## Nota del 6-oct-2026 · EC-L1147: O&M de la medición inteligente en el titular
Por decisión del usuario del 5-oct-2026, el titular de EC-L1147 incluye el O&M de la medición inteligente al 2,5 % anual del CAPEX, la tasa de las redes de distribución. VAN 33.101.387,79 USD de 2015 al 12 % (antes 33.821.041,83); TIR 18,34 %; B/C 1,4563; probabilidad de VAN negativo 7,70 %. Las celdas del Libro de Confiabilidad y VAN citadas en este memo se actualizaron a esa base: MCPF_ObsProy!E18 1,2770; Carbono_B!D95 −21.120.438,95, F95 5,50 % e I95 0,6105; CENS_ENS!D213 14.410.321,66 y F213 14,95 %. Los parámetros comunes con EC-L1160 no cambian.
'@
    $nota = [regex]::Replace($nota.Trim(), "`r?`n", $eol)
    if (-not $t.EndsWith("`n")) { $t += $eol }
    $t += $eol + $nota + $eol
    [System.IO.File]::WriteAllText($memo, $t, $utf8sinBom)
    Out '   nota del 6-oct añadida; guardado en UTF-8 sin BOM; copia previa en Soporte\copias previas\'
    $lineas = $t -split "`r?`n"; $patRev = '20,40|62 %|5,85|15,13|15,07|33,82|18,45|7,08|1,283|0,6238'
    $rev = @(); for ($i = 0; $i -lt $lineas.Count; $i++) { if ($lineas[$i] -match $patRev -and -not $lineas[$i].Contains('antes 33.821.041,83')) { $rev += ('      línea {0}: {1}' -f ($i + 1), $lineas[$i].Substring(0, [math]::Min(140, $lineas[$i].Length))) } }
    if ($rev.Count -gt 0) { Out '   Líneas que aún contienen cifras viejas, para revisar a mano:'; foreach ($r in $rev) { Out $r } }
    else { Out '   no quedan cifras viejas en el memo' }
  }
}

Out ''
Out "Informe guardado en: $informe"
Out 'Pegue el contenido de este informe en la sesión de la nube y adjunte el CSV del barrido.'
[System.IO.File]::WriteAllLines($informe, $L, $utf8sinBom)
