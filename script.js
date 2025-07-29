// DOM Elements
const searchInput = document.getElementById('searchInput');
const commandItems = document.querySelectorAll('.command-item');
const commandCategories = document.querySelectorAll('.command-category');

// Search functionality
function filterCommands() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    
    commandCategories.forEach(category => {
        let hasVisibleCommands = false;
        const commands = category.querySelectorAll('.command-item');
        
        commands.forEach(command => {
            const searchData = command.getAttribute('data-search').toLowerCase();
            const commandText = command.querySelector('.command').textContent.toLowerCase();
            const descriptionText = command.querySelector('.command-description').textContent.toLowerCase();
            
            const isMatch = searchData.includes(searchTerm) || 
                           commandText.includes(searchTerm) || 
                           descriptionText.includes(searchTerm);
            
            if (isMatch || searchTerm === '') {
                command.classList.remove('hidden');
                hasVisibleCommands = true;
            } else {
                command.classList.add('hidden');
            }
        });
        
        // Hide category if no visible commands
        if (hasVisibleCommands) {
            category.classList.remove('empty');
        } else {
            category.classList.add('empty');
        }
    });
    
    // Show "no results" message if needed
    const visibleCommands = document.querySelectorAll('.command-item:not(.hidden)');
    handleNoResults(visibleCommands.length === 0 && searchTerm !== '');
}

// Handle no search results
function handleNoResults(show) {
    let noResultsMessage = document.getElementById('noResultsMessage');
    
    if (show && !noResultsMessage) {
        noResultsMessage = document.createElement('div');
        noResultsMessage.id = 'noResultsMessage';
        noResultsMessage.className = 'no-results';
        noResultsMessage.innerHTML = `
            <div style="text-align: center; padding: 3rem; color: var(--text-muted);">
                <i class="fas fa-search" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                <h3 style="margin-bottom: 0.5rem;">No commands found</h3>
                <p>Try searching with different keywords or check your spelling.</p>
            </div>
        `;
        document.querySelector('.commands-grid').appendChild(noResultsMessage);
    } else if (!show && noResultsMessage) {
        noResultsMessage.remove();
    }
}

// Copy to clipboard functionality
function copyToClipboard(text) {
    // Try using the modern Clipboard API first
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            showCopyFeedback(event.target);
        }).catch(() => {
            // Fallback to older method
            fallbackCopyToClipboard(text);
        });
    } else {
        // Fallback for older browsers
        fallbackCopyToClipboard(text);
    }
}

// Fallback copy method for older browsers
function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showCopyFeedback(event.target);
    } catch (err) {
        console.error('Failed to copy text: ', err);
        showCopyError(event.target);
    }
    
    document.body.removeChild(textArea);
}

// Show copy success feedback
function showCopyFeedback(button) {
    const originalIcon = button.innerHTML;
    const originalTitle = button.title;
    
    button.innerHTML = '<i class="fas fa-check"></i>';
    button.title = 'Copied!';
    button.classList.add('copied');
    
    setTimeout(() => {
        button.innerHTML = originalIcon;
        button.title = originalTitle || 'Copy to clipboard';
        button.classList.remove('copied');
    }, 1500);
}

// Show copy error feedback
function showCopyError(button) {
    const originalIcon = button.innerHTML;
    const originalTitle = button.title;
    
    button.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
    button.title = 'Copy failed';
    button.style.backgroundColor = 'var(--danger-color)';
    
    setTimeout(() => {
        button.innerHTML = originalIcon;
        button.title = originalTitle || 'Copy to clipboard';
        button.style.backgroundColor = '';
    }, 2000);
}

// Keyboard shortcuts
function handleKeyboardShortcuts(e) {
    // Focus search on Ctrl/Cmd + K
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        searchInput.focus();
        searchInput.select();
    }
    
    // Clear search on Escape
    if (e.key === 'Escape' && document.activeElement === searchInput) {
        searchInput.value = '';
        filterCommands();
        searchInput.blur();
    }
}

// Debounced search to improve performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Analytics for popular commands (optional)
function trackCommandCopy(command) {
    // You can implement analytics tracking here
    console.log(`Command copied: ${command}`);
}

// Initialize tooltips for copy buttons
function initializeTooltips() {
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        if (!button.title) {
            button.title = 'Copy to clipboard';
        }
    });
}

// Smooth scroll to category
function scrollToCategory(categoryId) {
    const category = document.querySelector(`[data-category="${categoryId}"]`);
    if (category) {
        category.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Add search result highlighting
function highlightSearchTerm(text, searchTerm) {
    if (!searchTerm) return text;
    
    const regex = new RegExp(`(${searchTerm})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

// Enhanced search with highlighting
function filterCommandsWithHighlight() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    
    commandCategories.forEach(category => {
        let hasVisibleCommands = false;
        const commands = category.querySelectorAll('.command-item');
        
        commands.forEach(command => {
            const searchData = command.getAttribute('data-search').toLowerCase();
            const commandText = command.querySelector('.command').textContent.toLowerCase();
            const descriptionText = command.querySelector('.command-description').textContent.toLowerCase();
            
            const isMatch = searchData.includes(searchTerm) || 
                           commandText.includes(searchTerm) || 
                           descriptionText.includes(searchTerm);
            
            if (isMatch || searchTerm === '') {
                command.classList.remove('hidden');
                hasVisibleCommands = true;
                
                // Add highlighting (optional enhancement)
                if (searchTerm) {
                    const description = command.querySelector('.command-description');
                    const originalText = description.getAttribute('data-original-text') || description.textContent;
                    if (!description.getAttribute('data-original-text')) {
                        description.setAttribute('data-original-text', originalText);
                    }
                    description.innerHTML = highlightSearchTerm(originalText, searchTerm);
                } else {
                    // Remove highlighting
                    const description = command.querySelector('.command-description');
                    const originalText = description.getAttribute('data-original-text');
                    if (originalText) {
                        description.textContent = originalText;
                    }
                }
            } else {
                command.classList.add('hidden');
            }
        });
        
        // Hide category if no visible commands
        if (hasVisibleCommands) {
            category.classList.remove('empty');
        } else {
            category.classList.add('empty');
        }
    });
    
    // Show "no results" message if needed
    const visibleCommands = document.querySelectorAll('.command-item:not(.hidden)');
    handleNoResults(visibleCommands.length === 0 && searchTerm !== '');
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize tooltips
    initializeTooltips();
    
    // Search functionality with debouncing
    const debouncedFilter = debounce(filterCommandsWithHighlight, 300);
    searchInput.addEventListener('input', debouncedFilter);
    
    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);
    
    // Copy button functionality
    document.addEventListener('click', (e) => {
        if (e.target.closest('.copy-btn')) {
            const button = e.target.closest('.copy-btn');
            const commandText = button.previousElementSibling.textContent;
            copyToClipboard(commandText);
            trackCommandCopy(commandText);
        }
    });
    
    // Add search placeholder animation
    let placeholderIndex = 0;
    const placeholders = [
        'Search commands...',
        'Try "branch", "commit", "push"...',
        'Find Git commands quickly...',
        'Type to filter commands...'
    ];
    
    setInterval(() => {
        if (document.activeElement !== searchInput) {
            searchInput.placeholder = placeholders[placeholderIndex];
            placeholderIndex = (placeholderIndex + 1) % placeholders.length;
        }
    }, 3000);
    
    // Add focus ring for better accessibility
    searchInput.addEventListener('focus', () => {
        searchInput.parentElement.classList.add('focused');
    });
    
    searchInput.addEventListener('blur', () => {
        searchInput.parentElement.classList.remove('focused');
    });
});

// Export functions for potential use in other scripts
window.GitCommandsApp = {
    copyToClipboard,
    scrollToCategory,
    filterCommands: filterCommandsWithHighlight
};