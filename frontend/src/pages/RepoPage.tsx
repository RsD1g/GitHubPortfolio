import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import RepoRow from '../components/RepoRow';
import { RepoDetails } from '../api';

const RepoPage: React.FC = () => {
  const { name } = useParams<{ name: string }>();
  const [repo, setRepo] = useState<any>(null);

  const { theme } = useTheme();

  useEffect(() => {
    const fetchRepo = async () => {
      const repoData = await (RepoDetails.get(repoName: name) as Promise<any>);
      setRepo(repoData);
    };

    fetchRepo();
  }, [name]);

  if (!repo) {
    return <div>Загрузка репозитория...</div>;
  }

  return (
    <div className="p-4 min-h-screen bg-card text-muted">
      <ThemeToggle />

      <div className="mt-4">
        <RepoRow repo={repo} />
      </div>
    </div>
  );
};

export default RepoPage;