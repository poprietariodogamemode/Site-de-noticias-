import json
import os
import re
import feedparser
from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)
ARQUIVO = "/tmp/noticias.json"

FEEDS = [
    {"url": "https://feeds.ign.com/ign/all", "categoria": "Geral"},
    {"url": "https://www.rockpapershotgun.com/feed", "categoria": "PC"},
    {"url": "https://kotaku.com/rss", "categoria": "Geral"},
    {"url": "https://www.eurogamer.net/?format=rss", "categoria": "Geral"},
    {"url": "https://gamerant.com/feed/", "categoria": "Geral"},
    {"url": "https://www.thegamer.com/feed/", "categoria": "Geral"},
    {"url": "https://www.vg247.com/feed", "categoria": "Consoles"},
    {"url": "https://www.pushsquare.com/feeds/latest", "categoria": "PlayStation"},
    {"url": "https://www.purexbox.com/feeds/latest", "categoria": "Xbox"},
    {"url": "https://www.nintendolife.com/feeds/latest", "categoria": "Nintendo"},
]

def limpar_html(texto):
    if not texto:
        return ""
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = re.sub(r'&[a-zA-Z]+;', ' ', texto)
    texto = texto.strip()
    return texto[:300] + "..." if len(texto) > 300 else texto

def coletar():
    noticias = []
    links_vistos = set()

    for feed_info in FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            nome_fonte = feed.feed.get("title", "Desconhecido")
            for entry in feed.entries[:8]:
                link = entry.get("link", "")
                if link in links_vistos:
                    continue
                links_vistos.add(link)

                imagem = ""
                if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
                    imagem = entry.media_thumbnail[0].get("url", "")
                elif hasattr(entry, "media_content") and entry.media_content:
                    imagem = entry.media_content[0].get("url", "")
                elif hasattr(entry, "enclosures") and entry.enclosures:
                    enc = entry.enclosures[0]
                    if "image" in enc.get("type", ""):
                        imagem = enc.get("url", "")

                published = entry.get("published", "")
                try:
                    from email.utils import parsedate_to_datetime
                    dt = parsedate_to_datetime(published)
                    published_fmt = dt.strftime("%d/%m/%Y %H:%M")
                    timestamp = dt.timestamp()
                except:
                    published_fmt = ""
                    timestamp = 0

                noticias.append({
                    "titulo": entry.get("title", "Sem título"),
                    "link": link,
                    "resumo": limpar_html(entry.get("summary", "")),
                    "fonte": nome_fonte,
                    "categoria": feed_info["categoria"],
                    "imagem": imagem,
                    "publicado": published_fmt,
                    "timestamp": timestamp,
                })
        except Exception as e:
            print(f"Erro ao coletar {feed_info['url']}: {e}")

    noticias.sort(key=lambda x: x["timestamp"], reverse=True)

    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(noticias, f, ensure_ascii=False)

    return noticias

def carregar_noticias():
    try:
        with open(ARQUIVO, encoding="utf-8") as f:
            return json.load(f)
    except:
        return coletar()

@app.route("/")
def index():
    noticias = carregar_noticias()
    categorias = sorted(set(n["categoria"] for n in noticias))
    return render_template("index.html", noticias=noticias, categorias=categorias)

@app.route("/api/atualizar")
def atualizar():
    noticias = coletar()
    return jsonify({"status": "ok", "total": len(noticias)})

@app.route("/api/noticias")
def api_noticias():
    return jsonify(carregar_noticias())
