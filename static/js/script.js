

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










// Funkcja wyświetlająca werset we wszystkich tłumaczeniach
async function displayVerseAllTranslations() {
    try {
        const selectElement_1 = document.getElementById('translation_comparison');
        const selectElement_2 = document.getElementById('book_comparison');
        const selectElement_3 = document.getElementById('chapter_comparison');
        const selectElement_4 = document.getElementById('verse_comparison');
        const selectElement_5 = document.getElementById('verse2_comparison');
        const errorElement = document.getElementById('error');
        const resultElement = document.getElementById('verseResult');

        const selectedBookValue = selectElement_2 ? selectElement_2.value : '';
        const selectedChapterValue = selectElement_3 ? selectElement_3.value : '';
        const selectedVerseValue = selectElement_4 ? selectElement_4.value : '0';
        const selectedVerseValue2 = selectElement_5 ? selectElement_5.value : '0';

        // Walidacja pól
        if (!selectedBookValue || !selectedChapterValue) {
            if (errorElement) errorElement.textContent = 'Uzupełnij księgę i rozdział.';
            return;
        }

        // Wyczyszczenie poprzednich komunikatów
        if (errorElement) errorElement.textContent = '';
        if (resultElement) resultElement.textContent = '';

        // Lista wszystkich tłumaczeń z pełnymi nazwami
        const translations = [
            {code: 'ug', name: 'Uwspółcześniona Biblia Gdańska'},
            {code: 'ng', name: 'Nowa Biblia Gdańska'},
            {code: 'bg', name: 'Biblia Gdańska'},
            {code: 'bt', name: 'Biblia Tysiąclecia'},
            {code: 'bw', name: 'Biblia Warszawska'},
            {code: 'br', name: 'Biblia Warszawsko-Praska'},
            {code: 'esp', name: 'Edycja Świętego Pawła'},
            {code: 'bb', name: 'Biblia Brzeska'},
            {code: 'bp', name: 'Biblia Poznańska'},
            {code: 'jw', name: 'Biblia Jakuba Wujka'},
            {code: 'bm', name: 'Biblia Mesjańska'},
            {code: 'ns', name: 'Biblia Nowego Świata'},
            {code: 'bl', name: 'Biblia Lubelska'},
            {code: 'sz', name: 'Słowo Życia'},
            {code: 'eib', name: 'Przekład Dosłowny'},
            {code: 'tnp', name: 'Biblia Toruńska'},
            {code: 'kjv', name: 'King James Version (Eng.)'},
            {code: 'web', name: 'Webster Bible (Eng.)'},
            {code: 'ylt', name: 'Young\'s Literal Translation (Eng.)'},
            {code: 'vul', name: 'Łacińska Vulgata'},
            {code: 'gr', name: 'Grecka Septuaginta'}
        ];
        
        // Wyświetl komunikat ładowania
        resultElement.innerHTML = '<div style="text-align: center; padding: 20px;"><h3>Ładowanie wersetu we wszystkich tłumaczeniach...</h3></div>';

        // Pobierz wersety dla wszystkich tłumaczeń
        const promises = translations.map(async (translation) => {
            try {
                const response = await fetch('/test', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        translation: translation.code,
                        book: selectedBookValue,
                        chapter: selectedChapterValue,
                        verse: selectedVerseValue,
                        verse2: selectedVerseValue2
                    })
                });

                if (!response.ok) {
                    throw new Error(`Nieistniejący werset dla tego tłumaczenia / Verse does not exist in this translation: ${response.status}`);
                }

                const data = await response.json();
                
                if (data.status !== 'success') {
                    throw new Error(`Nieistniejący werset dla tego tłumaczenia / Verse does not exist in this translation`);
                }

                return {
                    translation: translation.code,
                    name: translation.name,
                    reference: data.reference,
                    verses: data.verses
                };
            } catch (error) {
                console.error(`Błąd dla tłumaczenia ${translation.name}:`, error);
                return {
                    translation: translation.code,
                    name: translation.name,
                    error: 'Nieistniejący werset dla tego tłumaczenia / Verse does not exist in this translation'
                };
            }
        });

        const results = await Promise.all(promises);
        
        // Formatowanie wyników
        let html = '';
        results.forEach(result => {
            if (result.error) {
                html += `
                    <div style="margin: 20px 0; border: 1px solid #ddd; padding: 15px; border-radius: 8px;">
                        <div style="font-weight: bold; color: #d32f2f; margin-bottom: 10px;">
                            Błąd: ${result.name} - ${result.error}
                        </div>
                    </div>
                `;
            } else {
                const versesHtml = result.verses.map(verse => 
                    `<div class="verse">${verse}</div>`
                ).join('');
                
                html += `
                    <div style="margin: 20px 0; border: 1px solid #ddd; padding: 15px; border-radius: 8px;">
                        <div style="font-weight: bold; color: #333; margin-bottom: 10px; background-color: #f5f5f5; padding: 8px; border-radius: 4px;">
                            ${result.reference} (${result.name})
                        </div>
                        <div class="verses" style="font-family: Arial, sans-serif; font-size: 16px; line-height: 1.6; color: black;">
                            ${versesHtml}
                        </div>
                    </div>
                `;
            }
        });

        resultElement.innerHTML = html;

    } catch (err) {
        console.error('Błąd:', err);
        const errorElement = document.getElementById('error');
        const resultElement = document.getElementById('verseResult');
        
        if (errorElement) {
            errorElement.textContent = 'Wystąpił nieoczekiwany błąd. Proszę spróbować ponownie.';
        }
        if (resultElement) {
            resultElement.innerHTML = '<div style="color: #d32f2f; text-align: center; padding: 20px;">Błąd ładowania wersetów</div>';
        }
    }
}



    // Obsługa nowego przycisku
    const allTranslationsButton = document.getElementById('showVerseButtonAllTranslations');
    if (allTranslationsButton) {
        allTranslationsButton.addEventListener('click', displayVerseAllTranslations);
    } else {
        console.error('Przycisk showVerseButtonAllTranslations nie znaleziony');
    }

    // Funkcje do ładowania danych formularzy
    async function loadBooks() {
        try {
            const response = await fetch('/api/books');
            const books = await response.json();
            const bookSelect = document.getElementById('book_comparison');
            
            if (bookSelect) {
                bookSelect.innerHTML = '<option value="">Wybierz księgę</option>';
                books.forEach(book => {
                    bookSelect.innerHTML += `<option value="${book.value}">${book.name}</option>`;
                });
            }
        } catch (error) {
            console.error('Błąd ładowania ksiąg:', error);
        }
    }

    async function loadChapters(book) {
        if (!book) return;
        
        try {
            const response = await fetch(`/api/chapters/${book}`);
            const chapters = await response.json();
            const chapterSelect = document.getElementById('chapter_comparison');
            
            if (chapterSelect) {
                chapterSelect.innerHTML = '<option value="">Wybierz rozdział</option>';
                chapters.forEach(chapter => {
                    chapterSelect.innerHTML += `<option value="${chapter}">${chapter}</option>`;
                });
            }
        } catch (error) {
            console.error('Błąd ładowania rozdziałów:', error);
        }
    }

    async function loadVerses(book, chapter) {
        if (!book || !chapter) return;
        
        try {
            const response = await fetch(`/api/verses/${book}/${chapter}`);
            const verses = await response.json();
            const verseSelect = document.getElementById('verse_comparison');
            const verse2Select = document.getElementById('verse2_comparison');
            
            if (verseSelect) {
                verseSelect.innerHTML = '<option value="">Wybierz werset</option>';
                verses.forEach(verse => {
                    verseSelect.innerHTML += `<option value="${verse}">${verse}</option>`;
                });
            }
            
            if (verse2Select) {
                verse2Select.innerHTML = '<option value="">Wybierz werset końcowy</option>';
                verses.forEach(verse => {
                    verse2Select.innerHTML += `<option value="${verse}">${verse}</option>`;
                });
            }
        } catch (error) {
            console.error('Błąd ładowania wersetów:', error);
        }
    }

    // Obsługa zmian w polach formularza
    document.addEventListener('DOMContentLoaded', function() {
        const bookSelect = document.getElementById('book_comparison');
        const chapterSelect = document.getElementById('chapter_comparison');
        
        if (bookSelect) {
            bookSelect.addEventListener('change', function() {
                loadChapters(this.value);
                loadVerses(this.value, chapterSelect.value);
            });
        }
        
        if (chapterSelect) {
            chapterSelect.addEventListener('change', function() {
                const book = bookSelect ? bookSelect.value : '';
                loadVerses(book, this.value);
            });
        }
        
        // Załaduj początkowe dane
        loadBooks();
    });
});

