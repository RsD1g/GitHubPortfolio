import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import Home from './pages/Home';
import RepoPage from './pages/RepoPage';

const App: React.FC = () => {
  return (
    <ThemeProvider>
      <div className="p-4 min-h-screen bg-card text-muted">
        <header className="mb-4">
          <h1 className="text-3xl font-bold text-primary text-left">Портфолио разработчика</h1>
          <p className="text-sm text-muted">Итоги: количество репозиториев, звёзд, форков</p>
          <Link to="/" className="absolute top-0 right-0 mt-2 mr-2">
            <button className="btn">
              Перейти к содержимому
            </button>
          </Link>
        </header>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
          <Route path="/" element={<Home />} />
          <Route path="/projects/:name" element={<RepoPage />} />
        </div>
      </div>
    </ThemeProvider>
  );
};

export default App;