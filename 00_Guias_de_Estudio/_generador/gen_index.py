import os, unicodedata, urllib.parse, html
ROOT = "/home/kioryu/Descargas/Electronica1 - P1"
N = lambda s: unicodedata.normalize("NFC", s).lower()
import json
MOVES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "movimientos.json"), encoding="utf-8"))
FILES = {}
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        rel = os.path.relpath(os.path.join(dp, f), ROOT)
        FILES[N(rel)] = rel

def L(path, page=None):
    np_ = N(path)
    if np_.startswith(N("Guias_Estudio_Parcial1/")):
        np_ = N("00_Guias_de_Estudio/") + np_[len("guias_estudio_parcial1/"):]
    np_ = N(MOVES.get(unicodedata.normalize("NFC", path), path)).lower() if unicodedata.normalize("NFC", path) in MOVES else np_
    real = FILES.get(np_)
    if real is None:
        raise SystemExit("FALTA: " + path)
    u = urllib.parse.quote(real)
    return u + (f"#page={page}" if page else "")

G = "00_Guias_de_Estudio/"
def guide(n, anchor=""):
    names = {0: "00_Plan_de_Estudio", 1: "01_Guia_Diodos_Fisica_y_Modelos", 2: "02_Guia_Rectificadores_Zener_Recortadores",
             3: "03_Guia_MOSFET", 4: "04_Prediccion_y_Problemas_Resueltos"}
    return L(G + names[n] + ".html") + (("#" + anchor) if anchor else "")
def img(p):
    return urllib.parse.quote(G + "img/" + p + ".png")
esc = html.escape

# ---------------- datos ----------------
PROBS = [  # (n, titulo, prob, nivel, tema, parcial_archivo)
 (1, "Puente con condensador y corrección por ΔT", 70, "alta", "rect", "2023 P3 · 2023R P3"),
 (2, "MOSFET con la señal en la fuente: VG,min, VDD,min, ID en triodo", 55, "alta", "mosdc", "2024 P4 · 2014 P5"),
 (3, "Cargador de batería con puente, R y batería", 50, "alta", "carg", "2023 P1"),
 (4, "Recortador con dos diodos y fuentes, entrada triangular", 45, "alta", "recort", "2024 P1 · 2013 P5"),
 (5, "Vt y KN medidos y regiones contra Vi", 45, "alta", "mosdc", "2021 P4 y P5"),
 (6, "NMOS con divisor y RS, lectura de curvas", 45, "alta", "mosdc", "2023 P4 · 2023R P4a"),
 (7, "Diseño de una fuente con puente", 40, "media", "rect", "2017 P2"),
 (8, "Cargador con condensador: elegir Vs y eficiencia", 40, "media", "carg", "2023R P1"),
 (9, "Cargador con fuente de corriente", 35, "media", "carg", "2025 P1"),
 (10, "Dos diseños de regulador shunt con el 1N5235", 35, "media", "zener", "2025 P2 · nota7 P3"),
 (11, "Tabla de la fuente del laboratorio y hueco de tensión", 35, "media", "rect", "2024 P2 y P3"),
 (12, "Transferencia de puente de diodos con Zener", 30, "media", "recort", "2017 P3 · repe P4"),
 (13, "Espejo PMOS y circuito trampa", 30, "media", "mosdc", "2023R P4b · 2023 P4c"),
 (14, "Foco incandescente con diodo ahorrador", 30, "media", "carg", "2023 P2 · 2023R P2"),
 (15, "Transferencia con ramas resistivas", 30, "media", "recort", "2021 P1 · 2014 P1"),
 (16, "Rizado de 4.5 % y 1.25 % en un puente", 25, "baja", "rect", "nota7 P4"),
 (17, "Sujetador con diodo y Zener", 20, "baja", "recort", "2021 P3"),
 (18, "Tres diodos en DC", 20, "baja", "ideal", "2017 P1"),
 (19, "Unión pn y corto", 15, "baja", "fisica", "2017 P4 · Corto"),
]

P = "Parciales_anteriores/"
EXAMS = [  # (año, archivo, solucion, temas, nota)
 ("2025", P+"fusil20252.jpeg", None, "Cargador con fuente de corriente · regulador shunt 1N5235", "Solo la primera hoja. Resueltos en problemas 9 y 10."),
 ("2024", "DOCUMENTO 20 SEPTIEMBRE 2024.pdf", "examen 1 comentado.pdf", "Recortador con triangular · fuente del lab · hueco de tensión · MOSFET CD4007", "Solución oficial solo con respuestas."),
 ("2023 repetido", P+"EXAMEN REPETIDO 1 ELC-115 2023 COMENTADO.pdf", P+"EXAMEN REPETIDO 1 ELC-115 2023 COMENTADO.pdf", "Cargador con C · foco + diodo · puente con PF · divisor y espejo PMOS", "Solución oficial en Mathcad dentro del mismo PDF."),
 ("2023", P+"EXAMEN 1 ELC-115 2023.pdf", None, "Cargador puente · foco + diodo · corrección por ΔT · MOSFET con curvas", "Resuelto en problemas 1, 3, 6, 13 y 14."),
 ("2021", P+"96e76ab7-5148-4531-a108-f4bd23429d25 (1).pdf", P+"96e76ab7-5148-4531-a108-f4bd23429d25 (1).pdf", "Transferencia · rectificador con batería · sujetador Zener · Vt y KN · regiones", "Solución de un estudiante; la tabla del P5 está invertida."),
 ("2017 V1", P+"EXAMEN 1 ELC-115 2017 V1 (1).pdf", P+"EXAMEN 1 ELC-115 2017 V1 (1).pdf", "3 diodos · diseño de fuente · puente + Zener · unión pn", "Con respuestas oficiales."),
 ("2017 V2", P+"EXAMEN 1 ELC-115 2017  V2.pdf", P+"EXAMEN 1 ELC-115 2017  V2.pdf", "Igual que V1 con otros números", "Con respuestas oficiales."),
 ("≈2018–2020", P+"Solucion P1 ELC-115 nota7.pdf", P+"Solucion P1 ELC-115 nota7.pdf", "Dos diodos y área · pequeña señal · 1N5235 · rizado 4.5 % y 1.25 %", "Solución de un estudiante con nota 7."),
 ("Repetido sin fecha", P+"repe.pdf", None, "3 diodos · temperatura · fuente partida con 1N4742 · puente + Zener", "Sin solución."),
 ("≈2015–2016", P+"examen1-elc115_compress.pdf", None, "Corrientes del transformador · doblador · diferenciador", "Sin solución."),
 ("2014", P+"examen 1 elc 115 2014.pdf", P+"examen 1 elc 115 2014.pdf", "Transferencia · fallas en puente · iterativo · Zener 1N4733A · MOSFET", "Con solución; tipeo en P1: +1 V debe ser +1.7 V."),
 ("2013", P+"EXAMEN 1 ELC-115 2013.pdf", P+"EXAMEN 1 ELC-115 2013.pdf", "Puente con generador · resistencia de 50 Ω · Zener 1N4733A · recortador", "Con solución."),
 ("Corto unión pn", P+"Corto union PN.pdf", P+"Solu corto union PN.pdf", "Portadores, difusión, V0 y W", "Solución manuscrita."),
]

TOPICS = [
 dict(id="fisica", t="Física del semiconductor y unión pn", pr="baja", prob=15, g=(1, "s1"),
      k="semiconductor intrinseco dopado portadores difusion desplazamiento deriva union pn potencial contacto V0 agotamiento W campo Emax einstein",
      res="Portadores, dopado, corrientes de difusión y desplazamiento, y la unión pn en equilibrio, directa e inversa. En el parcial solo salió en 2017; suele ir en un corto aparte.",
      f=["V0 = VT·ln(NA·ND/ni²)", "W = √[(2εs/q)(1/NA+1/ND)(V0+VR)]", "Emax = 2(V0+VR)/W", "pn = ni²/ND · τ = L²/D"],
      imgs=[("clase/union_pn", "Unión pn en circuito abierto"), ("clase/pn_directa", "Polarización directa"), ("clase/pn_inversa", "Polarización inversa")],
      mat=[("FUNCIONAMIENTO FÍSICO DE DIODOS.pdf", "Lección: semiconductores y unión pn"), ("GUÍA DE ESTUDIO QUE ACOMPAÑA LOS VIDEOS DEL TEMA “PRINCIPIO DE FUNCIONAMIENTO DE CELDA SOLAR BASADA EN SEMICONDUCTORES”.pdf", "Guía de videos: celda solar y semiconductores"), (P+"Corto union PN.pdf", "Corto de unión pn"), (P+"Solu corto union PN.pdf", "Solución del corto")]),
 dict(id="ideal", t="Diodo ideal y análisis por estados", pr="media", prob=25, g=(1, "s2"),
      k="diodo ideal caida constante lineal por tramos suponer estados ON OFF varios diodos media onda compuerta OR",
      res="Modelos ideal, de caída constante y lineal por tramos. Método de suponer estados y verificar. Base de todos los problemas de diodos.",
      f=["ON: I > 0 · OFF: V < VD0", "Media onda: Iprom = Vp/(πR) · Irms = Vp/(2R)", "Conduce entre θ = arcsen(VD/Vp) y π − θ"],
      imgs=[("clase/diodo_ideal", "Diodo ideal"), ("clase/rectificador_ideal", "Rectificador con diodo ideal"), ("clase/ej31_cargador", "Ejemplo 3.1: cargador de 12 V"), ("f17_p1", "Parcial 2017 P1: tres diodos")],
      mat=[("DIODOS IDEALES LECCIÓN 24 JULIO 2023.pdf", "Lección: diodo ideal"), ("DIODOS APLICACIONES PARTE 1.pdf", "Aplicaciones de diodos, parte 1"), ("DISCUSION DE PROBLEMAS DIODO MODELO IDEAL.pdf", "Discusión de problemas con modelo ideal"), ("PROBLEMAS 4 y 9.pdf", "Problemas 4 y 9 resueltos"), ("problemas 11-23.pdf", "Enunciados de problemas 11 a 23")]),
 dict(id="real", t="Diodo real: exponencial, temperatura y pequeña señal", pr="baja", prob=15, g=(1, "s3"),
      k="exponencial shockley IS VT iterativo temperatura 2 mV area pequeña señal rd atenuador logaritmico",
      res="Ecuación exponencial, análisis iterativo y gráfico, efecto de la temperatura y del área, y modelo de pequeña señal. Salió en parciales antiguos, no en los recientes.",
      f=["i = IS·e^(v/nVT)", "ΔV = nVT·ln(I2/I1) ≈ 60 mV/década", "dV/dT ≈ −2 mV/°C", "rd = nVT/ID"],
      imgs=[],
      mat=[("DIODO DE UNIÓN LECCIÓN 26 JULIO 2023.pdf", "Lección: diodo de unión"), ("Diodos Características i-v.pdf", "Características i-v"), ("PROBLEMAS 27 Y 30.pdf", "Problemas 27 y 30: área y temperatura"), ("PROBLEMAS 35 Y 48.pdf", "Problemas 35 y 48: iterativo y pequeña señal"), ("PROBLEMAS 50 Y 59.pdf", "Problemas 50 y 59: atenuador y Zener"), ("LABORATORIO 1 ELC-115 2025.pdf", "Laboratorio 1: amplificador logarítmico y fuentes")]),
 dict(id="rect", t="Rectificadores y fuentes con filtro capacitivo", pr="muy alta", prob=90, g=(2, "s2"),
      k="rectificador media onda onda completa puente derivacion central condensador filtro rizado Vr delta T conduccion corriente pico PIV potencia factor de potencia diseño fuente transformador hueco",
      res="El tema más evaluado: salió en todos los parciales. Rizado, tiempo de conducción, corrección por ΔT, corriente pico, potencia, factor de potencia y diseño completo de una fuente.",
      f=["Vr = Vp/(2fRC) = IL/(2fC)", "Vdc = Vp − Vr/2", "ωΔT = √(2Vr/Vp)", "Corregido: Vr = (Vp/RC)(T/2 − ΔT)", "Ipico ≈ Idc·T/ΔT", "Iac = Ip√(2ΔT/3T) · PF = P/S"],
      imgs=[("clase/fuente_bloques", "Bloques de un alimentador DC"), ("clase/puente", "Rectificador puente"), ("clase/onda_completa_tap", "Onda completa con derivación central"), ("f23_p3", "Parcial 2023 P3"), ("g23_p3", "Rizado y pulsos de corriente simulados"), ("f17_p2", "Parcial 2017 P2: diseño")],
      mat=[("DIODO ZENER Y CIRCUTOS RECTIFICADORES.pdf", "Lección: rectificadores (desde la diapositiva 12)", 12), ("PROBLEMAS 76 Y 77 i.pdf", "Problemas 76 y 77: rectificador complementario"), ("LABORATORIO 1 ELC-115 2025.pdf", "Laboratorio 1")]),
 dict(id="carg", t="Cargadores de batería y cargas especiales", pr="alta", prob=70, g=(2, "s3"),
      k="cargador bateria tiempo de carga amperio hora eficiencia fuente de corriente foco lampara incandescente ahorrador 1N4004 rms promedio",
      res="Salió en los cuatro parciales más recientes que tienen cargador: batería con R, con condensador y con fuente de corriente. También el foco con diodo en serie.",
      f=["θ1 = arcsen((nVD + VB)/Vs)", "Iprom = [2Vs·cosθ1 − (nVD+VB)(π − 2θ1)]/(πR)", "t = Ah/Iprom · η = VB·I/Pentrada", "Foco: R = V²/P, media onda da P/2"],
      imgs=[("f23_p1", "Parcial 2023 P1"), ("f25_p1", "Parcial 2025 P1"), ("g25_p1", "Corriente de batería del 2025 P1"), ("clase/ej31_cargador", "Ejemplo 3.1"), ("f23_p2", "Parcial 2023 P2: foco")],
      mat=[("DIODOS IDEALES LECCIÓN 24 JULIO 2023.pdf", "Ejemplo 3.1: cargador con diodo (diapositiva 17)", 17), ("DIODOS APLICACIONES PARTE 1.pdf", "Aplicación: cargador de celular")]),
 dict(id="zener", t="Diodo Zener y regulador shunt", pr="alta", prob=55, g=(2, "s4"),
      k="zener regulador shunt regulacion de linea regulacion de carga VZ0 rz IZK IZT 1N5235 1N4733A 1N4742 potencia",
      res="Modelo del Zener, diseño de la resistencia serie, regulación de línea y de carga, potencia máxima y rizado a la salida del regulador.",
      f=["VZ0 = VZT − IZT·rz", "Reg. línea = rz/(R + rz)", "Reg. carga = −(rz ∥ R)", "Rmax = (VSmin − VZ0 − rz·IZK)/(ILmax + IZK)"],
      imgs=[("clase/zener_iv", "Característica del Zener"), ("clase/zener_ej38", "Ejemplo 3.8: regulador shunt")],
      mat=[("DIODO ZENER Y CIRCUTOS RECTIFICADORES.pdf", "Lección: Zener (diapositivas 1 a 11)", 1), ("PROBLEMAS 50 Y 59.pdf", "Problema 59: especificaciones de Zener")]),
 dict(id="recort", t="Recortadores, transferencia y sujetadores", pr="alta", prob=60, g=(2, "s5"),
      k="recortador limitador caracteristica de transferencia vo vi triangular senoidal pendiente sujetador fijador restaurador dc doblador puente zener",
      res="Trazar vo contra vi con puntos de quiebre y pendientes, luego dibujar la salida para una onda triangular o senoidal. Incluye sujetadores y dobladores.",
      f=["Quiebre: fuente de la rama + VD", "Pendiente: Rrama/(R + Rrama)", "Puente + Zener: ±(2VD0 + VZ0)", "Sujetador: promedio = −(Vp − Vlímite)"],
      imgs=[("f24_p1", "Parcial 2024 P1"), ("g24_p1", "Salida del 2024 P1"), ("f21_p1", "Parcial 2021 P1"), ("f17_p3", "Parcial 2017 P3"), ("clase/sujetador", "Sujetador"), ("clase/doblador", "Doblador de tensión")],
      mat=[("DISCUSIÓN DE CIRCUITOS CON DIODOS Y CONDENSADORES.pdf", "Sujetadores y dobladores"), ("PROBLEMA 88 i.pdf", "Problema 88: transferencia de dos circuitos unidos"), ("DISCUSION DE PROBLEMAS DIODO MODELO IDEAL.pdf", "Problema 4: formas de onda")]),
 dict(id="mosfet", t="MOSFET: estructura, ecuaciones y regiones", pr="muy alta", prob=85, g=(3, "s1"),
      k="mosfet nmos pmos enriquecimiento canal umbral Vt sobretension VOV triodo saturacion corte KN kn rDS estrangulamiento lambda",
      res="Cómo se forma el canal, las tres regiones y sus ecuaciones. Atención a la convención del profesor: ID = ½·KN·VOV² con KN = k′n·W/L.",
      f=["VOV = VGS − Vt", "Saturación: ID = ½KN·VOV², VDS ≥ VOV", "Triodo: ID = KN(VOV·VDS − ½VDS²)", "rDS = 1/(KN·VOV)"],
      imgs=[("clase/nmos_estructura", "Estructura del NMOS"), ("clase/mos_simbolos", "Símbolos"), ("clase/nmos_regiones", "Triodo y saturación"), ("clase/nmos_caracteristicas", "Características iD-vDS"), ("clase/nmos_id_vgs", "iD contra vGS")],
      mat=[("MOSFET´S Lecciones semana 1 2022.pdf", "Lecciones semana 1 (2022)"), ("MOSFET Lecciones Semana 1 con anotaciones.pdf", "Lecciones semana 1 con anotaciones"), ("CORRIENTE DE DRENAJE.pdf", "Deducción de la corriente de drenaje"), ("PROBLEMAS MOSFET PARTE II.pdf", "Problemas 16 a 21: características i-v")]),
 dict(id="mosdc", t="MOSFET: circuitos en DC", pr="muy alta", prob=85, g=(3, "s4"),
      k="mosfet dc polarizacion divisor RS RD punto Q conectado como diodo espejo de corriente PMOS CD4007 medir Vt KN curvas VDD minimo VG minimo regiones",
      res="Aparece en todos los parciales desde 2021, casi siempre con el CD4007. Obtener Vt y KN, resolver el punto Q, verificar la región y encontrar límites de operación.",
      f=["r = √(I1/I2) · Vt = (r·VGS2 − VGS1)/(r − 1)", "VG = VGS + ID·RS", "VDD,min = VG − Vt + ID,max·RD", "Frontera: VD = VG − Vt"],
      imgs=[("f24_p4", "Parcial 2024 P4"), ("f21_p4", "Parcial 2021 P4"), ("f21_p5", "Parcial 2021 P5"), ("g21_p5", "ID contra Vi"), ("f23r_p4", "Parcial 2023R P4"), ("f23_p4c", "Parcial 2023 P4c"), ("clase/mos_ej4_diodo", "Transistor conectado como diodo")],
      mat=[("MOSFETs EJEMPLOS 12 septiembre.pdf", "Ejemplos resueltos en clase"), ("PROBLEMAS DE CIRCUITOS CON MOSFETS EN DC.pdf", "Problemas 44 a 52: circuitos en DC"), ("LABORATORIO INTRODUCCIÓN A CMOS 2024 v2.pdf", "Laboratorio CD4007")]),
]
PR_CLASS = {"muy alta": "p4", "alta": "p3", "media": "p2", "baja": "p1"}

REF = [("Circuitos Microelectrónicos - Sedra & Smith 5ed (solucionario).pdf.pdf", "Solucionario Sedra 5.ª ed. (libro del curso): capítulo 3 Diodos, problemas, desde la pág. 61", 61),
       ("Circuitos Microelectrónicos - Sedra & Smith 5ed (solucionario).pdf.pdf", "Solucionario Sedra 5.ª ed.: capítulo 4 MOSFET, problemas, desde la pág. 118 aprox.", 118),
       ("Microelectronics Circuits (6th) Edition Sedra Smith SOL MANUAL.pdf", "Manual Sedra 6.ª ed.: ejercicios cap. 3 Semiconductores (pág. 22)", 22),
       ("Microelectronics Circuits (6th) Edition Sedra Smith SOL MANUAL.pdf", "Manual Sedra 6.ª ed.: ejercicios cap. 4 Diodos (pág. 30)", 30),
       ("Microelectronics Circuits (6th) Edition Sedra Smith SOL MANUAL.pdf", "Manual Sedra 6.ª ed.: ejercicios cap. 5 MOSFET (pág. 44)", 44),
       ("Microelectronics Circuits (6th) Edition Sedra Smith SOL MANUAL.pdf", "Manual Sedra 6.ª ed.: problemas cap. 3 Semiconductores (pág. 189); el archivo termina ahí", 189),
       ("appendix_L.pdf", "Respuestas a problemas seleccionados del Sedra"),
       ("TÓPICOS ESENCIALES EN LTSPICE VF.pdf", "Tópicos esenciales en LTspice"),
       ("LABORATORIO 1 ELC-115 2025.pdf", "Laboratorio 1 (2025)"),
       ("LABORATORIO INTRODUCCIÓN A CMOS 2024 v2.pdf", "Laboratorio de introducción a CMOS (2024)"),
       ("99_Duplicados_y_Otros/guia-teorica-y-formulario-parcial1-electronica.pdf", "Guía teórica previa (convención de KN distinta)"),
       ("99_Duplicados_y_Otros/guia-problemas-resueltos-parcial1-electronica.pdf", "Guía de problemas previa (tiene un error en el MOSFET)")]

# ---------------- html ----------------
o = []
w = o.append
def pdfico(path):
    return "IMG" if path.lower().endswith((".jpeg", ".jpg", ".png")) else ("HTML" if path.endswith(".html") else "PDF")

for tp in TOPICS:
    probs = [p for p in PROBS if p[4] == tp["id"]]
    w(f'<section class="topic" id="t-{tp["id"]}" data-topic="{tp["id"]}">')
    w(f'<header class="th"><h2>{esc(tp["t"])}</h2><span class="pri {PR_CLASS[tp["pr"]]}">Prioridad {tp["pr"]} · {tp["prob"]} %</span></header>')
    w(f'<p class="res item" data-k="{esc(tp["k"])}">{esc(tp["res"])}</p>')
    w('<div class="cols">')
    w('<div class="col">')
    w(f'<h3>Fórmulas clave</h3><ul class="fl">' + "".join(f'<li class="item"><code>{esc(x)}</code></li>' for x in tp["f"]) + '</ul>')
    gn, ga = tp["g"]
    w(f'<h3>Guía de estudio</h3><ul class="links"><li class="item" data-k="{esc(tp["k"])} guia teoria"><a href="{guide(gn, ga)}"><span class="ft">HTML</span>Guía 0{gn}: {esc(tp["t"])}</a></li></ul>')
    w('<h3>Material de la plataforma</h3><ul class="links">')
    for m in tp["mat"]:
        path, label = m[0], m[1]; page = m[2] if len(m) > 2 else None
        w(f'<li class="item" data-k="{esc(tp["k"])} {esc(path)}"><a href="{L(path, page)}"><span class="ft">{pdfico(path)}</span>{esc(label)}</a><span class="fn">{esc(os.path.basename(path))}</span></li>')
    w('</ul>')
    if probs:
        w('<h3>Problemas resueltos de parciales</h3><ul class="links">')
        for n, t, pr, lv, _, src in probs:
            w(f'<li class="item" data-k="{esc(tp["k"])} {esc(src)} problema resuelto"><a href="{guide(4, "p"+str(n))}"><span class="lv {lv}">{pr} %</span>{n}. {esc(t)}</a><span class="fn">{esc(src)}</span></li>')
        w('</ul>')
    w('</div>')
    if tp["imgs"]:
        w('<div class="col"><h3>Circuitos de ejemplo</h3><div class="thumbs">')
        for p, c in tp["imgs"]:
            w(f'<figure class="item" data-k="{esc(tp["k"])} circuito figura"><button class="zoom" data-src="{img(p)}" data-cap="{esc(c)}" aria-label="Ampliar {esc(c)}"><img loading="lazy" src="{img(p)}" alt="{esc(c)}"></button><figcaption>{esc(c)}</figcaption></figure>')
        w('</div></div>')
    w('</div></section>')
TOPIC_HTML = "\n".join(o)

o = []
for n, t, pr, lv, tid, src in PROBS:
    tt = next(x["t"] for x in TOPICS if x["id"] == tid)
    o.append(f'<tr class="item" data-k="{esc(tt)} {esc(src)}"><td><span class="lv {lv}">{pr} %</span></td><td><a href="{guide(4, "p"+str(n))}">{n}. {esc(t)}</a></td><td>{esc(src)}</td><td><a href="#t-{tid}">{esc(tt)}</a></td></tr>')
PROB_HTML = "\n".join(o)

o = []
for y, f, s, t, nota in EXAMS:
    sol = f'<a href="{L(s)}">Solución</a>' if s else '<span class="muted">—</span>'
    o.append(f'<tr class="item" data-k="parcial examen {esc(y)} {esc(t)}"><td><b>{esc(y)}</b></td><td><a href="{L(f)}"><span class="ft">{pdfico(f)}</span>Enunciado</a></td><td>{sol}</td><td>{esc(t)}<div class="muted">{esc(nota)}</div></td></tr>')
EXAM_HTML = "\n".join(o)

REF_HTML = "\n".join(f'<li class="item" data-k="consulta referencia solucionario sedra libro {esc(r[0])}"><a href="{L(r[0], r[2] if len(r)>2 else None)}"><span class="ft">PDF</span>{esc(r[1])}</a><span class="fn">{esc(r[0])}</span></li>' for r in REF)
REF_HTML = f'<li class="item" data-k="instructivo ia resolver problemas convenciones errores"><a href="{urllib.parse.quote(G + "INSTRUCTIVO_RESOLUCION_PROBLEMAS.md")}"><span class="ft">MD</span>Instructivo para resolver problemas (para ti y para una IA)</a><span class="fn">00_Guias_de_Estudio/INSTRUCTIVO_RESOLUCION_PROBLEMAS.md</span></li>\n' + REF_HTML

GUIDES = [(0, "Plan de estudio", "Orden del material, mapa de parciales y cronograma de 4 días"),
          (1, "Guía 01 · Diodos: física y modelos", "Unión pn, diodo ideal, análisis por estados, modelo exponencial"),
          (2, "Guía 02 · Rectificadores, Zener y recortadores", "El núcleo del parcial, con circuitos de ejemplo"),
          (3, "Guía 03 · MOSFET en DC", "Regiones, extracción de Vt y KN, polarización y espejos"),
          (4, "Guía 04 · Predicción y problemas resueltos", "Probabilidades por tema y 19 problemas resueltos paso a paso")]
names = {0: "00_Plan_de_Estudio", 1: "01_Guia_Diodos_Fisica_y_Modelos", 2: "02_Guia_Rectificadores_Zener_Recortadores", 3: "03_Guia_MOSFET", 4: "04_Prediccion_y_Problemas_Resueltos"}
GUIDE_HTML = "\n".join(f'<div class="gcard item" data-k="guia {esc(d)}"><a class="gt" href="{guide(n)}">{esc(t)}</a><p>{esc(d)}</p><div class="gl"><a href="{guide(n)}">Abrir HTML</a><a href="{L(G+names[n]+".pdf")}">Abrir PDF</a></div></div>' for n, t, d in GUIDES)

SHORT={"fisica":"Unión pn","ideal":"Diodo ideal","real":"Diodo real","rect":"Rectificadores","carg":"Cargadores","zener":"Zener","recort":"Recortadores","mosfet":"MOSFET: teoría","mosdc":"MOSFET: DC"}
NAV = "".join(f'<a href="#t-{t["id"]}">{SHORT[t["id"]]}</a>' for t in TOPICS)

tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "index_tpl.html"), encoding="utf-8").read()
out = (tpl.replace("{{TOPICS}}", TOPIC_HTML).replace("{{PROBS}}", PROB_HTML).replace("{{EXAMS}}", EXAM_HTML)
          .replace("{{REF}}", REF_HTML).replace("{{GUIDES}}", GUIDE_HTML).replace("{{NAV}}", NAV))
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)
print("ok", len(out))
