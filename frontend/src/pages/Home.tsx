import React, { useEffect, useState } from 'react';
import { useTheme } from '../context/ThemeContext';
import ThemeToggle from '../components/ThemeToggle';
import LanguageChart from '../components/LanguageChart';
import StarsChart from '../components/StarsChart';
import RepoRow from '../components/RepoRow';
import { Repositories } from '../api';

const Home: React.FC = () => {
  const { theme } = useTheme();
  const [repos, setRepos] = useState<Array<any>>([]);
  const [languages, setLanguages] = useState<Array<any>>([]);

  const fetchData = async () => {
    const [reposData, languagesData] = await Promise.all([
      (Repositories.repos() as Promise<any>).then(res => res),
      (Repositories.overview() as Promise<any>).then(res => res)
    ]);

    setRepos(reposData);
    setLanguages(languagesData.languages);
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="min-h-screen p-4 bg-card text-muted">
      <ThemeToggle />

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        <div className="col-span-3">
          <div className="text-center pt-6">
            <h2 className="text-2xl font-bold mb-2 text-primary">Домой</h2>
            <p className="text-lg text-muted">{repos.length} репозиториев • {languages.reduce((sum, lang) => sum + lang.count, 0)} звёзд • {repos.reduce((sum, repo) => sum + repo.forks, 0)} форков</p>
          </div>

          <div className="mt-8">
            <LanguageChart languages={languages} />
          </div>
        </div>

        <div className="col-span-1">
          <div className="mt-6">
            <StarsChart />
          </div>
        </div>
      </div>

      <div className="mt-8">
        <h3 className="text-xl font-bold text-primary">Список репозиториев</h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 gap-2">
          {repos.map(repo => (
            <RepoRow key={repo.id} repo={repo} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;