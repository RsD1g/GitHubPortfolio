import React from 'react';
import { useTheme } from './ThemeContext';

interface Repo {
  name: string;
  description: string;
  language: string | null;
  stars: number;
  forks: number;
  topics: string[];
}

const RepoItem: React.FC<{ repo: Repo }> = ({ repo }) => {
  return (
    <div
      key={repo.name}
      className="flex flex-col md:flex-row border-b border-muted py-2"
    >
      <div className="flex-1">
        <h3 className="font-fraunces text-xl">{repo.name}</h3>
        <p className="text-muted text-sm">{repo.description}</p>
        {repo.language && (
          <span className="inline-flex items-center rounded-full bg-muted px-2 py-1 text-xs text-fg">
            {repo.language}
          </span>
        )}
        <ul className="flex flex-wrap mt-2 space-x-1 text-xs">
          {repo.topics.map((topic) => (
            <li key={topic} className="inline-flex items-center rounded-full bg-muted px-2 py-0.5 text-xs">
              #{topic}
            </li>
          ))}
        </ul>
      </div>
      <div className="flex-1 text-end space-y-2">
        <span className="text-fg">{repo.stars}</span>
        <span className="text-muted">★</span>
        <span className="text-muted">{repo.forks}</span>
        <span className="text-muted">🗂️</span>
      </div>
    </div>
  );
};

const ReposList: React.FC<{ repos: any[] }> = ({ repos }) => {
  return (
    <section className="space-y-4">
      {repos.length === 0 ? (
        <p className="text-muted">Нет репозиториев для отображения.</p>
      ) : (
        repos.map((repo) => (
          <RepoItem key={repo.name} repo={repo} />
        ))
      )}
    </section>
  );
};

export default ReposList;