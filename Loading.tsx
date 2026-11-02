import React from 'react';

export default function Loading(): JSX.Element {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <p className="text-2xl text-muted">Загрузка данных...</p>
    </div>
  );
}