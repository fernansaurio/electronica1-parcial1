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

PRE = re.compile(r'<pre class="ascii"(?: data-plot="(\w+)")?>(.*?)</pre>', re.S)


def rellenar(m):
    clave, cuerpo = m.group(1), m.group(2)
    if re.search(r"&(lt|gt|amp);", cuerpo):
        raise SystemExit("Entidad HTML dentro de un bloque ASCII (escribe el carácter literal): " + cuerpo[:60])
    if clave:
        extra = cuerpo.strip("\n")
        cuerpo = PLOTS[clave]() + ("\n" + extra if extra else "")
    cuerpo = cuerpo.strip("\n")
    return '<pre class="ascii">' + html.escape(cuerpo, quote=False) + "</pre>"


def main():
    pdf = "--sin-pdf" not in sys.argv
    fuentes = sorted(f for f in os.listdir(os.path.join(AQUI, "fuentes")) if f.endswith(".html"))
    for f in fuentes:
        src = open(os.path.join(AQUI, "fuentes", f), encoding="utf-8").read()
        out = PRE.sub(rellenar, src)
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
