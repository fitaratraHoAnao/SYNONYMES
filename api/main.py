from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/recherche', methods=['GET'])
def recherche():
    # Obtenir le paramètre 'synonyme' de la requête
    mot = request.args.get('synonyme', 'miracle')
    
    # URL à scraper
    url = f"https://www.cnrtl.fr/synonymie/{mot}"
    
    # Envoyer une requête HTTP GET à la page
    response = requests.get(url)
    
    # Vérifier si la requête a réussi
    if response.status_code != 200:
        return jsonify({"error": "Impossible d'accéder à la page CNRTL"}), 500
    
    # Parse la réponse HTML avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Scraper les synonymes à partir de la structure HTML
    synonyme_section = soup.find('div', {'id': 'contentbox'})
    
    # Si la section des synonymes n'existe pas
    if not synonyme_section:
        return jsonify({"error": f"Aucun résultat trouvé pour le mot '{mot}'"}), 404
    
    synonymes = synonyme_section.find_all('td', class_='syno_format')
    
    # Extraire les synonymes sous forme de liste
    result = []
    for syn in synonymes:
        result.append(syn.get_text(strip=True))
    
    # Si aucun synonyme n'a été trouvé
    if not result:
        return jsonify({"message": f"Aucun synonyme trouvé pour le mot '{mot}'"}), 200
    
    # Créer une réponse JSON
    return jsonify({
        "synonyme": mot,
        "synonymes": result
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
