
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

COMMON_APPS = [
    "klaviyo", "judge.me", "loox", "reconvert", "yotpo",
    "shopify inbox", "pagefly", "aftership", "gempages",
    "one click upsell", "booster apps", "bold", "revy", "hulkapps"
]

@app.route("/analyze", methods=["GET"])
def analyze():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Falta la URL"})

    try:
        if not url.startswith("http"):
            url = "https://" + url

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        script_tags = soup.find_all("script", src=True)
        html = response.text.lower()

        apps_found = []
        for app in COMMON_APPS:
            if app in html:
                apps_found.append(app)

        theme = "Desconocido"
        for tag in script_tags:
            if "theme" in tag["src"] or "theme.js" in tag["src"]:
                theme = tag["src"].split("/")[-2] if "/" in tag["src"] else tag["src"]

        return jsonify({
            "domain": url,
            "apps_detected": apps_found,
            "theme": theme
        })

    except Exception as e:
        return jsonify({"error": f"No se pudo analizar la tienda: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=False, port=5000)
