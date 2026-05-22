document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.toast-close').forEach((button) => {
        button.addEventListener('click', () => {
            const toast = button.closest('.toast');
            if (!toast) {
                return;
            }
            const removeToast = () => {
                const stack = toast.closest('.flash-toast-stack');
                toast.remove();
                if (stack && !stack.querySelector('.toast')) {
                    stack.remove();
                }
            };
            toast.classList.add('toast--dismissing');
            toast.addEventListener('transitionend', removeToast, { once: true });
            window.setTimeout(removeToast, 300);
        });
    });

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
