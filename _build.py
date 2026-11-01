#!/usr/bin/env python3
"""Genera el prototipo estático de hgs.cl (ES + EN) desde el brief v1.
Uso: build.py <salida> <modo>   modo = site | artifact
"""
import os, shutil, sys

OUT, MODE = sys.argv[1], sys.argv[2]
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
ART = MODE == "artifact"
HOME = {"es": "inicio.html" if ART else "index.html", "en": "home.html" if ART else "index.html"}

PAGES = [  # clave, slug es, slug en, menú es, menú en
    ("home", None, None, "Inicio", "Home"),
    ("how", "como-trabajamos.html", "how-we-work.html", "Cómo trabajamos", "How we work"),
    ("cats", "categorias.html", "categories.html", "Categorías", "Categories"),
    ("cases", "casos.html", "case-studies.html", "Casos", "Case studies"),
    ("about", "nosotros.html", "about.html", "Nosotros", "About us"),
    ("contact", "contacto.html", "contact.html", "Contacto", "Contact"),
]

def slug(key, lang):
    for k, es, en, *_ in PAGES:
        if k == key:
            return HOME[lang] if k == "home" else (es if lang == "es" else en)

def href(key, from_lang, to_lang=None):
    to_lang = to_lang or from_lang
    s = slug(key, to_lang)
    if from_lang == to_lang:
        return s
    return ("en/" + s) if to_lang == "en" else ("../" + s)

ICONS = {
    "define": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
    "factory": '<path d="M3 21V11l5 3v-3l5 3V5h5v16z"/><path d="M7 17.5h2M11.5 17.5h2"/>',
    "brand": '<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/><path d="M3 7.5 12 12l9-4.5M12 12v9"/>',
    "quality": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/><path d="m7.8 10.6 2 2 3.4-4"/>',
    "ship": '<path d="M3 15h18l-2.2 5H5.2z"/><path d="M6 15V9.5h12V15"/><path d="M9.5 9.5V5.5h5v4"/>',
}
CAM = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 8h4l2-3h6l2 3h4v12H3z"/><circle cx="12" cy="13.5" r="3.5"/></svg>'

from hgs_logo import LOGO_RINGS, LOGO_HGS, LOGO_TAG, LOGO_LINE  # logo vectorial HGS
# Collage del mix de herrajes (caso destacado): fotos reales de producto HGS, sin marcas. src/img/herrajes/
HERRAJES = [
    ("corredera-telescopica", "Correderas telescópicas", "Telescopic drawer slides"),
    ("bisagra-cazoleta", "Bisagras de cazoleta", "Concealed cup hinges"),
    ("tirador", "Tiradores", "Pull handles"),
    ("corredera-rodillo", "Correderas de rodillo", "Roller drawer runners"),
    ("perilla", "Perillas", "Knobs"),
    ("cerradura", "Cerraduras de mueble", "Furniture locks"),
    ("pata", "Patas de mueble", "Furniture legs"),
    ("cargador-usb", "Cargadores USB de escritorio", "Desk USB chargers"),
    ("guia-bisagras", "Guías de instalación de bisagras", "Hinge drilling jigs"),
]

def herrajes_grid(lang):
    pre = "" if lang == "es" else "../"
    title = "Mix de herrajes para muebles" if lang == "es" else "Furniture hardware mix"
    cells = "".join(
        f'<figure><img src="{pre}img/herrajes/{k}.webp" alt="{es if lang == "es" else en}" loading="lazy" decoding="async" width="640" height="640">'
        f'<figcaption>{es if lang == "es" else en}</figcaption></figure>' for k, es, en in HERRAJES)
    return f'<div class="hx-grid" role="group" aria-label="{title}">{cells}</div>'


def logo(full=False, label="HGS Hardware Global Sourcing"):
    if full:
        return f'<svg class="logo logo-full" viewBox="0 0 402 208" role="img" aria-label="{label}">{LOGO_RINGS}{LOGO_HGS}{LOGO_LINE}{LOGO_TAG}</svg>'
    return f'<svg class="logo logo-mark" viewBox="0 0 402 129" aria-hidden="true">{LOGO_RINGS}{LOGO_HGS}</svg>'

FAVICON = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 0 129 129"><style>.lg-g{{fill:#00a990}}.lg-b{{fill:#0897de}}</style>{LOGO_RINGS}</svg>'

def icon(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'

def ph(lang, desc, cls=""):
    k = "Foto pendiente" if lang == "es" else "Photo pending"
    return f'<figure class="ph {cls}" role="img" aria-label="{k}: {desc}">{CAM}<span class="ph-k">{k}</span><span class="ph-d">{desc}</span></figure>'

def pend(lang, es, en):
    return f'<span class="pend">{es if lang == "es" else en}</span>'

# Fotos reales aprobadas por Pato (01-nov-2026). Archivo en src/img/, alt ES, alt EN, encuadre.
PHOTOS = {
    "fabrica-sacos": ("Patricio Campos en una f\u00e1brica de sacos de polipropileno en China", "Patricio Campos at a polypropylene sack factory in China", "50% 45%"),
    "feria-canton": ("Patricio Campos en la entrada de la Feria de Cant\u00f3n", "Patricio Campos at the entrance of the Canton Fair", "50% 70%"),
    "feria-herramientas": ("Patricio Campos con un proveedor de herramientas en la Feria de Cant\u00f3n", "Patricio Campos with a tool supplier at the Canton Fair", "50% 40%"),
    "escala-exhibicion": ("Escalas articuladas DRAVIK exhibidas en góndola", "DRAVIK folding ladders on display in store", "50% 55%"),
    "empaque-muestras": ("Revisión de empaques terminados, sin marca visible", "Reviewing finished packaging, brand not shown", "50% 60%"),
    "contenedor-puerta": ("Contenedor cargado con pallets, listo para cerrar y sellar", "Container loaded with pallets, ready to be closed and sealed", "50% 50%"),
    "saco-escombros": ("Sacos de escombros en obra, cargados en camioneta", "Debris sacks on a building site, loaded onto a truck", "50% 50%"),
    "escala-bodega": ("Escala articulada DRAVIK 4x3 en uso como andamio", "DRAVIK 4x3 folding ladder used as a scaffold", "50% 55%"),
    "equipo-patricio-phoebe": ("Patricio Campos y Phoebe, el equipo de HGS en China", "Patricio Campos and Phoebe, the HGS team in China", "50% 58%"),
    "stand-feria": ("Visita a un proveedor en su stand de la Feria de Cant\u00f3n", "Visiting a supplier at their Canton Fair booth", "50% 8%"),
    "patio-alambre": ("Patricio Campos en el patio de una f\u00e1brica de alambre", "Patricio Campos in the yard of a wire factory", "50% 55%"),
    "bodega-palas": ("Bodega de una f\u00e1brica de palas", "Warehouse of a shovel factory", "50% 35%"),
    "soldadura": ("Control en l\u00ednea de producci\u00f3n: soldadura en f\u00e1brica", "In-line production check: welding at the factory", "60% 40%"),
    "sacos-bodega": ("Sacos terminados en bodega, listos para embarque", "Finished sacks in the warehouse, ready to ship", "50% 50%"),
    "feria-cerrajeria": ("Stand de cerrajer\u00eda y candados de seguridad en feria", "Locks and safety padlocks booth at a trade fair", "50% 22%"),
    "carga-contenedor": ("Carga de pallets en el contenedor antes del embarque", "Loading pallets into the container before shipping", "50% 45%"),
}

def photo(lang, key, cls=""):
    pre = "" if lang == "es" else "../"
    if key not in PHOTOS:  # foto de producto cuadrada
        alt = T(lang, PRODUCTS[key])
        return f'<figure class="photo prod {cls}"><img src="{pre}img/productos/{key}.webp" alt="{alt}" loading="lazy" decoding="async"></figure>'
    es_alt, en_alt, pos = PHOTOS[key]
    alt = es_alt if lang == "es" else en_alt
    return f'<figure class="photo {cls}"><img src="{pre}img/{key}.webp" alt="{alt}" loading="lazy" decoding="async" style="object-position:{pos}"></figure>'

def media(lang, item, cls=""):
    """item: clave de PHOTOS (foto real) o par (es, en) para un marcador pendiente."""
    if item == "collage-herrajes":
        return f'<div class="hx-fig {cls}">{herrajes_grid(lang)}</div>'
    return photo(lang, item, cls) if isinstance(item, str) else ph(lang, T(lang, item), cls)

# Fotos de producto (zip v2, 01-nov-2026), cuadradas 800 px en src/img/productos/. Sin marcas de clientes;
# las escalas muestran DRAVIK, marca propia de HGS. Clave: (alt es, alt en).
PRODUCTS = {
    "bisagra-cazoleta-a": ("Bisagra de cazoleta con cierre suave", "Soft-close concealed cup hinge"),
    "bisagra-cazoleta-b": ("Bisagra de cazoleta y base", "Concealed cup hinge and mounting plate"),
    "bisagra-cazoleta-c": ("Bisagra de cazoleta", "Concealed cup hinge"),
    "corredera-telescopica": ("Correderas telescópicas", "Telescopic drawer slides"),
    "corredera-rodillo": ("Correderas de rodillo", "Roller drawer runners"),
    "perilla": ("Perillas", "Knobs"),
    "tirador-a": ("Tirador embutido", "Recessed pull handle"),
    "tirador-b": ("Tirador de acero inoxidable", "Stainless steel pull handle"),
    "parasol": ("Parasol para auto", "Car sun shade"),
    "pata": ("Pata de mueble", "Furniture leg"),
    "cerradura": ("Cerradura de mueble", "Furniture lock"),
    "cargador-usb": ("Cargador USB de escritorio", "Desk USB charger"),
    "cargador-inalambrico": ("Cargador inalámbrico de escritorio", "Desk wireless charger"),
    "plataforma-a": ("Plataforma de carga ensamblable", "Modular moving dolly"),
    "plataforma-b": ("Plataforma de carga con manilla", "Moving dolly with handle"),
    "prensa-esquinera": ("Prensa esquinera", "Corner clamp"),
    "guia-bisagras": ("Guía de instalación de bisagras", "Hinge drilling jig"),
    "plantilla-bisagras": ("Plantilla de instalación de bisagras", "Hinge installation template"),
    "saco-rojo": ("Saco de polipropileno rojo", "Red polypropylene sack"),
    "saco-blanco": ("Saco de polipropileno blanco", "White polypropylene sack"),
    "escala-articulada": ("Escala articulada de aluminio DRAVIK", "DRAVIK folding aluminum ladder"),
    "escala-tijera": ("Escala tijera de aluminio DRAVIK", "DRAVIK aluminum step ladder"),
    "piso-2-peldanos": ("Piso de 2 peldaños DRAVIK", "DRAVIK 2-step stool"),
    "escala-ferreteria": ("Escala articulada DRAVIK en ferretería", "DRAVIK folding ladder at a hardware store"),
    "escala-obra": ("Escala DRAVIK en obra", "DRAVIK ladder on a building site"),
    "piso-garage": ("Piso DRAVIK en uso", "DRAVIK step stool in use"),
    "escala-exterior": ("Escala tijera DRAVIK en uso", "DRAVIK step ladder in use"),
    "clavo-granel": ("Clavos a granel en caja de exportación", "Bulk nails in an export carton"),
    "clavo-medicion": ("Medición de clavos con pie de metro", "Measuring nails with a caliper"),
    "clavo-techo-medicion": ("Medición de clavo de techo en inspección", "Measuring a roofing nail during inspection"),
}

def tile(lang, key, caption=True):
    """Mosaico cuadrado: foto de producto (PRODUCTS) o foto de terreno (PHOTOS)."""
    pre = "" if lang == "es" else "../"
    if key in PRODUCTS:
        alt, src = T(lang, PRODUCTS[key]), f"{pre}img/productos/{key}.webp"
    else:
        alt, src = T(lang, PHOTOS[key][:2]), f"{pre}img/{key}.webp"
    cap = f"<figcaption>{alt}</figcaption>" if caption else ""
    return f'<figure><img src="{src}" alt="{alt}" loading="lazy" decoding="async" width="800" height="800">{cap}</figure>'

STAGES = [
    ("define",
     ("Definir la línea", "Define the line"),
     ("Entendemos tu negocio, revisamos tu surtido y tu competencia, y definimos productos, calidad y precio objetivo.",
      "We get to know your business, review your assortment and competitors, and define products, quality and target price."),
     (["Revisión de tu surtido", "Análisis de la competencia", "Definición de productos", "Calidad y precio objetivo"],
      ["Assortment review", "Competitor analysis", "Product definition", "Target quality and price"]),
     ["stand-feria"]),
    ("factory",
     ("Encontrar la fábrica y validar muestras", "Find the factory and validate samples"),
     ("Buscamos, evaluamos y auditamos fábricas. Pedimos, comparamos y aprobamos muestras.",
      "We search, assess and audit factories. We request, compare and approve samples."),
     (["Búsqueda de fábricas", "Evaluación y auditoría", "Comparación de muestras", "Aprobación de muestras"],
      ["Factory search", "Assessment and audit", "Sample comparison", "Sample approval"]),
     ["patio-alambre", "bisagra-cazoleta-a", "bodega-palas"]),
    ("brand",
     ("Crear la marca y el empaque", "Create the brand and packaging"),
     ("Nombre, logo, artes de caja, etiquetas y códigos de barra.",
      "Name, logo, box artwork, labels and barcodes."),
     (["Nombre", "Logo", "Artes de caja", "Etiquetas", "Códigos de barra"],
      ["Name", "Logo", "Box artwork", "Labels", "Barcodes"]),
     ["escala-exhibicion", "empaque-muestras", "piso-2-peldanos"]),
    ("quality",
     ("Asegurar la calidad", "Assure quality"),
     ("Fichas técnicas, control en producción e inspección antes del embarque.",
      "Technical specs, in-production control and pre-shipment inspection."),
     (["Fichas técnicas", "Control en producción", "Inspección antes del embarque"],
      ["Technical specs", "In-production control", "Pre-shipment inspection"]),
     ["soldadura", "clavo-techo-medicion", "clavo-medicion"]),
    ("ship",
     ("Embarcar y entregar", "Ship and deliver"),
     ("Consolidamos la carga (incluso en contenedores mixtos), coordinamos el embarque y lo seguimos hasta tu bodega.",
      "We consolidate cargo (including mixed containers), coordinate shipping and track it all the way to your warehouse."),
     (["Consolidación, incluso contenedores mixtos", "Coordinación del embarque", "Seguimiento hasta tu bodega"],
      ["Consolidation, including mixed containers", "Shipping coordination", "Tracking to your warehouse"]),
     ["carga-contenedor", "contenedor-puerta"]),
]

CTA = ("Conversemos tu proyecto", "Let's talk about your project")
CTA_NOTE = ("Te acompañamos desde la idea hasta que el producto llega a tu bodega. Te respondemos en 1 día hábil.",
            "We support you from the idea until the product reaches your warehouse. We reply within 1 business day.")
PATH_MSG = ("No te vendemos un servicio suelto: te acompañamos en todo el camino y respondemos por el resultado.",
            "We don't sell you a one-off service: we stay with you the whole way and take responsibility for the result.")

def T(lang, pair):
    return pair[0] if lang == "es" else pair[1]

def cta(lang, note=True, cls=""):
    a = f'<a class="btn {cls}" href="{href("contact", lang)}">{T(lang, CTA)} <span class="arr" aria-hidden="true">→</span></a>'
    if not note:
        return a
    return f'<div class="cta-group">{a}<p class="cta-note">{T(lang, CTA_NOTE)}</p></div>'

def cta_band(lang):
    h = T(lang, ("Cuéntanos qué quieres desarrollar.", "Tell us what you want to develop."))
    return f'''<section class="cta-band"><div class="wrap">
<h2>{h}</h2>{cta(lang)}</div></section>'''

def path_list(lang):
    items = []
    for i, (ic, title, body, _, _) in enumerate(STAGES, 1):
        et = T(lang, ("Etapa", "Stage"))
        items.append(f'<li><span class="ic">{icon(ic)}</span><div><span class="num">{et} {i}</span><h3>{T(lang, title)}</h3><p>{T(lang, body)}</p></div></li>')
    return '<ol class="path">' + "".join(items) + "</ol>"

# ---------- páginas ----------

def page_home(lang):
    es = lang == "es"
    return f'''
<section class="hero"><div class="wrap hero-grid">
  <div>
    <p class="eyebrow">Hardware Global Sourcing</p>
    <h1>{"Especialistas en ferretería y construcción" if es else "Hardware &amp; construction specialists"}</h1>
    <p class="lead">{"Desarrollamos marcas propias desde China para cadenas, distribuidores y ferreterías latinoamericanas." if es else "We develop private-label brands from China for retail chains, distributors and hardware stores across Latin America."}</p>
    {cta(lang)}
  </div>
  {photo(lang, "feria-canton", "tall")}
</div></section>

<section class="section rule" aria-labelledby="trust"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">{"Confían en nosotros" if es else "Trusted by"}</p>
  <h2 id="trust">{"Trabajamos con cadenas líderes, distribuidores y ferreterías del mercado chileno." if es else "We work with leading retail chains, distributors and hardware stores in the Chilean market."}</h2></div>
  <div class="proof">
    <div><p class="big">{"Cientos de productos desarrollados" if es else "Hundreds of products developed"}</p><p>{"En ferretería, construcción y herrajes." if es else "In hardware, construction and furniture fittings."}</p></div>
    <div><p class="big">{"Más de 20 años de red" if es else "A network built over 20+ years"}</p><p>{"Ferias, fábricas y contactos construidos en la trayectoria de nuestro equipo." if es else "Trade fairs, factories and contacts built over our team's career."}</p></div>
    <div><p class="big">{"Un solo socio" if es else "One single partner"}</p><p>{"Respondemos por el resultado completo, de la idea a tu bodega." if es else "We are accountable for the whole result, from idea to your warehouse."}</p></div>
  </div>
</div></section>

<section class="section" aria-labelledby="range"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">{"Lo que ya hemos desarrollado" if es else "What we have already developed"}</p>
  <h2 id="range">{"Productos reales, vendidos y con ficha técnica, de los herrajes a la obra." if es else "Real products, sold and fully specified, from furniture fittings to the building site."}</h2></div>
  <div class="pgrid pgrid-4">{"".join(tile(lang, k) for k in HOME_RANGE)}</div>
  <p style="margin-top:28px"><a class="textlink" href="{href("cats", lang)}">{"Ver todas las categorías" if es else "See all categories"} →</a></p>
</div></section>

<section class="section tint" aria-labelledby="path"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">{"Cómo trabajamos" if es else "How we work"}</p>
  <h2 id="path">{"Un solo camino en 5 etapas" if es else "One path in 5 stages"}</h2></div>
  {path_list(lang)}
  <p class="path-msg">{T(lang, PATH_MSG)}</p>
  <p style="margin-top:28px"><a class="textlink" href="{href("how", lang)}">{"Ver las 5 etapas en detalle" if es else "See the 5 stages in detail"} →</a></p>
</div></section>

<section class="section" aria-labelledby="featured"><div class="wrap featured">
  <div style="display:grid;gap:20px;justify-items:start">
    <p class="eyebrow" id="featured">{"Caso destacado" if es else "Featured case"}</p>
    <blockquote>{"Desarrollamos líneas completas de herrajes para marcas propias reconocidas del retail chileno." if es else "We develop complete furniture-hardware lines for well-known private labels in Chilean retail."}</blockquote>
    <div class="pend-box">{"Detalle del caso por redactar (sin nombre del cliente)." if es else "Case details to be written (without the client's name)."}</div>
    <a class="textlink" href="{href("cases", lang)}">{"Ver casos de éxito" if es else "See case studies"} →</a>
  </div>
  <div class="hx-fig">{herrajes_grid(lang)}</div>
</div></section>

<section class="section rule" aria-labelledby="founder"><div class="wrap split">
  {photo(lang, "feria-herramientas", "tall")}
  <div class="text">
    <p class="eyebrow" id="founder">{"El fundador" if es else "The founder"}</p>
    <h2>{"Más de 20 años creando marcas propias para el mundo ferretero latinoamericano." if es else "Over 20 years creating private labels for the Latin American hardware world."}</h2>
    <p class="lead" style="font-size:1.05rem">{"Lideró el desarrollo de Kutz, Bauker, Redline, Humboldt y Dairu, y de cientos de productos." if es else "He led the development of Kutz, Bauker, Redline, Humboldt and Dairu, and of hundreds of products."}</p>
    <div><p class="founder-name">Patricio Campos Araya</p><p class="founder-role">{"Fundador y Director General" if es else "Founder and CEO"}</p></div>
    <a class="textlink" href="{href("about", lang)}">{"Conoce al equipo" if es else "Meet the team"} →</a>
  </div>
</div></section>
{cta_band(lang)}'''

def page_how(lang):
    es = lang == "es"
    blocks = []
    for i, (ic, title, body, items, photos) in enumerate(STAGES, 1):
        lis = "".join(f"<li>{x}</li>" for x in (items[0] if es else items[1]))
        phs = "".join(media(lang, p, "wide" if j == 0 else "") for j, p in enumerate(photos))
        et = "Etapa" if es else "Stage"
        blocks.append(f'''<article class="stage" id="etapa-{i}">
  <div>
    <div class="stage-top"><span class="ic">{icon(ic)}</span><span class="eyebrow">{et} {i} / 5</span></div>
    <h2>{T(lang, title)}</h2>
    <p class="body">{T(lang, body)}</p>
    <ul class="items">{lis}</ul>
  </div>
  <div class="stage-media">{phs}</div>
</article>''')
    return f'''
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">{"Cómo trabajamos" if es else "How we work"}</p>
  <h1>{"Un solo camino en 5 etapas, con un solo responsable." if es else "One path in 5 stages, with one accountable partner."}</h1>
  <p class="lead">{T(lang, PATH_MSG)}</p>
  {cta(lang, note=False)}
</div></section>
<section class="section tint"><div class="wrap">{path_list(lang)}</div></section>
<section class="section"><div class="wrap">{"".join(blocks)}</div></section>
{cta_band(lang)}'''

HOME_RANGE = ["bisagra-cazoleta-b", "corredera-telescopica", "parasol", "cargador-inalambrico",
              "escala-articulada", "clavo-granel", "saco-rojo", "plataforma-a"]

# Familias aprobadas por Pato (01-nov-2026). (nombre es/en, descripción es/en, subproductos es/en, fotos)
# Una foto es una clave de PRODUCTS o PHOTOS, o un par (es, en) para un marcador pendiente.
CATS = [
    (("Herrajes para muebles", "Furniture hardware"),
     ("Nuestra familia más grande: muchos códigos vendidos a cadenas y distribuidores, cada uno con su ficha técnica.",
      "Our largest family: many SKUs sold to retail chains and distributors, each with its own spec sheet."),
     (["Bisagras de cazoleta", "Correderas telescópicas", "Correderas de rodillo", "Tiradores", "Perillas", "Patas", "Cerraduras de mueble", "Cargadores USB e inalámbricos de escritorio"],
      ["Concealed cup hinges", "Telescopic drawer slides", "Roller drawer runners", "Pull handles", "Knobs", "Legs", "Furniture locks", "Desk USB and wireless chargers"]),
     ["bisagra-cazoleta-a", "bisagra-cazoleta-b", "bisagra-cazoleta-c", "corredera-telescopica", "corredera-rodillo",
      "tirador-a", "tirador-b", "perilla", "pata", "cerradura", "cargador-usb", "cargador-inalambrico"]),
    (("Accesorios para mueblistas", "Accessories for furniture makers"),
     ("Herramientas pensadas para el taller y la instalación: armar, mover e instalar muebles más rápido.",
      "Tools for the workshop and on-site installation: build, move and install furniture faster."),
     (["Plataformas de carga ensamblables", "Prensas esquineras", "Guías y plantillas de instalación de bisagras"],
      ["Modular moving dollies", "Corner clamps", "Hinge drilling jigs and templates"]),
     ["plataforma-a", "plataforma-b", "prensa-esquinera", "guia-bisagras", "plantilla-bisagras"]),
    (("Escalas", "Ladders"),
     ("Escalas articuladas, tijera y pisos de aluminio y acero, desarrollados bajo DRAVIK, nuestra marca propia.",
      "Folding ladders, step ladders and step stools in aluminum and steel, developed under DRAVIK, our own brand."),
     (["Escalas articuladas", "Escalas tijera", "Pisos de 2 y 3 peldaños"], ["Folding ladders", "Step ladders", "2- and 3-step stools"]),
     ["escala-articulada", "escala-tijera", "piso-2-peldanos", "escala-ferreteria", "escala-obra", "piso-garage"]),
    (("Clavos y fijaciones", "Nails and fasteners"),
     ("Clavos a granel, en caja y en bolsa, y clavos de techo, medidos y pesados en cada inspección.",
      "Bulk, boxed and bagged nails and roofing nails, measured and weighed at every inspection."),
     (["Clavo corriente", "Clavo de techo", "Formatos a granel, caja de 25 kg y bolsa de 1 kg"], ["Common nails", "Roofing nails", "Bulk, 25 kg carton and 1 kg bag formats"]),
     ["clavo-granel", "clavo-medicion", "clavo-techo-medicion"]),
    (("Alambres y mallas", "Wire and mesh"),
     ("Alambres para construcción y campo, y mallas para cierres.", "Wire for construction and farming, and mesh for fencing."),
     (["Alambre de púas", "Alambre galvanizado", "Alambre recocido", "Malla hexagonal"], ["Barbed wire", "Galvanized wire", "Annealed wire", "Hexagonal mesh"]),
     ["patio-alambre", ("Rollos de alambre y malla (foto en edición, sin marca del cliente)", "Wire and mesh rolls (photo being edited, client brand removed)")]),
    (("Sacos y envases", "Sacks and packaging"),
     ("Sacos de polipropileno tejido en distintos colores, medidas y gramajes.", "Woven polypropylene sacks in different colors, sizes and weights."),
     (["Sacos de polipropileno", "Sacos para escombros"], ["Polypropylene sacks", "Debris sacks"]),
     ["saco-escombros", "saco-rojo", "saco-blanco", "fabrica-sacos"]),
]

def cat_media(lang, item):
    return tile(lang, item) if isinstance(item, str) else ph(lang, T(lang, item))

def page_cats(lang):
    es = lang == "es"
    fams = []
    for i, (name, desc, subs, pics) in enumerate(CATS, 1):
        chips = "".join(f'<span class="chip">{x}</span>' for x in (subs[0] if es else subs[1]))
        fams.append(f'''<article class="fam" id="fam-{i}">
  <div class="fam-text"><p class="eyebrow">{i:02d}</p><h2>{T(lang, name)}</h2><p>{T(lang, desc)}</p><div class="meta">{chips}</div></div>
  <div class="pgrid">{"".join(cat_media(lang, p) for p in pics)}</div>
</article>''')
    return f'''
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">{"Categorías" if es else "Categories"}</p>
  <h1>{"Todo el mundo ferretero y de construcción, con un solo socio." if es else "The entire hardware and construction world, with one single partner."}</h1>
  <p class="lead">{"Estas son familias que ya hemos desarrollado, vendido y especificado. Dentro del mundo ferretero y de construcción desarrollamos todas las categorías; fuera de él, ninguna." if es else "These are families we have already developed, sold and specified. Within hardware and construction we develop every category; outside it, none."}</p>
</div></section>
<section class="section"><div class="wrap">
  <div class="fams">{"".join(fams)}</div>
  <div class="cat-close">
    <p>{"¿Tu categoría no está aquí? Si es ferretería o construcción, sabemos cómo desarrollarla. Conversemos." if es else "Don't see your category? If it's hardware or construction, we know how to develop it. Let's talk."}</p>
    {cta(lang, note=False)}
  </div>
</div></section>
{cta_band(lang)}'''

CASES = [
    (("Línea completa de herrajes para la marca propia de una cadena chilena", "A complete furniture-hardware line for a Chilean retail chain's private label"),
     [("Herrajes para muebles", "Furniture hardware"), ("Cadena", "Retail chain"), ("Chile", "Chile")],
     "collage-herrajes"),
    (("Escalas articuladas de aluminio DRAVIK", "DRAVIK folding aluminum ladders"),
     [("Escalas", "Ladders"), ("Marca propia HGS", "HGS own brand")],
     "escala-bodega"),
    (("Sacos de polipropileno", "Polypropylene sacks"),
     [("Sacos y envases", "Sacks and packaging")],
     "saco-escombros"),
]

def page_cases(lang):
    es = lang == "es"
    keys = [("El desafío", "The challenge"), ("Qué hicimos", "What we did"), ("Resultado", "Result")]
    out = []
    for title, chips, photo in CASES:
        ch = "".join(f'<span class="chip">{T(lang, c)}</span>' for c in chips)
        rows = "".join(f'<div><span class="k">{T(lang, k)}</span><span>{pend(lang, "Por redactar", "To be written")}</span></div>' for k in keys)
        out.append(f'''<article class="case">
  {media(lang, photo)}
  <div class="case-body"><div class="meta">{ch}</div><h2>{T(lang, title)}</h2><div class="case-struct">{rows}</div></div>
</article>''')
    return f'''
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">{"Casos" if es else "Case studies"}</p>
  <h1>{"Casos de éxito" if es else "Success stories"}</h1>
  <p class="lead">{"Proyectos reales, contados sin nombres de clientes." if es else "Real projects, told without client names."}</p>
  <div class="pend-box">{"Los casos están por redactar. Abajo, los tres candidatos del brief con la estructura propuesta." if es else "Cases are still to be written. Below are the three candidates from the brief, with the proposed structure."}</div>
</div></section>
<section class="section"><div class="wrap cases">{"".join(out)}</div></section>
{cta_band(lang)}'''

def page_about(lang):
    es = lang == "es"
    pillars = [
        (("Especialización", "Specialization"), ("Solo ferretería, construcción y herrajes. Dentro de ese mundo, todas las categorías; fuera de él, nada.", "Only hardware, construction and fittings. Within that world, every category; outside it, nothing.")),
        (("Un solo socio, responsabilidad total", "One partner, full accountability"), ("Respondemos por el resultado completo. No vendemos servicios sueltos.", "We are accountable for the whole result. We don't sell one-off services.")),
        (("Una red de más de 20 años", "A network built over 20+ years"), ("Ferias, fábricas y contactos construidos en la trayectoria de Patricio y Phoebe.", "Trade fairs, factories and contacts built over Patricio's and Phoebe's careers.")),
    ]
    pl = "".join(f'<div><h3>{T(lang, a)}</h3><p>{T(lang, b)}</p></div>' for a, b in pillars)
    return f'''
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">{"Nosotros" if es else "About us"}</p>
  <h1>{"Un solo socio, responsable de la idea a tu bodega." if es else "One partner, accountable from idea to your warehouse."}</h1>
  <p class="lead">{"HGS (Hardware Global Sourcing) desarrolla marcas propias de ferretería y construcción desde China para el mercado latinoamericano." if es else "HGS (Hardware Global Sourcing) develops hardware and construction private labels from China for the Latin American market."}</p>
</div></section>

<section class="section"><div class="wrap"><div class="pillars">{pl}</div></div></section>

<section class="section rule" aria-labelledby="team"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">{"Equipo" if es else "Team"}</p><h2 id="team">{"Quiénes están detrás" if es else "Who is behind HGS"}</h2></div>
  {photo(lang, "equipo-patricio-phoebe", "wide team-photo")}
  <div class="people">
    <article class="person">
      <div class="info">
        <p class="founder-role">{"Fundador y Director General · Chile" if es else "Founder and CEO · Chile"}</p>
        <h3>Patricio Campos Araya</h3>
        <p>{"Más de 20 años creando marcas propias para el mundo ferretero y de la construcción en Latinoamérica. Lideró el desarrollo de Kutz, Bauker, Redline, Humboldt y Dairu, y de cientos de productos." if es else "Over 20 years creating private labels for the Latin American hardware and construction world. He led the development of Kutz, Bauker, Redline, Humboldt and Dairu, and of hundreds of products."}</p>
        <p>{"Su trayectoria incluye proyectos en Chile, Perú, Paraguay, Colombia, Ecuador y México." if es else "His career includes projects in Chile, Peru, Paraguay, Colombia, Ecuador and Mexico."}</p>
      </div>
    </article>
    <article class="person">
      <div class="info">
        <p class="founder-role">{"Directora de Operaciones en China" if es else "Director of Operations, China"}</p>
        <h3>Phoebe {pend(lang, "apellido por confirmar", "surname to be confirmed")}</h3>
        <div class="pend-box">{"Trayectoria y apellido por confirmar con Phoebe." if es else "Background and surname to be confirmed with Phoebe."}</div>
      </div>
    </article>
  </div>
</div></section>

<section class="section tint" aria-labelledby="brands"><div class="wrap">
  <div class="sec-head"><h2 id="brands">{"Marcas en cuyo desarrollo participó el fundador" if es else "Brands the founder helped develop"}</h2></div>
  <div class="brands"><span>Kutz</span><span>Bauker</span><span>Redline</span><span>Humboldt</span><span>Dairu</span></div>
  <p style="margin-top:14px;color:var(--muted);font-size:.9rem">{"Trayectoria personal del fundador. No son clientes de HGS." if es else "The founder's personal track record. These are not HGS clients."}</p>
</div></section>

<section class="section" aria-labelledby="dravik"><div class="wrap dravik">
  <figure class="ph" role="img" aria-label="Logo DRAVIK">{CAM}<span class="ph-k">{"Logo pendiente" if es else "Logo pending"}</span><span class="ph-d">{"Logo DRAVIK en vectorial (.ai, .svg o .pdf). El .jpeg actual se ve pixelado." if es else "DRAVIK logo in vector format (.ai, .svg or .pdf). The current .jpeg looks pixelated."}</span></figure>
  <div style="display:grid;gap:14px">
    <p class="eyebrow">{"Marca propia" if es else "Own brand"}</p>
    <h2 id="dravik">{"DRAVIK, marca propia de HGS" if es else "DRAVIK, HGS's own brand"}</h2>
    <p class="lead" style="font-size:1.05rem">{"Escalas articuladas de aluminio desarrolladas por HGS." if es else "Folding aluminum ladders developed by HGS."}</p>
  </div>
</div></section>

<section class="section rule" aria-labelledby="offices"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">{"Oficinas" if es else "Offices"}</p><h2 id="offices">{"Dos oficinas, un solo equipo" if es else "Two offices, one team"}</h2></div>
  <div class="offices">
    <div class="office"><p class="country">Chile</p><h3>Santiago</h3><p>{"Área comercial, a cargo de Patricio." if es else "Commercial team, led by Patricio."}</p></div>
    <div class="office"><p class="country">China</p><h3>{"Shanghái" if es else "Shanghai"}</h3><p>{"Operación en China, a cargo de Phoebe: recibe y revisa muestras y coordina fábricas." if es else "Operations in China, led by Phoebe: receives and reviews samples and coordinates factories."}</p></div>
  </div>
</div></section>
{cta_band(lang)}'''

def page_contact(lang):
    es = lang == "es"
    def L(a, b): return a if es else b
    err = L("Completa este campo.", "Please fill in this field.")
    types = [("Cadena", "Retail chain"), ("Distribuidor", "Distributor"), ("Ferretería", "Hardware store"), ("Otro", "Other")]
    stages = [("Tengo un producto claro", "I have a clear product in mind"), ("Quiero desarrollar una línea o marca", "I want to develop a line or brand"), ("Estoy explorando", "I'm exploring")]
    tr = "".join(f'<label class="choice"><input type="radio" name="tipo" id="tipo-{i}" value="{t[0]}"> {T(lang, t)}</label>' for i, t in enumerate(types))
    sr = "".join(f'<label class="choice"><input type="radio" name="etapa" id="etapa-{i}" value="{t[0]}"> {T(lang, t)}</label>' for i, t in enumerate(stages))
    return f'''
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">{L("Contacto", "Contact")}</p>
  <h1>{T(lang, CTA)}</h1>
  <p class="lead">{T(lang, CTA_NOTE)}</p>
</div></section>
<section class="section"><div class="wrap contact-grid">
  <div>
    <form class="form" id="contact-form" novalidate>
      <div class="row2">
        <div class="field" data-req><label for="f-nombre">{L("Nombre", "Name")}</label><input id="f-nombre" name="nombre" autocomplete="name"><span class="err" hidden>{err}</span></div>
        <div class="field" data-req><label for="f-empresa">{L("Empresa", "Company")}</label><input id="f-empresa" name="empresa" autocomplete="organization"><span class="err" hidden>{err}</span></div>
      </div>
      <div class="field" data-req><label for="f-pais">{L("País", "Country")}</label><input id="f-pais" name="pais" autocomplete="country-name"><span class="err" hidden>{err}</span></div>
      <fieldset class="field" data-req><legend>{L("Tipo de empresa", "Type of company")}</legend><div class="chips-radio">{tr}</div><span class="err" hidden>{L("Elige una opción.", "Choose an option.")}</span></fieldset>
      <div class="field" data-req><label for="f-producto">{L("Producto o categoría de interés", "Product or category of interest")}</label><input id="f-producto" name="producto"><span class="err" hidden>{err}</span></div>
      <fieldset class="field" data-req><legend>{L("¿En qué etapa estás?", "Where are you in the process?")}</legend><div class="choices">{sr}</div><span class="err" hidden>{L("Elige una opción.", "Choose an option.")}</span></fieldset>
      <div class="cta-group"><button class="btn" type="submit">{L("Enviar", "Send")} <span class="arr" aria-hidden="true">→</span></button>
      <p class="cta-note" style="font-size:.85rem">{L("Prototipo: el formulario no envía datos todavía.", "Prototype: the form does not send data yet.")}</p></div>
    </form>
    <div class="thanks" id="thanks" tabindex="-1" hidden>
      <h2>{L("Gracias, recibimos tu proyecto.", "Thank you, we've received your project.")}</h2>
      <p>{L("Te respondemos en 1 día hábil. Si prefieres, agenda de inmediato una primera conversación.", "We'll reply within 1 business day. If you prefer, book a first conversation right away.")}</p>
      <a class="btn ghost" href="#thanks">{L("Agenda 20 minutos", "Book 20 minutes")}</a>
      {pend(lang, "Falta el enlace a la página de reservas de Google Calendar", "Google Calendar booking link pending")}
    </div>
  </div>
  <aside class="side" aria-label="{L("Otros canales", "Other channels")}">
    <div class="channel"><span class="k">{L("Correo", "Email")}</span><span class="v" id="c-mail">contact@hgspyme.cl</span>
      <button class="copy" type="button" data-copy="c-mail" data-ok="{L("Copiado", "Copied")}">{L("Copiar", "Copy")}</button>
      {pend(lang, "Verificar que el correo exista", "Check that the address exists")}</div>
    <div class="channel"><span class="k">WhatsApp</span><span class="v" id="c-wa">+56 9 7799 9363</span>
      <div style="display:flex;gap:10px;flex-wrap:wrap"><button class="copy" type="button" data-copy="c-wa" data-ok="{L("Copiado", "Copied")}">{L("Copiar", "Copy")}</button>
      <a class="textlink" href="https://wa.me/56977999363" target="_blank" rel="noopener">{L("Abrir WhatsApp", "Open WhatsApp")} →</a></div></div>
    <div class="channel"><span class="k">{L("Oficinas", "Offices")}</span><span>Santiago, Chile</span><span>{L("Shanghái", "Shanghai")}, China</span></div>
  </aside>
</div></section>'''

BUILDERS = {"home": page_home, "how": page_how, "cats": page_cats, "cases": page_cases, "about": page_about, "contact": page_contact}
TITLES = {
    "home": ("HGS · Marcas propias de ferretería y construcción desde China", "HGS · Hardware & construction private labels from China"),
    "how": ("Cómo trabajamos · HGS", "How we work · HGS"),
    "cats": ("Categorías · HGS", "Categories · HGS"),
    "cases": ("Casos de éxito · HGS", "Case studies · HGS"),
    "about": ("Nosotros · HGS", "About us · HGS"),
    "contact": ("Conversemos tu proyecto · HGS", "Let's talk about your project · HGS"),
}
DESCS = {
    "es": "HGS desarrolla marcas propias de ferretería y construcción desde China para cadenas, distribuidores y ferreterías latinoamericanas.",
    "en": "HGS develops hardware and construction private labels from China for retail chains, distributors and hardware stores across Latin America.",
}
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;1,8..60,500&display=swap">'

def render(key, lang, skeleton=True):
    es = lang == "es"
    pre = "" if es else "../"
    nav = []
    for k, _, _, mes, men in PAGES:
        cur = ' aria-current="page"' if k == key else ""
        nav.append(f'<a href="{href(k, lang)}"{cur}>{mes if es else men}</a>')
    other = "en" if es else "es"
    lang_sw = (f'<span>ES</span><a href="{href(key, lang, "en")}" hreflang="en" lang="en">EN</a>' if es
               else f'<a href="{href(key, lang, "es")}" hreflang="es" lang="es">ES</a><span>EN</span>')
    head = f'''<title>{T(lang, TITLES[key])}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{DESCS[lang]}">
{FONTS}
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{pre}styles.css">'''
    body = f'''<div class="proto"><div class="wrap"><span><b>{"PROTOTIPO v1" if es else "PROTOTYPE v1"}</b> · {"Fotos y textos marcados en amarillo son provisorios." if es else "Photos and text marked in yellow are placeholders."}</span><span>hgs.cl</span></div></div>
<header class="site-head"><div class="wrap">
  <a class="brand" href="{href("home", lang)}" aria-label="HGS {"inicio" if es else "home"}">{logo()}<span class="brand-sub">Hardware<br>Global Sourcing</span></a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">{"Menú" if es else "Menu"}</button>
  <nav class="nav" id="nav" aria-label="{"Principal" if es else "Main"}">{"".join(nav)}
    <span class="lang" aria-label="{"Idioma" if es else "Language"}">{lang_sw}</span>
    <a class="btn small head-cta" href="{href("contact", lang)}" style="color:#fff;border-bottom:0">{T(lang, CTA)}</a>
  </nav>
</div></header>
<main>{BUILDERS[key](lang)}</main>
<footer class="site-foot"><div class="wrap">
  <div class="foot-grid">
    <div style="display:grid;gap:16px;align-content:start">{logo(full=True)}<p style="max-width:28em">{DESCS[lang]}</p></div>
    <div><p class="k">{"Páginas" if es else "Pages"}</p><ul>{"".join(f"<li>{a}</li>" for a in nav)}</ul></div>
    <div><p class="k">{"Oficinas" if es else "Offices"}</p><ul><li>Santiago, Chile</li><li>{"Shanghái" if es else "Shanghai"}, China</li></ul></div>
  </div>
  <div class="foot-legal"><span>© 2026 HGS Hardware Global Sourcing</span><span>{"Prototipo v1, no publicar" if es else "Prototype v1, not for release"}</span></div>
</div></footer>
<script src="{pre}app.js"></script>'''
    if not skeleton:
        return head + "\n" + body + "\n"
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head}
</head>
<body>
{body}
</body>
</html>
'''

os.makedirs(os.path.join(OUT, "en"), exist_ok=True)
for f in ("styles.css", "app.js"):
    shutil.copy(os.path.join(SRC, f), os.path.join(OUT, f))
if os.path.isdir(os.path.join(SRC, "img")):
    shutil.copytree(os.path.join(SRC, "img"), os.path.join(OUT, "img"), dirs_exist_ok=True)
with open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8") as fh:
    fh.write(FAVICON)
for k, *_ in PAGES:
    for lang in ("es", "en"):
        p = slug(k, lang)
        path = os.path.join(OUT, p) if lang == "es" else os.path.join(OUT, "en", p)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(render(k, lang))
if ART:
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(render("home", "es", skeleton=False))
print("ok", OUT)
