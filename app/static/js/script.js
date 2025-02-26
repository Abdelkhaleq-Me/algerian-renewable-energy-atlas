 // Theme Switcher Logic (Vanilla JavaScript)
        const themeToggle = document.getElementById('theme-toggle');
        const themeIconLight = document.getElementById('theme-icon-light');
        const themeIconDark = document.getElementById('theme-icon-dark');
        const htmlElement = document.documentElement; // Get the root html element

        const currentTheme = localStorage.getItem('theme');
        if (currentTheme) {
            htmlElement.dataset.theme = currentTheme;
            if (currentTheme === 'dark') {
                themeIconDark.classList.remove('hidden');
                themeIconLight.classList.add('hidden');
            } else {
                themeIconLight.classList.remove('hidden');
                themeIconDark.classList.add('hidden');
            }
        } else {
            // Default to light theme if no theme is set in localStorage
            htmlElement.dataset.theme = 'light';
            themeIconLight.classList.remove('hidden');
            themeIconDark.classList.add('hidden');
        }


        themeToggle.addEventListener('click', () => {
            if (htmlElement.dataset.theme === 'light') {
                htmlElement.dataset.theme = 'dark';
                localStorage.setItem('theme', 'dark');
                themeIconDark.classList.remove('hidden');
                themeIconLight.classList.add('hidden');
            } else {
                htmlElement.dataset.theme = 'light';
                localStorage.setItem('theme', 'light');
                themeIconLight.classList.remove('hidden');
                themeIconDark.classList.add('hidden');
            }
        });

        // Language Switcher Dropdown Logic
        const langButton = document.getElementById('lang-button');
        const langDropdown = document.getElementById('lang-dropdown');

        langButton.addEventListener('click', () => {
            langDropdown.classList.toggle('hidden');
            langButton.setAttribute('aria-expanded', !langDropdown.classList.contains('hidden'));
        });

        // Close dropdown when clicking outside
        window.addEventListener('click', (event) => {
            if (!langButton.contains(event.target) && !langDropdown.contains(event.target) && !langDropdown.classList.contains('hidden')) {
                langDropdown.classList.add('hidden');
                langButton.setAttribute('aria-expanded', 'false');
            }
        });
