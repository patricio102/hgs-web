# HGS · sitio web (prototipo v1)

Sitio estático de hgs.cl en español (raíz) e inglés (`/en/`).

- `_build.py`: todo el contenido y la estructura de las páginas.
- `hgs_logo.py`: trazados del logo HGS (vectorizado desde el PDF original).
- `src/`: estilos, script y fotos (`src/img/`).

Generar el sitio localmente:

```
python3 _build.py public site
```

Vercel corre ese mismo comando en cada push a `main` y publica la carpeta `public/`.
