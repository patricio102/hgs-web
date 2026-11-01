"""Ilustración del mix de herrajes para muebles (caso destacado de Inicio).

Dibujo vectorial propio: correderas telescópicas, bisagras de cazoleta, tiradores,
correderas de rodillo, perillas y accesorios de fijación. Sin marcas.
"""

LABELS = {
    "es": ["Correderas telescópicas", "Bisagras de cazoleta", "Tiradores",
           "Correderas de rodillo", "Perillas", "Fijaciones y accesorios"],
    "en": ["Telescopic drawer slides", "Concealed cup hinges", "Pull handles",
           "Roller drawer runners", "Knobs", "Fittings and accessories"],
}

# Cada pieza se dibuja en una celda de 500 x 400 con origen arriba a la izquierda.

def _slide():
    """Corredera telescópica de bolas, extendida en tres tramos."""
    holes = lambda x0, x1, y, step: "".join(
        f'<rect x="{x}" y="{y}" width="18" height="7" rx="3.5" class="h"/>' for x in range(x0, x1, step))
    balls = lambda x0, n, y: "".join(f'<circle cx="{x0 + i * 13}" cy="{y}" r="4.2" class="b"/>' for i in range(n))
    return f'''
<g transform="translate(40 120)">
  <rect x="0" y="0" width="300" height="56" rx="4" class="m1"/>
  {holes(18, 290, 10, 56)}{holes(18, 290, 39, 56)}
  <rect x="110" y="9" width="300" height="38" rx="3" class="m2"/>
  {balls(116, 5, 28)}
  {holes(190, 400, 24, 60)}
  <rect x="220" y="16" width="200" height="24" rx="3" class="m3"/>
  {balls(226, 4, 28)}
  <rect x="226" y="23" width="18" height="7" rx="3.5" class="h"/><rect x="330" y="23" width="18" height="7" rx="3.5" class="h"/>
  <path d="M410 16v24" class="ln"/>
  <path d="M0 96h420" class="dim"/><path d="M0 90v12M420 90v12" class="dim"/>
</g>
<g transform="translate(60 250)">
  <rect x="0" y="0" width="380" height="40" rx="4" class="m1"/>
  {holes(18, 370, 8, 52)}{holes(18, 370, 25, 52)}
  <rect x="8" y="7" width="364" height="26" rx="3" class="m2" opacity=".55"/>
</g>'''


def _hinge():
    """Bisagra de cazoleta (35 mm) con brazo y base, vista superior."""
    return '''
<g transform="translate(70 95)">
  <circle cx="80" cy="110" r="70" class="m1"/>
  <circle cx="80" cy="110" r="52" class="m3"/>
  <circle cx="80" cy="110" r="30" class="m2"/>
  <rect x="0" y="62" width="34" height="96" rx="10" class="m2"/>
  <circle cx="17" cy="82" r="9" class="b"/><circle cx="17" cy="138" r="9" class="b"/>
  <path d="M12 82h10M12 138h10" class="sl"/>
  <path d="M110 84h210a26 26 0 0 1 0 52H110z" class="m2"/>
  <rect x="150" y="92" width="150" height="36" rx="18" class="m3"/>
  <circle cx="190" cy="110" r="10" class="b"/><circle cx="260" cy="110" r="10" class="b"/>
  <path d="M184 110h12M260 104v12" class="sl"/>
  <path d="M232 168h110v40h-28v34h-54v-34h-28z" class="m1"/>
  <circle cx="287" cy="190" r="8" class="b"/><circle cx="287" cy="226" r="7" class="b"/>
  <path d="M287 136v32" class="ln"/>
</g>'''


def _handles():
    """Tres tiradores: barra, perfil y concha."""
    return '''
<g transform="translate(50 90)">
  <rect x="0" y="0" width="400" height="22" rx="11" class="dk"/>
  <rect x="50" y="20" width="16" height="34" rx="3" class="dk"/><rect x="334" y="20" width="16" height="34" rx="3" class="dk"/>
  <rect x="40" y="52" width="36" height="8" rx="2" class="m2"/><rect x="324" y="52" width="36" height="8" rx="2" class="m2"/>
</g>
<g transform="translate(70 200)">
  <path d="M0 0h300v14h-14v26H14V14H0z" class="m2"/>
  <path d="M14 14h272" class="ln"/>
</g>
<g transform="translate(130 285)">
  <path d="M0 10Q0 0 10 0h220q10 0 10 10v20q0 30-30 30H30Q0 60 0 30z" class="m1"/>
  <path d="M24 16h192q8 0 8 8v4q0 18-18 18H34q-18 0-18-18v-4q0-8 8-8z" class="dk"/>
</g>'''


def _roller():
    """Correderas de rodillo (epoxi) con ruedas."""
    return '''
<g transform="translate(40 110)">
  <path d="M0 0h400v20H22v24H0z" class="ep"/>
  <circle cx="400" cy="10" r="20" class="wh"/><circle cx="400" cy="10" r="7" class="b"/>
  <circle cx="60" cy="10" r="4" class="h"/><circle cx="200" cy="10" r="4" class="h"/><circle cx="330" cy="10" r="4" class="h"/>
</g>
<g transform="translate(60 210)">
  <path d="M0 0h400v44h-22V20H0z" class="ep"/>
  <circle cx="0" cy="10" r="20" class="wh"/><circle cx="0" cy="10" r="7" class="b"/>
  <circle cx="70" cy="10" r="4" class="h"/><circle cx="210" cy="10" r="4" class="h"/><circle cx="340" cy="10" r="4" class="h"/>
</g>'''


def _knobs():
    """Perillas: redonda, cuadrada y cónica, vista en perspectiva simple."""
    return '''
<g transform="translate(60 150)">
  <rect x="34" y="70" width="22" height="40" rx="4" class="m2"/>
  <circle cx="45" cy="50" r="48" class="m1"/><circle cx="45" cy="50" r="30" class="m3"/>
</g>
<g transform="translate(205 160)">
  <rect x="34" y="60" width="22" height="50" rx="4" class="dk"/>
  <rect x="0" y="0" width="90" height="80" rx="16" class="dk"/><rect x="14" y="12" width="62" height="56" rx="10" class="dk2"/>
</g>
<g transform="translate(345 150)">
  <rect x="34" y="70" width="22" height="40" rx="4" class="m2"/>
  <path d="M0 30Q0 0 45 0t45 30v14Q90 80 45 80T0 44z" class="br"/>
  <ellipse cx="45" cy="24" rx="30" ry="12" class="br2"/>
</g>'''


def _fittings():
    """Tornillos, soportes de repisa, escuadra y excéntrica."""
    screw = lambda x, y, l: (f'<g transform="translate({x} {y})"><circle cx="0" cy="0" r="16" class="m1"/>'
                             f'<path d="M-8 0h16M0 -8v16" class="sl"/>'
                             f'<path d="M-7 14h14l-4 {l}h-6z" class="m2"/>'
                             + "".join(f'<path d="M-8 {22 + i * 9}l16 -4" class="ln"/>' for i in range(l // 10)) + '</g>')
    return f'''
{screw(70, 100, 90)}{screw(130, 100, 70)}
<g transform="translate(190 90)">
  <path d="M0 0h24v86h70v24H0z" class="m2"/>
  <circle cx="12" cy="30" r="5" class="h"/><circle cx="12" cy="66" r="5" class="h"/><circle cx="48" cy="98" r="5" class="h"/><circle cx="76" cy="98" r="5" class="h"/>
</g>
<g transform="translate(345 120)">
  <circle cx="40" cy="40" r="40" class="m1"/><circle cx="40" cy="40" r="26" class="m3"/>
  <path d="M28 40h24" class="sl" style="stroke-width:5"/>
  <path d="M40 80v14" class="ln"/>
</g>
<g transform="translate(80 270)">
  {"".join(f'<g transform="translate({i * 70} 0)"><rect x="0" y="0" width="14" height="40" rx="3" class="m2"/><rect x="-8" y="40" width="30" height="10" rx="2" class="m1"/></g>' for i in range(4))}
  <rect x="300" y="0" width="22" height="50" rx="11" class="wd"/><rect x="336" y="0" width="22" height="50" rx="11" class="wd"/>
  <path d="M300 10h22M300 20h22M300 30h22M300 40h22M336 10h22M336 20h22M336 30h22M336 40h22" class="ln" opacity=".5"/>
</g>'''


DRAW = [_slide, _hinge, _handles, _roller, _knobs, _fittings]

STYLE = """
.hx .cell{fill:#fff;stroke:#d9e3e8}
.hx .m1{fill:#c9d3d9;stroke:#4a5a63;stroke-width:2}
.hx .m2{fill:#e3e9ec;stroke:#4a5a63;stroke-width:2}
.hx .m3{fill:#f4f7f8;stroke:#4a5a63;stroke-width:2}
.hx .dk{fill:#2b3236;stroke:#111;stroke-width:2}
.hx .dk2{fill:#3c454a}
.hx .br{fill:#c9a25b;stroke:#7a5b22;stroke-width:2}
.hx .br2{fill:#e2c88f}
.hx .ep{fill:#f7f7f5;stroke:#4a5a63;stroke-width:2}
.hx .wh{fill:#e8eef1;stroke:#4a5a63;stroke-width:2}
.hx .wd{fill:#e6c99a;stroke:#9a7a44;stroke-width:2}
.hx .b{fill:#9fb0b9;stroke:#4a5a63;stroke-width:1.5}
.hx .h{fill:#4a5a63}
.hx .sl{stroke:#4a5a63;stroke-width:3;stroke-linecap:round;fill:none}
.hx .ln{stroke:#4a5a63;stroke-width:1.5;fill:none}
.hx .dim{stroke:#0080B8;stroke-width:1.5;stroke-dasharray:4 4;fill:none}
.hx .lbl{font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:34px;font-weight:600;fill:#1b2a31}
.hx .num{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:24px;fill:#309880}
"""


def herrajes_svg(lang):
    labels = LABELS[lang]
    title = "Mix de herrajes para muebles" if lang == "es" else "Furniture hardware mix"
    cells = []
    for i, draw in enumerate(DRAW):
        x, y = (i % 3) * 520, (i // 3) * 440
        cells.append(f'''<g transform="translate({x} {y})">
<rect class="cell" x="0.5" y="0.5" width="499" height="419"/>
<text class="num" x="24" y="44">{i + 1:02d}</text>
<text class="lbl" x="24" y="396">{labels[i]}</text>
{draw()}
</g>''')
    return (f'<svg class="hx" viewBox="0 0 1540 860" role="img" aria-label="{title}: {", ".join(labels)}">'
            f'<title>{title}</title><style>{STYLE}</style>{"".join(cells)}</svg>')
