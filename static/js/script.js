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