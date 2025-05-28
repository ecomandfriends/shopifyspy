from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)
CORS(app)

def analizar_tienda(url):
    if not url.startswith("http"):
        url = "https://" + url

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        texto = soup.get_text().lower()

        tecnologias = []
        if "shopify" in texto or "cdn.shopify" in texto:
            tecnologias.append("Shopify")

        if "klaviyo" in texto:
            tecnologias.append("Klaviyo")

        if "gem pages" in texto:
            tecnologias.append("GemPages")

        if "gempages" in texto:
            tecnologias.append("GemPages")

        if "judge.me" in texto or "judgeme" in texto:
            tecnologias.append("Judge.me")

        if "reconvert" in texto:
            tecnologias.append("ReConvert")

        if "yotpo" in texto:
            tecnologias.append("Yotpo")

        if "loox" in texto:
            tecnologias.append("Loox")

        theme = None
        theme_match = re.search(r"theme\s*['\"]name['\"]\s*:\s*['\"](.+?)['\"]", response.text)
        if theme_match:
            theme = theme_match.group(1)

        return {
            "domain": url,
            "apps_detected": list(set(tecnologias)),
            "theme": theme or "No detectado"
        }

    except Exception as e:
        return {
            "error": "No se pudo analizar la tienda",
            "detalle": str(e)
        }

@app.route("/analyze")
def analizar():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Falta la URL"}), 400
    resultado = analizar_tienda(url)
    return jsonify(resultado)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

