// Baner Cookies - Style CSS
const cookieStyles = `
.cookie-banner {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #2c3e50;
    color: white;
    padding: 15px;
    text-align: center;
    z-index: 1000;
    display: none;
}
.cookie-banner button {
    margin: 0 10px;
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}
.cookie-accept {
    background: #27ae60;
    color: white;
}
.cookie-reject {
    background: #e74c3c;
    color: white;
}
.cookie-settings {
    background: #3498db;
    color: white;
}
`;

// Dodanie stylów do strony
function addCookieStyles() {
    if (!document.getElementById('cookie-styles')) {
        const styleElement = document.createElement('style');
        styleElement.id = 'cookie-styles';
        styleElement.textContent = cookieStyles;
        document.head.appendChild(styleElement);
    }
}

// Tworzenie banera cookies
function createCookieBanner() {
    if (document.getElementById('cookieBanner')) {
        return; // Baner już istnieje
    }

    const bannerHTML = `
        <div id="cookieBanner" class="cookie-banner">
            <p>Ta strona używa plików cookies do analizy ruchu. Możesz zaakceptować wszystkie, odrzucić lub dostosować ustawienia.</p>
            <button class="cookie-accept" onclick="acceptAllCookies()">Akceptuj wszystkie</button>
            <button class="cookie-reject" onclick="rejectAllCookies()">Odrzuć wszystkie</button>
            <button class="cookie-settings" onclick="showCookieSettings()">Ustawienia</button>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', bannerHTML);
}

// Sprawdzenie zgody cookies
function checkCookieConsent() {
    const consent = localStorage.getItem('cookieConsent');
    if (!consent) {
        showCookieBanner();
    } else {
        applyConsentSettings(JSON.parse(consent));
    }
}

// Pokaż baner
function showCookieBanner() {
    const banner = document.getElementById('cookieBanner');
    if (banner) {
        banner.style.display = 'block';
    }
}

// Akceptuj wszystkie cookies
function acceptAllCookies() {
    const consent = {
        analytics: true,
        marketing: true,
        functional: true
    };
    localStorage.setItem('cookieConsent', JSON.stringify(consent));
    applyConsentSettings(consent);
    hideCookieBanner();
}

// Odrzuć wszystkie cookies
function rejectAllCookies() {
    const consent = {
        analytics: false,
        marketing: false,
        functional: true
    };
    localStorage.setItem('cookieConsent', JSON.stringify(consent));
    applyConsentSettings(consent);
    hideCookieBanner();
}

// Zastosuj ustawienia zgody
function applyConsentSettings(consent) {
    // Upewnij się, że gtag jest dostępny
    if (typeof gtag !== 'undefined') {
        // Konfiguracja gtag z analytics_storage
        gtag('consent', 'update', {
            'analytics_storage': consent.analytics ? 'granted' : 'denied',
            'ad_storage': consent.marketing ? 'granted' : 'denied',
            'functionality_storage': 'granted'
        });
        
        // Ponowna konfiguracja gtag z nowymi ustawieniami
        gtag('config', 'G-7XMBQJMBVJ', {
            'anonymize_ip': !consent.analytics,
            'update': true
        });
    }
}

// Ukryj baner
function hideCookieBanner() {
    const banner = document.getElementById('cookieBanner');
    if (banner) {
        banner.style.display = 'none';
    }
}

// Ustawienia (można rozwinąć)
function showCookieSettings() {
    alert('Tutaj można dodać bardziej zaawansowane ustawienia cookies');
}

// Inicjalizacja systemu cookies
function initCookieSystem() {
    addCookieStyles();
    createCookieBanner();
    
    // Opóźnij sprawdzanie zgody, aby gtag.js się załadował
    setTimeout(checkCookieConsent, 100);
}

// Inicjalizacja przy ładowaniu strony
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCookieSystem);
} else {
    initCookieSystem();
}

// Eksportuj funkcje dla globalnego dostępu (jeśli potrzebne)
window.cookieFunctions = {
    acceptAllCookies,
    rejectAllCookies,
    showCookieSettings,
    checkCookieConsent,
    applyConsentSettings
};
