// Initialisation commune des présentations de projets
(function () {
    // Le bouton « Retour au portfolio » est inutile quand la page est ouverte dans la fenêtre d'aperçu du portfolio
    if (window.self !== window.top) {
        const back = document.querySelector('.back-link');
        if (back) back.remove();
    }

    Reveal.initialize({
        hash: true,
        slideNumber: 'c/t',
        transition: 'fade',
        width: 1280,
        height: 720,
        margin: 0.05,
        center: true
    });

    // Clic sur une capture : affichage en grand
    const zoom = document.createElement('div');
    zoom.className = 'zoom';
    zoom.innerHTML = '<img alt="">';
    document.body.appendChild(zoom);
    const big = zoom.querySelector('img');
    document.querySelectorAll('img.shot').forEach(img => img.addEventListener('click', () => {
        big.src = img.src;
        big.alt = img.alt;
        zoom.classList.add('open');
    }));
    zoom.addEventListener('click', () => zoom.classList.remove('open'));
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && zoom.classList.contains('open')) {
            e.stopPropagation();
            zoom.classList.remove('open');
        }
    }, true);
})();
