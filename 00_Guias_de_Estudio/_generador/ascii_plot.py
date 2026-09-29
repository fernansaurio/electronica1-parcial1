"""Gráficas en arte ASCII para las guías (formas de onda, transferencias, rectas de carga).

plot() devuelve un texto listo para ir dentro de <pre class="ascii">.
Las funciones pueden devolver None en los puntos donde no deben dibujarse.
"""
from math import floor


def _fmt(v):
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:g}"


def plot(series, x0, x1, y0, y1, W=64, H=15, hlines=(), vlines=(), yticks=(), xticks=(),
         ytitle="", xtitle="", notes=(), axis_y0=True):
    """series: [(f, ch)], hlines: [(y, etiqueta)], vlines: [(x, etiqueta)],
    yticks: [y] o [(y, texto)], xticks: [(x, texto)], notes: líneas extra al pie."""
    grid = [[" "] * W for _ in range(H)]

    def row(y):
        return int(round((y1 - y) / (y1 - y0) * (H - 1)))

    def col(x):
        return int(round((x - x0) / (x1 - x0) * (W - 1)))

    # eje x (y = 0)
    if axis_y0 and y0 <= 0 <= y1:
        r0 = row(0)
        for c in range(W):
            grid[r0][c] = "-"
    # líneas horizontales de referencia
    hl_rows = []
    for y, lab in hlines:
        r = row(y)
        if 0 <= r < H:
            for c in range(0, W, 2):
                if grid[r][c] == " ":
                    grid[r][c] = "-"
            hl_rows.append((r, lab))
    # líneas verticales de referencia
    for x, lab in vlines:
        c = col(x)
        if 0 <= c < W:
            for r in range(H):
                if grid[r][c] in (" ", "-"):
                    grid[r][c] = ":"
    # curvas
    for f, ch in series:
        prev = None
        for c in range(W):
            x = x0 + c * (x1 - x0) / (W - 1)
            y = f(x)
            if y is None:
                prev = None
                continue
            r = row(y)
            rr = min(max(r, 0), H - 1)
            if 0 <= r < H:
                grid[r][c] = ch
            if prev is not None and abs(rr - prev) > 1:
                step = 1 if rr > prev else -1
                for k in range(prev + step, rr, step):
                    if 0 <= k < H:
                        # vertical: rellena en la columna más cercana a la transición
                        grid[k][c if abs(k - rr) < abs(k - prev) else max(c - 1, 0)] = ch
            prev = rr if 0 <= r < H else None

    # etiquetas del eje y
    labels = {}
    for t in yticks:
        if isinstance(t, tuple):
            y, txt = t
        else:
            y, txt = t, _fmt(t)
        r = row(y)
        if 0 <= r < H:
            labels[r] = txt
    if axis_y0 and y0 <= 0 <= y1:
        labels.setdefault(row(0), "0")
    L = max([len(v) for v in labels.values()] + [len(ytitle), 1]) + 1
    out = []
    if ytitle:
        out.append(ytitle.rjust(L) + "^" if False else " " * L + "^  " + ytitle)
    for r in range(H):
        lab = labels.get(r, "")
        axis = "+" if lab else "|"
        line = lab.rjust(L - 1) + " " + axis + "".join(grid[r]).rstrip()
        for rr, hl in hl_rows:
            if rr == r and hl:
                line = line.ljust(L + 1 + W) + "  " + hl
        out.append(line.rstrip())
    # eje x inferior con marcas
    if xticks:
        tick = [" "] * (W + 30)
        for x, txt in xticks:
            c = col(x)
            s = max(c - len(txt) // 2, 0)
            if all(ch == " " for ch in tick[s:s + len(txt) + 1]):
                for i, ch in enumerate(txt):
                    tick[s + i] = ch
        out.append(" " * (L + 1) + "".join(tick).rstrip() + ("   " + xtitle if xtitle else ""))
    elif xtitle:
        out.append(" " * (L + 1 + W - len(xtitle)) + xtitle)
    vl = [lab for _, lab in vlines if lab]
    for n in notes:
        out.append(n)
    return "\n".join(out)
