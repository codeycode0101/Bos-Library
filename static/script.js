document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('book-search');
    const bookGrid = document.getElementById('book-grid');
    const noResults = document.getElementById('no-results');

    if (!searchInput || !bookGrid) {
        return;
    }

    const bookCards = Array.from(bookGrid.querySelectorAll('.book-card'));

    const updateSearch = () => {
        const query = searchInput.value.trim().toLowerCase();
        let visibleCount = 0;

        bookCards.forEach(card => {
            const text = card.dataset.search.toLowerCase();
            const match = query === '' || text.includes(query);
            card.style.display = match ? 'flex' : 'none';
            if (match) visibleCount += 1;
        });

        noResults.hidden = visibleCount !== 0;
    };

    searchInput.addEventListener('input', updateSearch);
    updateSearch();
});
