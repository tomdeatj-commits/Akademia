"""Monta simulador_3pg_eucalyptus.html a partir de fonte2.html, inserindo o motor (modelo3pg.js), os dados
(dados_min.json), a biblioteca de conceitos (conceitos.js) a interface dos conceitos (conceitos_ui.js) e o módulo de cubagem e toras (cubagem.js)."""
from pathlib import Path
d = Path(__file__).parent
ler = lambda n: (d / n).read_text(encoding="utf8")
html = ler("fonte2.html")
for marca, arq in [("/*MODELO*/", "modelo3pg.js"), ("/*DADOS*/", "dados_min.json"), ("/*CONCEITOS*/", "conceitos.js"), ("/*CONCEITOS_UI*/", "conceitos_ui.js"), ("/*CUBAGEM*/", "cubagem.js"), ("/*MATERIAL*/", "material_tcc.js"), ("/*MATERIAL_UI*/", "material_ui.js")]:
    assert html.count(marca) == 1, marca
    html = html.replace(marca, ler(arq).strip())
(d / "simulador_3pg_eucalyptus.html").write_text(html, encoding="utf8")
print("ok", len(html) // 1024, "KB")
# cópia para o GitHub Pages (Settings → Pages → Deploy from a branch → main /docs)
docs = d.parent / "docs"; docs.mkdir(exist_ok=True)
(docs / "index.html").write_text(html, encoding="utf8"); (docs / ".nojekyll").write_text("")
(docs / "integrado.html").write_text(ler("integrado.html"), encoding="utf8")
print("docs/index.html atualizado")
