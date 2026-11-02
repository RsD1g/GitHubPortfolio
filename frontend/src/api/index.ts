import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const repos = async (params: any) => {
  const response = await api.get('/repos', { params });
  return response.data;
};

export const overview = async () => {
  const response = await api.get('/stats/overview');
  return response.data;
};

export const repo = async (name: string) => {
  const response = await api.get(`/repos/${name}`);
  return response.data;
};

export const repoHistory = async (name: string) => {
  const response = await api.get(`/repos/${name}/history`);
  return response.data;
};