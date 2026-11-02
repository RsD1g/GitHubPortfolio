import React from 'react';
import { Link } from 'react-router-dom';

interface Repo {
  id: number;
  name: string;
  description: string | null;
  language: string | null;
  topics: string[];
  stars: number;
  forks: number;
  pushed_at: string;
}

const RepoRow: React.FC<{ repo: Repo }> = ({ repo }) => {
  const topicTags = repo.topics.map(topic => (
    <span key={topic} className="inline-block bg-blue-50 text-blue-700 text-xs font-medium mr-1 mb-1 rounded-full py-1 px-2">
      {topic}
    </span>
  ));

  return (
    <Link to={`/projects/${repo.name}`} className="block clickable hover:opacity-90">
      <div className="flex flex-col md:flex-row items-center gap-2 pb-2 border-b border-muted/30">
        <div className="md:flex-1">
          <h3 className="text-xl font-bold text-primary">{repo.name}</h3>
          {repo.description ? <p className="text-sm text-muted">{repo.description}</p> : null}
          {repo.language ? (
            <span className="mt-1 bg-gray-200 text-gray-800 text-xs rounded-full px-2 py-1">
              {repo.language}
            </span>
          ) : null
          </div>
          <div className="flex items-center">
            <span className="text-amber-500 mr-2">#{' '.join(repo.topics)}</span>
            <span className="text-gray-600 ml-2">
              <svg width="16" height="16" viewBox="0 0 24 24" className="inline-block">
                <path fill="currentColor" d="M12 0C6.48 0 2 6.48 2 12c0 5.52 4.48 10 10 10s10-4.48 10-10S17.52 2 12 2zm1 15H9v2h4v6h2v-6h4v2H11v2H9v-2H7v-4h5v2z"/>
              </svg>
              {repo.stars}
            </span>
            <span className="ml-2">
              <svg width="16" height="16" viewBox="0 0 24 24" className="inline-block">
                <path fill="currentColor" d="M12 2C7.59 2 4 5.59 4 12s3.59 10 8 10 10-3.59 10-10S16.41 2 12 2zM12 17C13.7 17 16 14.4 16 12s-3.7 5-8 5-8-5-8 5-3.7-10 0-8-5 5-3.7 10 0 8 3.7 5 8 5zM12 6H8C5.46 6 4.44 6.61 4 7.42S4.44 8.4 4 8.75c0 .29.2.54.5.54h3v1H16c.21.24
                .46.54 1 .54h8c.29 0 .52-.25 1-.54l1-1V6H12v2z"/>
              </svg>
              {repo.forks}
            </span>
            <span className="ml-2 text-sm text-muted">
              {new Date(repo.pushed_at).toLocaleDateString('ru-RU')}
            </span>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default RepoRow;