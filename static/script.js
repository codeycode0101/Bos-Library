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

    document.querySelectorAll('.book-cover').forEach((image) => {
        image.addEventListener('error', () => {
            image.hidden = true;
            const fallback = image.nextElementSibling;
            if (fallback) fallback.hidden = false;
        }, { once: true });
    });

    const searchInput = document.getElementById('book-search');
    const bookGrid = document.getElementById('book-grid');
    const noResults = document.getElementById('no-results');
    const searchSuggestions = document.getElementById('book-search-suggestions');

    if (searchInput && bookGrid && noResults && searchSuggestions) {
        const bookCards = Array.from(bookGrid.querySelectorAll('.book-card'));
        let matches = [];
        let activeSuggestion = -1;

        const closeSuggestions = () => {
            searchSuggestions.hidden = true;
            searchSuggestions.replaceChildren();
            searchInput.setAttribute('aria-expanded', 'false');
            activeSuggestion = -1;
        };

        const chooseSuggestion = (card) => {
            searchInput.value = card.dataset.title;
            updateSearch();
            closeSuggestions();
        };

        const showSuggestions = () => {
            const query = searchInput.value.trim().toLowerCase();
            if (!query) {
                closeSuggestions();
                return;
            }

            const fragment = document.createDocumentFragment();
            matches.slice(0, 6).forEach((card, index) => {
                const item = document.createElement('li');
                item.setAttribute('role', 'option');
                item.id = `book-suggestion-${index}`;

                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'search-suggestion';
                button.innerHTML = `<span class="search-suggestion-title"></span><span class="search-suggestion-meta"></span>`;
                button.querySelector('.search-suggestion-title').textContent = card.dataset.title;
                button.querySelector('.search-suggestion-meta').textContent = `${card.dataset.author} · ${card.dataset.isbn}`;
                button.addEventListener('click', () => chooseSuggestion(card));
                item.append(button);
                fragment.append(item);
            });

            searchSuggestions.replaceChildren(fragment);
            searchSuggestions.hidden = matches.length === 0;
            searchInput.setAttribute('aria-expanded', String(matches.length > 0));
        };

        const updateSearch = () => {
            const query = searchInput.value.trim().toLowerCase();
            let visibleCount = 0;

            matches = bookCards.filter(card => {
                const text = card.dataset.search.toLowerCase();
                const match = query === '' || text.includes(query);
                card.style.display = match ? 'flex' : 'none';
                if (match) visibleCount += 1;
                return query !== '' && match;
            });

            noResults.hidden = visibleCount !== 0;
            showSuggestions();
        };

        searchInput.addEventListener('input', updateSearch);
        searchInput.addEventListener('keydown', (event) => {
            const buttons = Array.from(searchSuggestions.querySelectorAll('.search-suggestion'));
            if (!buttons.length) return;

            if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
                event.preventDefault();
                activeSuggestion = event.key === 'ArrowDown'
                    ? (activeSuggestion + 1) % buttons.length
                    : (activeSuggestion - 1 + buttons.length) % buttons.length;
                buttons.forEach((button, index) => button.classList.toggle('is-active', index === activeSuggestion));
                searchInput.setAttribute('aria-activedescendant', `book-suggestion-${activeSuggestion}`);
            } else if (event.key === 'Enter' && activeSuggestion >= 0) {
                event.preventDefault();
                chooseSuggestion(matches[activeSuggestion]);
            } else if (event.key === 'Escape') {
                closeSuggestions();
            }
        });
        searchInput.addEventListener('focus', showSuggestions);
        document.addEventListener('click', (event) => {
            if (!event.target.closest('.search-box')) closeSuggestions();
        });
        updateSearch();
    }

    const readJsonData = (id) => {
        const element = document.getElementById(id);
        if (!element) {
            return [];
        }

        try {
            return JSON.parse(element.textContent.trim() || '[]');
        } catch (error) {
            console.warn(`Could not parse ${id}`, error);
            return [];
        }
    };

    const borrowers = readJsonData('borrower-suggestions-data').map((borrower) => ({
        id: String(borrower.id),
        value: borrower.name,
        title: borrower.name,
        meta: borrower.role ? `ID ${borrower.id} - ${borrower.role}` : `ID ${borrower.id}`,
        search: borrower.search || `${borrower.id} ${borrower.name} ${borrower.role || ''}`,
    }));

    const books = readJsonData('book-suggestions-data').map((book) => ({
        id: book.isbn,
        value: book.title,
        title: book.title,
        meta: `${book.author} - ${book.isbn} - ${book.status}`,
        search: `${book.title} ${book.author} ${book.isbn} ${book.genre} ${book.status}`,
    }));

    const activeBorrows = readJsonData('active-borrow-suggestions-data');
    const activeBorrowRecords = activeBorrows.map((borrow) => {
        const borrowerName = `${borrow.first_name || ''} ${borrow.last_name || ''}`.trim();
        return {
            id: String(borrow.idBorrow),
            userId: String(borrow.idUser),
            copyId: String(borrow.book_copy_id || ''),
            value: borrow.Title || '',
            title: borrow.Title || 'Untitled',
            borrowerName,
            meta: `${borrowerName} - copy ${borrow.book_copy_id} - due ${borrow.due_date || 'unknown'}`,
            search: `${borrow.Title || ''} ${borrow.book_copy_ISBN || ''} ${borrow.book_copy_id || ''} ${borrowerName} ${borrow.idUser}`,
        };
    });

    const activeBorrowersById = new Map();
    activeBorrows.forEach((borrow) => {
        const userId = String(borrow.idUser);
        const borrowerName = `${borrow.first_name || ''} ${borrow.last_name || ''}`.trim();
        if (!activeBorrowersById.has(userId)) {
            activeBorrowersById.set(userId, {
                id: userId,
                value: borrowerName,
                title: borrowerName,
                meta: '1 active borrow',
                search: `${userId} ${borrowerName}`,
                count: 1,
            });
            return;
        }

        const borrower = activeBorrowersById.get(userId);
        borrower.count += 1;
        borrower.meta = `${borrower.count} active borrows`;
    });

    const smartSources = {
        borrowers,
        books,
        activeBorrowers: Array.from(activeBorrowersById.values()),
        activeBorrows: activeBorrowRecords,
    };

    const closeSmartSuggestions = (input, list) => {
        list.hidden = true;
        list.replaceChildren();
        input.setAttribute('aria-expanded', 'false');
        input.removeAttribute('aria-activedescendant');
    };

    const chooseSmartSuggestion = (input, list, item) => {
        input.value = item.value;

        const hiddenTargetId = input.dataset.hiddenTarget;
        if (hiddenTargetId) {
            const hiddenInput = document.getElementById(hiddenTargetId);
            if (hiddenInput) {
                hiddenInput.value = item.id || item.userId || '';
            }
        }

        if (input.id === 'return-title') {
            const copyInput = document.getElementById('copy-id');
            const returnerInput = document.getElementById('returner-name');
            const returnerIdInput = document.getElementById('returner-id');

            if (copyInput && item.copyId) {
                copyInput.value = item.copyId;
            }
            if (returnerInput && item.borrowerName) {
                returnerInput.value = item.borrowerName;
            }
            if (returnerIdInput && item.userId) {
                returnerIdInput.value = item.userId;
            }
        }

        if (input.id === 'returner-name') {
            const returnTitleInput = document.getElementById('return-title');
            const copyInput = document.getElementById('copy-id');

            if (returnTitleInput) {
                returnTitleInput.value = '';
            }
            if (copyInput) {
                copyInput.value = '';
            }

            window.setTimeout(() => returnTitleInput?.focus(), 0);
        }

        closeSmartSuggestions(input, list);
    };

    document.querySelectorAll('.smart-search-input').forEach((input) => {
        const listId = input.getAttribute('aria-controls');
        const list = listId ? document.getElementById(listId) : null;
        const source = smartSources[input.dataset.smartSource] || [];
        let matches = [];
        let activeIndex = -1;

        if (!list || !source.length) {
            return;
        }

        const updateMatches = () => {
            const query = input.value.trim().toLowerCase();
            const selectedReturnerId = document.getElementById('returner-id')?.value;
            const showAllOnFocus = input.dataset.showAllOnFocus === 'true';

            if (!query && !showAllOnFocus) {
                matches = [];
                return;
            }

            matches = source.filter((item) => {
                const itemText = (item.search || item.title || item.value || '').toLowerCase();
                const queryMatches = !query || itemText.includes(query);
                if (input.id !== 'return-title' || !selectedReturnerId) {
                    return queryMatches;
                }
                return queryMatches && item.userId === selectedReturnerId;
            }).slice(0, 6);
        };

        const renderSuggestions = () => {
            updateMatches();

            const fragment = document.createDocumentFragment();
            matches.forEach((item, index) => {
                const option = document.createElement('li');
                option.setAttribute('role', 'option');
                option.id = `${input.id}-suggestion-${index}`;

                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'search-suggestion';
                button.innerHTML = '<span class="search-suggestion-title"></span><span class="search-suggestion-meta"></span>';
                button.querySelector('.search-suggestion-title').textContent = item.title;
                button.querySelector('.search-suggestion-meta').textContent = item.meta;
                button.addEventListener('click', () => chooseSmartSuggestion(input, list, item));

                option.append(button);
                fragment.append(option);
            });

            list.replaceChildren(fragment);
            list.hidden = matches.length === 0;
            input.setAttribute('aria-expanded', String(matches.length > 0));
            activeIndex = -1;
        };

        input.addEventListener('input', () => {
            const hiddenTargetId = input.dataset.hiddenTarget;
            if (hiddenTargetId) {
                const hiddenInput = document.getElementById(hiddenTargetId);
                if (hiddenInput) {
                    hiddenInput.value = '';
                }
            }

            if (input.id === 'returner-name') {
                const returnTitleInput = document.getElementById('return-title');
                const copyInput = document.getElementById('copy-id');
                if (returnTitleInput) {
                    returnTitleInput.value = '';
                }
                if (copyInput) {
                    copyInput.value = '';
                }
            }

            if (input.id === 'return-title') {
                const copyInput = document.getElementById('copy-id');
                if (copyInput) {
                    copyInput.value = '';
                }
            }

            renderSuggestions();
        });

        input.addEventListener('focus', renderSuggestions);
        input.addEventListener('keydown', (event) => {
            const buttons = Array.from(list.querySelectorAll('.search-suggestion'));
            if (!buttons.length) {
                return;
            }

            if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
                event.preventDefault();
                activeIndex = event.key === 'ArrowDown'
                    ? (activeIndex + 1) % buttons.length
                    : (activeIndex - 1 + buttons.length) % buttons.length;
                buttons.forEach((button, index) => button.classList.toggle('is-active', index === activeIndex));
                input.setAttribute('aria-activedescendant', `${input.id}-suggestion-${activeIndex}`);
            } else if (event.key === 'Enter' && activeIndex >= 0) {
                event.preventDefault();
                chooseSmartSuggestion(input, list, matches[activeIndex]);
            } else if (event.key === 'Escape') {
                closeSmartSuggestions(input, list);
            }
        });

        document.addEventListener('click', (event) => {
            if (!event.target.closest(`#${input.id}, #${list.id}`)) {
                closeSmartSuggestions(input, list);
            }
        });
    });

    document.querySelectorAll('.availability-fill').forEach((fill) => {
        const width = fill.dataset.width;
        if (width) {
            fill.style.width = `${width}%`;
        }
    });

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
