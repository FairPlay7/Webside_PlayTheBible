
import os
import json
import string
from unittest import result
from jinja2.nodes import Output
import requests
from bs4 import BeautifulSoup
from pprint import pprint

from flask import Flask, render_template, request, redirect, send_file, session, jsonify
from flask_cors import CORS

from dotenv import load_dotenv
from pathlib import Path

import re

load_dotenv() # wczyta zmienne z .env

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

CORS(app)



# Przenieś do strony głównej
@app.route('/index')
def index():  
    return render_template('index.html')

# Przenieś do podstrony random_verse
@app.route('/random_verse')
def random_verse():  
    return render_template('random_verse.html')

# Przenieś do podstrony edition_comparison
@app.route('/edition_comparison')
def edition_comparison():  
    return render_template('edition_comparison.html')


# Przenieś do podstrony schemat
@app.route('/schemat')
def schemat():
    return render_template('schemat.html')










@app.route('/')

def home():
    return render_template('index.html')


@app.route('/test', methods=['POST'])
def test():
    try:
        # Pobieranie i walidacja danych wejściowych
        data = request.get_json()
        if not data:
            return {"status": "error", "message": "Brak danych wejściowych"}, 400

        required_fields = ['translation', 'book', 'chapter', 'verse', 'verse2']
        if not all(field in data for field in required_fields):
            return {"status": "error", "message": "Brak wymaganych pól w danych wejściowych"}, 400

        # Konwersja i walidacja typów
        try:
            translation_name = str(data['translation'])
            book_name = str(data['book'])
            chapter_number = int(data['chapter'])
            verse_number = int(data['verse'])
            verse_number2 = int(data['verse2'])
        except (ValueError, TypeError) as e:
            return {"status": "error", "message": "Nieprawidłowy format danych wejściowych"}, 400

        # Walidacja wartości
        if chapter_number <= 0 or verse_number < 0 or verse_number2 < 0:
            return {"status": "error", "message": "Numery rozdziałów i wersetów muszą być dodatnie"}, 400

        if verse_number2 != 0 and verse_number2 < verse_number:
            return {"status": "error", "message": "Drugi werset nie może być mniejszy niż pierwszy"}, 400

        # Budowanie URL z walidacją
        base_url = f"https://www.biblia.info.pl/biblia/{translation_name}/{book_name}/{chapter_number}"
        if verse_number == 0:
            url = base_url
        elif verse_number2 != 0:
            url = f"{base_url}/{verse_number}-{verse_number2}"
        else:
            url = f"{base_url}/{verse_number}"

        # Pobieranie i przetwarzanie danych
        try:
            response = requests.get(url)
            response.raise_for_status()  # Sprawdza kod odpowiedzi HTTP
        except requests.RequestException as e:
            return {"status": "error", "message": f"Błąd podczas pobierania danych z API: {str(e)}"}, 502

        soup = BeautifulSoup(response.text, 'html.parser')
        verses = soup.find_all('span', class_='verse')

        all_verses = []
        for verse in verses:
            content = verse.get_text(strip=True)
            content = re.sub(r'\(\d+\)\s*', '', content, flags=re.UNICODE).strip()
            content = ' '.join(content.split())
            if content:
                all_verses.append(content)

        # Budowanie odpowiedzi
        if verse_number == 0:
            reference = f"{book_name} {chapter_number}"
        elif verse_number2 != 0:
            reference = f"{book_name} {chapter_number}:{verse_number}-{verse_number2}"
        else:
            reference = f"{book_name} {chapter_number}:{verse_number}"

        return {
            "status": "success",
            "verses": all_verses,
            "reference": reference,
            "translation": translation_name
        }

    except Exception as e:
        # Logowanie błędu
        print(f"Błąd w funkcji test: {str(e)}", file=sys.stderr)
        return {"status": "error", "message": "Wystąpił nieoczekiwany błąd serwera"}, 500
    
    



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


# ----------------------- Do podstrony Losowanie Wersetów -----------------------



def get_random_verse_api(verse_path):
    # Mapowanie ścieżek na pełne nazwy ksiąg
    verse_mapping = {
        'wj/20/2[+15]': 'Wyjścia 20:2-17',
        'joz/1/9': 'Jozuego 1:9',
        'ne/8/10': 'Nehemiasza 8:10',
        'ps/1/1[+1]': 'Psalm 1:1-2',
        'ps/16/11': 'Psalm 16:11',
        'ps/19/15': 'Psalm 19:15',
        'ps/23/1': 'Psalm 23:1',
        'ps/27/1': 'Psalm 27:1',
        'ps/28/7': 'Psalm 28:7',
        'ps/34/5': 'Psalm 34:5',
        'ps/34/19': 'Psalm 34:19',
        'ps/37/4': 'Psalm 37:4',
        'ps/46/2': 'Psalm 46:2',
        'ps/55/23': 'Psalm 55:23',
        'ps/118/24': 'Psalm 118:24',
        'ps/119/11': 'Psalm 119:11',
        'ps/119/105': 'Psalm 119:105',
        'ps/121/1[+1]': 'Psalm 121:1-2',
        'ps/139/14': 'Psalm 139:14',
        'ps/150/6': 'Psalm 150:6',
        'prz/3/5': 'Przysłów 3:5',
        'prz/4/23': 'Przysłów 4:23',
        'prz/17/17': 'Przysłów 17:17',
        'prz/18/10': 'Przysłów 18:10',
        'pnp/8/7': 'Pieśń nad Pieśniami 8:7',
        'iz/26/3': 'Izajasza 26:3',
        'iz/40/31': 'Izajasza 40:31',
        'iz/41/10': 'Izajasza 41:10',
        'iz/43/2': 'Izajasza 43:2',
        'jr/29/11': 'Jeremiasza 29:11',
        'lm/3/22[+1]': 'Lamentacje 3:22-23',
        'mi/6/8': 'Michasza 6:8',
        'mt/5/3[+7]': 'Mateusza 5:3-10',
        'mt/5/16': 'Mateusza 5:16',
        'mt/6/33': 'Mateusza 6:33',
        'mt/7/7': 'Mateusza 7:7',
        'mt/7/12': 'Mateusza 7:12',
        'mt/11/28': 'Mateusza 11:28',
        'mt/22/37': 'Mateusza 22:37',
        'mt/28/20': 'Mateusza 28:20',
        'mk/9/23': 'Marka 9:23',
        'jan/1/12': 'Jana 1:12',
        'jan/3/16': 'Jana 3:16',
        'jan/8/32': 'Jana 8:32',
        'jan/11/25': 'Jana 11:25',
        'jan/13/35': 'Jana 13:35',
        'jan/14/6': 'Jana 14:6',
        'jan/14/27': 'Jana 14:27',
        'jan/15/5': 'Jana 15:5',
        'jan/15/12': 'Jana 15:12',
        'dz/4/12': 'Dzieje Apostolskie 4:12',
        'rz/1/16': 'Rzymian 1:16',
        'rz/3/23': 'Rzymian 3:23',
        'rz/5/8': 'Rzymian 5:8',
        'rz/6/23': 'Rzymian 6:23',
        'rz/8/1': 'Rzymian 8:1',
        'rz/8/28': 'Rzymian 8:28',
        'rz/10/9': 'Rzymian 10:9',
        'rz/12/2': 'Rzymian 12:2',
        'rz/12/9': 'Rzymian 12:9',
        'rz/15/13': 'Rzymian 15:13',
        '1kor/10/13': '1 Koryntian 10:13',
        '1kor/13/4': '1 Koryntian 13:4',
        '1kor/13/7': '1 Koryntian 13:7',
        '1kor/13/13': '1 Koryntian 13:13',
        '1kor/16/14': '1 Koryntian 16:14',
        '2kor/5/17': '2 Koryntian 5:17',
        '2kor/12/9': '2 Koryntian 12:9',
        'ga/2/20': 'Galatów 2:20',
        'ga/5/1': 'Galatów 5:1',
        'ga/5/22': 'Galatów 5:22',
        'ga/6/9': 'Galatów 6:9',
        'ef/2/8[+1]': 'Efezjan 2:8-9',
        'ef/4/26': 'Efezjan 4:26',
        'ef/4/32': 'Efezjan 4:32',
        'ef/5/2': 'Efezjan 5:2',
        'ef/6/10': 'Efezjan 6:10',
        'flp/3/14': 'Filipian 3:14',
        'flp/4/6': 'Filipian 4:6',
        'flp/4/13': 'Filipian 4:13',
        'kol/3/14': 'Kolosan 3:14',
        'kol/3/17': 'Kolosan 3:17',
        'kol/3/23': 'Kolosan 3:23',
        '1tes/5/16[+2]': '1 Tesaloniczan 5:16-18',
        '2tm/1/7': '2 Tymoteusza 1:7',
        '2tm/3/16': '2 Tymoteusza 3:16',
        'hbr/11/1': 'Hebrajczyków 11:1',
        'hbr/12/1[+1]': 'Hebrajczyków 12:1-2',
        'hbr/13/5': 'Hebrajczyków 13:5',
        'jk/1/5': 'Jakuba 1:5',
        'jk/1/22': 'Jakuba 1:22',
        '1p/3/15': '1 Piotra 3:15',
        '1p/4/8': '1 Piotra 4:8',
        '1p/5/7': '1 Piotra 5:7',
        '1j/1/9': '1 Jana 1:9',
        '1j/3/18': '1 Jana 3:18',
        '1j/4/8': '1 Jana 4:8',
        '1j/4/12': '1 Jana 4:12',
        '1j/4/19': '1 Jana 4:19',
        'ap/21/4': 'Objawienie 21:4'
    }
    
    # Jeśli verse_path jest pusty, wybierz losową ścieżkę
    if not verse_path:
        import random
        verse_path = random.choice(list(verse_mapping.keys()))
    
    url = "https://www.biblia.info.pl/biblia/ug/" + verse_path
    
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    verses = soup.find_all('span', class_='verse')

    all_verses = []
    for verse in verses:
        content = verse.get_text(strip=True)
        content = re.sub(r'\(\d+\)\s*', '', content, flags=re.UNICODE).strip()
        content = ' '.join(content.split())
        if content:
            all_verses.append(content)

    return all_verses, verse_mapping.get(verse_path, verse_path)






# endpoint do losowania wersetu
@app.route('/api/random-verse')
def get_random_verse_endpoint():
    try:
        # Wywołaj funkcję bez parametru, aby wybrać losowy werset
        verses, verse_name = get_random_verse_api('')
        return jsonify({
            'text': ' '.join(verses) if verses else 'Werset nie znaleziony',
            'name': verse_name,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'text': f'Błąd: {str(e)}',
            'name': 'Nieznany werset',
            'success': False
        })





