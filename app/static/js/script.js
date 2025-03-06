// Theme Switcher
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const lightIcon = document.getElementById('theme-icon-light');
    const darkIcon = document.getElementById('theme-icon-dark');

    // Check for saved theme preference or use system preference
    const savedTheme = localStorage.getItem('theme');
    const systemDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && systemDarkMode)) {
        document.documentElement.setAttribute('data-theme', 'dark');
        lightIcon.classList.remove('hidden');
        darkIcon.classList.add('hidden');
    }

    // Theme toggle click handler
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        if (newTheme === 'dark') {
            lightIcon.classList.remove('hidden');
            darkIcon.classList.add('hidden');
        } else {
            lightIcon.classList.add('hidden');
            darkIcon.classList.remove('hidden');
        }
    });

    // Language Dropdown
    const langButton = document.getElementById('lang-button');
    const langDropdown = document.getElementById('lang-dropdown');

    langButton.addEventListener('click', () => {
        const isExpanded = langButton.getAttribute('aria-expanded') === 'true';
        langButton.setAttribute('aria-expanded', !isExpanded);
        langDropdown.classList.toggle('hidden');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (event) => {
        if (!langButton.contains(event.target) && !langDropdown.contains(event.target)) {
            langButton.setAttribute('aria-expanded', 'false');
            langDropdown.classList.add('hidden');
        }
    });

    // Mobile Navigation
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileNav = document.querySelector('.main-nav ul');

    if (mobileMenuButton && mobileNav) {
        mobileMenuButton.addEventListener('click', () => {
            mobileNav.classList.toggle('hidden');
            mobileNav.classList.toggle('mobile-nav-open');
        });
    }
});

// Handle RTL for Arabic language
document.documentElement.dir = document.documentElement.lang === 'ar' ? 'rtl' : 'ltr';
