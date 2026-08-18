+++
title = "RexMar - Agua de Mar Perú"
aliases = ["/wp/home/formas-de-uso-y-tips/de/"]
+++

Rex Mar Agua de Mar

<style>
.rexmar-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  width: 100%;
}
.rexmar-grid img {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 8px;
}
@media (max-width: 600px) {
  .rexmar-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>

<div class="rexmar-grid">
  <a href="/sociales/donaciones/"><img decoding="async" src="/images/compraanimales.png" alt="Donaciones" /></a>
  <a href="/home/formas-de-uso-y-tips/calculadora-isotonica/"><img decoding="async" src="/images/calculadora.png" alt="Calculadora Isotónica gratuita" /></a>
  <a href="/home/formas-de-uso-y-tips/equilibrio-electrolitico-y-adm/"><img decoding="async" src="/images/porqueisotonizar.png" alt="Por qué isotonizar" /></a>
  <a href="/bajarinf/" target="_blank"><img decoding="async" src="/images/bajarinforme.png" alt="Bajar informe" /></a>
</div>

Agua de Mar RexMar es una fuente natural de vitaminas, minerales, oligoelementos, ácidos nucleicos, aminoácidos esenciales, proteínas, grasas, hidratos de carbono, zooplancton y fitoplancton.

{# Contenedor visible #}
<div class="nube-paginas-widget">
  <h3>Páginas al azar</h3>
  <div id="nube-visible"></div>
</div>

{# Estilos inyectados directamente para evitar peleas con el tema #}
<style>
  #nube-visible {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 10px !important;
    margin-top: 15px !important;
    padding: 10px !important;
    background-color: rgba(255, 255, 255, 0.05) !important;
    border-radius: 8px !important;
  }

  #nube-visible a.tag-nube {
    display: inline-block !important;
    padding: 6px 12px !important;
    background-color: #2c3e50 !important; /* Azul oscuro */
    color: #ffffff !important;
    text-decoration: none !important;
    border-radius: 20px !important;
    font-size: 0.9em !important;
    border: 1px solid #34495e !important;
    transition: all 0.2s ease-in-out !important;
    line-height: 1.5 !important;
  }

  #nube-visible a.tag-nube:hover {
    background-color: #e74c3c !important; /* Rojo al pasar el mouse */
    border-color: #c0392b !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
    color: #ffffff !important;
  }
</style>

{# Script que genera los enlaces #}
<script>
document.addEventListener("DOMContentLoaded", () => {
  const contenedor = document.getElementById('nube-visible');
  if (!contenedor) return;

  const urlIndex = '{{ get_url(path="search_index.es.json") }}';

  fetch(urlIndex)
    .then(response => response.json())
    .then(data => {
      let paginas = data.filter(p => p.title && p.url);
      if (paginas.length === 0) return;

      for (let i = paginas.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [paginas[i], paginas[j]] = [paginas[j], paginas[i]];
      }

      paginas.slice(0, 6).forEach(p => {
        const a = document.createElement('a');
        a.href = p.url;
        a.textContent = p.title;
        a.className = 'tag-nube';
        contenedor.appendChild(a);
      });
    })
    .catch(err => console.error("Error cargando la nube:", err));
});
</script>


Entrevista de Griselda Donatucci a RexMar Agua de Mar

<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px;">
<iframe src="https://www.youtube.com/embed/4T4btupWNKs" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" allowfullscreen loading="lazy" title="YouTube video"></iframe>
</div>

---

Último viaje de Extracción:

Ver [viajes anteriores en Rumble](https://rumble.com/search/all?q=viaje%20completo%20rexmar)

<iframe class="rumble" width="640" height="360" src="https://rumble.com/embed/v7bun1s/?pub=1wgpuu" frameborder="0" allowfullscreen></iframe>

---

<iframe class="rumble" width="640" height="360" src="https://rumble.com/embed/v765gga/?pub=1wgpuu" frameborder="0" allowfullscreen></iframe>

¿Qué es el agua de mar?

El agua de mar es un medio orgánico completo que contiene todos los elementos necesarios para la vida. Nuestro agua de mar es extraída artesanalmente de las profundidades del océano, preservando todas sus propiedades naturales.

<iframe class="rumble" width="640" height="360" src="https://rumble.com/embed/v78i3ly/?pub=1wgpuu" frameborder="0" allowfullscreen></iframe>

Redes Sociales

Seguinos en nuestras redes:

<a href="https://www.facebook.com/rexmar.adm"><img src="/images/fb.svg" alt="Facebook" width="32" height="32" /></a> | <a href="https://rumble.com/c/c-2565560"><img src="/images/rumble.svg" alt="Rumble" width="32" height="32" /></a>  | <a href="https://t.me/RexMarAdMPeru"><img src="/images/tg.svg" alt="Telegram" width="32" height="32" /></a> | <a href="https://twitter.com/Rexmar_adm"><img src="/images/tw.svg" alt="Twitter" width="32" height="32" /></a> | <a href="https://www.instagram.com/rexmar.adm"><img src="/images/ig.svg" alt="Instagram" width="32" height="32" /></a> | <a href="https://www.tiktok.com/@rexmar.adm"><img src="/images/tt.svg" alt="Tiktok" width="32" height="32" /></a> |<a href="https://www.youtube.com/@RexMarAguadeMarPeru"><img src="/images/yt.svg" alt="Youtube" width="32" height="32" /></a>  | <a href="https://www.facebook.com/groups/346911354063842/"><img src="/images/fb.svg" alt="Grupo Facebook" width="32" height="32" /></a> | <a href="https://t.me/RexMarAdMPeru/1"><img src="/images/tg.svg" alt="Grupo Telegram" width="32" height="32" /></a>  

<script>
document.addEventListener("DOMContentLoaded", () => {
  const contenedor = document.getElementById('nube-visible');
  if (!contenedor) return;

  // Zola reemplaza esto con la URL correcta antes de enviar el HTML al navegador
  const urlIndex = '{{ get_url(path="search_index.es.json") }}';

  fetch(urlIndex)
    .then(response => response.json())
    .then(data => {
      let paginas = data.filter(p => p.title && p.url);
      
      if (paginas.length === 0) return;

      // Mezclar array (Fisher-Yates)
      for (let i = paginas.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [paginas[i], paginas[j]] = [paginas[j], paginas[i]];
      }

      // Tomar 6 al azar
      paginas.slice(0, 6).forEach(p => {
        const a = document.createElement('a');
        a.href = p.url;
        a.textContent = p.title;
        a.className = 'tag-nube';
        contenedor.appendChild(a);
      });
    })
    .catch(err => console.error("Error cargando la nube:", err));
});
</script>
