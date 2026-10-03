+++
title = "Contacto"
date = "2024-01-01"
aliases = ["/contacto1/"]
[taxonomies]
tags = ["rexmar", "agua de mar", "Perú", "biología", "salud", "ciencia"]
+++

# Contacto

¿Tenés consultas sobre el Agua de Mar RexMar? ¿Querés ser distribuidor? ¿Necesitás más información?

Completá el formulario y te responderemos a la brevedad.

## Formulario de Contacto
<form action="https://contact-form.rexmaradm.workers.dev" method="POST">
  Nombre: <input type="text" name="Nombre" required><br>
  Email: <input type="email" name="Email" required><br>
  Tel. Whatsapp: <input type="tel" name="Teléfono Whatsapp sólo mensajes"><br>
  Motivo: 
  <select name="Motivo">
    <option value="Consulta">Consulta</option>
    <option value="Contacto por Angela">Contacto por Angela</option>
    <option value="Soporte">Quiero ser distribuidor</option>
  </select><br>
  Mensaje: <textarea name="Mensaje" required></textarea><br>
  <button type="submit">Enviar</button>
</form>

## Otras formas de contacto
- Email directo: rexmaradm@gmail.com
- WhatsApp: [Chateá con nosotros](https://wa.me/51904743809)
- Redes sociales: Seguinos en nuestras redes (ver pie de página principal)

*Nota: Todos los campos son obligatorios. Te responderemos dentro de las 24-48 horas hábiles.*

<div align="center">
[ir a Inicio](/)
</div>

<script>
document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const motivo = params.get('motivo');
  if (!motivo) return;
  
  const select = document.querySelector('select[name="Motivo"]');
  if (!select) return;

  for (let i = 0; i < select.options.length; i++) {
    if (select.options[i].value === motivo || select.options[i].text === motivo) {
      select.selectedIndex = i;
      break;
    }
  }
});
</script>
