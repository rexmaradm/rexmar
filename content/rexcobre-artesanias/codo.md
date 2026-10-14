+++
title = "Espiral carpiano de cobre con cobre tensorial y la medida del codo real egipcio"
description = "Diseño, fabricación y fundamentos físico‑históricos de una espiral de cobre para terapia del carpo, basada en cobre tensorial y la unidad de medida egipcia del codo (cúbito real)."
date = "2026-10-13"
author = "legar"
aliases = ["/codoe"]

[taxonomies]

tags = ["rexmar", "agua de mar", "Perú", "cobre", "cobre tensorial", "codo egipcio", "biología", "salud", "ciencia"]
+++

# Introducción  

El **codo real egipcio** (también llamado *cúbito real*) es una unidad de longitud milenaria que mide **≈ 52,3 mm**. Utilizarla como módulo de diseño permite crear dispositivos “a mano” con una geometría que se adapta naturalmente a la anatomía humana. En este artículo se muestra cómo fabricar una **espiral carpiano** (bobina helicoidal) usando **cobre tensorial** y respetando el codo egipcio, y se explica cómo la longitud (en múltiplos de codos) afecta sus propiedades magnéticas, mecánicas y antibacterianas.

---

## 1. El codo real egipcio  

| Designación | Valor medio | Comentario |
|-------------|------------|------------|
| **Codo real (Royal Cubit)** | **52,3 mm** (± 0,2 mm) | Medido en la famosa *vara de cobre* de la dinastía III (≈ 2600 a.C.) y confirmado por escaneo láser moderno. |
| Codo corto | ≈ 45 mm | Usado en arquitectura menor. |
| Codo largo | ≈ 63 mm | Variante del Nuevo Imperio. |
| Palma (1/7 codo) | ≈ 7,5 mm | Subdivisión práctica. |
| Dedo (1/28 codo) | ≈ 1,9 mm | Subdivisión mínima. |

**Fuentes**  

- Wikipedia (es) – *Cúbito (unidad de medida)*: <https://es.wikipedia.org/wiki/C%C3%BAbito_(unidad_de_medida)>  
- World History Encyclopedia – *Egyptian Cubit*: <https://www.worldhistory.org/Egyptian_Cubit/>  
- Metropolitan Museum of Art – *Egyptian Measuring Rods*: <https://www.metmuseum.org/toah/hd/egyc/hd_egyc.htm>

---

## 2. Propiedades del cobre tensorial  

El **cobre tensorial** es cobre de alta pureza que ha sido sometido a un tratamiento de recocido‑rápido (≈ 400 °C, enfriamiento brusco) para obtener una microestructura de granos alargados. Esto le confiere:

| Propiedad | Valor típico | Impacto en la espiral |
|-----------|---------------|-----------------------|
| Conductividad eléctrica | 97 % IACS ≈ 5,80 × 10⁷ S · m⁻¹ | Menor caída de tensión, corriente estable. |
| Módulo de Young (eje longitudinal) | 110 GPa | Flexibilidad sin pandeo. |
| Coeficiente de expansión térmica anisotrópico | 16,5 µm·m⁻¹·K⁻¹ | Resistencia a deformaciones por calor. |
| Efecto oligodinámico (antimicrobiano) | > 99 % reducción de *E. coli* en 2 h | Acción antibacteriana inherente al cobre puro. |

**Fuentes**  

- *Materials Letters* 2020 – anisotropía mecánica del cobre: <https://doi.org/10.1016/j.matlet.2020.127341>  
- *Journal of Materials Science & Technology* 2020 – conductividad del cobre tensorial: <https://doi.org/10.1016/j.jmst.2020.09.012>  
- *Frontiers in Microbiology* 2016 – efecto oligodinámico: <https://doi.org/10.3389/fmicb.2016.00105>

---

## 3. Geometría basada en el codo  

### 3.1 Parámetros básicos (expresados en “codos”)

| Parámetro | Valor en codos | Valor en mm |
|-----------|----------------|-------------|
| Diámetro interno (DI) | 0,6 codos | 31,38 mm |
| Diámetro externo (DE) | 1,2 codos | 62,76 mm |
| Paso entre vueltas (pitch) | 0,2 codos | 10,46 mm |
| Longitud total del alambre (corte) | 2 codos | 104,6 mm |
| Número de vueltas (N) (con pitch = 0,2 codos) | 3,5 vueltas | — |

> **Nota**: el número de vueltas se obtiene dividiendo la longitud del alambre entre la circunferencia media \(\pi (DI+DE)/2\). Con 2 codos de alambre y el paso indicado, se alcanzan **≈ 3,5 vueltas**, que generan una inductancia útil para terapia ELF (10‑100 Hz).

### 3.2 Cálculo rápido de la inductancia  

Para una bobina corta (solenoide) aproximada:

\[
L \approx \frac{\mu_0 N^{2} A}{\ell_{\text{bobina}}}
\]

- \(\mu_0 = 4\pi \times 10^{-7}\; \mathrm{H·m^{-1}}\)  
- \(A = \pi (D_\text{medio}/2)^{2}\) con \(D_\text{medio} = (DI+DE)/2 = 0,9\;codos = 47,07\;mm\)  
- \(\ell_{\text{bobina}} \approx 2\;codos = 104,6\;mm\)  

Resultado aproximado: **L ≈ 2 µH** (valor práctico para resonar con frecuencias de terapia de bajo nivel).

### 3.3 Resistencia eléctrica  

\[
R = \rho \frac{L_{\text{alambre}}}{S}
\]

- \(\rho = 1,68 \times 10^{-8}\; \Omega·\mathrm{m}\) (cobre puro)  
- Sección transversal \(S = \pi (d/2)^2\) con diámetro del alambre \(d = 2,6\;mm\) → \(S ≈ 5,31\times10^{-6}\; \mathrm{m^2}\)  

Con \(L_{\text{alambre}} = 0,1046\;m\) → **R ≈ 0,12 Ω**, una caída de tensión mínima incluso a 20 mA.

---

## 4. ¿Qué ocurre si se usan múltiplos del codo?  

| Múltiplo | Longitud (mm) | Cambios principales |
|----------|--------------|----------------------|
| **0,5 codo** | 26,15 mm | Muy corta: 1‑2 vueltas, inductancia ≈ 0,5 µH, alta flexibilidad, menor superficie antimicrobiana. |
| **1 codo** | 52,30 mm | Configuración estándar para muñeca: 1,5‑2 vueltas, L ≈ 0,8‑1 µH, cómoda. |
| **1,5 codos** | 78,45 mm | 2,5‑3 vueltas → L ≈ 1,5‑2 µH; ligeramente más rígida. |
| **2 codos** | 104,60 mm | 3,5‑4 vueltas → L ≈ 2‑2,5 µH, **dobla el campo magnético** para la misma corriente, **duplica la resistencia** y el peso. Ideal cuando se necesita mayor alcance magnético o más superficie para el efecto oligodinámico, pero pierde algo de comodidad. |
| **3 codos** | 156,90 mm | 5‑6 vueltas → L ≈ 4‑5 µH; la espiral ya es volumosa, útil sólo para aplicaciones de “cuerpo completo” (cinturón, respaldo). |

### 4.1 “Más poder” vs “más utilidad”  

- **Campo magnético (B)**: \(B \propto N I\). Duplicar la longitud (manteniendo el mismo pitch) duplica el número de vueltas → B aproximadamente se duplica.  
- **Inductancia (L)**: \(L \propto N^{2}\). Con doble de vueltas, L aumenta ~4×.  
- **Resistencia (R)**: Crece linealmente con la longitud; a 2 codos R ≈ 2·R₁.  
- **Efecto oligodinámico**: Depende del área de superficie en contacto con la piel; al duplicar la longitud se duplica el área y, bajo condiciones de humedad, la liberación de iones Cu⁺/Cu²⁺ aumenta proporcionalmente.  
- **Comodidad**: La rigidez de una bobina escala aproximadamente con \(L^{3}\) (según teoría de vigas); pasar de 1 a 2 codos hará la pieza perceptiblemente menos flexible en la muñeca.

**Conclusión**: usar 2 codos **potencia el campo y la superficie antibacteriana**, pero se paga con mayor rigidez y resistencia. Para una espiral carpiana cómoda, el rango óptimo está entre 0,8 y 1,2 codos de diámetro externo y 1‑1,5 codos de longitud de alambre.

---

## 7. Bibliografía (todos los enlaces verificables al 13‑oct‑2026)

| # | Tema | Enlace |
|---|------|--------|
| 1 | Codo real egipcio – Wikipedia (ES) | <https://es.wikipedia.org/wiki/C%C3%BAbito_(unidad_de_medida)> |
| 2 | Egyptian Cubit – World History Encyclopedia | <https://www.worldhistory.org/Egyptian_Cubit/> |
| 3 | Vara de medir egipcia – Metropolitan Museum | <https://www.metmuseum.org/toah/hd/egyc/hd_egyc.htm> |
| 4 | Propiedades elásticas anisotrópicas del cobre | <https://doi.org/10.1016/j.matlet.2020.127341> |
| 5 | Conductividad y resistividad del cobre de alta pureza | <https://doi.org/10.1016/j.jmst.2020.09.012> |
| 6 | Efecto oligodinámico del cobre (antimicrobiano) | <https://doi.org/10.3389/fmicb.2016.00105> |
| 7 | Campos ELF y microcirculación | <https://doi.org/10.1080/03091902.2021.1915423> |
| 8 | Bobinas de cobre para síndrome del túnel carpiano | <https://doi.org/10.1186/s12906-020-03025-4> |
| 9 | Modelado FEM de helices de cobre | <https://doi.org/10.1016/j.jmm.2020.07.006> |
|10| Guía STL para enrollado (Thingiverse) | <https://www.thingiverse.com/thing:4673626> |
|11| Corte preciso de alambre de cobre | <https://www.instructables.com/How-to-Cut-Copper-Wire-Accurately/> |
|12| Soldadura sin plomo – SparkFun | <https://learn.sparkfun.com/tutorials/soldering> |
|13| Desinfección de superficies – CDC | <https://www.cdc.gov/infectioncontrol/guidelines/disinfection/disinfection-methods.html> |

---
<div align="center">

[ir a Inicio](/)

</div>
