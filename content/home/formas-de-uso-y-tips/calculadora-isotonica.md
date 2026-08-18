+++
title = "Calculadora de Isotonización con Agua de Mar"
description = "Calculá los mL de Agua de Mar hipertónica necesarios para isotonizar según el volumen de tu recipiente. Por RexMar Agua de Mar Perú."
date = 2026-08-18
+++

<h2 style="text-align:center;">Ingrese el volumen de su taza / jarro / jarra en mL</h2>
<p style="text-align:center;">(ej: 1 L = 1000 mL)</p>
<p style="text-align:center;">Ver explicación <a href="/home/formas-de-uso-y-tips/equilibrio-electrolitico-y-adm/">aquí</a></p>

<div style="max-width:700px; margin:20px auto; text-align:center;">
    <label for="cantidad" style="font-size:1.1em; margin-right:10px;">Cantidad (mL):</label>
    <input type="number" id="cantidad" min="1" placeholder="Ej: 1000"
           style="padding:10px 15px; font-size:16px; width:200px; border:2px solid #3b82f6; border-radius:8px; background:#ffffff; color:#1e3a8a;">
    <br><br>
    <button onclick="generarTabla()"
            style="padding:12px 25px; background:#2563eb; color:#fff; border:none; border-radius:8px; font-size:16px; cursor:pointer; font-weight:bold;">
        Generar Tabla Completa
    </button>
</div>

<div id="resultado"></div>

<script>
function generarTabla() {
    const cantidad = parseFloat(document.getElementById('cantidad').value);
    const div = document.getElementById('resultado');

    if (!cantidad || cantidad <= 0) {
        div.innerHTML = '<p style="text-align:center; color:#f87171; font-weight:bold;">⚠️ Por favor, ingrese un número válido mayor a 0.</p>';
        return;
    }

    const factores = [
        ["5", 0.14], ["5.5", 0.15], ["6", 0.17], ["6.5", 0.18],
        ["7", 0.19], ["7.5", 0.21], ["8", 0.22], ["8.5", 0.24],
        ["9", 0.25], ["9.5", 0.27], ["10", 0.28], ["10.5", 0.29],
        ["11", 0.31], ["11.5", 0.32], ["12", 0.33], ["12.5", 0.35],
        ["13", 0.36], ["13.5", 0.38], ["14", 0.39], ["14.5", 0.41],
        ["15", 0.42], ["15.5", 0.43]
    ];

    let html = '<div style="max-width:700px; margin:30px auto; padding:20px; background:#1e40af; border-radius:10px; border:1px solid #3b82f6;">';
    html += '<h3 style="text-align:center; color:#bfdbfe;">Valores para ' + cantidad.toLocaleString('es') + ' mL</h3>';
    html += '<table style="width:100%; border-collapse:collapse; margin:15px 0;">';
    html += '<thead><tr>';
    html += '<th style="padding:10px; border-bottom:2px solid #3b82f6; color:#93c5fd; text-align:left;">% Sal (gr x Litro)</th>';
    html += '<th style="padding:10px; border-bottom:2px solid #3b82f6; color:#93c5fd; text-align:right;">mL de AdM Hipertónica</th>';
    html += '</tr></thead><tbody>';

    for (let i = 0; i < factores.length; i++) {
        const sal = factores[i][0];
        const factor = factores[i][1];
        const ml = (cantidad * factor).toFixed(2);
        html += '<tr style="border-bottom:1px solid #2563eb;">';
        html += '<td style="padding:8px 10px; color:#bfdbfe;"><strong>' + sal + ' gr/L</strong></td>';
        html += '<td style="padding:8px 10px; color:#ffffff; text-align:right;">' + ml + ' mL</td>';
        html += '</tr>';
    }

    html += '</tbody></table>';
    html += '<p style="text-align:center; font-size:0.9em; color:#93c5fd; margin-top:15px;">Servicio gratuito de RexMar Agua de Mar Perú</p>';
    html += '<div style="text-align:center; margin-top:20px;">';
    html += '<button onclick="window.print()" style="padding:10px 20px; background:#2563eb; color:#fff; border:2px solid #3b82f6; border-radius:8px; cursor:pointer; font-size:15px; font-weight:bold;">🖨️ Imprimir o Guardar como PDF</button>';
    html += '</div>';
    html += '</div>';

    div.innerHTML = html;
}
</script>

<style>
@media print {
    header, footer, .tools-container, nav, button { display: none !important; }
    main { background: white !important; color: black !important; box-shadow: none !important; }
    #resultado div { background: white !important; border: none !important; }
    #resultado table { color: black !important; }
    #resultado td, #resultado th { color: black !important; border-bottom: 1px solid #ccc !important; }
    #resultado h3 { color: black !important; }
}
</style>
