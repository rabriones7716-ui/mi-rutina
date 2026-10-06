# exportar_eeo5_06102026.ps1 · EC-L1147 · exporta celdas del Libro de Confiabilidad y VAN a un archivo de texto
# Lee el .xlsx guardado directamente del disco (sin Excel, sin inteligencia artificial) y escribe hoja, celda y valor
# de las celdas listadas, más los percentiles del Montecarlo. No modifica el libro.
# Ejecutar:  powershell -ExecutionPolicy Bypass -File "<ruta>\exportar_eeo5_06102026.ps1"
param(
  [string]$Libro  = 'G:\Mi unidad\EC_L1147\Estudio\Entrega Final v4\Libro_Confiabilidad_VAN_EC-L1147.xlsx',
  [string]$Salida = '',
  [string]$Lista  = '',
  [string[]]$MCHojas = @('MC_B', 'MC_B_Replica'),
  [string]$MCCol = 'AV', [int]$MCR1 = 20, [int]$MCR2 = 10019
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
$cult = [System.Globalization.CultureInfo]::InvariantCulture
$utf8sinBom = New-Object System.Text.UTF8Encoding($false)
if ($Salida -eq '') {
  $raiz = Split-Path $Libro
  $dir = Join-Path $raiz 'Soporte\Revisión 29092026\agentes'
  if (-not (Test-Path $dir)) { $dir = $raiz }
  $Salida = Join-Path $dir 'export_eeo5_20261006.txt'
}
$listaTexto = @'
Flujo_Anual: A1:V70
AMI_Regla: A1:H50
VAN_Programa: A1:K30, A110:A114
Brecha_Tarifaria: A1:J60
Sostenibilidad_Tasa: A20:F30, A48:F64, A82:F95
MC_B: A1:H20, M3:Z10, AJ10:AJ20
MC_B_Replica: A1:H20, M3:Z10
Carbono_B: A36:L40, A93:P106, R100:T104
Matriz_Estructural: A15:F32, DG15:DP24, DG34:DJ46, DG73:DG76, A137:F152, X183:Z187
Motor_B: A38:H50, A80:H97
MCPF_ObsProy: A15:F30, A39:D46, A50:I60, A100:D105
VAN_Financiero: A1:D30, A45:D60, A70:D80, A130:D166
CENS_ENS: A68:F76, A150:I160, A160:F166, A188:J216, A216:D226
Umbrales_B: A38:G72, A100:G150
Precios_Sociales: A40:F46
Perdidas_ST: A15:H30
Amenazas_Grados: A30:F38, A93:F97
Precio_Energia: A5:D14, A86:D99
Reparto_L1160: A5:L14, A29:L35, A69:L75, A86:L90
Retraso_B: A40:I60
ExAnte_ExPost: A14:G24, A35:C44, A69:J73
Canales_Canonica: A5:S26, A30:M44, A50:K66, A79:F87
Sensibilizador_B: DU7:DW30, DU52:DW76, DS136:DT140
AMI_Sens: A1:H35, A40:F80
AMI_Delta: A4:D16
Léeme: A1:F100
Coincidencia_Docs: A1:G90
Parámetros: A88:F94
Mapa_Objetivos: A18:K30
Control_Cambios: A490:F530
Verificación: A1:H120
Verificacion: A1:H120
Parametros: A88:F94
Leeme: A1:F100
'@
if ($Lista -ne '') { $listaTexto = [System.IO.File]::ReadAllText($Lista, [System.Text.Encoding]::UTF8) }
function Col-Num([string]$s) { $n = 0; foreach ($ch in $s.ToCharArray()) { $n = $n * 26 + ([int][char]$ch - 64) }; $n }
function Parse-Ref([string]$r) { $m = [regex]::Match($r, '^([A-Z]+)(\d+)$'); @{ c = (Col-Num $m.Groups[1].Value); r = [int]$m.Groups[2].Value } }
$quiero = [ordered]@{}
foreach ($linea in ($listaTexto -split "`r?`n")) {
  if ($linea.Trim() -eq '') { continue }
  $p = $linea.IndexOf(':'); $hoja = $linea.Substring(0, $p).Trim(); $rects = @()
  foreach ($ref in ($linea.Substring($p + 1) -split ',')) {
    $ref = $ref.Trim().ToUpper(); if ($ref -eq '') { continue }
    if ($ref -match '^([A-Z]+\d+):([A-Z]+\d+)$') { $a = Parse-Ref $matches[1]; $b = Parse-Ref $matches[2]; $rects += , @([math]::Min($a.c, $b.c), [math]::Min($a.r, $b.r), [math]::Max($a.c, $b.c), [math]::Max($a.r, $b.r)) }
    elseif ($ref -match '^[A-Z]+\d+$') { $a = Parse-Ref $ref; $rects += , @($a.c, $a.r, $a.c, $a.r) }
  }
  $quiero[$hoja] = $rects
}
foreach ($h in $MCHojas) { if (-not $quiero.Contains($h)) { $quiero[$h] = @() } }
$mcColNum = Col-Num $MCCol

$fs = [System.IO.File]::Open($Libro, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
$sha = ([System.Security.Cryptography.SHA256]::Create().ComputeHash($fs) | ForEach-Object { $_.ToString('X2') }) -join ''
$fs.Dispose()
$fi = Get-Item $Libro
$out = New-Object System.Collections.Generic.List[string]
$out.Add("# Libro`t$Libro")
$out.Add(("# Bytes`t{0}`t# Modificado`t{1}`t# SHA-256`t{2}" -f $fi.Length, $fi.LastWriteTime.ToString('yyyy-MM-dd HH:mm'), $sha))
$out.Add("hoja`tcelda`tvalor")
Write-Host "Libro: $Libro"; Write-Host "SHA-256: $sha"

$zip = [System.IO.Compression.ZipFile]::OpenRead($Libro)
try {
  function Leer([string]$nombre) { $e = $zip.GetEntry($nombre); if ($null -eq $e) { return '' }; $sr = New-Object System.IO.StreamReader($e.Open()); try { $sr.ReadToEnd() } finally { $sr.Dispose() } }
  $wb = Leer 'xl/workbook.xml'; $rels = Leer 'xl/_rels/workbook.xml.rels'
  $mapa = @{}
  foreach ($m in [regex]::Matches($wb, '<sheet\b[^>]*?name="([^"]*)"[^>]*?r:id="([^"]*)"')) {
    $nombre = [System.Net.WebUtility]::HtmlDecode($m.Groups[1].Value); $rid = $m.Groups[2].Value
    $r = [regex]::Match($rels, '<Relationship\b[^>]*?Id="' + [regex]::Escape($rid) + '"[^>]*?Target="([^"]*)"')
    if (-not $r.Success) { $r = [regex]::Match($rels, '<Relationship\b[^>]*?Target="([^"]*)"[^>]*?Id="' + [regex]::Escape($rid) + '"') }
    if ($r.Success) { $t = $r.Groups[1].Value; if ($t.StartsWith('/')) { $t = $t.Substring(1) } else { $t = 'xl/' + $t }; $mapa[$nombre] = $t }
  }
  # cadenas compartidas
  $ss = New-Object System.Collections.Generic.List[string]
  $e = $zip.GetEntry('xl/sharedStrings.xml')
  if ($e) {
    $xr = [System.Xml.XmlReader]::Create($e.Open()); $sb = $null; $inT = $false; $pend = $false
    while ($true) {
      if ($pend) { $pend = $false } elseif (-not $xr.Read()) { break }
      if ($xr.EOF) { break }
      if ($xr.NodeType -eq [System.Xml.XmlNodeType]::Element) {
        if ($xr.LocalName -eq 'si') { $sb = New-Object System.Text.StringBuilder }
        elseif ($xr.LocalName -eq 't' -and $null -ne $sb) { $inT = -not $xr.IsEmptyElement }
        elseif ($xr.LocalName -eq 'rPh') { $xr.Skip(); $pend = $true; continue }
      } elseif ($xr.NodeType -eq [System.Xml.XmlNodeType]::Text -or $xr.NodeType -eq [System.Xml.XmlNodeType]::SignificantWhitespace -or $xr.NodeType -eq [System.Xml.XmlNodeType]::Whitespace) {
        if ($inT) { [void]$sb.Append($xr.Value) }
      } elseif ($xr.NodeType -eq [System.Xml.XmlNodeType]::EndElement) {
        if ($xr.LocalName -eq 't') { $inT = $false }
        elseif ($xr.LocalName -eq 'si') { $ss.Add($sb.ToString()); $sb = $null }
      }
    }
    $xr.Dispose()
  }
  Write-Host ("Cadenas compartidas: {0}" -f $ss.Count)
  foreach ($nombre in $quiero.Keys) {
    $rects = $quiero[$nombre]; $esMC = $MCHojas -contains $nombre
    if (-not $mapa.ContainsKey($nombre)) { $out.Add("$nombre`t(hoja no encontrada)`t"); Write-Host "   $nombre : NO ENCONTRADA"; continue }
    $e = $zip.GetEntry($mapa[$nombre]); $xr = [System.Xml.XmlReader]::Create($e.Open())
    $mcVals = New-Object System.Collections.Generic.List[double]
    $ref = ''; $tipo = ''; $want = $false; $esMCcelda = $false; $inV = $false; $inT = $false; $val = ''; $n = 0; $pend = $false
    while ($true) {
      if ($pend) { $pend = $false } elseif (-not $xr.Read()) { break }
      if ($xr.EOF) { break }
      $nt = $xr.NodeType
      if ($nt -eq [System.Xml.XmlNodeType]::Element) {
        $ln = $xr.LocalName
        if ($ln -eq 'c') {
          $ref = $xr.GetAttribute('r'); $tipo = $xr.GetAttribute('t'); $val = ''; $want = $false; $esMCcelda = $false
          $m = [regex]::Match($ref, '^([A-Z]+)(\d+)$'); $col = Col-Num $m.Groups[1].Value; $row = [int]$m.Groups[2].Value
          foreach ($rc in $rects) { if ($col -ge $rc[0] -and $col -le $rc[2] -and $row -ge $rc[1] -and $row -le $rc[3]) { $want = $true; break } }
          if ($esMC -and $col -eq $mcColNum -and $row -ge $MCR1 -and $row -le $MCR2) { $esMCcelda = $true }
          if ($xr.IsEmptyElement) { $ref = '' }
          elseif (-not $want -and -not $esMCcelda) { $xr.Skip(); $ref = ''; $pend = $true; continue }
        }
        elseif ($ln -eq 'v' -and $ref -ne '') { $inV = -not $xr.IsEmptyElement }
        elseif ($ln -eq 't' -and $ref -ne '' -and $tipo -eq 'inlineStr') { $inT = -not $xr.IsEmptyElement }
        elseif ($ln -eq 'f' -and $ref -ne '') { $xr.Skip(); $pend = $true; continue }
      } elseif ($nt -eq [System.Xml.XmlNodeType]::Text -or $nt -eq [System.Xml.XmlNodeType]::SignificantWhitespace -or $nt -eq [System.Xml.XmlNodeType]::Whitespace) {
        if ($inV -or $inT) { $val += $xr.Value }
      } elseif ($nt -eq [System.Xml.XmlNodeType]::EndElement) {
        $ln = $xr.LocalName
        if ($ln -eq 'v') { $inV = $false }
        elseif ($ln -eq 't') { $inT = $false }
        elseif ($ln -eq 'c' -and $ref -ne '') {
          $texto = $val
          if ($tipo -eq 's' -and $val -ne '') { $texto = $ss[[int]$val] }
          if ($want) { $n++; $out.Add(("{0}`t{1}`t{2}" -f $nombre, $ref, ($texto -replace '[\t\r\n]', ' '))) }
          if ($esMCcelda -and $tipo -ne 's' -and $tipo -ne 'str' -and $tipo -ne 'e' -and $val -ne '') { $d = 0.0; if ([double]::TryParse($val, [System.Globalization.NumberStyles]::Float, $cult, [ref]$d)) { $mcVals.Add($d) } }
          $ref = ''
        }
      }
    }
    $xr.Dispose()
    $msg = "   $nombre : $n celdas"
    if ($esMC -and $mcVals.Count -gt 0) {
      $arr = $mcVals.ToArray(); [System.Array]::Sort($arr); $N = $arr.Length
      $suma = 0.0; foreach ($v in $arr) { $suma += $v }; $media = $suma / $N
      $sq = 0.0; foreach ($v in $arr) { $sq += ($v - $media) * ($v - $media) }; $sd = [math]::Sqrt($sq / ($N - 1))
      $neg = 0; foreach ($v in $arr) { if ($v -lt 0) { $neg++ } }
      $out.Add(("{0}`tMC_n`t{1}" -f $nombre, $N)); $out.Add(("{0}`tMC_media`t{1}" -f $nombre, $media.ToString('F2', $cult))); $out.Add(("{0}`tMC_desv`t{1}" -f $nombre, $sd.ToString('F2', $cult)))
      $out.Add(("{0}`tMC_P(VAN<0)`t{1}" -f $nombre, ($neg / $N).ToString('F6', $cult))); $out.Add(("{0}`tMC_min`t{1}" -f $nombre, $arr[0].ToString('F2', $cult))); $out.Add(("{0}`tMC_max`t{1}" -f $nombre, $arr[$N - 1].ToString('F2', $cult)))
      for ($p = 1; $p -le 99; $p++) { $k = ($N - 1) * $p / 100.0; $f = [math]::Floor($k); $c = [math]::Min($f + 1, $N - 1); $v = $arr[$f] + ($k - $f) * ($arr[$c] - $arr[$f]); $out.Add(("{0}`tMC_P{1:D2}`t{2}" -f $nombre, $p, $v.ToString('F2', $cult))) }
      $msg += (" · Montecarlo: {0} valores, media {1}, P(VAN<0) {2}" -f $N, $media.ToString('F2', $cult), ($neg / $N).ToString('P2', $cult))
    }
    Write-Host $msg
  }
} finally { $zip.Dispose() }
[System.IO.File]::WriteAllLines($Salida, $out, $utf8sinBom)
Write-Host ''
Write-Host ("Exportación guardada en: {0} ({1} líneas). Suba este archivo a la sesión de la nube." -f $Salida, $out.Count)
