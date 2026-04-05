
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










# endpoint do wszystkich tłumaczeń wersetów
@app.route('/api/books')
def get_books():
    try:
        # Lista ksiąg Starego i Nowego Testamentu
        books = [
            {"value": "rdz", "name": "Rodzaju"},
            {"value": "wj", "name": "Wyjścia"},
            {"value": "kpl", "name": "Kpł"},
            {"value": "lb", "name": "Lewitic"},
            {"value": "lb", "name": "Lb"},
            {"value": "joz", "name": "Jozuego"},
            {"value": "sdz", "name": "Sędzi"},
            {"value": "sdz", "name": "Sdz"},
            {"value": "ne", "name": "Nehemiasza"},
            {"value": "est", "name": "Estery"},
            {"value": "job", "name": "Joba"},
            {"value": "ps", "name": "Psalm"},
            {"value": "prz", "name": "Przysłów"},
            {"value": "pnp", "name": "Pieśń nad Pieśniami"},
            {"value": "iz", "name": "Izajasza"},
            {"value": "jr", "name": "Jeremiasza"},
            {"value": "lm", "name": "Lamentacje"},
            {"value": "ez", "name": "Ezechiela"},
            {"value": "dn", "name": "Daniela"},
            {"value": "oz", "name": "Ozejasza"},
            {"value": "jo", "name": "Joela"},
            {"value": "am", "name": "Amosa"},
            {"value": "jon", "name": "Jonasza"},
            {"value": "mi", "name": "Michasza"},
            {"value": "nah", "name": "Nahuma"},
            {"value": "hab", "name": "Habakuka"},
            {"value": "sof", "name": "Sofoniasza"},
            {"value": "ag", "name": "Aggeusza"},
            {"value": "za", "name": "Zachariasza"},
            {"value": "mal", "name": "Malachiasza"},
            {"value": "mt", "name": "Mateusza"},
            {"value": "mk", "name": "Marka"},
            {"value": "łk", "name": "Łukasza"},
            {"value": "jan", "name": "Jana"},
            {"value": "dz", "name": "Dzieje Apostolskie"},
            {"value": "rz", "name": "Rzymian"},
            {"value": "1kor", "name": "1 Koryntian"},
            {"value": "2kor", "name": "2 Koryntian"},
            {"value": "ga", "name": "Galatów"},
            {"value": "ef", "name": "Efezjan"},
            {"value": "flp", "name": "Filipian"},
            {"value": "kol", "name": "Kolosan"},
            {"value": "1tes", "name": "1 Tesaloniczan"},
            {"value": "2tes", "name": "2 Tesaloniczan"},
            {"value": "1tm", "name": "1 Tymoteusza"},
            {"value": "2tm", "name": "2 Tymoteusza"},
            {"value": "tyt", "name": "Tytusa"},
            {"value": "flm", "name": "Filemona"},
            {"value": "hbr", "name": "Hebrajczyków"},
            {"value": "jk", "name": "Jakuba"},
            {"value": "1p", "name": "1 Piotra"},
            {"value": "2p", "name": "2 Piotra"},
            {"value": "1j", "name": "1 Jana"},
            {"value": "2j", "name": "2 Jana"},
            {"value": "3j", "name": "3 Jana"},
            {"value": "jud", "name": " Judy"},
            {"value": "obj", "name": "Objawienie"}
        ]
        
        return jsonify(books)
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Błąd: {str(e)}"}, 500)

@app.route('/api/chapters/<book>')
def get_chapters(book):
    try:
        # Mapowanie liczby rozdziałów dla poszczególnych ksiąg
        chapters_count = {
            "rdz": 50, "wj": 40, "kpl": 27, "lb": 24, "joz": 24, "sdz": 12, "ne": 13,
            "est": 10, "job": 42, "ps": 150, "prz": 31, "pnp": 8, "iz": 66, "jr": 52,
            "lm": 5, "ez": 48, "dn": 12, "oz": 14, "jo": 9, "am": 9, "jon": 4,
            "mi": 7, "nah": 3, "hab": 3, "sof": 3, "ag": 14, "za": 14, "mal": 4,
            "mt": 28, "mk": 16, "łk": 24, "jan": 21, "dz": 28, "rz": 16, "1kor": 16,
            "2kor": 13, "ga": 6, "ef": 6, "flp": 4, "kol": 4, "1tes": 5, "2tes": 3,
            "1tm": 6, "2tm": 4, "tyt": 3, "flm": 1, "hbr": 13, "jk": 5, "1p": 5,
            "2p": 3, "1j": 5, "2j": 1, "3j": 1, "jud": 1, "obj": 22
        }
        
        max_chapters = chapters_count.get(book, 0)
        if max_chapters == 0:
            return jsonify({"status": "error", "message": "Nieznana księga"}, 404)
        
        chapters = [{"value": i, "name": f"Rozdział {i}"} for i in range(1, max_chapters + 1)]
        return jsonify(chapters)
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Błąd: {str(e)}"}, 500)

@app.route('/api/verses/<book>/<chapter>')
def get_verses(book, chapter):
    try:
        # Mapowanie liczby wersetów dla poszczególnych ksiąg i rozdziałów
        # Używamy przybliżonej liczby wersetów (może się różnić w zależności od wydania Biblii)
        verses_count = {
            "rdz": {1: 31, 2: 25, 3: 24, 4: 26, 5: 32, 6: 22, 7: 24, 8: 22, 9: 29, 10: 32, 11: 32, 12: 20, 13: 18, 14: 24, 15: 21, 16: 16, 17: 28, 18: 33, 19: 38, 20: 18, 21: 24, 22: 24, 23: 20, 24: 67, 25: 34, 26: 35, 27: 46, 28: 22, 29: 29, 30: 43, 31: 55, 32: 32, 33: 20, 34: 31, 35: 29, 36: 43, 37: 36, 38: 30, 39: 23, 40: 38, 41: 57, 42: 51, 43: 34, 44: 23, 45: 28, 46: 34, 47: 31, 48: 35, 49: 26, 50: 26},
            "wj": {1: 22, 2: 25, 3: 17, 4: 20, 5: 23, 6: 30, 7: 25, 8: 16, 9: 20, 10: 22, 11: 10, 12: 46, 13: 23, 14: 31, 15: 22, 16: 18, 17: 18, 18: 27, 19: 25, 20: 26, 21: 37, 22: 31, 23: 45, 24: 23, 25: 23, 26: 27, 27: 21, 28: 43, 29: 46, 30: 38, 31: 22, 32: 35, 33: 20, 34: 35, 35: 23, 36: 38, 37: 29, 38: 31, 39: 43, 40: 38},
            "kpl": {1: 22, 2: 25, 3: 17, 4: 24, 5: 23, 6: 25, 7: 24, 8: 18, 9: 20, 10: 29, 11: 16, 12: 23, 13: 18, 14: 31, 15: 20, 16: 33, 17: 27, 18: 26, 19: 25, 20: 29, 21: 37, 22: 24, 23: 21, 24: 28, 25: 23, 26: 46, 27: 22},
            "lb": {1: 29, 2: 23, 3: 20, 4: 24, 5: 21, 6: 25, 7: 24, 8: 17, 9: 28, 10: 29, 11: 32, 12: 23, 13: 18, 14: 22, 15: 26, 16: 33, 17: 24, 18: 27, 19: 36, 20: 18, 21: 33, 22: 20, 23: 30, 24: 51, 25: 23, 26: 46, 27: 22},
            "joz": {1: 18, 2: 24, 3: 17, 4: 20, 5: 23, 6: 25, 7: 24, 8: 18, 9: 28, 10: 43, 11: 23, 12: 15, 13: 29, 14: 22, 15: 20, 16: 18, 17: 17, 18: 9, 19: 18, 20: 46, 21: 26, 22: 33, 23: 27, 24: 16},
            "sdz": {1: 15, 2: 23, 3: 20, 4: 21, 5: 22, 6: 25, 7: 18, 8: 18, 9: 20, 10: 27, 11: 23, 12: 25, 13: 19, 14: 24, 15: 19, 16: 20},
            "ne": {1: 11, 2: 20, 3: 32, 4: 6, 5: 19, 6: 15, 7: 73, 8: 18, 9: 38, 10: 34, 11: 31, 12: 22, 13: 31},
            "est": {1: 22, 2: 23, 3: 14, 4: 17, 5: 27, 6: 14, 7: 15, 8: 17, 9: 15, 10: 26},
            "job": {1: 22, 2: 13, 3: 19, 4: 21, 5: 27, 6: 30, 7: 21, 8: 22, 9: 35, 10: 42, 11: 20, 12: 13, 13: 15, 14: 17, 15: 21, 16: 22, 17: 16, 18: 21, 19: 29, 20: 29, 21: 34, 22: 30, 23: 24, 24: 17, 25: 17, 26: 33, 27: 23, 28: 28, 29: 25, 30: 24, 31: 21, 32: 22, 33: 25, 34: 29, 35: 30, 36: 33, 37: 23, 38: 41, 39: 31, 40: 26, 41: 34, 42: 17},
            "ps": {1: 6, 2: 12, 3: 8, 4: 8, 5: 12, 6: 9, 7: 17, 8: 9, 9: 20, 10: 4, 11: 7, 12: 9, 13: 6, 14: 7, 15: 5, 16: 11, 17: 15, 18: 50, 19: 14, 20: 9, 21: 13, 22: 31, 23: 6, 24: 10, 25: 22, 26: 12, 27: 14, 28: 9, 29: 11, 30: 12, 31: 11, 32: 11, 33: 7, 34: 22, 35: 28, 36: 13, 37: 40, 38: 22, 39: 8, 40: 13, 41: 13, 42: 9, 43: 17, 44: 26, 45: 17, 46: 11, 47: 14, 48: 20, 49: 20, 50: 26, 51: 19, 52: 11, 53: 6, 54: 11, 55: 24, 56: 17, 57: 11, 58: 11, 59: 17, 60: 12, 61: 8, 62: 12, 63: 11, 64: 10, 65: 13, 66: 20, 67: 7, 68: 35, 69: 13, 70: 19, 71: 24, 72: 20, 73: 17, 74: 16, 75: 22, 76: 12, 77: 72, 78: 39, 79: 13, 80: 7, 81: 13, 82: 8, 83: 18, 84: 13, 85: 13, 86: 17, 87: 7, 88: 18, 89: 52, 90: 17, 91: 16, 92: 15, 93: 11, 94: 23, 95: 12, 96: 17, 97: 12, 98: 9, 99: 9, 100: 5, 101: 10, 102: 22, 103: 8, 104: 17, 105: 9, 106: 23, 107: 16, 108: 13, 109: 19, 110: 6, 111: 10, 112: 10, 113: 7, 114: 8, 115: 18, 116: 18, 117: 9, 118: 72, 119: 72, 120: 6, 121: 7, 122: 9, 123: 6, 124: 8, 125: 9, 126: 9, 127: 6, 128: 8, 129: 8, 130: 6, 131: 7, 132: 18, 133: 17, 134: 12, 135: 7, 136: 9, 137: 9, 138: 3, 139: 8, 140: 13, 141: 10, 142: 12, 143: 5, 144: 8, 145: 19, 146: 17, 147: 20, 148: 14, 149: 9, 150: 6}
        }
        
        book_verses = verses_count.get(book, {})
        chapter_verses = book_verses.get(int(chapter), 0)
        
        if chapter_verses == 0:
            return jsonify({"status": "error", "message": "Nieznany rozdział lub brak wersetów"}, 404)
        # Przetwórz wersety
        verses_list = []
        for verse in verses:
            verses_list.append({"value": verse[0], "name": verse[0]})
        
        return jsonify(verses_list)
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Błąd: {str(e)}"}, 500)

