import React from 'react';
import { LineChart } from 'recharts';
import { useTheme } from '../context/ThemeContext';

interface DataPoint {
  date: string;
  value: number;
}

const getRandomData = (size: number): DataPoint[] => {
  const dates = Array.from({ length: size }, (_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - (size - i));
    return {
      date: d.toISOString().split('T')[0],
      value: Math.round(Math.random() * 1000) / 100,
    };
  });

  return dates;
};

const StarsChart: React.FC = () => {
  const { theme } = useTheme();
  const data = getRandomData(10); // Will show placeholder points until real data comes

  return (
    <div className="mb-6">
      <h3 className="text-lg font-semibold text-primary mb-2">История звёзд по дням</h3>
      <div className="text-center text-gray-500 italic">
        История появится после нескольких ежедневных синхронизаций
      </div>
      {data.length > 0 && (
        <LineChart
          width={300}
          height={150}
          data={data}
          margin={{ top: 20, right: 32, left: 32, bottom: 5 }}
          className="w-full"
          resultToColor={(value) => value > 500 ? 'rgb(var(--accent))' : 'rgb(var(--border))'}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#111827" />
          <XAxis stroke="#111827" />
          <YAxis stroke="#111827" />
          <Line type="cubic" strokeWidth={2} dataKey="value" fill={(value) => value > 500 ? 'rgb(var(--accent))' : 'rgb(var(--border))'} />
        </LineChart>
      )}
    </div>
  );
};

export default StarsChart;