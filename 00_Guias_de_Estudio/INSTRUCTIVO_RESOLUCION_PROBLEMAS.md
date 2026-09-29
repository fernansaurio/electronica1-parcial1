# Instructivo para resolver problemas · Parcial 1 ELC-115

**Curso:** Electrónica 1 (ELC-115), Escuela de Ingeniería Eléctrica, Universidad de El Salvador
**Profesor:** José Ramos López
**Alcance:** diodos (física, modelos, rectificadores, cargadores, Zener, recortadores) y MOSFET en DC
**Última verificación de resultados:** 2026-09-29 · **Guías ampliadas a versión completa paso a paso:** 2026-09-29

Este documento sirve para dos lectores:

1. **Tú, al estudiar.** Te dice qué procedimiento usar para cada tipo de problema y con qué valores comparar tu resultado.
2. **Una IA que te ayude.** Si le pides a una IA que resuelva o explique un problema del curso, dale este archivo primero. Las secciones marcadas con **[REGLA]** son obligatorias y evitan los errores que ya aparecieron en guías anteriores.

### Etiquetas usadas en este documento

| Etiqueta | Significado |
|---|---|
| **[REGLA]** | Obligatorio. No se negocia ni se "mejora". |
| **[VERIFICADO]** | Resultado recalculado y comparado con la solución oficial o con simulación. |
| **[OFICIAL]** | Valor que aparece en la solución del profesor. |
| **[ERROR EN FUENTE]** | Un documento de la carpeta contiene un error. Se indica el valor correcto. |
| **[AMBIGUO]** | El enunciado admite dos lecturas. Declarar la suposición. |
| **[TRAMPA]** | Detalle que hace fallar a quien resuelve en automático. |

---

## 1. Reglas del profesor

> **[REGLA 1] Convención del MOSFET.**
> Usar siempre `K_N = k'_n · (W/L) = μ_n·C_ox·(W/L)`, en mA/V².
> Saturación: `I_D = ½ · K_N · (V_GS − V_t)²`.
> Triodo: `I_D = K_N · [ (V_GS − V_t)·V_DS − ½·V_DS² ]`.
> Nunca escribir `I_D = K_N · V_OV²` sin el ½. Con esa otra convención la corriente sale el doble. Es exactamente el error de la guía previa que decía 13.27 mA en lugar de 6.64 mA.

> **[REGLA 2] Verificar la región siempre.**
> Todo cálculo de MOSFET termina comprobando `V_DS ≥ V_OV` para saturación, o `V_DS < V_OV` para triodo. Si la suposición falla, se resuelve de nuevo en la otra región. Nunca se reporta una corriente de saturación sin esta verificación.

> **[REGLA 3] Modelo de diodo del enunciado.**
> Usar exactamente el modelo que pide el problema: ideal, caída constante con el V_D dado, o lineal por tramos con V_D0 y r_D.
> Valores que ya usó el profesor: 0.5 V (1N914 "observado en laboratorio", parcial 2024), 0.6 V, 0.65 V, 0.7 V, 0.85 V, 1 V y 1.25 V.
> Si el enunciado dice "use su observación de laboratorio", declarar el valor usado. En 2024 la respuesta oficial corresponde a V_D = 0.5 V.

> **[REGLA 4] Tensión térmica.**
> El profesor usa `V_T = 25 mV` en los problemas de unión pn y de diodos (por ejemplo V_0 = 0.728 V en 2017). Si el problema da la temperatura, calcular `V_T = kT/q`. Declarar el valor usado.

> **[REGLA 5] Rizado con corrección por ΔT.**
> Cuando el rizado no es pequeño frente a V_p, el profesor exige:
> 1. Calcular `V_r = V_p/(2fRC)` y `ΔT = (1/ω)·√(2V_r/V_p)`.
> 2. Recalcular `V_r = (V_p/RC)·(T/2 − ΔT)`.
> 3. Con el nuevo V_r, recalcular V_dc, I_dc y la potencia.
> En la solución oficial 2023R, la corriente pico usa el ΔT del paso 1.

> **[REGLA 6] Corriente pico del diodo.**
> Existen dos fórmulas válidas. Se debe indicar cuál se usa.
> - Profesor (pulso triangular, onda completa): `I_pico ≈ I_dc · T/ΔT`, con T = 1/60 s.
> - Sedra (onda completa): `i_D,max = I_L·(1 + 2π·√(V_p/2V_r))`. En el diseño de 2017 el profesor omite el "+1".

> **[REGLA 7] Respuesta con unidades y en el espacio pedido.**
> El examen dice "asegurarse de escribir las respuestas en los espacios indicados". Cada literal termina con un valor numérico, su unidad y 3 cifras significativas. Las preguntas de opinión ("¿SÍ o NO y por qué?", "¿cuál es el problema?") requieren una respuesta explícita y una justificación con números.

> **[REGLA 8] No inventar datos de figuras.**
> Si un valor depende de una figura que no se puede leer, decirlo y pedir el dato o dar la respuesta en función de ese dato. No suponer valores de resistencias, orientaciones de diodos ni lecturas de curvas sin declararlo.

---

## 2. Mapa de fuentes

### 2.1 Carpetas

| Carpeta | Contenido | Uso |
|---|---|---|
| `00_Guias_de_Estudio/` | Guías 00 a 04 en HTML y PDF, figuras, este instructivo | Resumen y soluciones verificadas |
| `01_Fisica_Semiconductores_Union_PN/` | Funcionamiento físico, guía de celda solar | Teoría de unión pn |
| `02_Diodo_Ideal_y_Analisis/` | Diodo ideal, aplicaciones, problemas 4, 9, 11–23 | Modelos y análisis por estados |
| `03_Diodo_Real_Exponencial_Temperatura/` | Diodo de unión, i-v, problemas 27, 30, 35, 48, 50, 59 | Exponencial, temperatura, pequeña señal |
| `04_Zener_y_Rectificadores/` | Lección Zener y rectificadores, problemas 76 y 77 | Zener, rectificadores, filtro |
| `05_Recortadores_y_Sujetadores/` | Circuitos con diodos y condensadores, problema 88 | Recortadores, sujetadores, dobladores |
| `06_MOSFET_Teoria/` | Lecciones MOSFET, corriente de drenaje, problemas 16–21 | Ecuaciones y regiones |
| `07_MOSFET_Circuitos_DC/` | Ejemplos del 12 de septiembre, problemas 44–52 | Polarización y circuitos DC |
| `08_Laboratorios_y_LTspice/` | Laboratorio 1, laboratorio CMOS (CD4007), LTspice | Contexto de los problemas de examen |
| `09_Parciales_Anteriores/` | Parciales 2012 a 2025, nombrados por año | Práctica y banco de problemas |
| `10_Libro_y_Solucionarios/` | Solucionario Sedra 5.ª ed., manual Sedra 6.ª ed., apéndice L | Consulta |
| `99_Duplicados_y_Otros/` | Copias "(1)", zip original, guías previas con errores | No usar para estudiar |

### 2.2 Jerarquía de autoridad

Cuando dos fuentes no coinciden, manda la primera de esta lista:

1. **Solución oficial del profesor** (Mathcad o respuestas en azul): 2024 con respuestas, 2023 repetido, 2017 V1 y V2, 2014 y 2013.
2. **Documentos del profesor** (lecciones y "CORRIENTE DE DRENAJE"), porque fijan la convención.
3. **Guía 04** de esta carpeta, cuyos resultados están verificados en la sección 5.
4. **Solucionarios de Sedra.** Usan la convención del libro. Revisar si K es `k'n·W/L` o su mitad antes de copiar un número.
5. **Soluciones de estudiantes** (2021 y "nota 7"). Contienen errores confirmados; ver la sección 6.
6. **Guías previas** en `99_Duplicados_y_Otros/`. No usar para valores de MOSFET.

### 2.3 Dónde está cada capítulo en los solucionarios de Sedra

El curso sigue la 5.ª edición en español. Los números de problema de las tareas (4, 9, 11–23, 27, 30, 35, 48, 50, 59, 76, 77, 88, 90) son del capítulo 3 de esa edición.

| Archivo | Contenido | Páginas del PDF |
|---|---|---|
| Solucionario Sedra 5.ª ed. (manuscrito, 466 págs.) | Capítulo 2 problemas | desde la 31 aprox. |
| | **Capítulo 3 Diodos, problemas** | **61 a 117 aprox.** |
| | **Capítulo 4 MOSFET, problemas** | **118 a 147 aprox.** |
| | Capítulo 5 BJT en adelante | desde la 148 aprox. |
| Manual Sedra 6.ª ed. (226 págs.) | Ejercicios cap. 3 Semiconductores | 22 a 29 |
| | **Ejercicios cap. 4 Diodos** | **30 a 43** |
| | **Ejercicios cap. 5 MOSFET** | **44 a 55** |
| | Problemas cap. 1 a 3 | 153 a 226 |

> **[TRAMPA]** El manual de la 6.ª edición anuncia problemas de los capítulos 1 a 16, pero el archivo termina en el capítulo 3. No trae problemas de diodos ni de MOSFET, solo sus ejercicios. Además, la numeración de problemas de la 6.ª edición no coincide con la de la 5.ª.

> **[TRAMPA]** Las páginas del solucionario de la 5.ª edición son aproximadas porque el escaneo no tiene encabezados. Confirma el número de problema escrito a mano en la página.

---

## 3. Procedimiento general de resolución

1. **Identificar el tipo de problema** con la tabla de la sección 4.
2. **Listar datos y unidades.** Convertir todo a V, A, Ω, F y s.
3. **Declarar el modelo** del diodo o del MOSFET, según las reglas 1 a 4.
4. **Suponer estados o región** y escribir el circuito equivalente.
5. **Resolver** con nodos o mallas. Si aparece una cuadrática, conservar la raíz físicamente posible y decir por qué se descarta la otra.
6. **Verificar** los estados supuestos: I_D > 0 en diodos encendidos, V_D < V_D0 en apagados, y la región del MOSFET.
7. **Comprobar el orden de magnitud** contra el banco de la sección 5 si el problema es una variante conocida.
8. **Responder** cada literal con valor, unidad y una frase de interpretación.

---

## 4. Procedimientos por tipo de problema

### 4.1 Circuito DC con varios diodos

- Suponer estados. Sustituir cada diodo encendido por una fuente V_D y cada apagado por un circuito abierto.
- Resolver y verificar: I_D > 0 en los encendidos y V_ánodo − V_cátodo < V_D en los apagados.
- **[TRAMPA]** Si un diodo encendido resulta con I_D < 0, la suposición es falsa. No se "corrige el signo".

### 4.2 Característica de transferencia y recortadores

1. Con todos los diodos apagados, encontrar la relación base: `v_o = v_i` o un divisor.
2. Para cada diodo, el umbral en v_o es la fuente de su rama más V_D, con el signo según la orientación.
3. Llevar el umbral a v_i con la relación base.
4. En cada región con diodo encendido, la pendiente es `R_rama/(R_serie + R_rama)`. Si la rama no tiene resistencia, la salida queda plana.
5. Dibujar v_o contra v_i con puntos de quiebre, pendientes y valores en los extremos.
6. Para una entrada triangular o senoidal, marcar los instantes de quiebre y los niveles de recorte.

- **[TRAMPA]** Puente de diodos con Zener: el Zener conduce siempre en el mismo sentido, así que el límite es simétrico `±(2V_D0 + V_Z0)`.
- **[TRAMPA]** Modelo lineal por tramos del Zener: `V_Z0 = V_ZT − I_ZT·r_z`. No usar V_ZT como fuente del modelo.

### 4.3 Rectificador con filtro capacitivo

| Magnitud | Fórmula |
|---|---|
| Pico en el condensador | Puente: `V_p = V_s − 2V_D`. Derivación central o media onda: `V_p = V_s − V_D`. |
| Rizado | `V_r = V_p/(2fRC)` en onda completa y `V_p/(fRC)` en media onda |
| Salida DC | `V_dc = V_p − V_r/2` e `I_dc = V_dc/R` |
| Conducción | `ωΔT = √(2V_r/V_p)` |
| Corrección (regla 5) | `V_r = (V_p/RC)·(T/2 − ΔT)` |
| Pico (regla 6) | `I_dc·T/ΔT` o `I_L·(1 + 2π√(V_p/2V_r))` |
| Promedio por diodo | `I_dc/2` en onda completa |
| Corriente de entrada | pulsos triangulares: `I_ac = I_p·√(2ΔT/3T)` |
| Potencias | `P ≈ V_dc·I_dc + n·V_D·I_dc`. `S = V_ac·I_ac`. `PF = P/S`. |
| PIV | Puente: `V_s − V_D`. Derivación central: `2V_s − V_D`. Usar la línea máxima si hay variación. |

- **[TRAMPA]** `V_s` en estas fórmulas es el valor pico del secundario, no el rms.
- **[TRAMPA]** Una relación 10:1 con 120 Vac da `V_s = 12 Vrms = 16.97 V` pico.
- **[TRAMPA]** Más capacidad significa menos rizado, pero ΔT más corto y un pico de corriente mucho mayor.

### 4.4 Cargador de batería

- **Sin condensador:** el diodo conduce entre `θ1 = arcsen((nV_D + V_B)/V_s)` y `π − θ1`.
  `I_pico = (V_s − nV_D − V_B)/R`.
  `I_prom = [2V_s·cosθ1 − (nV_D + V_B)(π − 2θ1)]/(πR)` para onda completa. En media onda se divide entre 2π en lugar de π.
  `t_carga = capacidad (A·h)/I_prom`.
  `P = V_B·I_prom + nV_D·I_prom + R·I_rms²`.
- **Con condensador:** primero `I_dc = (V_p − V_B)/R`, luego V_r, luego `V_dc = V_p − V_r/2`, y se recalcula I_dc.
  La eficiencia es `η = V_B·I_dc/P_entrada`.
- **Con fuente de corriente (2025):** la corriente de la fuente sale por el diodo cuyo cátodo está más bajo. La batería recibe I cuando v_i > V_B.

### 4.5 Regulador Zener shunt

- `V_Z0 = V_ZT − I_ZT·r_z`.
- Sin carga: `I_Z = (V_S − V_Z0)/(R + r_z)`.
- Regulación de línea: `r_z/(R + r_z)` en mV/V.
- Regulación de carga: `−(r_z ∥ R)` en mV/mA.
- Diseño para el peor caso: `R ≤ (V_S,min − V_Z0 − r_z·I_ZK)/(I_L,max + I_ZK)`.
- Potencia máxima del Zener: sin carga y con V_S máxima.
- **[TRAMPA]** Con dos r_z distintas (1N5235), usar la r_z del punto de operación del diseño: 5 Ω a 20 mA y 750 Ω a 0.25 mA.

### 4.6 MOSFET: extraer V_t y K_N

- Dos puntos en saturación: `r = √(I_1/I_2)`, `V_t = (r·V_GS2 − V_GS1)/(r − 1)` y `K_N = 2I_1/(V_GS1 − V_t)²`.
- Conectado como diodo: `V_GS = V_DS`, siempre en saturación, e `I = (V_DD − V_1)/R_D`.
- **[TRAMPA]** Descartar la raíz con V_t mayor que algún V_GS medido.
- **[AMBIGUO]** Si se leen de una curva, el resultado depende de la lectura. Reportar los valores leídos.

### 4.7 MOSFET: punto de operación

- `V_G` del divisor, porque I_G = 0.
- Con R_S: `V_G = V_GS + I_D·R_S`. En la forma del profesor, con `x = √I_D`: `R_S·x² + √(2/K_N)·x + (V_t − V_G) = 0`.
- Calcular V_D y V_DS y aplicar la regla 2.
- Si falla la saturación: `(V_DD − V_DS)/R_D = K_N·(V_OV·V_DS − ½V_DS²)` y tomar la raíz con V_DS < V_OV.

### 4.8 MOSFET: límites de región cuando la señal está en la fuente

- Fuera de corte: `V_G,min = V_IN,max + V_t`.
- Siempre en saturación: `V_DD,min = V_G − V_t + I_D,max·R_D`, con I_D,max evaluada en V_IN,min.
- Frontera saturación/triodo: `V_D = V_G − V_t`.
- **[TRAMPA]** V_i pequeño da corriente grande, así que el transistor entra en **triodo**. V_i grande lo lleva a **corte**. La saturación queda en medio.

### 4.9 Espejos y circuitos con varios MOSFET

- Un transistor con G unido a D, o con una resistencia entre G y D sin corriente de compuerta, está en saturación.
- El espejo copia la corriente solo si el transistor de salida está en saturación. Verificarlo.
- **[TRAMPA]** Si el transistor de salida no tiene camino de corriente, su I_D es 0 y no copia nada (2023 P4c).

---

## 5. Banco de ejercicios resueltos verificados

Úsalo para comprobar resultados. Si una variante de examen da un orden de magnitud muy distinto, revisar el procedimiento. La columna "Estado" indica de dónde viene la confirmación.

### 5.1 Rectificadores y fuentes

| Problema | Datos clave | Respuestas | Estado |
|---|---|---|---|
| 2023 P3 | 169.7 V pico sin transformador, puente, V_D = 1 V, C = 1000 µF, R = 20 Ω | Tradicional: V_r = 69.9 V, ΔT = 2.42 ms, V_dc = 132.8 V, I_dc = 6.64 A, I_pico = 45.7 A, P ≈ 881 W. Corregido: V_r = 49.6 V, V_dc = 142.9 V, I_dc = 7.15 A, P ≈ 1021 W, I_pico ≈ 49 A. 1N4004: **NO** (1 A promedio y 30 A de sobrecarga no alcanzan). | [VERIFICADO] con simulación: V_r ≈ 44 V, I_pico ≈ 46 A |
| 2023R P3 | Igual con R = 12 Ω y sin caída en diodos | V_r = 117.9 V, ΔT = 3.13 ms, V_r corregido = 73.6 V, V_dc = 132.9 V, I_dc = 11.07 A, P = 1472 W, I_pico = 59.0 A, I_ac = 20.9 A, S = 2505 VA, PF = 0.587 | [OFICIAL] [VERIFICADO] |
| 2017 P2 V1 | 12 V, 1 % de rizado, 2 A, puente, V_D = 1 V | 9.9 Vrms, C = 138 889 µF, PIV = 13 V, I_pico = 88.86 A, P_trafo = 28 W | [OFICIAL] [VERIFICADO] |
| 2017 P2 V2 | 15 V, 1 %, 1 A | 12 Vrms, 55 555 µF, PIV = 16 V, 44.43 A, 17 W | [OFICIAL] [VERIFICADO] |
| 2024 P2 | Transformador del laboratorio, V_p ≈ 17.07 V en C | 100 Ω/470 µF: 15.55 V, 3.03 V, 2.42 W. 100 Ω/1000 µF: 16.36 V, 1.42 V, 2.68 W. 1 kΩ/470 µF: 16.92 V, 0.30 V, 0.29 W. 1 kΩ/1000 µF: 17.0 V, 0.14 V, 0.29 W | [OFICIAL] [VERIFICADO] |
| 2024 P3 | Hueco de 100 ms, mismo V_r que con 1000 µF y 100 Ω | C = I_L·0.1/V_r ≈ 12 000 µF. I_pico = 9.48 A oficial; 9.1–9.2 A con las fórmulas | [OFICIAL] |
| "nota 7" P4 | 12:1, puente de 4 diodos, V_D = 0.7 V, R = 1 kΩ, V_p = 12.74 V | 4.5 %: C = 185 µF, V_o = 12.45 V, 4.77 %, 143 mA, 273 mA. 1.25 %: C = 667 µF, 12.66 V, 2.52 %, 264 mA, 516 mA | [VERIFICADO] |
| 2014 P4 | V_s = 6.9 Vrms, R = 100 Ω, línea +10 % | PIV = 10.73 V. Con 5 % de rizado: C = 1667 µF, V_dc = 9.51 V | [OFICIAL] |

### 5.2 Cargadores y cargas especiales

| Problema | Datos clave | Respuestas | Estado |
|---|---|---|---|
| 2023 P1 | 10:1, puente, V_D = 0.85 V, R = 10 Ω, batería 6 V y 800 mAh | I_pico = 0.927 A, θ1 = 27.0°, I_bat = 0.424 A, I_diodo = 0.212 A, t = 1.89 h, P ≈ 6.38 W (2.54 W batería, 3.11 W resistencia, 0.72 W diodos) | [VERIFICADO] |
| 2023R P1 | Puente, C = 5000 µF, R = 10 Ω, batería 12 V y 50 Ah, V_D = 1.25 V | Con 12 V: 0.23 A y 220 h, no sirve. Con **24 V**: I_dc = 1.78 A, unas 28 h, I_diodo = 0.89 A, I_pico = 26.8 A, P = 57.6 W, η = 37 % | [OFICIAL] [VERIFICADO] |
| 2025 P1 | Fuente de 60 mA, v_i de 12 V pico, V_D = 0.7 V, batería 6 V | i_B es un pulso de 60 mA entre 30° y 150°. Pico 60 mA, promedio 20 mA. Con pico −10 %: 60 mA y 18.75 mA | [VERIFICADO] |
| 2023 P2 | Foco de 100 W a 120 V con diodo ideal | R = 144 Ω, P = 50 W, I_p = 1.18 A, I_prom = 0.375 A, I_rms = 0.589 A | [VERIFICADO] |
| 2023R P2 | Foco de 60 W | R = 240 Ω, I_p = 0.707 A, I_prom = 0.225 A, I_rms = 0.354 A | [OFICIAL] |

### 5.3 Zener

| Problema | Datos clave | Respuestas | Estado |
|---|---|---|---|
| 2025 P2 | 1N5235, 10 ± 1 V, sin carga | Diseño 1: R = 160 Ω, 30.3 mV/V. Diseño 2: R ≈ 13.2 kΩ, 53.8 mV/V | [VERIFICADO] |
| "nota 7" P3 | Igual con 9.5 V | 135 Ω y 35.7 mV/V. 11.2 kΩ y 62.8 mV/V | [VERIFICADO] |
| 2014 P4 c–e | 1N4733A: 5.1 V a 49 mA, r_z = 7 Ω | V_Z0 = 4.757 V, I_ZQ = 35 mA para 5 V, carga máxima ≈ 94 mA, P_Z,max ≈ 0.52 W | [OFICIAL] |
| Clase, ejemplo 3.8 | V_Z0 = 6.7 V, r_z = 20 Ω, R = 0.5 kΩ, 10 V | I_Z = 6.35 mA, regulación 38.5 mV/V | [OFICIAL] |

### 5.4 Recortadores, transferencia y sujetadores

| Problema | Datos clave | Respuestas | Estado |
|---|---|---|---|
| 2024 P1 | R1 = RL = 5.1 kΩ, fuentes 1.5 V y 1 V, V_D = 0.5 V, triangular de 5 V | V_out = V_s/2 entre −3 V y 4 V. Recorta en +2 V y −1.5 V | [OFICIAL] |
| 2021 P1 | R1 = 500 Ω, rama D1 con 1.5 V y 750 Ω, rama D2 con 250 Ω, V_D = 0.6 V | V_o = V_i entre −0.6 y 2.1 V. Arriba: 0.6V_i + 0.84 (6.84 V en 10 V). Abajo: V_i/3 − 0.4 (−3.73 V en −10 V) | [VERIFICADO] |
| 2017 P3 V1 | Puente con Zener de 6.8 V a 37 mA, r_z = 3.5 Ω, V_D0 = 0.65 V, r_D = 30 Ω, R = 1 kΩ | Quiebre en ±7.97 V, pendiente 1/16.75, v_o(10 V) = 8.09 V | [OFICIAL] [VERIFICADO] |
| 2017 P3 V2 | Zener de 5.6 V a 45 mA, r_z = 5 Ω | Quiebre en ±6.675 V, pendiente 1/16.38 | [OFICIAL] |
| repe P4 | V_D = 0.65 V, V_Z = 5.1 V, r_z = 0 | Salida plana en ±6.4 V | [VERIFICADO] |
| 2021 P3 | Sujetador con V_D = 0.6 V y Zener de 5.1 V, 10 Vrms | C se carga a 8.44 V. V_o entre +5.7 V y −22.6 V. Promedio −8.44 V | [VERIFICADO] |
| 2013 P5 | V1 = 2.75 V, V2 = 2 V, R = 4.7 kΩ, triangular de 10 V | +3.45 V y −2.7 V. I_D1,max = 0.66 mA, I_D2,max = 0.98 mA | [OFICIAL] |
| 2014 P1 | R = 1 kΩ, rama D1 con 1 V y 1.5 kΩ, rama D2 con 0.5 kΩ | Arriba de 1.7 V: V_o = 1.7 + (V_i − 1.7)·0.6. Abajo de −0.7 V: V_o = −0.7 + (V_i + 0.7)/3 | [VERIFICADO], corrige la fuente |

### 5.5 Diodos en DC, física y modelos

| Problema | Respuestas | Estado |
|---|---|---|
| 2017 P1 V1 | D1 y D2 conducen, D3 apagado. I_D1 = I_D2 = 0.976 mA, V1 = 0.467 V, V2 = V3 = −0.233 V | [OFICIAL] |
| 2017 P1 V2 | D1 y D3 conducen, D2 apagado. I_D1 = 1.215 mA, I_D3 = 0.93 mA, V1 = −2.15 V, V2 = −2.85 V, V3 = −0.7 V | [OFICIAL] |
| 2017 P4 V1 | N_A = 10¹⁷, N_D = 10¹⁶: V_0 = 0.728 V, E_max = 45.2 kV/cm, W = 0.32 µm | [OFICIAL] [VERIFICADO] |
| 2017 P4 V2 | 10¹⁸ y 10¹⁷: 0.843 V, 153.9 kV/cm, 0.109 µm | [OFICIAL] [VERIFICADO] |
| 2014 P3 | V_DD = 1.5 V, R = 500 Ω, I_S = 10⁻¹⁴ A: I_D = 1.71 mA, V_D = 0.647 V | [OFICIAL] |
| "nota 7" P1 | 10 mA, V = 60 mV, V_T = 25 mV: R ≈ 72 Ω | [VERIFICADO] |
| Corto unión pn | Minoritarios 1.445×10⁴ cm⁻³. J_dif = 750 A/cm². τ = 14.8 µs. Con 10¹⁶/10¹⁸: n_p = 2.25×10⁴ cm⁻³, p_n = 225 cm⁻³, V_bi ≈ 0.81 V, W ≈ 0.33 µm | [VERIFICADO] |

### 5.6 MOSFET

| Problema | Datos clave | Respuestas | Estado |
|---|---|---|---|
| 2024 P4 | Curva (2.5 V; 0.8 mA) y (5 V; 6.6 mA), R_D = 1.1 kΩ, −1.5 ≤ V_IN ≤ 1.5 V | V_t = 1.16 V, K_N = 0.90 mA/V². V_G,min = 2.66 V. V_DD,min = 17.9 V. Con 20 V: I_D = 6.64 mA en saturación. Con 10 V: **triodo**, V_DS = 3.03 V, I_D = 6.34 mA | [OFICIAL] [VERIFICADO] |
| 2014 P5 | K_N = 1 mA/V², V_t = 1 V, R_L = 1 kΩ, −1 ≤ V_IN ≤ 1 V | V_G,min = 2 V, V_DD,min = 16.5 V, I_D = 8 mA con 20 V. Con 4 V: triodo, V_DS = 0.877 V, I_D = 3.12 mA | [OFICIAL] [VERIFICADO] |
| 2021 P4 | Conectado como diodo, V_DD = 10 V: 1.2 kΩ → 4.14 V y 2.7 kΩ → 3.28 V | V_t = 1.14 V, K_N = 1.08 mA/V² | [VERIFICADO] |
| 2021 P5 | V_G = 5 V, fuente en V_i, R_D = 2.7 kΩ, V_DD = 10 V | Triodo 0–1.81 V, saturación 1.81–3.86 V, corte > 3.86 V | [VERIFICADO], corrige la fuente |
| 2023 P4a | Curvas: 12.0 mA con 5 V, unos 3.65 mA con 3 V, a V_DS = 5 V | V_t ≈ 0.54 V (0.50–0.58 según lectura), K_N ≈ 1.21 mA/V² | [VERIFICADO], [AMBIGUO] por la lectura |
| 2023 P4b | 850 k/650 k, V_DD = 15 V, R_D = 2.2 kΩ, R_S = 2 kΩ | V_G = 6.5 V, V_GS = 2.39 V, I_D = 2.06 mA, V_DS = 6.36 V, saturación | [VERIFICADO] |
| 2023 P4c | M3 con compuerta en −10 V | M3 en corte. **V_OUT = −10 V**. M1: 5.05 mA, V_GS = 3.43 V | [VERIFICADO] |
| 2023R P4a | CD4007: K_N = 1.1, V_t = 1.4 V, 700 k/800 k, R_D = R_S = 3 kΩ, V_DD = 15 V | V_G = 8 V, I_D = 1.627 mA, V_GS = 3.12 V, V_DS = 5.24 V | [OFICIAL] [VERIFICADO] |
| 2023R P4b | Espejo PMOS con K_P = 0.7, R_B = 12 kΩ; M1 con R_G entre G y D | V_SG3 = 3.08 V, I_D = 0.993 mA, V_GS1 = V_DS1 = 2.74 V. M2 saturado: 12.26 V > 1.68 V | [OFICIAL] [VERIFICADO] |

---

## 6. Errores conocidos en las fuentes

| Documento | Error | Correcto |
|---|---|---|
| `99_Duplicados_y_Otros/guia-problemas-resueltos…` | Usa `I_D = K_N·V_OV²` y obtiene 13.27 mA en el MOSFET de 2024 | Con la regla 1: 6.64 mA |
| La misma guía | Dice que con V_DD = 10 V el transistor está "acercándose al borde de triodo" | Está en triodo: V_DS = 3.03 V < V_OV = 3.84 V |
| `99_Duplicados_y_Otros/guia-teorica…` | Define `K_n = ½·k'_n·W/L` | Contradice la convención del profesor. Usar la regla 1 |
| `2021 - Parcial con solucion de estudiante.pdf`, P5 | Tabla con saturación para 0–1.81 V y triodo para 1.81–3.86 V | Está invertida: triodo 0–1.81 V y saturación 1.81–3.86 V |
| `2014 - Parcial con solucion.pdf`, P1 | Escribe "+ 1 V" al final de la recta para V_i > 1.7 V | Debe ser + 1.7 V para que la curva sea continua |
| `2024 - Parcial con respuestas oficiales.pdf` | Valores redondeados: 6.61 mA y 6.32 mA | Sin redondeo: 6.64 mA y 6.34 mA. La diferencia es solo de redondeo |

---

## 7. Estructura obligatoria de resolución

Actúa como profesor experto en análisis de circuitos (ELC-115). Toda solución, tuya o de una IA, se divide en **pasos**, y **cada paso** sigue estos cinco puntos, en este orden. Las guías 01 a 04 están escritas exactamente así.

1. **Nombre del paso e identificación de la técnica.** Un título descriptivo y la ley o método usado: *LVK*, *LCK*, *Ley de Ohm*, *divisor de tensión*, *Thévenin*, *superposición*, *transformación de fuentes*, *método de estados supuestos*, *modelo ideal*, *modelo de caída constante*, *modelo lineal por tramos*, *análisis de pequeña señal*, *ecuación de saturación o de triodo*, *espejo de corriente*, etc.
2. **¿Se redibuja el circuito?** Decir explícitamente **Sí** o **No**. Si es sí, enumerar cada reemplazo:
   - Diodo en conducción (ON) → batería V_D (más r_D si el modelo la tiene); con modelo ideal, corto.
   - Diodo en corte (OFF) → **circuito abierto**: se borra la rama.
   - Zener en ruptura → batería V_Z0 en serie con r_z. Zener sin llegar a ruptura → abierto.
   - MOSFET en saturación → fuente de corriente ½·K_N·V_OV² entre D y S. En triodo → elemento I_D = K_N[V_OV·V_DS − ½V_DS²]. En corte → abierto. La compuerta siempre es un abierto (I_G = 0).
   - Condensador en DC → abierto. Condensador grande en pequeña señal → corto. Condensador sin camino de descarga → batería con la tensión a la que se cargó.
   - Pequeña señal: fuente DC de tensión → corto a tierra; fuente DC de corriente → abierto; diodo → r_d = nV_T/I_D.
   - Thévenin o simplificaciones: indicar los nodos de corte y los elementos que se desprecian (y por qué).
3. **Ilustración en arte ASCII.** Si el paso redibuja, mostrar el circuito equivalente en ASCII. Si se analiza una señal, dibujar la forma de onda, la característica de transferencia o la recta de carga (punto Q) en ASCII. Símbolos: `--/\/\/--` resistencia, `-->|--` diodo (ánodo → cátodo), `-->|Z-` Zener, `--||--` condensador, `(+ V -)` fuente DC, `(~ vs)` fuente senoidal, `(^ I)` fuente de corriente, `o   o` rama abierta, `-)-` cruce sin conexión, `GND` tierra. Verticales: `\ /` sobre `---` es un diodo que conduce hacia abajo; `---` sobre `/ \` conduce hacia arriba.
4. **Planteamiento matemático.** Primero la ecuación simbólica o general; después la sustitución numérica **con unidades** (V, A, Ω, F, Hz, s); después el despeje paso a paso, sin saltar operaciones intermedias.
5. **Resultado del paso**, destacado en negrita, con unidad y 3 cifras significativas.

### 7.1 Reglas de conducta y estilo

- **Cero ambigüedad en diodos.** Nunca afirmar que los 4 diodos de un puente conducen a la vez. Decir qué par conduce (ON) y qué par está abierto (OFF) en cada semiciclo. Con la numeración de las guías: semiciclo positivo → D1 y D2 ON, D3 y D4 OFF; semiciclo negativo → D3 y D4 ON, D1 y D2 OFF. Si la figura numera distinto, seguir la figura y decirlo.
- **Verificar cada suposición.** Diodo ON con I_D > 0; diodo OFF con V_A − V_K < V_D; MOSFET con la condición de su región. Si falla, se cambia la suposición y se redibuja; nunca se "corrige" un signo.
- **Simbolismo claro.** Variables con subíndices explícitos: V_s,pico, I_pico, R_L, V_Z0, V_OV. En texto plano usar guion bajo; en documentos, subíndices.
- **Explicar los errores comunes.** Si la pregunta es sobre un procedimiento ("¿por qué no reemplacé X?"), explicar primero la razón teórica y después corregir el circuito.
- **Cerrar con la respuesta por literal** y una frase de interpretación física (qué significa y qué cambiaría si cambia un dato).

---

## 8. Lista de autoverificación antes de responder

- [ ] ¿Usé ½·K_N en saturación?
- [ ] ¿Verifiqué la región del MOSFET o el estado de cada diodo?
- [ ] ¿Usé el V_D que pide el enunciado?
- [ ] ¿Convertí Vrms a valor pico donde correspondía?
- [ ] ¿Usé 2V_D en el puente y 1 V_D en media onda o derivación central?
- [ ] ¿Apliqué la corrección por ΔT cuando V_r supera un 10 % de V_p?
- [ ] ¿Dije qué fórmula usé para la corriente pico?
- [ ] ¿Descarté la raíz imposible de la cuadrática y expliqué por qué?
- [ ] ¿Cada respuesta tiene unidad y está en el literal correcto?
- [ ] ¿El orden de magnitud coincide con una variante del banco?
- [ ] ¿Respondí las preguntas de opinión con SÍ/NO y una razón numérica?
- [ ] ¿Cada paso dice la técnica, si se redibuja, y tiene su dibujo ASCII cuando cambia el circuito?
- [ ] ¿En el puente dije qué par de diodos conduce en cada semiciclo?

---

## 9. Mensaje sugerido para usar con una IA

Copia este texto al inicio de la conversación y adjunta este archivo:

```
Eres tutor de Electrónica 1 (ELC-115, UES, Prof. José Ramos López).
Antes de resolver, lee el archivo INSTRUCTIVO_RESOLUCION_PROBLEMAS.md que adjunto
y cumple todas las reglas marcadas [REGLA].
En particular:
- MOSFET: I_D = ½·K_N·(V_GS − V_t)² con K_N = k'n·W/L. Verifica siempre la región.
- Diodos: usa exactamente el modelo y el V_D del enunciado.
- Rectificadores: aplica la corrección de V_r por T/2 − ΔT cuando el rizado es grande,
  e indica qué fórmula usas para la corriente pico.
- Si el problema es una variante de la sección 5, compara tu resultado con el banco
  y explica cualquier diferencia.
- Si no puedes leer un dato de la figura, dilo; no lo inventes.
Resuelve con la ESTRUCTURA OBLIGATORIA de la sección 7: en cada paso da
(1) nombre y técnica, (2) ¿se redibuja? con cada reemplazo, (3) dibujo ASCII del
equivalente o de la forma de onda, (4) ecuación simbólica -> sustitución con unidades
-> despeje, (5) resultado en negrita. En puentes, di qué par de diodos conduce.
Termina con la lista de la sección 8.
Problema:
<pega aquí el enunciado y describe o adjunta la figura>
```
