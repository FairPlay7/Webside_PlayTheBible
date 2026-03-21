async function displayVerse() {
    try {
        const selectElement_1 = document.getElementById('translation');
        const selectElement_2 = document.getElementById('book');
        const selectElement_3 = document.getElementById('chapter');
        const selectElement_4 = document.getElementById('verse');
        const selectElement_5 = document.getElementById('verse2');
        const errorElement = document.getElementById('error');
        const resultElement = document.getElementById('result');

        const selectedTranslationValue = selectElement_1.value;
        const selectedBookValue = selectElement_2.value;
        const selectedChapterValue = selectElement_3.value;
        const selectedVerseValue = selectElement_4.value || '0';
        const selectedVerseValue2 = selectElement_5.value || '0';

        // Walidacja pól
        if (!selectedTranslationValue || !selectedBookValue || !selectedChapterValue) {
            if (errorElement) errorElement.textContent = 'Uzupełnij tłumaczenie, księgę i rozdział.';
            return;
        }

        // Wyczyszczenie poprzednich komunikatów
        if (errorElement) errorElement.textContent = '';
        if (resultElement) resultElement.textContent = '';

        // Zapytanie do backendu
        const response = await fetch('/test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                translation: selectedTranslationValue,
                book: selectedBookValue,
                chapter: selectedChapterValue,
                verse: selectedVerseValue,
                verse2: selectedVerseValue2
            })
        });

        const data = await response.json();
        
        if (!response.ok) {
            const errorMessage = data.message || 'Nie udało się pobrać wersetu.';
            if (errorElement) errorElement.textContent = `Błąd: ${errorMessage}`;
            return;
        }

        if (data.status !== 'success') {
            if (errorElement) errorElement.textContent = 'Nie udało się przetworzyć odpowiedzi serwera.';
            return;
        }

        // Wyświetlanie wyników
        if (resultElement) {
            // Formatowanie wersetów
            const versesHtml = data.verses.map(verse => 
                `<div class="verse">${verse}</div>`
            ).join('');
            
            resultElement.innerHTML = `
                <div class="bible-reference">${data.reference} (${data.translation})</div>
                <div class="verses">${versesHtml}</div>
            `;
        }

    } catch (err) {
        console.error('Błąd:', err);
        const errorElement = document.getElementById('error');
        if (errorElement) {
            errorElement.textContent = 'Wystąpił nieoczekiwany błąd. Proszę spróbować ponownie.';
        }
    }
}

// Dodaj obsługę przycisku
document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('get-verse-btn');
    if (button) {
        button.addEventListener('click', displayVerse);
    }
});









// Do podstrony Losowanie Wersetów

function displayRandomVerse() {
    console.log('Rozpoczynam pobieranie wersetu...');
    
    const resultElement = document.getElementById('verseRandomResult');
    if (!resultElement) {
        console.error('Element verseRandomResult nie znaleziony');
        return;
    }
    
    // Wyświetl komunikat ładowania
    resultElement.innerHTML = 
        '<div style="text-align: center; padding: 20px;">' +
        '<h3>Ładowanie wersetu...</h3>' +
        '</div>';
    
    // Wywołaj API dla losowego wersetu
    fetch('/api/random-verse')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Wyświetl werset z nazwą na białym pasku
                const verseTitle = data.name || 'Losowy werset';
                
                resultElement.innerHTML = 
                    '<div style="margin: 20px 0;">' +
                        '<div style="font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; color: black; margin-bottom: 10px;">' +
                            'Został wylosowany werset: ' + verseTitle +
                        '</div>' +
                        '<div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">' +
                            '<div style="font-family: Arial, sans-serif; font-size: 18px; line-height: 1.6; color: black; text-align: left;">' +
                                data.text +
                            '</div>' +
                        '</div>' +
                    '</div>';
            } else {
                // Wyświetl błąd
                resultElement.innerHTML = 
                    '<div style="margin: 20px 0;">' +
                        '<div style="font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; color: #d32f2f; margin-bottom: 10px;">' +
                            'Błąd ładowania wersetu' +
                        '</div>' +
                        '<div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">' +
                            '<p style="color: #666;">' + data.text + '</p>' +
                        '</div>' +
                    '</div>';
            }
        })
        .catch(error => {
            console.error('Błąd fetch:', error);
            
            // Wyświetl błąd sieciowy
            resultElement.innerHTML = 
                '<div style="margin: 20px 0;">' +
                    '<div style="font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; color: #d32f2f; margin-bottom: 10px;">' +
                        'Błąd połączenia z serwerem' +
                    '</div>' +
                    '<div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">' +
                        '<p style="color: #666;">Szczegóły: ' + error.message + '</p>' +
                        '<button onclick="location.reload()" style="margin-top: 10px; padding: 8px 16px; background-color: #87CEFA; color: white; border: none; border-radius: 4px; cursor: pointer;">Spróbuj ponownie</button>' +
                    '</div>' +
                '</div>';
        });
}





// Obsługa przycisku losowego wersetu
document.addEventListener('DOMContentLoaded', function() {
    const randomButton = document.getElementById('showRandomButton');
    if (randomButton) {
        randomButton.addEventListener('click', displayRandomVerse);
    } else {
        console.error('Przycisk showRandomButton nie znaleziony');
    }
});

