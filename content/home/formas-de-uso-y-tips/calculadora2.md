+++
title = "Calculadora isotónica"
description = "Calculadora isotónica RexMar"
date = "2026-09-12"
author = "legar"
aliases = ["/calc2"]
+++

<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Calculadora de isotonización con agua de mar RexMar</title>
<style>
  /* Forzamos esquema claro para que el tema oscuro del navegador no oculte texto */
  :root { color-scheme: light; }

  html, body {
    background: #ffffff !important;
    color: #1a1a1a !important;
  }

  body {
    font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
    max-width: 950px;
    margin: 2rem auto;
    padding: 0 1rem;
    line-height: 1.4;
  }

  h1 { font-size: 1.6rem; color: #111 !important; }

  .controles {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
    max-width: 320px;
  }

  label {
    display: block;
    font-weight: 600;
    margin-bottom: .25rem;
    color: #111 !important;
  }

  input {
    width: 100%;
    padding: .45rem .5rem;
    font-size: 1rem;
    background: #fff !important;
    color: #111 !important;
    border: 1px solid #bbb !important;
    border-radius: 4px;
  }

  button {
    padding: .6rem 1rem;
    font-size: 1rem;
    cursor: pointer;
    margin-right: .5rem;
    margin-bottom: .5rem;
    background: #f3f3f3;
    color: #111;
    border: 1px solid #999;
    border-radius: 4px;
  }

  button:hover { background: #e6e6e6; }

  .botones { margin: 1rem 0; }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
    background: #fff !important;
    color: #111 !important;
    border: 2px solid #222 !important; /* borde exterior grueso */
  }

  th, td {
    border: 1px solid #444 !important; /* bordes de filas y columnas bien marcados */
    padding: .5rem .6rem;
    text-align: right;
    color: #111 !important;
    background: #fff !important;
  }

  th {
    background: #e0e0e0 !important;
    text-align: center;
    font-weight: 700;
    border-bottom: 2px solid #222 !important; /* separa encabezado del cuerpo */
  }

  /* Bordes exteriores más gruesos en las celdas de los extremos */
  tr th:first-child, tr td:first-child {
    border-left: 2px solid #222 !important;
  }
  tr th:last-child, tr td:last-child {
    border-right: 2px solid #222 !important;
  }
  tbody tr:last-child td {
    border-bottom: 2px solid #222 !important;
  }

  td:first-child, th:first-child {
    text-align: center;
  }

  .nota {
    font-size: .95rem;
    color: #444 !important;
    margin-top: 1rem;
  }

  @media print {
    .no-print { display: none !important; }
    body { margin: 0; max-width: none; font-size: 11pt; }
    table { page-break-inside: auto; }
    tr { page-break-inside: avoid; page-break-after: auto; }
  }
</style>
</head>
<body>

<h1>Calculadora de isotonización con agua de mar RexMar</h1>

## Para ver y entender el porqué de ésta calculadora <a href="https://th.org.pe/home/formas-de-uso-y-tips/equilibrio-electrolitico-y-adm/" target="_blank">presione aquí</a>

## coloque el volumen en ML del recipiente que quiere usar para isotonizar

<div class="controles no-print">
  <div>
    <label for="volumen">Volumen de la taza (ml)</label>
    <input type="number" id="volumen" value="0" min="1" step="1">
  </div>
</div>

<div class="botones no-print" align="center">
  <button type="button" onclick="calcular()">Calcular</button>
  <button type="button" onclick="window.print()">Imprimir / Guardar como PDF</button>
  <button type="button" onclick="descargarPDF()">Descargar PDF</button>
</div>

<div id="resultado"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.8.2/jspdf.plugin.autotable.min.js"></script>
<script>
  // Parámetros fijos
  const PASO_PCT = 0.05;    // 0,05 % = 0,5 g/L
  const INICIO_PCT = 0.5;   // 0,5 % = 5 g/L
  const FIN_PCT = 1.55;     // 1,55 % = 15,5 g/L
  const SAL_MAR_G_L = 35;   // g/L fijos (no se muestra al público)

  let filasGlobales = [];

  function fmt(n, dec = 1) {
    return Number(n).toLocaleString('es-ES', {
      minimumFractionDigits: dec,
      maximumFractionDigits: dec
    });
  }

  function calcular() {
    const volumen = parseFloat(document.getElementById('volumen').value);

    if (!volumen || volumen <= 0) {
      document.getElementById('resultado').innerHTML = '<p>Ingresá un volumen válido.</p>';
      return;
    }

    const salMarina_g_ml = SAL_MAR_G_L / 1000;
    const pasos = Math.round((FIN_PCT - INICIO_PCT) / PASO_PCT);

    const filas = [];
    for (let i = 0; i <= pasos; i++) {
      const s = Math.round((INICIO_PCT + i * PASO_PCT) * 100) / 100;
      const gPorLitro = Math.round(s * 100) / 10;
      const salNecesaria = (s / 100) * volumen;
      const aguaMar = salNecesaria / salMarina_g_ml;
      const aguaComun = volumen - aguaMar;
      const salAportada = aguaMar * salMarina_g_ml;

      filas.push({
        salinidadGL: gPorLitro,
        aguaMar: aguaMar,
        aguaComun: aguaComun,
        salAportada: salAportada,
        volumenFinal: volumen
      });
    }

    filasGlobales = filas;

    // Estilos inline: ganan a cualquier CSS del tema
    const estiloTabla =
      'width:100%;border-collapse:collapse;margin-top:1rem;' +
      'background:#fff;color:#111;border:2px solid #222;';

    const estiloTh =
      'border:1px solid #444;padding:8px 10px;text-align:center;' +
      'background:#e0e0e0;color:#111;font-weight:700;' +
      'border-bottom:2px solid #222;';

    const estiloTd =
      'border:1px solid #444;padding:8px 10px;text-align:right;' +
      'background:#fff;color:#111;';

    const estiloTdCentrado =
      'border:1px solid #444;padding:8px 10px;text-align:center;' +
      'background:#fff;color:#111;';

    let html = '<table id="tablaResultados" style="' + estiloTabla + '">';
    html += '<thead><tr>';
    html += '<th style="' + estiloTh + '">Salinidad objetivo (g/L)</th>';
    html += '<th style="' + estiloTh + '">Agua de mar (ml)</th>';
    html += '<th style="' + estiloTh + '">Agua común (ml)</th>';
    html += '<th style="' + estiloTh + '">Sal aportada (g)</th>';
    html += '<th style="' + estiloTh + '">Volumen final (ml)</th>';
    html += '</tr></thead><tbody>';

    filas.forEach(f => {
      html += '<tr>';
      html += '<td style="' + estiloTdCentrado + '">' + fmt(f.salinidadGL, 1) + '</td>';
      html += '<td style="' + estiloTd + '">' + fmt(f.aguaMar, 1) + '</td>';
      html += '<td style="' + estiloTd + '">' + fmt(f.aguaComun, 1) + '</td>';
      html += '<td style="' + estiloTd + '">' + fmt(f.salAportada, 2) + '</td>';
      html += '<td style="' + estiloTd + '">' + fmt(f.volumenFinal, 0) + '</td>';
      html += '</tr>';
    });

    html += '</tbody></table>';
    html += '<p class="nota">Volumen de taza: ' + fmt(volumen, 0) + ' ml.</p>';

    document.getElementById('resultado').innerHTML = html;
  }

  function descargarPDF() {
    if (!filasGlobales.length) {
      alert('Primero calculá la tabla.');
      return;
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.setFontSize(14);
    doc.text('Tabla de isotonización con agua de mar', 14, 16);

    const cuerpo = filasGlobales.map(f => [
      fmt(f.salinidadGL, 1),
      fmt(f.aguaMar, 1),
      fmt(f.aguaComun, 1),
      fmt(f.salAportada, 2),
      fmt(f.volumenFinal, 0)
    ]);

    doc.autoTable({
      startY: 22,
      head: [[
        'Salinidad objetivo (g/L)',
        'Agua de mar (ml)',
        'Agua común (ml)',
        'Sal aportada (g)',
        'Volumen final (ml)'
      ]],
      body: cuerpo,
      styles: { fontSize: 9, cellPadding: 2 },
      headStyles: { fillColor: [235, 235, 235], textColor: 20 },
      columnStyles: {
        0: { halign: 'center' },
        1: { halign: 'right' },
        2: { halign: 'right' },
        3: { halign: 'right' },
        4: { halign: 'right' }
      }
    });

    doc.save('isotonizacion_agua_mar.pdf');
  }

  // Calcular al cargar
  calcular();
</script>

## Si ésta calculadora le sirvió y quiere agradecer  <a href="https://th.org.pe/agradecer" target="_blank">presione aquí</a>

</body>
</html>
