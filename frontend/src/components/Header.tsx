import React from 'react';
import { useTheme } from '../context/ThemeContext';

const Header: React.FC = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="mb-4">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-primary">
          Портфолио разработчика
        </h1>
        <div className="space-x-4">
          <button
            onClick={toggleTheme}
            className="flex items-center space-x-2"
            aria-label={`Текущая тема: ${theme === 'light' ? 'светлая' : theme === 'dark' ? 'тёмная' : 'системная'}`}
          >
            {theme === 'light' && <span className="text-lg">Светлая</span>}
            {theme === 'dark' && <span className="text-lg">Тёмная</span>}
            {theme === 'system' && <span className="text-lg">Системная</span>}
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;