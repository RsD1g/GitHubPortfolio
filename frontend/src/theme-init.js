// src/theme-init.js
(function () {
  const storedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

  // Determine initial theme
  let themeClass = 'light';
  if (storedTheme === 'dark' || (storedTheme === null && prefersDark)) {
    themeClass = 'dark';
  } else if (storedTheme === 'light') {
    themeClass = 'light';
  }

  // Apply theme class to html element
  document.documentElement.classList.add(themeClass);

  // Update color scheme style
  const colorScheme = document.createElement('style');
  colorScheme.textContent = `
    html {
      color-scheme: ${themeClass === 'dark' ? 'dark' : 'light'};
    }
    body {
      background-color: ${themeClass === 'dark' ? 'rgb(var(--bg))' : 'rgb(var(--bg))'};
      color: ${themeClass === 'dark' ? 'rgb(var(--fg))' : 'rgb(var(--fg))'};
    }
  `;
  document.head.appendChild(colorScheme);

  // Function to toggle theme
  const toggleTheme = () => {
    const isDark = document.documentElement.classList.contains('dark');
    const newTheme = isDark ? 'light' : 'dark';

    // Remove current class and add new one
    document.documentElement.classList.remove('dark', 'light');
    document.documentElement.classList.add(newTheme);

    // Save to localStorage
    localStorage.setItem('theme', newTheme);
  };

  // Initialize ThemeToggle component
  const initThemeToggle = () => {
    const themeToggle = document.createElement('button');
    themeToggle.type = 'button';
    themeToggle.className = 'theme-toggle';
    themeToggle.setAttribute('aria-label', 'Текущая тема: светлая');

    const updateLabel = () => {
      const isDark = document.documentElement.classList.contains('dark');
      themeToggle.textContent = isDark ? 'тёмная' : 'светлая';
      themeToggle.setAttribute('aria-label', `Текущая тема: ${isDark ? 'тёмная' : 'светлая'}`);
      const nextTheme = isDark ? 'светлая' : 'тёмная';
      themeToggle.setAttribute('aria-pressed', isDark);
    };

    themeToggle.addEventListener('click', () => {
      toggleTheme();
      updateLabel();
    });

    document.getElementById('root').appendChild(themeToggle);
    updateLabel();
  };

  // Execute theme init
  initThemeToggle();
})();