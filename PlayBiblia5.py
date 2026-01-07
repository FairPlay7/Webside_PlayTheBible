
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


# Przenieś do podstrony schemat.html
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



