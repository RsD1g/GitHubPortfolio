import React from 'react';
import { Sun, Moon, Monitor } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const ThemeToggle: React.FC = () => {
  const { theme, toggleTheme } = useTheme();

  const iconMap: Record<ThemeContextType, React.ReactNode> = {
    light: <Sun />,
    dark: <Moon />,
    system: <Monitor />,
  };

  return (
    <div className="flex items-center space-x-2">
      <span className="text-lg font-medium">{theme.charAt(0).toUpperCase() + theme.slice(1)}</span>
      <button
        onClick={toggleTheme}
        aria-label={`Переключить тему на ${theme === 'light' ? 'тёмную' : theme === 'dark' ? 'светлую' : 'системную'}`}
        className="w-8 h-8 flex items-center justify-center rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        {iconMap[theme]}
      </button>
    </div>
  );
};

export default ThemeToggle;