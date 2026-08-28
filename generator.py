"""
Gerador do site de achadinhos.

O que este script faz sozinho (automatico, via GitHub Actions):
1. Le data/products.csv (produtos com link de afiliado que VOCE adicionou).
2. Gera o site estatico em docs/ (index.html + sitemap.xml + robots.txt).
3. Busca no Mercado Livre (API publica) ideias de produtos por palavra-chave
   e salva em data/ml_ideas.json -- SUGESTOES para voce revisar e, se quiser,
   colocar em products.csv com o link de afiliado correspondente.

O que este script NAO faz sozinho:
- Gerar o link de afiliado em si. Isso exige estar logado no painel de
  afiliado da Shopee/Mercado Livre (login humano), entao precisa ser voce
  pegando o link e colando em data/products.csv. E o unico passo manual
  que sobra -- sem ele nao ha comissao nenhuma, com ou sem automacao.
"""
import csv
import json
import os
from datetime import datetime, timezone

import requests
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR = os.path.join(BASE_DIR, "docs")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")


def load_config():
    with open(os.path.join(BASE_DIR, "config.json"), encoding="utf-8") as f:
        return json.load(f)


def load_products():
    path = os.path.join(DATA_DIR, "products.csv")
    products = []
    if not os.path.exists(path):
        return products
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("affiliate_link", "").strip():
                products.append(row)
    return products


def fetch_ml_ideas(keywords, limit_per_keyword=10):
    """Busca produtos publicos no Mercado Livre para virarem ideias de conteudo.
    Nao gera link de afiliado (isso exige o painel de afiliados); serve so
    para voce saber o que esta em alta e decidir o que anunciar.

    Aviso: o Mercado Livre restringiu essa busca publica e agora costuma
    responder 403 sem um app registrado com OAuth (mais um cadastro manual).
    Por isso esta funcao e "melhor esforco": se falhar, o site continua
    sendo gerado normalmente a partir de data/products.csv.
    """
    ideas = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept": "application/json",
    }
    for kw in keywords:
        try:
            resp = requests.get(
                "https://api.mercadolibre.com/sites/MLB/search",
                params={"q": kw, "limit": limit_per_keyword},
                headers=headers,
                timeout=15,
            )
            resp.raise_for_status()
            for item in resp.json().get("results", []):
                ideas.append({
                    "keyword": kw,
                    "title": item.get("title"),
                    "price": item.get("price"),
                    "permalink": item.get("permalink"),
                    "thumbnail": item.get("thumbnail"),
                })
        except requests.RequestException as e:
            print(f"[aviso] falha ao buscar '{kw}' no Mercado Livre: {e}")
    return ideas


def render_site(config, products):
    os.makedirs(OUT_DIR, exist_ok=True)
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)

    index_tpl = env.get_template("index.html")
    html = index_tpl.render(
        site_title=config["site_title"],
        site_description=config["site_description"],
        products=products,
    )
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    write_sitemap(config)
    write_robots(config)


def write_sitemap(config):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    site_url = config["site_url"].rstrip("/")
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{site_url}/</loc>
    <lastmod>{now}</lastmod>
  </url>
</urlset>
"""
    with open(os.path.join(OUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)


def write_robots(config):
    site_url = config["site_url"].rstrip("/")
    robots = f"User-agent: *\nAllow: /\nSitemap: {site_url}/sitemap.xml\n"
    with open(os.path.join(OUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)


def main():
    config = load_config()
    products = load_products()

    os.makedirs(DATA_DIR, exist_ok=True)
    ideas = fetch_ml_ideas(config.get("ml_search_keywords", []))
    with open(os.path.join(DATA_DIR, "ml_ideas.json"), "w", encoding="utf-8") as f:
        json.dump(ideas, f, ensure_ascii=False, indent=2)

    render_site(config, products)
    print(f"Site gerado com {len(products)} produtos publicados e {len(ideas)} ideias novas em data/ml_ideas.json")


if __name__ == "__main__":
    main()
