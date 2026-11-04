#!/usr/bin/env python3
"""HGS · template carrusel curvo. Genera el sitio estático (ES en raíz, EN en /en/).

Uso: python3 _build.py [salida]   (por defecto: public)
"""
import os, shutil, sys
from html import escape
from hgs_logo import LOGO_RINGS, LOGO_HGS, LOGO_TAG, LOGO_LINE

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "public")

EMAIL = "contact@hgspyme.cl"
WA_TXT = "+56 9 7799 9363"
WA_URL = "https://wa.me/56977999363"

PAGES = [  # clave, ES (archivo, nav), EN (archivo, nav)
    ("home", ("index.html", "Inicio"), ("index.html", "Home")),
    ("how", ("como-trabajamos.html", "Cómo trabajamos"), ("how-we-work.html", "How we work")),
    ("cats", ("categorias.html", "Categorías"), ("categories.html", "Categories")),
    ("cases", ("casos.html", "Casos"), ("case-studies.html", "Case studies")),
    ("about", ("nosotros.html", "Nosotros"), ("about.html", "About us")),
    ("contact", ("contacto.html", "Contacto"), ("contact.html", "Contact")),
]

lang = "es"
CUT = ' class="cut"'


def L(es, en):
    return es if lang == "es" else en


def href(key):
    for k, es, en in PAGES:
        if k == key:
            return (es if lang == "es" else en)[0]
    raise KeyError(key)


def other_href(key):
    for k, es, en in PAGES:
        if k == key:
            return ("en/" + en[0]) if lang == "es" else ("../" + es[0])


def img(name):
    return ("" if lang == "es" else "../") + "img/" + name


def asset(name):
    return ("" if lang == "es" else "../") + "assets/" + name


def logo(full=False, label="HGS Hardware Global Sourcing"):
    if full:
        return f'<svg class="logo" viewBox="0 0 402 208" role="img" aria-label="{label}">{LOGO_RINGS}{LOGO_HGS}{LOGO_LINE}{LOGO_TAG}</svg>'
    return f'<svg class="logo" viewBox="0 0 402 129" role="img" aria-label="HGS">{LOGO_RINGS}{LOGO_HGS}</svg>'


def cta(cls=""):
    return f'<span class="cta-ring {cls}"><a class="pill pill-green" href="{href("contact")}">{L("Conversemos tu proyecto", "Let&#39;s talk about your project")}</a></span>'


def nav_links(cur):
    out = []
    for k, es, en in PAGES[1:]:
        f, name = es if lang == "es" else en
        cur_attr = ' aria-current="page"' if k == cur else ""
        out.append(f'<a href="{f}"{cur_attr}>{name}</a>')
    return "".join(out)


def sheet(cur):
    return f'''<div class="sheet" role="dialog" aria-modal="true" aria-label="{L("Menú", "Menu")}">
  <div class="row"><a href="{href("home")}">{logo()}</a><button class="close-btn" data-menu aria-label="{L("Cerrar menú", "Close menu")}">×</button></div>
  <nav>{nav_links(cur)}</nav>
  <div class="bottom"><a class="pill pill-green" href="{href("contact")}">{L("Conversemos tu proyecto", "Let&#39;s talk about your project")}</a><a class="pill pill-white" href="{other_href(cur)}" hreflang="{L("en", "es")}">{L("English", "Español")}</a></div>
</div>'''


def menu_btn():
    return f'<button class="menu-btn" data-menu aria-label="{L("Abrir menú", "Open menu")}"><span></span></button>'


def topbar(cur):
    return f'''<header class="top">
  <a class="brand" href="{href("home")}" aria-label="HGS · {L("Inicio", "Home")}">{logo()}</a>
  <nav aria-label="{L("Principal", "Main")}">{nav_links(cur)}</nav>
  <div class="acts"><a class="pill pill-white lang" href="{other_href(cur)}" hreflang="{L("en", "es")}">{L("EN", "ES")}</a><a class="pill pill-green" href="{href("contact")}">{L("Conversemos tu proyecto", "Let&#39;s talk about your project")}</a>{menu_btn()}</div>
</header>'''


def final_band():
    return f'''<section class="final"><div class="wrap"><div class="final-box">
  <h2>{L("¿Tienes un producto o una línea en mente?", "Do you have a product or a line in mind?")}</h2>
  <p>{L("Cuéntanos qué quieres desarrollar. Revisamos tu caso y te proponemos un camino concreto.", "Tell us what you want to develop. We review your case and propose a concrete path.")}</p>
  {cta()}
  <span class="note">{L("Te respondemos en 1 día hábil", "We reply within 1 business day")}</span>
</div></div></section>'''


def footer(cur):
    return f'''<footer class="foot"><div class="wrap">
  <div class="foot-grid">
    <div>{logo(full=True)}<p>{L("Marcas propias de ferretería, construcción y herrajes para muebles, desarrolladas en China para Latinoamérica.", "Private-label hardware, construction and furniture fittings, developed in China for Latin America.")}</p></div>
    <div><h4>{L("Sitio", "Site")}</h4><ul>{"".join(f"<li>{a}</li>" for a in nav_links(cur).replace("</a>", "</a>|").split("|") if a)}</ul></div>
    <div><h4>{L("Oficinas", "Offices")}</h4><ul><li>Santiago, Chile</li><li>{L("Shanghái, China", "Shanghai, China")}</li></ul></div>
  </div>
  <div class="foot-bottom"><span>© 2026 HGS Hardware Global Sourcing</span><a href="{other_href(cur)}" hreflang="{L("en", "es")}">{L("English version", "Versión en español")}</a></div>
</div></footer>'''


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@600&family=Inter+Tight:wght@600;700&family=Inter:wght@400;500;600&display=swap">')
FAVICON = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 0 129 129"><style>.lg-g{{fill:#00a990}}.lg-b{{fill:#0897de}}</style>{LOGO_RINGS}</svg>'


def page(cur, title, desc, body):
    k_es = [p for p in PAGES if p[0] == cur][0]
    alt_es = "/" + (k_es[1][0] if k_es[1][0] != "index.html" else "")
    alt_en = "/en/" + (k_es[2][0] if k_es[2][0] != "index.html" else "")
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="alternate" hreflang="es" href="{alt_es}"><link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="icon" href="{("" if lang == "es" else "../")}favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#F4F7F1">
{FONTS}
<link rel="stylesheet" href="{asset("site.css")}">
</head>
<body>
<a class="skip" href="#main">{L("Saltar al contenido", "Skip to content")}</a>
{body}
{sheet(cur)}
{footer(cur)}
<script src="{asset("site.js")}" defer></script>
</body>
</html>
'''


# ---------------------------------------------------------------- Inicio
CAROUSEL = [  # archivo, recorte (cut = producto sobre blanco), ES, EN
    ("p-bisagra-cazoleta-b.webp", True, "Bisagras de cazoleta", "Concealed hinges"),
    ("p-escala-ferreteria.webp", False, "Escalas DRAVIK", "DRAVIK ladders"),
    ("fabrica-soldadura.webp", False, "Fábrica en China", "Factory in China"),
    ("p-corredera-telescopica.webp", True, "Correderas telescópicas", "Ball-bearing slides"),
    ("saco-escombros.webp", False, "Sacos de polipropileno", "Polypropylene bags"),
    ("p-clavo-techo-medicion.webp", False, "Control de calidad", "Quality control"),
    ("p-plataforma-a.webp", True, "Plataformas de carga", "Moving dollies"),
    ("p-clavo-granel.webp", False, "Clavos", "Nails"),
    ("carga-contenedor.webp", False, "Carga del contenedor", "Container loading"),
    ("p-tirador-b.webp", True, "Tiradores", "Cabinet handles"),
]

STEPS = [
    (("Definir la línea", "Qué productos, para qué cliente y con qué especificación."),
     ("Define the line", "Which products, for which customer and to what specification.")),
    (("Encontrar la fábrica", "Fábricas especialistas de nuestra red y muestras validadas."),
     ("Find the factory", "Specialist factories from our network and validated samples.")),
    (("Crear marca y empaque", "Marca, empaque, etiquetas e instructivos listos para góndola."),
     ("Create brand and packaging", "Brand, packaging, labels and instructions ready for the shelf.")),
    (("Asegurar la calidad", "Inspección en fábrica contra la ficha técnica aprobada."),
     ("Assure quality", "In-factory inspection against the approved spec sheet.")),
    (("Embarcar", "Supervisamos la carga y la documentación de exportación."),
     ("Ship", "We supervise loading and export documentation.")),
]

FAMILIES = [  # id, ES, EN, desc ES, desc EN, fotos [(archivo, cut, ES, EN)]
    ("herrajes", "Herrajes para muebles", "Furniture fittings",
     "Bisagras, correderas, tiradores, perillas, cerraduras y patas: la línea completa para el mueblista.",
     "Hinges, slides, handles, knobs, locks and legs: the full line for furniture makers.",
     [("p-bisagra-cazoleta-a.webp", True, "Bisagra de cazoleta con cierre suave", "Soft-close concealed hinge"),
      ("p-bisagra-cazoleta-c.webp", True, "Bisagra de cazoleta", "Concealed hinge"),
      ("p-corredera-telescopica.webp", True, "Correderas telescópicas", "Ball-bearing slides"),
      ("p-corredera-rodillo.webp", True, "Correderas de rodillo", "Roller slides"),
      ("p-tirador-b.webp", True, "Tirador de acero inoxidable", "Stainless steel handle"),
      ("p-tirador-a.webp", True, "Tirador embutido", "Recessed handle"),
      ("p-perilla.webp", True, "Perillas", "Knobs"),
      ("p-cerradura.webp", True, "Cerradura de mueble", "Furniture lock"),
      ("p-pata.webp", True, "Pata de mueble", "Furniture leg"),
      ("p-cargador-usb.webp", True, "Cargador USB de escritorio", "Desk USB charger"),
      ("p-cargador-inalambrico.webp", True, "Cargador inalámbrico de escritorio", "Desk wireless charger")]),
    ("mueblistas", "Accesorios para mueblistas", "Accessories for furniture makers",
     "Herramientas y ayudas para armar e instalar: plataformas de carga, prensas, guías y plantillas.",
     "Tools and aids for assembly and installation: dollies, clamps, guides and templates.",
     [("p-plataforma-a.webp", True, "Plataforma de carga ensamblable", "Modular moving dolly"),
      ("p-plataforma-b.webp", True, "Plataforma de carga con manilla", "Dolly with handle"),
      ("p-prensa-esquinera.webp", True, "Prensa esquinera", "Corner clamp"),
      ("p-guia-bisagras.webp", True, "Guía de instalación de bisagras", "Hinge drilling guide"),
      ("p-plantilla-bisagras.webp", True, "Plantilla de instalación de bisagras", "Hinge template")]),
    ("escalas", "Escalas DRAVIK", "DRAVIK ladders",
     "Escalas articuladas, de tijera y pisos de aluminio y acero bajo DRAVIK, la marca propia de HGS.",
     "Multi-position, step ladders and step stools in aluminum and steel under DRAVIK, HGS's own brand.",
     [("p-escala-articulada.webp", True, "Escala articulada de aluminio", "Aluminum multi-position ladder"),
      ("p-escala-tijera.webp", True, "Escala tijera de aluminio", "Aluminum step ladder"),
      ("p-piso-2-peldanos.webp", True, "Piso de 2 peldaños", "2-step stool"),
      ("p-escala-ferreteria.webp", False, "Escala articulada en ferretería", "Multi-position ladder in store"),
      ("p-escala-obra.webp", False, "Escala en obra", "Ladder on site"),
      ("p-piso-garage.webp", False, "Piso en uso", "Step stool in use")]),
    ("clavos", "Clavos y fijaciones", "Nails and fasteners",
     "Clavos corrientes, de techo y fijaciones, a granel o en empaque propio.",
     "Common nails, roofing nails and fasteners, in bulk or in your own packaging.",
     [("p-clavo-granel.webp", False, "Clavos a granel en caja de exportación", "Bulk nails in export carton"),
      ("p-clavo-medicion.webp", False, "Medición de clavos con pie de metro", "Measuring nails with a caliper"),
      ("p-clavo-techo-medicion.webp", False, "Medición de clavo de techo", "Measuring a roofing nail")]),
    ("alambres", "Alambres y mallas", "Wire and mesh",
     "Alambre de púas, galvanizado y recocido, y malla hexagonal para obra y campo.",
     "Barbed, galvanized and annealed wire, and hexagonal mesh for construction and farming.",
     []),
    ("sacos", "Sacos y envases", "Bags and packaging",
     "Sacos de polipropileno para escombros, áridos y uso agrícola, con impresión de tu marca.",
     "Polypropylene bags for rubble, aggregates and farming, printed with your brand.",
     [("p-saco-rojo.webp", True, "Saco de polipropileno rojo", "Red polypropylene bag"),
      ("p-saco-blanco.webp", True, "Saco de polipropileno blanco", "White polypropylene bag"),
      ("saco-escombros.webp", False, "Sacos de escombros en obra", "Rubble bags on site")]),
]
FAM_COVER = {"herrajes": ("p-bisagra-cazoleta-b.webp", True), "mueblistas": ("p-plataforma-a.webp", True),
             "escalas": ("p-escala-ferreteria.webp", False), "clavos": ("p-clavo-granel.webp", False),
             "alambres": (None, False), "sacos": ("saco-escombros.webp", False)}
ALAMBRES_CHIPS = (["Alambre de púas", "Alambre galvanizado", "Alambre recocido", "Malla hexagonal"],
                  ["Barbed wire", "Galvanized wire", "Annealed wire", "Hexagonal mesh"])


def doodles():
    # coordenadas en unidades del cuadro 1440x1080
    return '''<svg class="doodles" viewBox="0 0 1440 1080" preserveAspectRatio="none" aria-hidden="true">
  <path pathLength="1" d="M268 412 L286 380 M286 412 L304 380"/>
  <path pathLength="1" d="M1238 392 C1250 430 1236 470 1206 496 C1186 514 1170 528 1172 552"/>
  <path pathLength="1" d="M1158 534 L1172 556 L1190 538"/>
  <path class="blue" pathLength="1" d="M496 960 C530 966 556 958 578 942"/>
  <path class="blue" pathLength="1" d="M562 936 L580 940 L574 958"/>
</svg>'''


def home():
    cards = []
    for f, cut, es, en in CAROUSEL:
        cards.append(f'<div class="card{" cut" if cut else ""}"><img src="{img(f)}" alt="{escape(L(es, en))}" draggable="false" decoding="async"><span class="tag"><i></i>{L(es, en)}</span></div>')
    # 14 tarjetas para cubrir pantallas anchas (se repiten las primeras 4)
    cards = cards + cards[:4]
    h1 = L('<span>Marcas propias de ferretería,</span> <span><em>desarrolladas</em> en China</span>',
           '<span>Private-label hardware,</span> <span><em>developed</em> in China</span>')
    sub = L('<span>Diseñamos, fabricamos y controlamos tu línea de ferretería,</span> <span>construcción y herrajes para muebles. Un solo socio</span> <span>que responde por el resultado completo.</span>',
            '<span>We design, manufacture and inspect your hardware,</span> <span>construction and furniture fittings line. One single partner</span> <span>accountable for the whole result.</span>')
    hero = topbar("home") + f'''<section class="hero" aria-label="{L("Portada", "Cover")}">
<div class="frame">
  <span class="badge f-badge">{L("Más de 20 años en el mundo ferretero", "Over 20 years in the hardware trade")}</span>
  <h1 class="f-h1" id="main">{h1}</h1>
  <p class="f-sub">{sub}</p>
  <div class="cards" aria-label="{L("Productos y procesos de HGS", "HGS products and processes")}">{"".join(cards)}</div>
  {doodles()}
  <span class="note f-note1">{L("Productos reales<br>de nuestras líneas", "Real products<br>from our lines")}</span>
  <div class="f-cta">{cta()}</div>
  <span class="note f-note2">{L("Te respondemos<br>en 1 día hábil", "We reply within<br>1 business day")}</span>
</div>
</section>'''

    proof = f'''<section class="sec"><div class="wrap">
  <div class="proof">
    <div><b>{L("Cientos de productos", "Hundreds of products")}</b><span>{L("desarrollados para marcas propias del mundo ferretero.", "developed for private labels in the hardware trade.")}</span></div>
    <div><b>{L("Más de 20 años", "Over 20 years")}</b><span>{L("de red en ferias, fábricas y proveedores de China.", "of network across trade fairs, factories and suppliers in China.")}</span></div>
    <div><b>{L("Un solo socio", "One single partner")}</b><span>{L("de la idea al embarque, con responsabilidad total.", "from idea to shipment, fully accountable.")}</span></div>
  </div>
  <p class="proof-note">{L("Trabajamos con cadenas líderes, distribuidores y ferreterías del mercado chileno.", "We work with leading chains, distributors and hardware stores in the Chilean market.")}</p>
</div></section>'''

    steps = "".join(f'<div class="step"><h3>{L(e[0], n[0])}</h3><p>{L(e[1], n[1])}</p></div>' for e, n in STEPS)
    steps_sec = f'''<section class="sec"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">{L("Cómo trabajamos", "How we work")}</span><h2>{L("Un solo camino en 5 etapas", "One path in 5 stages")}</h2></div>
  <p>{L("No vendemos servicios sueltos: te acompañamos en todo el camino y respondemos por el resultado.", "We don’t sell stand-alone services: we walk the whole path with you and answer for the result.")} <a class="more" href="{href("how")}">{L("Ver el detalle →", "See the details →")}</a></p></div>
  <div class="steps">{steps}</div>
</div></section>'''

    cat_cards = []
    for fid, es, en, des, den, photos in FAMILIES:
        f, cut = FAM_COVER[fid]
        if f:
            ph = f'<img src="{img(f)}" alt="" loading="lazy"{CUT if cut else ""}>'
        else:
            ph = f'<div class="ph-text"><span>{L("Púas · galvanizado<br>recocido · malla", "Barbed · galvanized<br>annealed · mesh")}</span></div>'
        cat_cards.append(f'<a class="cat" href="{href("cats")}#{fid}"><div class="ph">{ph}</div><div class="tx"><h3>{L(es, en)}</h3><p>{L(des, den)}</p></div></a>')
    cats_sec = f'''<section class="sec"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">{L("Categorías", "Categories")}</span><h2>{L("Todo el mundo ferretero, con un solo socio", "The whole hardware trade, with one partner")}</h2></div>
  <p>{L("Solo ferretería, construcción y herrajes. Dentro de ese mundo, todas las categorías; fuera de él, nada.", "Only hardware, construction and fittings. Within that world, every category; outside it, nothing.")}</p></div>
  <div class="cats">{"".join(cat_cards)}</div>
</div></section>'''

    why = f'''<section class="sec"><div class="wrap">
  <div class="split">
    <div>
      <span class="eyebrow">{L("Por qué HGS", "Why HGS")}</span>
      <h2>{L("Especialistas, no intermediarios", "Specialists, not middlemen")}</h2>
      <p class="sub">{L("Conocemos el proceso de compra de una cadena: fichas técnicas, códigos, inspecciones y plazos. Por eso hablamos el mismo idioma que tu equipo comercial y que la fábrica.", "We know how a retail chain buys: spec sheets, item codes, inspections and lead times. That is why we speak the same language as your buying team and the factory.")}</p>
      <div class="pillars" style="margin-top:28px;grid-template-columns:1fr">
        <div><h3>{L("Oficina propia en China", "Our own office in China")}</h3><p>{L("En Shanghái recibimos y revisamos muestras y coordinamos con las fábricas.", "In Shanghai we receive and review samples and coordinate with factories.")}</p></div>
        <div><h3>{L("Comercial en Chile", "Commercial team in Chile")}</h3><p>{L("En Santiago entendemos tu mercado y tu cliente final.", "In Santiago we understand your market and your end customer.")}</p></div>
      </div>
    </div>
    <div class="shots"><div class="shot"><img src="{img("fabrica-soldadura.webp")}" alt="{L("Soldadura en una línea de producción en China", "Welding on a production line in China")}" loading="lazy"></div><div class="shot"><img src="{img("escala-exhibicion.webp")}" alt="{L("Escalas DRAVIK exhibidas en góndola", "DRAVIK ladders on display")}" loading="lazy"></div></div>
  </div>
</div></section>'''

    body = hero + f'<main>{proof}{steps_sec}{cats_sec}{why}{final_band()}</main>'
    return page("home", L("HGS · Marcas propias de ferretería desarrolladas en China", "HGS · Private-label hardware developed in China"),
                L("HGS desarrolla marcas propias de ferretería, construcción y herrajes para muebles en China, para cadenas, distribuidores y ferreterías de Latinoamérica.",
                  "HGS develops private-label hardware, construction products and furniture fittings in China for retail chains, distributors and hardware stores in Latin America."), body)


def page_hero(badge, h1, lead):
    return f'<section class="page-hero"><div class="wrap"><span class="badge">{badge}</span><h1 id="main">{h1}</h1><p class="lead">{lead}</p></div></section>'


# ---------------------------------------------------------------- Cómo trabajamos
STAGES = [
    (("Definir la línea", "Partimos por tu negocio, no por el catálogo de una fábrica.",
      ["Revisamos tu surtido, tu cliente final y los precios de góndola de tu mercado.",
       "Proponemos qué productos desarrollar y con qué especificación.",
       "Armamos la ficha técnica de cada producto."]),
     ("Define the line", "We start from your business, not from a factory catalog.",
      ["We review your assortment, your end customer and shelf prices in your market.",
       "We propose which products to develop and to what specification.",
       "We build the spec sheet for each product."]),
     [("escala-exhibicion.webp", False, "Línea de escalas DRAVIK exhibida en góndola", "DRAVIK ladder line on display")]),
    (("Encontrar la fábrica y validar muestras", "Elegimos entre fábricas especialistas que conocemos hace años.",
      ["Seleccionamos la fábrica según el producto, la capacidad y la calidad que necesitas.",
       "Pedimos muestras y las revisamos en nuestra oficina de Shanghái.",
       "Te enviamos las muestras aprobadas para tu validación final."]),
     ("Find the factory and validate samples", "We choose among specialist factories we have known for years.",
      ["We select the factory based on the product, capacity and quality you need.",
       "We request samples and review them at our Shanghai office.",
       "We send you the approved samples for your final sign-off."]),
     [("fabrica-soldadura.webp", False, "Soldadura en una línea de producción", "Welding on a production line")]),
    (("Crear la marca y el empaque", "Tu marca se ve profesional desde el primer producto.",
      ["Diseñamos o adaptamos la marca y el empaque de cada producto.",
       "Preparamos etiquetas, códigos de barra e instructivos en tu idioma.",
       "Cuidamos que todo cumpla lo que pide tu cliente o tu cadena."]),
     ("Create the brand and packaging", "Your brand looks professional from the very first product.",
      ["We design or adapt the brand and packaging for each product.",
       "We prepare labels, barcodes and instructions in your language.",
       "We make sure everything meets what your customer or chain requires."]),
     [("saco-escombros.webp", False, "Sacos de escombros con impresión de marca", "Rubble bags printed with a brand")]),
    (("Asegurar la calidad", "Revisamos en la fábrica, antes de que el producto salga.",
      ["Inspeccionamos durante la producción y antes del embarque.",
       "Medimos contra la ficha técnica aprobada, con fotos y registro.",
       "Si algo no cumple, se corrige en la fábrica, no en tu bodega."]),
     ("Assure quality", "We inspect at the factory, before the product leaves.",
      ["We inspect during production and before shipment.",
       "We measure against the approved spec sheet, with photos and records.",
       "If something fails, it is fixed at the factory, not in your warehouse."]),
     [("p-clavo-techo-medicion.webp", False, "Medición de clavo de techo en inspección", "Measuring a roofing nail during inspection"),
      ("p-clavo-medicion.webp", False, "Medición de clavos con pie de metro", "Measuring nails with a caliper")]),
    (("Embarcar", "Tu carga sale ordenada, completa y documentada.",
      ["Supervisamos la carga del contenedor.",
       "Preparamos la documentación de exportación.",
       "Si lo necesitas, te presentamos agente de aduanas y flete."]),
     ("Ship", "Your cargo leaves organized, complete and documented.",
      ["We supervise container loading.",
       "We prepare the export documentation.",
       "If you need it, we introduce you to a customs broker and freight forwarder."]),
     [("carga-contenedor.webp", False, "Carga de pallets en el contenedor", "Loading pallets into the container"),
      ("contenedor-puerta.webp", False, "Contenedor cargado listo para cerrar", "Loaded container ready to be sealed")]),
]


def how():
    rows = []
    for i, (es, en, photos) in enumerate(STAGES, 1):
        t = es if lang == "es" else en
        ticks = "".join(f"<li>{x}</li>" for x in t[2])
        if len(photos) == 1:
            f, cut, a_es, a_en = photos[0]
            ph = f'<div class="shot wide"><img src="{img(f)}" alt="{escape(L(a_es, a_en))}" loading="lazy"></div>'
        else:
            ph = '<div class="shots">' + "".join(f'<div class="shot"><img src="{img(f)}" alt="{escape(L(a, b))}" loading="lazy"></div>' for f, c, a, b in photos) + "</div>"
        rows.append(f'<div class="stage"><div class="stage-tx"><span class="stage-num">{L("Etapa", "Stage")} {i}</span><h2>{t[0]}</h2><p class="sub">{t[1]}</p><ul class="ticks">{ticks}</ul></div>{ph}</div>')
    body = topbar("how") + "<main>" + page_hero(
        L("Cómo trabajamos", "How we work"),
        L("Un solo camino en 5 etapas", "One path in 5 stages"),
        L("No te vendemos un servicio suelto: te acompañamos en todo el camino y respondemos por el resultado.",
          "We don’t sell you a stand-alone service: we walk the whole path with you and answer for the result.")
    ) + f'<section class="sec" style="padding-top:8px"><div class="wrap">{"".join(rows)}</div></section>' + final_band() + "</main>"
    return page("how", L("Cómo trabajamos · HGS", "How we work · HGS"),
                L("Las 5 etapas con que HGS desarrolla tu marca propia en China: definir la línea, encontrar la fábrica, crear la marca, asegurar la calidad y embarcar.",
                  "The 5 stages HGS follows to develop your private label in China: define the line, find the factory, create the brand, assure quality and ship."), body)


# ---------------------------------------------------------------- Categorías
def cats():
    blocks = []
    for n, (fid, es, en, des, den, photos) in enumerate(FAMILIES, 1):
        if photos:
            gal = '<div class="gal">' + "".join(
                f'<figure><img src="{img(f)}" alt="{escape(L(a, b))}" loading="lazy"{CUT if c else ""}><figcaption>{L(a, b)}</figcaption></figure>'
                for f, c, a, b in photos) + "</div>"
        else:
            gal = '<div class="chips">' + "".join(f"<span>{x}</span>" for x in ALAMBRES_CHIPS[0 if lang == "es" else 1]) + "</div>"
        blocks.append(f'<div class="fam" id="{fid}"><div class="fam-head"><div><span class="num">0{n}</span><h2>{L(es, en)}</h2></div><p>{L(des, den)}</p></div>{gal}</div>')
    other = f'''<div class="fam"><div class="split"><div><h2>{L("¿Tu categoría no está aquí?", "Is your category not here?")}</h2>
<p class="sub">{L("Si es del mundo ferretero o de la construcción, probablemente la conocemos. Cuéntanos qué buscas.", "If it belongs to the hardware or construction trade, we probably know it. Tell us what you are looking for.")}</p></div>
<div>{cta()}</div></div></div>'''
    body = topbar("cats") + "<main>" + page_hero(
        L("Categorías", "Categories"),
        L("Todo el mundo ferretero, con un solo socio", "The whole hardware trade, with one partner"),
        L("Seis familias de producto que ya desarrollamos. Fotos de productos reales, sin marcas de clientes.",
          "Six product families we already develop. Photos of real products, without client brands.")
    ) + f'<section class="sec" style="padding-top:8px"><div class="wrap">{"".join(blocks)}{other}</div></section>' + final_band() + "</main>"
    return page("cats", L("Categorías · HGS", "Categories · HGS"),
                L("Herrajes para muebles, accesorios para mueblistas, escalas DRAVIK, clavos, alambres y sacos: las categorías que HGS desarrolla en China.",
                  "Furniture fittings, accessories for furniture makers, DRAVIK ladders, nails, wire and bags: the categories HGS develops in China."), body)


# ---------------------------------------------------------------- Casos
def cases():
    herr = ["p-corredera-telescopica.webp", "p-bisagra-cazoleta-b.webp", "p-tirador-b.webp", "p-corredera-rodillo.webp",
            "p-perilla.webp", "p-cerradura.webp", "p-pata.webp", "p-cargador-usb.webp", "p-guia-bisagras.webp"]
    grid = '<div class="case-grid">' + "".join(f'<img src="{img(f)}" alt="" loading="lazy">' for f in herr) + "</div>"
    items = [
        (grid, [L("Herrajes para muebles", "Furniture fittings"), L("Cadena · Chile", "Retail chain · Chile")],
         L("Una línea completa de herrajes para la marca propia de una cadena", "A full line of fittings for a retail chain’s private label"),
         [(L("El desafío", "The challenge"), L("Ofrecer al mueblista una línea completa y coherente bajo una sola marca propia, en vez de productos sueltos de distintos proveedores.", "Offer furniture makers a complete, consistent line under one private label, instead of loose products from different suppliers.")),
          (L("Qué hicimos", "What we did"), L("Definimos la línea con la cadena, buscamos fábricas especialistas para cada familia, validamos muestras y desarrollamos el empaque de cada código.", "We defined the line with the chain, found specialist factories for each family, validated samples and developed the packaging for every item.")),
          (L("Qué incluye", "What it includes"), L("Bisagras de cazoleta, correderas telescópicas y de rodillo, tiradores, perillas, cerraduras, patas, cargadores de escritorio y guías de instalación.", "Concealed hinges, ball-bearing and roller slides, handles, knobs, locks, legs, desk chargers and installation guides."))]),
        (f'<div class="shot"><img src="{img("escala-bodega.webp")}" alt="{L("Escala articulada DRAVIK en uso", "DRAVIK multi-position ladder in use")}" loading="lazy"></div>',
         [L("Escalas", "Ladders"), L("Marca propia HGS", "HGS own brand")],
         L("DRAVIK: escalas de aluminio y acero con marca propia", "DRAVIK: aluminum and steel ladders under our own brand"),
         [(L("El desafío", "The challenge"), L("Crear una marca de escalas que compita en ferretería por calidad y diseño, no solo por precio.", "Build a ladder brand that competes in hardware stores on quality and design, not just price.")),
          (L("Qué hicimos", "What we did"), L("Desarrollamos los modelos, la marca, el empaque y las fotos de producto, y controlamos la calidad en fábrica.", "We developed the models, the brand, the packaging and the product photography, and controlled quality at the factory.")),
          (L("Qué incluye", "What it includes"), L("Escalas articuladas, escalas tijera y pisos de peldaños.", "Multi-position ladders, step ladders and step stools."))]),
        (f'<div class="shot"><img src="{img("saco-escombros.webp")}" alt="{L("Sacos de escombros en obra", "Rubble bags on site")}" loading="lazy"></div>',
         [L("Sacos y envases", "Bags and packaging")],
         L("Sacos de polipropileno con marca propia", "Private-label polypropylene bags"),
         [(L("El desafío", "The challenge"), L("Tener sacos resistentes, con medidas y capacidad claras, impresos con la marca del cliente.", "Strong bags with clear sizes and capacity, printed with the customer’s brand.")),
          (L("Qué hicimos", "What we did"), L("Elegimos la fábrica, definimos tejido, medidas e impresión, e inspeccionamos antes del embarque.", "We chose the factory, defined the weave, sizes and print, and inspected before shipment.")),
          (L("Qué incluye", "What it includes"), L("Sacos para escombros, áridos y uso agrícola.", "Bags for rubble, aggregates and farming."))]),
    ]
    blocks = []
    for media, tags, title, dl in items:
        dls = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in dl)
        blocks.append(f'<article class="case">{media}<div><div class="tags">{"".join(f"<span>{t}</span>" for t in tags)}</div><h2>{title}</h2><dl>{dls}</dl></div></article>')
    body = topbar("cases") + "<main>" + page_hero(
        L("Casos", "Case studies"),
        L("Proyectos reales, sin nombres de clientes", "Real projects, without client names"),
        L("Así se ve el camino de 5 etapas aplicado a líneas que ya están en el mercado.",
          "This is what the 5-stage path looks like on lines already on the market.")
    ) + f'<section class="sec" style="padding-top:8px"><div class="wrap">{"".join(blocks)}</div></section>' + final_band() + "</main>"
    return page("cases", L("Casos · HGS", "Case studies · HGS"),
                L("Proyectos de marca propia desarrollados por HGS: herrajes para muebles, escalas DRAVIK y sacos de polipropileno.",
                  "Private-label projects developed by HGS: furniture fittings, DRAVIK ladders and polypropylene bags."), body)


# ---------------------------------------------------------------- Nosotros
def about():
    body = topbar("about") + "<main>" + page_hero(
        L("Nosotros", "About us"),
        L("Un solo socio para tu marca propia", "One partner for your private label"),
        L("HGS (Hardware Global Sourcing) desarrolla marcas propias de ferretería, construcción y herrajes en China para Latinoamérica.",
          "HGS (Hardware Global Sourcing) develops private-label hardware, construction products and fittings in China for Latin America.")
    ) + f'''<section class="sec" style="padding-top:8px"><div class="wrap">
  <div class="mv">
    <div><h3>{L("Misión", "Mission")}</h3><p>{L("Ayudamos a ferreteros, distribuidores e importadores de Latinoamérica a crecer con marcas propias. Desarrollamos sus productos de ferretería, construcción y herrajes en China, y respondemos por todo el proceso: diseño, fabricación, control de calidad, empaque y branding.", "We help hardware retailers, distributors and importers in Latin America grow with private labels. We develop their hardware, construction and fittings products in China, and we answer for the whole process: design, manufacturing, quality control, packaging and branding.")}</p></div>
    <div><h3>{L("Visión", "Vision")}</h3><p>{L("Ser el socio de referencia en Latinoamérica para crear marcas propias de ferretería, construcción y herrajes para muebles: el primero en que piensa un importador cuando quiere un producto propio, bien hecho y competitivo.", "To be Latin America’s reference partner for creating private labels in hardware, construction and furniture fittings: the first one an importer thinks of when they want their own product, well made and competitive.")}</p></div>
  </div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="pillars">
    <div><h3>{L("Especialización", "Specialization")}</h3><p>{L("Solo ferretería, construcción y herrajes. Dentro de ese mundo, todas las categorías; fuera de él, nada.", "Only hardware, construction and fittings. Within that world, every category; outside it, nothing.")}</p></div>
    <div><h3>{L("Responsabilidad total", "Full accountability")}</h3><p>{L("Respondemos por el resultado completo. No vendemos servicios sueltos.", "We answer for the complete result. We don’t sell stand-alone services.")}</p></div>
    <div><h3>{L("Una red de más de 20 años", "A network built over 20 years")}</h3><p>{L("Ferias, fábricas y contactos construidos en la trayectoria de nuestro equipo.", "Trade fairs, factories and contacts built over our team’s career.")}</p></div>
  </div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="team">
    <div class="shot"><img src="{img("equipo.webp")}" alt="{L("Patricio Campos y Phoebe, el equipo de HGS", "Patricio Campos and Phoebe, the HGS team")}" loading="lazy"></div>
    <div>
      <span class="eyebrow">{L("Equipo", "Team")}</span>
      <div class="person"><small>{L("Fundador y Director General · Chile", "Founder and Managing Director · Chile")}</small><h3>Patricio Campos Araya</h3>
        <p>{L("Más de 20 años creando marcas propias para el mundo ferretero y de la construcción en Latinoamérica, con proyectos en Chile, Perú, Paraguay, Colombia, Ecuador y México.", "Over 20 years creating private labels for the hardware and construction trade in Latin America, with projects in Chile, Peru, Paraguay, Colombia, Ecuador and Mexico.")}</p>
        <p style="margin-top:12px">{L("Lideró el desarrollo de cientos de productos y de estas marcas:", "He led the development of hundreds of products and of these brands:")}</p>
        <div class="brands"><span>Kutz</span><span>Bauker</span><span>Redline</span><span>Humboldt</span><span>Dairu</span></div>
        <p style="margin-top:8px;font-size:14px">{L("Trayectoria personal del fundador. No son clientes de HGS.", "The founder’s personal track record. These are not HGS clients.")}</p>
      </div>
      <div class="person"><small>{L("Directora de Operaciones · China", "Director of Operations · China")}</small><h3>Phoebe</h3>
        <p>{L("Desde Shanghái coordina las fábricas, recibe y revisa las muestras y acompaña cada producción.", "From Shanghai she coordinates factories, receives and reviews samples and follows every production run.")}</p></div>
    </div>
  </div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="split rev">
    <div><span class="eyebrow">{L("Marca propia", "Own brand")}</span><h2>{L("DRAVIK, la marca propia de HGS", "DRAVIK, HGS’s own brand")}</h2>
      <p class="sub">{L("Escalas de aluminio y acero desarrolladas por HGS de punta a punta. Es la prueba de que aplicamos a nuestra propia marca el mismo camino que te proponemos.", "Aluminum and steel ladders developed by HGS end to end. Proof that we apply to our own brand the same path we propose to you.")}</p>
      <p style="margin-top:20px"><a class="more" href="{href("cats")}#escalas">{L("Ver escalas DRAVIK →", "See DRAVIK ladders →")}</a></p></div>
    <div class="shot wide"><img src="{img("escala-bodega.webp")}" alt="{L("Escala articulada DRAVIK en uso", "DRAVIK multi-position ladder in use")}" loading="lazy"></div>
  </div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">{L("Oficinas", "Offices")}</span><h2>{L("Dos oficinas, un solo equipo", "Two offices, one team")}</h2></div></div>
  <div class="offices">
    <div><small>Chile</small><h3>Santiago</h3><p>{L("Área comercial, a cargo de Patricio.", "Commercial team, led by Patricio.")}</p></div>
    <div><small>China</small><h3>{L("Shanghái", "Shanghai")}</h3><p>{L("Operación: fábricas, muestras y calidad, a cargo de Phoebe.", "Operations: factories, samples and quality, led by Phoebe.")}</p></div>
  </div>
</div></section>''' + final_band() + "</main>"
    return page("about", L("Nosotros · HGS", "About us · HGS"),
                L("Quiénes somos: misión, visión, equipo y oficinas de HGS en Santiago y Shanghái.",
                  "Who we are: HGS mission, vision, team and offices in Santiago and Shanghai."), body)


# ---------------------------------------------------------------- Contacto
def contact():
    types = [L("Cadena", "Retail chain"), L("Distribuidor", "Distributor"), L("Ferretería", "Hardware store"), L("Otro", "Other")]
    stages = [L("Tengo un producto claro", "I have a clear product"), L("Quiero desarrollar una línea o marca", "I want to develop a line or brand"), L("Estoy explorando", "I’m exploring")]
    opts = "".join(f"<option>{t}</option>" for t in types)
    radios = "".join(f'<label class="radio"><input type="radio" name="etapa" value="{s}" data-label="{L("Etapa", "Stage")}" required> {s}</label>' for s in stages)
    lab = lambda es, en: L(es, en)
    form = f'''<form class="form" id="contact-form" novalidate data-to="{EMAIL}" data-subject="{L("Conversemos tu proyecto", "Let's talk about your project")}">
  <label>{lab("Nombre", "Name")}<input name="nombre" data-label="{lab("Nombre", "Name")}" autocomplete="name" required></label>
  <label>{lab("Empresa", "Company")}<input name="empresa" data-label="{lab("Empresa", "Company")}" autocomplete="organization" required></label>
  <label>{lab("Correo", "Email")}<input name="correo" type="email" data-label="{lab("Correo", "Email")}" autocomplete="email" required></label>
  <label>{lab("País", "Country")}<input name="pais" data-label="{lab("País", "Country")}" autocomplete="country-name" required></label>
  <label>{lab("Tipo de empresa", "Type of company")}<select name="tipo" data-label="{lab("Tipo de empresa", "Type of company")}" required><option value="">{lab("Elige una opción", "Choose one")}</option>{opts}</select></label>
  <label>{lab("Producto o categoría de interés", "Product or category of interest")}<input name="producto" data-label="{lab("Producto o categoría", "Product or category")}" required></label>
  <fieldset class="full"><legend>{lab("¿En qué etapa estás?", "Where are you in the process?")}</legend>{radios}</fieldset>
  <p class="err full">{lab("Completa todos los campos para continuar.", "Please fill in every field to continue.")}</p>
  <div class="form-foot full"><span class="cta-ring"><button class="pill pill-green" type="submit">{lab("Conversemos tu proyecto", "Let’s talk about your project")}</button></span><span class="note">{lab("Te respondemos en 1 día hábil", "We reply within 1 business day")}</span></div>
</form>
<div class="thanks" role="status"><h2>{lab("¡Gracias!", "Thank you!")}</h2><p>{lab("Abrimos tu programa de correo con los datos listos para enviar. Si no se abrió, ", "We opened your email app with your details ready to send. If it didn’t open, ")}<a id="mail-link" href="mailto:{EMAIL}">{lab("haz clic aquí", "click here")}</a>{lab(" o escríbenos a ", " or write to ")}{EMAIL}.</p></div>'''
    body = topbar("contact") + "<main>" + page_hero(
        L("Contacto", "Contact"),
        L("Conversemos tu proyecto", "Let’s talk about your project"),
        L("Cuéntanos qué quieres desarrollar. Te respondemos en 1 día hábil.", "Tell us what you want to develop. We reply within 1 business day.")
    ) + f'''<section class="sec" style="padding-top:8px"><div class="wrap"><div class="contact">
  <div class="contact-main">{form}</div>
  <aside class="side">
    <div><small>{L("Correo", "Email")}</small><a href="mailto:{EMAIL}">{EMAIL}</a></div>
    <div><small>WhatsApp</small><a href="{WA_URL}" target="_blank" rel="noopener">{WA_TXT}</a></div>
    <div><small>{L("Oficinas", "Offices")}</small><p style="color:var(--ink);font-size:17px">Santiago, Chile · {L("Shanghái, China", "Shanghai, China")}</p></div>
  </aside>
</div></div></section></main>'''
    return page("contact", L("Contacto · HGS", "Contact · HGS"),
                L("Conversemos tu proyecto de marca propia. Te respondemos en 1 día hábil.", "Let’s talk about your private-label project. We reply within 1 business day."), body)


def build():
    global lang
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "en"))
    shutil.copytree(os.path.join(HERE, "assets"), os.path.join(OUT, "assets"))
    shutil.copytree(os.path.join(HERE, "img"), os.path.join(OUT, "img"))
    with open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8") as fh:
        fh.write(FAVICON)
    gens = {"home": home, "how": how, "cats": cats, "cases": cases, "about": about, "contact": contact}
    for lang in ("es", "en"):
        for k, es, en in PAGES:
            fn = (es if lang == "es" else en)[0]
            path = os.path.join(OUT, fn) if lang == "es" else os.path.join(OUT, "en", fn)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(gens[k]())
    print("ok →", OUT)


if __name__ == "__main__":
    build()
