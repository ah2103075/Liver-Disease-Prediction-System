// Theme Toggle Functionality
class ThemeManager {
    constructor() {
        this.THEME_KEY = 'app-theme';
        this.DARK_THEME = 'dark-theme';
        this.LIGHT_THEME = 'light-theme';
        this.init();
    }

    init() {
        // Check for saved theme preference
        const savedTheme = localStorage.getItem(this.THEME_KEY);
        
        if (savedTheme) {
            this.setTheme(savedTheme);
        } else {
            // Check system preference
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            this.setTheme(prefersDark ? this.DARK_THEME : this.LIGHT_THEME);
        }
        
        this.setupToggleButton();
    }

    setTheme(theme) {
        if (theme === this.DARK_THEME) {
            document.body.classList.add(this.DARK_THEME);
            localStorage.setItem(this.THEME_KEY, this.DARK_THEME);
        } else {
            document.body.classList.remove(this.DARK_THEME);
            localStorage.setItem(this.THEME_KEY, this.LIGHT_THEME);
        }
        this.updateToggleButton();
    }

    toggleTheme() {
        const isDarkTheme = document.body.classList.contains(this.DARK_THEME);
        this.setTheme(isDarkTheme ? this.LIGHT_THEME : this.DARK_THEME);
    }

    setupToggleButton() {
        const toggleBtn = document.getElementById('themeToggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggleTheme());
        }
    }

    updateToggleButton() {
        const toggleBtn = document.getElementById('themeToggle');
        if (toggleBtn) {
            const isDark = document.body.classList.contains(this.DARK_THEME);
            toggleBtn.textContent = isDark ? '☀️' : '🌙';
        }
    }

    getCurrentTheme() {
        return document.body.classList.contains(this.DARK_THEME) ? this.DARK_THEME : this.LIGHT_THEME;
    }
}

// Initialize theme manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
});
