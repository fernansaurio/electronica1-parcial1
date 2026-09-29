"""Arma las guías HTML (y sus PDF) a partir de _generador/fuentes/.

- Rellena cada <pre class="ascii" data-plot="nombre"></pre> con la gráfica de plots.py.
- Escapa el contenido de todos los bloques ASCII (así se pueden escribir < y & sin miedo).
- Imprime cada guía a PDF con Chrome sin cabeceras.

Uso:  python3 build_guias.py            (HTML + PDF)
      python3 build_guias.py --sin-pdf  (solo HTML)
"""
import html, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.dirname(AQUI)  # 00_Guias_de_Estudio
sys.path.insert(0, AQUI)
from plots import PLOTS

PRE = re.compile(r'<pre class="ascii"([^>]*)>(.*?)</pre>', re.S)
ATTR = re.compile(r'data-(\w+)="([^"]*)"')

BARRA = ('<div class="modo-bar" role="group" aria-label="Cómo ver los circuitos">'
         '<span>Circuitos:</span><button type="button" data-set="img">Imagen</button>'
         '<button type="button" data-set="ascii">ASCII</button>'
         '<span class="modo-nota">Cada circuito también tiene su propio botón.</span></div>')

SCRIPT = """<script>
(function () {
  var KEY = "elc115-modo-circuito";
  function set(fig, v) {
    fig.setAttribute("data-v", v);
    fig.querySelectorAll(".dual-bar button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === v); });
  }
  function global(v) {
    document.querySelectorAll("figure.dual").forEach(function (f) { set(f, v); });
    document.querySelectorAll(".modo-bar button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.set === v); });
    try { localStorage.setItem(KEY, v); } catch (e) {}
  }
  var inicial = "img";
  try { inicial = localStorage.getItem(KEY) || "img"; } catch (e) {}
  global(inicial);
  document.addEventListener("click", function (e) {
    var b = e.target.closest("button");
    if (!b) return;
    if (b.dataset.set) global(b.dataset.set);
    else if (b.dataset.v) set(b.closest("figure.dual"), b.dataset.v);
  });
})();
</script>"""


def rellenar(m):
    attrs = dict(ATTR.findall(m.group(1)))
    cuerpo = m.group(2)
    if re.search(r"&(lt|gt|amp);", cuerpo):
        raise SystemExit("Entidad HTML dentro de un bloque ASCII (escribe el carácter literal): " + cuerpo[:60])
    clave = attrs.get("plot")
    if clave:
        extra = cuerpo.strip("\n")
        cuerpo = PLOTS[clave]() + ("\n" + extra if extra else "")
    cuerpo = cuerpo.strip("\n")
    pre = '<pre class="ascii">' + html.escape(cuerpo, quote=False) + "</pre>"
    if "img" not in attrs:
        return pre
    imgs = "".join(f'<img src="{html.escape(src)}" alt="Circuito original">' for src in attrs["img"].split("|"))
    return ('<figure class="dual" data-v="img"><div class="dual-bar"><span>Circuito</span>'
            '<button type="button" data-v="img" aria-pressed="true">Imagen</button>'
            '<button type="button" data-v="ascii" aria-pressed="false">ASCII</button></div>'
            f'<div class="dual-img">{imgs}</div>{pre}</figure>')


def armar(src):
    out = PRE.sub(rellenar, src)
    if "figure class=\"dual\"" in out:
        out = out.replace("</h1>", "</h1>\n" + BARRA, 1).replace("</body>", SCRIPT + "\n</body>", 1)
    return out


def main():
    pdf = "--sin-pdf" not in sys.argv
    fuentes = sorted(f for f in os.listdir(os.path.join(AQUI, "fuentes")) if f.endswith(".html"))
    for f in fuentes:
        src = open(os.path.join(AQUI, "fuentes", f), encoding="utf-8").read()
        out = armar(src)
        destino = os.path.join(SALIDA, f)
        open(destino, "w", encoding="utf-8").write(out)
        print("HTML", f, len(out))
        if pdf:
            subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                            "--print-to-pdf=" + destino[:-5] + ".pdf", "file://" + destino],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("PDF ", f[:-5] + ".pdf")


if __name__ == "__main__":
    main()
