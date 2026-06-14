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
            toast.addEventListener('animationend', removeToast, { once: true });
            window.setTimeout(removeToast, 300);
        });
    });

    const searchInput = document.getElementById('book-search');
    const bookGrid = document.getElementById('book-grid');
    const noResults = document.getElementById('no-results');

    if (searchInput && bookGrid) {
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
    }

    const dashboardTabs = document.querySelectorAll('.dashboard-tab');
    const dashboardSections = document.querySelectorAll('.dashboard-section');

    if (dashboardTabs.length && dashboardSections.length) {
        dashboardTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const target = tab.dataset.target;
                if (!target) return;

                dashboardTabs.forEach(button => button.classList.remove('active'));
                dashboardSections.forEach(section => section.classList.remove('active'));

                tab.classList.add('active');
                const selectedSection = document.getElementById(target);
                if (selectedSection) {
                    selectedSection.classList.add('active');
                }
            });
        });

        const initialTab = document.querySelector('.dashboard-tab.active') || dashboardTabs[0];
        if (initialTab) {
            initialTab.click();
        }
    }
    // Active borrows table row selection highlighting when clicked, and deselect when clicking outside the table
    const activeBorrowTable = document.querySelector('#active-borrows-panel table.data-table');
    let selectedRow = null;

    if (activeBorrowTable) {
        const rows = Array.from(activeBorrowTable.querySelectorAll('.selectable-row'));

        rows.forEach(row => {
            row.addEventListener('click', (event) => {
                event.stopPropagation();
                const isSelected = row.classList.contains('selected');

                rows.forEach(r => r.classList.remove('selected'));
                if (!isSelected) {
                    row.classList.add('selected');
                    selectedRow = row;
                } else {
                    selectedRow = null;
                }
            });
        });

        document.addEventListener('click', (event) => {
            if (!activeBorrowTable.contains(event.target) && selectedRow) {
                selectedRow.classList.remove('selected');
                selectedRow = null;
            }
        });
    }

//     const headerPhrases = [
//         'Simple library management for students, readers, and staff',
//         'Designed for students, readers, and library staff',
//         'Easy borrowing, returning, and loan tracking'
//     ];
//     const typingElement = document.querySelector('.typing-text');
//     if (typingElement) {
//         let phraseIndex = 0;
//         let charIndex = 0;
//         let deleting = false;
//         const typeSpeed = 90;
//         const deleteSpeed = 50;
//         const pauseAfterTyping = 1800;

//         const updateText = () => {
//             const currentPhrase = headerPhrases[phraseIndex];

//             if (!deleting) {
//                 typingElement.textContent = currentPhrase.slice(0, charIndex + 1);
//                 charIndex += 1;

//                 if (charIndex === currentPhrase.length) {
//                     deleting = true;
//                     window.setTimeout(updateText, pauseAfterTyping);
//                     return;
//                 }
//             } else {
//                 typingElement.textContent = currentPhrase.slice(0, charIndex - 1);
//                 charIndex -= 1;

//                 if (charIndex === 0) {
//                     deleting = false;
//                     phraseIndex = (phraseIndex + 1) % headerPhrases.length;
//                     window.setTimeout(updateText, 500);
//                     return;
//                 }
//             }

//             window.setTimeout(updateText, deleting ? deleteSpeed : typeSpeed);
//         };

//         updateText();
//     }
});
