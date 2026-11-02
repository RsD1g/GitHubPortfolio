import React, { useEffect, useState } from 'react';
import { ThemeProvider } from './ThemeContext';
import ReposList from './ReposList';
import Loading from './Loading';
import { useTheme } from './ThemeContext';

interface Repo {
  name: string;
  description: string;
  language: string | null;
  stars: number;
  forks: number;
  topics: string[];
}

const App: React.FC = () => {
  const { theme, toggleTheme } = useTheme();
  const [repos, setRepos] = React.useState<Repo[]>([]);
  const [loading, setLoading] = React.useState(true);

  // Simulate data fetching
  useEffect(() => {
    const mockRepos: Repo[] = [
      { name: "repo1", description: "First repository", language: "JavaScript", stars: 42, forks: 15, topics: ["web", "js"] },
      { name: "repo2", description: "Second repository", language: "Python", stars: 15, forks: 5, topics: ["ml"] },
      { name: "repo3", description: "Third repository", language: "Go", stars: 8, forks: 0, topics: [] },
    ];

    const timer = setTimeout(() => {
      setRepos(mockRepos);
      setLoading(false);
    }, 1500);

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return <Loading />;
  }

  return (
    <div className={`container mx-auto ${theme === 'dark' ? 'dark' : ''} p-4 min-h-screen`}>
      <header className="flex justify-between items-center p-4 bg-card">
        <h1 className="text-3xl font-fraunces">Мои репозитории</h1>
        <button
          onClick={() => toggleTheme()}
          className="bg-mute text-fg px-4 py-2 rounded focus:outline-none"
        >
          {theme === 'system' ? 'Системная' : theme}
        </button>
      </header>

      <main className="my-8">
        <ReposList repos={repos} />
      </main>
    </div>
  );
};

export default App;