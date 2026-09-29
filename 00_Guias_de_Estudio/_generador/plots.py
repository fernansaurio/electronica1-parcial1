"""Formas de onda y curvas en ASCII usadas por las guías. Cada entrada de PLOTS devuelve texto."""
from math import sin, cos, asin, pi, exp, radians, sqrt, log
from ascii_plot import plot

PLOTS = {}


def reg(f):
    PLOTS[f.__name__] = f
    return f


def deg(x):
    return radians(x)


# ---------------------------------------------------------------- guía 01
@reg
def ej31_vs():
    vs = lambda x: 24 * sin(deg(x))
    a = plot([(vs, "*")], 0, 720, -26, 26, W=66, H=15,
             hlines=[(12, "V_B = 12 V")], vlines=[(30, ""), (150, ""), (390, ""), (510, "")],
             yticks=[24, 12, -12, -24], xticks=[(30, "30°"), (150, "150°"), (360, "360°"), (390, "390°"), (510, "510°"), (720, "720°")],
             ytitle="vs (V)", xtitle="wt")
    iD = lambda x: max(24 * sin(deg(x)) - 12, 0) / 100 * 1000
    b = plot([(iD, "#")], 0, 720, 0, 130, W=66, H=6, vlines=[(30, ""), (150, ""), (390, ""), (510, "")],
             yticks=[(120, "120 mA")], xticks=[(30, "30°"), (150, "150°"), (390, "390°"), (510, "510°")],
             ytitle="i_D", xtitle="wt")
    return a + "\n\n" + b + "\n   El diodo solo conduce mientras vs > 12 V (entre las líneas punteadas)."


@reg
def diodo_iv():
    def f(v):
        if v >= 0.3:
            y = 11 * ((v - 0.3) / 0.9) ** 3 - 0.25   # forma estilizada (no a escala)
            return y if y <= 12 else None
        if v <= -5:
            return max(-(-5 - v) * 25, -12)
        return -0.25
    return plot([(f, "*")], -6.5, 1.5, -12, 12, W=64, H=15,
                vlines=[(-5, "")],
                xticks=[(-5, "-V_ZK"), (0.7, "0.7 V")], ytitle="i", xtitle="v",
                notes=["   ruptura (izquierda)  |  inversa: i = -I_S, casi cero  |  directa: exponencial",
                       "   (dibujo estilizado: la escala de tensión no es la real en cada región)"])


@reg
def modelos_iv():
    IS = 1e-15
    ex = lambda v: IS * exp(v / 0.025) * 1e3 if IS * exp(v / 0.025) * 1e3 <= 11 else None
    pwl = lambda v: (v - 0.65) / 10 * 1e3 if 0.65 <= v <= 0.76 else (0 if v < 0.65 else None)
    cd = lambda v: 0 if v < 0.7 else None
    txt = plot([(ex, "*"), (pwl, "o")], 0, 1.0, 0, 11, W=60, H=12,
               vlines=[(0.7, "")], yticks=[(10, "10 mA"), (5, "5 mA")],
               xticks=[(0, "0"), (0.7, "0.7"), (1.0, "1.0 V")], ytitle="i", xtitle="v")
    return txt + ("\n   *  exponencial real (I_S = 1e-15 A)      o  lineal por tramos (V_D0 = 0.65 V, r_D = 10 ohm)"
                  "\n   :  caída constante: vertical en 0.7 V    el eje vertical (v = 0) es el diodo ideal")


@reg
def recta_carga():
    IS = 1e-14
    d = lambda v: IS * exp(v / 0.025) * 1e3 if IS * exp(v / 0.025) * 1e3 < 3.3 else None
    rl = lambda v: (1.5 - v) / 500 * 1e3 if 0 <= v <= 1.5 else None
    return plot([(rl, "o"), (d, "*")], 0, 1.6, 0, 3.3, W=64, H=13,
                hlines=[(1.707, "I_D = 1.71 mA")], vlines=[(0.647, "")],
                yticks=[(3.0, "3 mA"), (1.707, "1.71")],
                xticks=[(0.647, "0.647 V"), (1.5, "V_DD=1.5")], ytitle="i_D", xtitle="v_D",
                notes=["   o  recta de carga i = (1.5 - v)/500      *  curva del diodo      Q = cruce (0.647 V ; 1.71 mA)"])


# ---------------------------------------------------------------- guía 02
@reg
def media_onda():
    Vs = 16.97
    vs = lambda x: Vs * sin(deg(x))
    vo = lambda x: max(Vs * sin(deg(x)) - 0.7, 0)
    return plot([(vs, "."), (vo, "*")], 0, 720, -18, 18, W=66, H=13,
                yticks=[(16.27, "16.27"), (-16.97, "-16.97")], xticks=[(180, "180°"), (360, "360°"), (540, "540°"), (720, "720°")],
                ytitle="v (V)", xtitle="wt",
                notes=["   .  entrada vs (16.97 V pico)     *  salida v_o = vs - 0.7 V en el semiciclo +, 0 en el semiciclo -",
                       "   En el semiciclo - el diodo soporta toda la tensión inversa: PIV = 16.97 V"])


@reg
def onda_completa():
    Vs = 16.97
    vs = lambda x: Vs * sin(deg(x))
    vo = lambda x: max(abs(Vs * sin(deg(x))) - 1.4, 0)
    return plot([(vs, "."), (vo, "*")], 0, 720, -18, 18, W=66, H=13,
                yticks=[(15.57, "15.57"), (-16.97, "-16.97")], xticks=[(180, "180°"), (360, "360°"), (540, "540°"), (720, "720°")],
                ytitle="v (V)", xtitle="wt",
                notes=["   .  entrada vs      *  salida del puente |vs| - 2 V_D  (D1+D2 en los semiciclos +, D3+D4 en los -)"])


def _sim_filtro(Vp, RC, periodos=2.25, n=4000, full=True):
    T = 1 / 60
    pts = []
    v = 0.0
    dt = periodos * T / n
    for k in range(n + 1):
        t = k * dt
        vin = abs(Vp * sin(2 * pi * 60 * t)) if full else max(Vp * sin(2 * pi * 60 * t), 0)
        v = max(vin, v * exp(-dt / RC))
        pts.append((t, vin, v))
    return pts


@reg
def filtro():
    Vp = 10.0
    RC = 0.0233  # rizado exagerado (~30 %) para que se vea en ASCII
    pts = _sim_filtro(Vp, RC)
    T = 1 / 60

    def interp(t, idx):
        k = min(int(t / (2.25 * T) * 4000), 4000)
        return pts[k][idx]
    vin = lambda x: interp(x / 360 * T, 1)
    vo = lambda x: interp(x / 360 * T, 2)
    vmin = min(p[2] for p in pts if p[0] > T / 2)
    a = plot([(vin, "."), (vo, "*")], 0, 810, 0, 11, W=68, H=13,
             hlines=[(10, "V_p"), (vmin, "V_p - V_r")], yticks=[(10, "V_p"), (vmin, "min")],
             xticks=[(90, "90°"), (270, "270°"), (450, "450°"), (630, "630°")], ytitle="v", xtitle="wt")

    def iD(x):
        t = x / 360 * T
        k = min(int(t / (2.25 * T) * 4000), 4000)
        if k == 0:
            return 0
        vin_k, v_k = pts[k][1], pts[k][2]
        return 1.0 if (abs(vin_k - v_k) < 1e-9 and pts[k][2] >= pts[k - 1][2] and x > 60) else 0
    b = plot([(iD, "#")], 0, 810, 0, 1.2, W=68, H=4, yticks=[(1, "i_D")],
             xticks=[(90, "90°"), (270, "270°"), (450, "450°"), (630, "630°")], xtitle="wt")
    return (a + "\n" + b +
            "\n   .  |vs| rectificada     *  v_o con condensador (rizado exagerado para verlo)"
            "\n   Los diodos conducen solo en el tramo de subida justo antes de cada pico (duración ΔT):"
            "\n   ahí aparecen los pulsos de corriente ### ; el resto del tiempo C alimenta sola a la carga.")


@reg
def cargador():
    Vs, Vx = 16.97, 7.7
    v = lambda x: abs(Vs * sin(deg(x)))
    t1 = 27.0
    a = plot([(v, "*")], 0, 360, 0, 18, W=64, H=10, hlines=[(Vx, "2V_D + V_B = 7.7 V")],
             vlines=[(t1, ""), (180 - t1, ""), (180 + t1, ""), (360 - t1, "")], yticks=[(16.97, "16.97")],
             xticks=[(t1, "27°"), (153, "153°"), (207, "207°"), (333, "333°")], ytitle="|vs| (V)", xtitle="wt")
    i = lambda x: max(abs(Vs * sin(deg(x))) - Vx, 0) / 10
    b = plot([(i, "#")], 0, 360, 0, 1.0, W=64, H=6, yticks=[(0.927, "0.927 A")],
             vlines=[(t1, ""), (180 - t1, ""), (180 + t1, ""), (360 - t1, "")], xtitle="wt", ytitle="i_bat")
    return a + "\n\n" + b + "\n   La batería solo recibe corriente mientras |vs| supera 2 V_D + V_B (entre las líneas punteadas)."


@reg
def zener_iv():
    VZ0, rz_vis = 5.0, 0.18  # dibujo estilizado: V_Z0 = 5, pendiente exagerada

    def f(v):
        if v >= 0.3:
            y = 3 * ((v - 0.3) / 0.9) ** 3
            return y if y <= 4 else None
        if v > -VZ0 + 0.25:
            return -0.1
        if v > -VZ0 - 0.25:
            return -0.1 - 1.2 * ((-VZ0 + 0.25 - v) / 0.5) ** 2
        y = -(-v - VZ0) / rz_vis
        return y if y >= -12 else None
    ext = lambda v: -(-v - VZ0) / rz_vis if -VZ0 - 0.5 <= v <= -VZ0 else None
    return plot([(ext, "."), (f, "*")], -7.5, 1.5, -12, 4, W=64, H=15,
                hlines=[(-8, "-I_ZT (punto Q)")], vlines=[(-VZ0 - 8 * rz_vis, ""), (-VZ0, "")],
                xticks=[(-VZ0 - 8 * rz_vis, "-V_ZT"), (-VZ0 + 0.4, "-V_Z0"), (0.7, "0.7")], ytitle="i", xtitle="v",
                notes=["   En ruptura la curva es casi vertical: pendiente = 1/r_z. Su prolongación (....) corta el eje en -V_Z0.",
                       "   El codo está en i = -I_ZK. Dibujo estilizado (la pendiente real es mucho mayor)."])


@reg
def recortador_transf():
    vo = lambda x: min(x, 3.7)
    return plot([(vo, "*")], -10, 10, -10, 5, W=60, H=13, hlines=[(3.7, "v_o = 3.7 V (D ON)")],
                vlines=[(3.7, "")], yticks=[(3.7, "3.7"), (-10, "-10")],
                xticks=[(-10, "-10"), (3.7, "3.7"), (10, "10 V")], ytitle="v_o", xtitle="v_i",
                notes=["   Pendiente 1 (D OFF, v_o = v_i) hasta el quiebre en v_i = 3.7 V; después pendiente 0 (salida plana)."])


@reg
def recortador_t():
    vi = lambda x: 10 * sin(deg(x))
    vo = lambda x: min(10 * sin(deg(x)), 3.7)
    return plot([(vi, "."), (vo, "*")], 0, 720, -11, 11, W=66, H=13,
                hlines=[(3.7, "3.7 V")], yticks=[(10, "10"), (3.7, "3.7"), (-10, "-10")],
                xticks=[(21.7, "21.7°"), (158.3, "158.3°"), (360, "360°"), (720, "720°")], ytitle="v (V)", xtitle="wt",
                notes=["   .  v_i     *  v_o : se recorta arriba de 3.7 V entre 21.7° y 158.3° (arcsen(3.7/10) = 21.7°)"])


@reg
def sujetador():
    Vp = 5.0
    vi = lambda x: Vp * sin(deg(x))

    def vo(x):
        if x <= 180:
            return Vp * sin(deg(x))
        if x <= 270:
            return 0.0
        return Vp * sin(deg(x)) + Vp
    return plot([(vi, "."), (vo, "*")], 0, 900, -5.5, 10.5, W=68, H=15,
                hlines=[(10, "2V_p"), (5, "V_p = promedio")], yticks=[(10, "2Vp"), (5, "Vp"), (-5, "-Vp")],
                vlines=[(270, "")], xticks=[(270, "270°: C cargado"), (630, "630°")], ytitle="v", xtitle="wt",
                notes=["   .  v_i      *  v_o. Hasta 270° el diodo carga el condensador al pico negativo;",
                       "   después v_o = v_i + V_p: la misma senoidal desplazada, entre 0 y 2 V_p."])


# ---------------------------------------------------------------- guía 03
@reg
def mos_familia():
    KN, Vt = 1.0, 1.0

    def curva(VGS):
        Vov = VGS - Vt

        def f(v):
            return KN * (Vov * v - 0.5 * v * v) if v < Vov else 0.5 * KN * Vov ** 2
        return f
    borde = lambda v: 0.5 * KN * v * v if 0.5 * KN * v * v <= 4.8 else None
    return plot([(borde, "."), (curva(2), "*"), (curva(3), "*"), (curva(4), "*")], 0, 6, 0, 5, W=62, H=14,
                hlines=[(4.5, "V_GS = 4 V -> 4.5 mA"), (2, "V_GS = 3 V -> 2 mA"), (0.5, "V_GS = 2 V -> 0.5 mA")],
                yticks=[(4.5, "4.5"), (2, "2"), (0.5, "0.5")], xticks=[(1, "1"), (2, "2"), (3, "3"), (6, "6 V")],
                ytitle="i_D (mA)", xtitle="v_DS",
                notes=["   K_N = 1 mA/V^2, V_t = 1 V.   ....  frontera triodo/saturación: i_D = (1/2) K_N v_DS^2  (v_DS = V_OV)",
                       "   Izquierda de la frontera: TRIODO (curvas que suben).  Derecha: SATURACIÓN (curvas planas)."])


@reg
def mos_idvgs():
    f = lambda v: 0.5 * (v - 1) ** 2 if v > 1 else 0
    return plot([(f, "*")], 0, 4, 0, 4.6, W=48, H=10, yticks=[(4.5, "4.5"), (2, "2"), (0.5, "0.5")],
                xticks=[(1, "V_t=1"), (2, "2"), (3, "3"), (4, "4 V")], ytitle="i_D (mA), saturación", xtitle="v_GS",
                notes=["   Parábola que despega en V_t: i_D = (1/2) K_N (v_GS - V_t)^2.  En corte (v_GS < V_t) i_D = 0."])


# ---------------------------------------------------------------- guía 04
@reg
def p1_rizado():
    Vp, RC = 167.7, 20 * 1e-3
    pts = _sim_filtro(Vp, RC, periodos=2.25)
    T = 1 / 60

    def g(x, idx):
        k = min(int(x / 360 * T / (2.25 * T) * 4000), 4000)
        return pts[k][idx]
    vmin = min(p[2] for p in pts if p[0] > T / 2)
    return plot([(lambda x: g(x, 1), "."), (lambda x: g(x, 2), "*")], 0, 810, 0, 175, W=68, H=13,
                hlines=[(167.7, "V_p = 167.7 V"), (vmin, "mínimo real ~ %.0f V" % vmin)],
                yticks=[(167.7, "167.7"), (vmin, "%.0f" % vmin)],
                xticks=[(90, "90°"), (270, "270°"), (450, "450°"), (630, "630°")], ytitle="v_o (V)", xtitle="wt",
                notes=["   Simulación ideal con V_p = 167.7 V y RC = 20 ms: el rizado real es ~%.0f V." % (Vp - vmin),
                       "   La fórmula tradicional (69.9 V) lo sobreestima; la corregida (49.6 V) se acerca mucho más."])


@reg
def p2_curva():
    Vt, KN = 1.16, 0.90
    f = lambda v: 0.5 * KN * (v - Vt) ** 2 if v > Vt else 0
    return plot([(f, "*")], 0, 5, 0, 7, W=60, H=12, hlines=[(6.6, "(5 V ; 6.6 mA)"), (0.8, "(2.5 V ; 0.8 mA)")],
                vlines=[(2.5, ""), (5, "")], yticks=[(6.6, "6.6"), (0.8, "0.8")],
                xticks=[(1.16, "1.16"), (2.5, "2.5"), (5, "5 V")], ytitle="I_D (mA)", xtitle="V_GS",
                notes=["   Curva de la figura P4a reconstruida con V_t = 1.16 V y K_N = 0.90 mA/V^2: pasa por los dos puntos marcados."])


@reg
def p4_t():
    def tri(x):  # triangular de 5 V pico, periodo 360
        x = x % 360
        if x < 90:
            return 5 * x / 90
        if x < 270:
            return 5 - 10 * (x - 90) / 180
        return -5 + 5 * (x - 270) / 90

    def vo(x):
        v = tri(x) / 2
        return min(max(v, -1.5), 2.0)
    return plot([(tri, "."), (vo, "*")], 0, 720, -5.5, 5.5, W=66, H=15,
                hlines=[(2, "+2 V (D1 ON)"), (-1.5, "-1.5 V (D2 ON)")], yticks=[(5, "5"), (2, "2"), (-1.5, "-1.5"), (-5, "-5")],
                xticks=[(90, "T/4"), (180, "T/2"), (270, "3T/4"), (360, "T")], ytitle="V", xtitle="t",
                notes=["   .  V_S triangular de 5 V pico      *  V_out: sigue V_S/2 y se recorta en +2 V y en -1.5 V",
                       "   Recorte superior: mientras V_S > 4 V (10 % del periodo). Recorte inferior: mientras V_S < -3 V (20 %)."])


@reg
def p4_transf():
    vo = lambda x: min(max(x / 2, -1.5), 2.0)
    return plot([(vo, "*")], -5, 5, -2.5, 2.5, W=56, H=11, hlines=[(2, "+2 V"), (-1.5, "-1.5 V")],
                vlines=[(4, ""), (-3, "")], yticks=[(2, "2"), (-1.5, "-1.5")],
                xticks=[(-5, "-5"), (-3, "-3"), (4, "4"), (5, "5 V")], ytitle="V_out", xtitle="V_S",
                notes=["   Pendiente 1/2 (divisor R1-RL) entre V_S = -3 V y V_S = 4 V; plana fuera de ese intervalo."])


def _id_2021(Vi, Vt=1.14, KN=1.08, VG=5.0, RD=2.7, VDD=10.0):
    VGS = VG - Vi
    if VGS <= Vt:
        return 0.0
    Vov = VGS - Vt
    I = 0.5 * KN * Vov ** 2
    VDS = VDD - I * RD - Vi
    if VDS >= Vov:
        return I
    # triodo: (VDD - Vi - x)/RD = KN (Vov x - x^2/2)
    a, b, c = KN / 2, -(KN * Vov + 1 / RD), (VDD - Vi) / RD
    x = (-b - sqrt(b * b - 4 * a * c)) / (2 * a)
    return (VDD - Vi - x) / RD


@reg
def p5_id():
    return plot([(_id_2021, "*")], 0, 5, 0, 3.6, W=60, H=11, vlines=[(1.81, ""), (3.86, "")],
                yticks=[(3.33, "3.33"), (2.27, "2.27")], hlines=[(2.27, "frontera triodo/sat")],
                xticks=[(0, "0"), (1.81, "1.81"), (3.86, "3.86"), (5, "5 V")], ytitle="I_D (mA)", xtitle="V_i",
                notes=["   |<----- TRIODO ----->|<------ SATURACIÓN ------>|<- CORTE ->|",
                       "   En triodo I_D casi no cambia: el transistor es casi un corto y R_D limita la corriente."])


@reg
def p9_ib():
    vi = lambda x: 12 * sin(deg(x))
    a = plot([(vi, "*")], 0, 720, -13, 13, W=66, H=11, hlines=[(6, "V_B = 6 V")],
             vlines=[(30, ""), (150, ""), (390, ""), (510, "")], yticks=[(12, "12"), (6, "6"), (-12, "-12")],
             xticks=[(30, "30°"), (150, "150°"), (390, "390°"), (510, "510°")], ytitle="v_i (V)", xtitle="wt")
    ib = lambda x: 60 if 12 * sin(deg(x)) > 6 else 0
    b = plot([(ib, "#")], 0, 720, 0, 70, W=66, H=5, yticks=[(60, "60 mA")],
             vlines=[(30, ""), (150, ""), (390, ""), (510, "")], ytitle="i_B", xtitle="wt")
    return a + "\n\n" + b + "\n   i_B es un pulso RECTANGULAR de 60 mA (lo fija la fuente) durante 1/3 del ciclo: promedio 20 mA."


@reg
def p12_transf():
    def vo(x):
        b = 7.9705
        m = 63.5 / 1063.5
        if x > b:
            return b + (x - b) * m
        if x < -b:
            return -b + (x + b) * m
        return x
    return plot([(vo, "*")], -12, 12, -10, 10, W=60, H=13, hlines=[(7.97, "+7.97 V"), (-7.97, "-7.97 V")],
                vlines=[(7.97, ""), (-7.97, "")], yticks=[(7.97, "7.97"), (-7.97, "-7.97")],
                xticks=[(-7.97, "-7.97"), (0, "0"), (7.97, "7.97"), (12, "12 V")], ytitle="v_o", xtitle="v_i",
                notes=["   Región I (|v_i| < 7.97 V): pendiente 1.   Regiones II y III: pendiente 1/16.75 (casi plana)."])


@reg
def p15_transf():
    def vo(x):
        if x > 2.1:
            return 0.6 * x + 0.84
        if x < -0.6:
            return x / 3 - 0.4
        return x
    return plot([(vo, "*")], -10, 10, -4.5, 7.5, W=60, H=13, vlines=[(2.1, ""), (-0.6, "")],
                yticks=[(6.84, "6.84"), (2.1, "2.1"), (-3.73, "-3.73")],
                xticks=[(-10, "-10"), (-0.6, "-0.6"), (2.1, "2.1"), (10, "10 V")], ytitle="V_o", xtitle="V_i",
                notes=["   Pendientes: 1/3 (D2 ON) | 1 (ambos OFF) | 0.6 (D1 ON).  Quiebres en V_i = -0.6 V y 2.1 V."])


@reg
def p17_t():
    Vp = 14.14
    vi = lambda x: Vp * sin(deg(x))

    def vo(x):
        if x <= 90:
            return min(Vp * sin(deg(x)), 5.7)
        return Vp * sin(deg(x)) - 8.44
    return plot([(vi, "."), (vo, "*")], 0, 720, -24, 16, W=66, H=15, hlines=[(5.7, "+5.7 V"), (-8.44, "promedio -8.44 V")],
                yticks=[(14.14, "14.1"), (5.7, "5.7"), (-8.44, "-8.44"), (-22.58, "-22.6")],
                xticks=[(90, "90°"), (270, "270°"), (450, "450°"), (630, "630°")], ytitle="V", xtitle="wt",
                notes=["   .  v_i      *  v_o. En el primer pico la rama D1+Zener carga C a 8.44 V; después v_o = v_i - 8.44 V."])
