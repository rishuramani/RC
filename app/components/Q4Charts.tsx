'use client';

import { useState, useRef, useEffect, useCallback } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  type ChartData,
  type ChartOptions,
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

// Brand colors
const rcGreen = '#0A4E44';
const sage = '#8FB3A9';
const sageLight = '#B8D4CB';
const darkBlue = '#1a365d';
const gridColor = '#E2E8F0';

const quarterLabels = [
  'Q1 21','Q2 21','Q3 21','Q4 21',
  'Q1 22','Q2 22','Q3 22','Q4 22',
  'Q1 23','Q2 23','Q3 23','Q4 23',
  'Q1 24','Q2 24','Q3 24','Q4 24',
  'Q1 25','Q2 25','Q3 25','Q4 25',
];

/* ─── Filter Buttons ─── */
function FilterBar({
  options,
  active,
  onChange,
}: {
  options: { label: string; value: string }[];
  active: string;
  onChange: (v: string) => void;
}) {
  return (
    <div className="chart-filters">
      {options.map((o) => (
        <button
          key={o.value}
          className={`filter-btn${active === o.value ? ' active' : ''}`}
          onClick={() => onChange(o.value)}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}

/* ─── 1. Rent & Occupancy ─── */
export function RentOccupancyChart() {
  const [filter, setFilter] = useState('all');
  const chartRef = useRef<ChartJS<'bar'>>(null);

  const updateVisibility = useCallback((f: string) => {
    const chart = chartRef.current;
    if (!chart) return;
    chart.data.datasets.forEach((ds, i) => {
      ds.hidden = f === 'all' ? false : (f === 'rent' ? i !== 0 : i !== 1);
    });
    chart.update();
  }, []);

  useEffect(() => { updateVisibility(filter); }, [filter, updateVisibility]);

  const data: ChartData<'bar'> = {
    labels: quarterLabels,
    datasets: [
      {
        label: 'Average Rent ($)',
        type: 'bar' as const,
        data: [1050,1080,1120,1160,1200,1240,1280,1310,1320,1310,1300,1290,1285,1280,1275,1277,1265,1268,1273,1258],
        backgroundColor: rcGreen,
        borderRadius: 4,
        yAxisID: 'y',
      },
      {
        label: 'Occupancy (%)',
        type: 'line' as const,
        data: [90.5,91.0,91.2,91.5,91.2,90.8,90.2,89.5,89.0,88.5,88.2,88.0,87.8,88.0,88.2,88.4,89.0,89.5,90.1,90.4],
        borderColor: sage,
        backgroundColor: sage,
        tension: 0.3,
        pointRadius: 3,
        pointBackgroundColor: sage,
        yAxisID: 'y1',
      },
    ],
  };

  const options: ChartOptions<'bar'> = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    plugins: {
      legend: { position: 'top', labels: { usePointStyle: true, padding: 20 } },
    },
    scales: {
      x: { grid: { display: false } },
      y: {
        type: 'linear',
        position: 'left',
        title: { display: true, text: 'Rent ($)' },
        min: 0,
        max: 1400,
        grid: { color: gridColor },
      },
      y1: {
        type: 'linear',
        position: 'right',
        title: { display: true, text: 'Occupancy (%)' },
        min: 86,
        max: 92,
        grid: { display: false },
      },
    },
  };

  return (
    <div className="chart-container">
      <h4>Houston Rent & Occupancy Trends (2021-2025)</h4>
      <FilterBar
        options={[
          { label: 'All Data', value: 'all' },
          { label: 'Rent Only', value: 'rent' },
          { label: 'Occupancy Only', value: 'occupancy' },
        ]}
        active={filter}
        onChange={setFilter}
      />
      <div className="chart-wrapper">
        <Bar ref={chartRef} data={data} options={options} />
      </div>
      <p className="chart-source">Source: Colliers, MRI Apartment Data</p>
    </div>
  );
}

/* ─── 2. Class Performance ─── */
export function ClassPerformanceChart() {
  const [filter, setFilter] = useState('all');
  const chartRef = useRef<ChartJS<'bar'>>(null);

  const updateVisibility = useCallback((f: string) => {
    const chart = chartRef.current;
    if (!chart) return;
    chart.data.datasets.forEach((ds, i) => {
      ds.hidden = f === 'all' ? false : (f === 'occupancy' ? i !== 0 : i !== 1);
    });
    chart.update();
  }, []);

  useEffect(() => { updateVisibility(filter); }, [filter, updateVisibility]);

  const data: ChartData<'bar'> = {
    labels: ['Class A', 'Class B', 'Class C', 'Class D'],
    datasets: [
      {
        label: 'Occupancy (%)',
        data: [86.1, 92.1, 92.5, 89.8],
        backgroundColor: rcGreen,
        borderRadius: 4,
        yAxisID: 'y',
      },
      {
        label: 'Monthly Rent ($)',
        data: [1704, 1249, 982, 784],
        backgroundColor: sage,
        borderRadius: 4,
        yAxisID: 'y1',
      },
    ],
  };

  const options: ChartOptions<'bar'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top', labels: { usePointStyle: true, padding: 20 } },
    },
    scales: {
      x: { grid: { display: false } },
      y: {
        type: 'linear',
        position: 'left',
        title: { display: true, text: 'Occupancy (%)' },
        min: 80,
        max: 95,
        grid: { color: gridColor },
      },
      y1: {
        type: 'linear',
        position: 'right',
        title: { display: true, text: 'Rent ($)' },
        min: 0,
        max: 2000,
        grid: { display: false },
      },
    },
  };

  return (
    <div className="chart-container">
      <h4>Occupancy & Rent by Property Class (Q4 2025)</h4>
      <FilterBar
        options={[
          { label: 'All Data', value: 'all' },
          { label: 'Occupancy Only', value: 'occupancy' },
          { label: 'Rent Only', value: 'rent' },
        ]}
        active={filter}
        onChange={setFilter}
      />
      <div className="chart-wrapper">
        <Bar ref={chartRef} data={data} options={options} />
      </div>
      <p className="chart-source">Source: Colliers, MRI Apartment Data</p>
    </div>
  );
}

/* ─── 3. Submarket Activity ─── */
export function SubmarketChart() {
  const [filter, setFilter] = useState('all');
  const chartRef = useRef<ChartJS<'bar'>>(null);

  const filterMap: Record<string, number[]> = {
    delivered: [0],
    absorption: [1],
    construction: [2],
  };

  const updateVisibility = useCallback((f: string) => {
    const chart = chartRef.current;
    if (!chart) return;
    chart.data.datasets.forEach((ds, i) => {
      if (f === 'all') { ds.hidden = false; }
      else { ds.hidden = !filterMap[f]?.includes(i); }
    });
    chart.update();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => { updateVisibility(filter); }, [filter, updateVisibility]);

  const data: ChartData<'bar'> = {
    labels: ['Central', 'Northeast', 'Northwest', 'Southeast', 'Southwest'],
    datasets: [
      {
        label: 'Units Delivered',
        data: [0, 725, 1881, 389, 0],
        backgroundColor: darkBlue,
        borderRadius: 4,
      },
      {
        label: 'Net Absorption',
        data: [1, 987, 1184, 977, 862],
        backgroundColor: rcGreen,
        borderRadius: 4,
      },
      {
        label: 'Under Construction',
        data: [1345, 0, 3017, 2292, 1446],
        backgroundColor: sageLight,
        borderRadius: 4,
      },
    ],
  };

  const options: ChartOptions<'bar'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top', labels: { usePointStyle: true, padding: 20 } },
    },
    scales: {
      x: { grid: { display: false } },
      y: {
        title: { display: true, text: '# of Units' },
        grid: { color: gridColor },
      },
    },
  };

  return (
    <div className="chart-container">
      <h4>Houston Multifamily Activity by Submarket (Q4 2025)</h4>
      <FilterBar
        options={[
          { label: 'All Data', value: 'all' },
          { label: 'Delivered', value: 'delivered' },
          { label: 'Absorption', value: 'absorption' },
          { label: 'Under Construction', value: 'construction' },
        ]}
        active={filter}
        onChange={setFilter}
      />
      <div className="chart-wrapper">
        <Bar ref={chartRef} data={data} options={options} />
      </div>
      <p className="chart-source">Source: Colliers, MRI Apartment Data</p>
    </div>
  );
}

/* ─── 4. Price Per Unit ─── */
export function PricePerUnitChart() {
  const [filter, setFilter] = useState('all');
  const chartRef = useRef<ChartJS<'line'>>(null);

  const filterMap: Record<string, number[]> = { us: [0], texas: [1], houston: [2] };

  const updateVisibility = useCallback((f: string) => {
    const chart = chartRef.current;
    if (!chart) return;
    chart.data.datasets.forEach((ds, i) => {
      if (f === 'all') { ds.hidden = false; }
      else { ds.hidden = !filterMap[f]?.includes(i); }
    });
    chart.update();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => { updateVisibility(filter); }, [filter, updateVisibility]);

  const data: ChartData<'line'> = {
    labels: quarterLabels,
    datasets: [
      {
        label: 'U.S.',
        data: [165000,175000,190000,210000,225000,235000,240000,230000,220000,210000,205000,200000,195000,198000,205000,210000,212000,215000,218000,220752],
        borderColor: '#718096',
        backgroundColor: 'transparent',
        tension: 0.3,
        pointRadius: 2,
      },
      {
        label: 'Texas',
        data: [130000,140000,155000,170000,180000,188000,192000,185000,175000,168000,165000,162000,160000,163000,168000,170000,171000,172000,174000,174260],
        borderColor: sage,
        backgroundColor: 'transparent',
        tension: 0.3,
        pointRadius: 2,
      },
      {
        label: 'Houston',
        data: [115000,125000,140000,155000,165000,172000,175000,168000,158000,150000,148000,145000,143000,148000,155000,145500,155000,162000,167000,173079],
        borderColor: rcGreen,
        backgroundColor: 'transparent',
        tension: 0.3,
        pointRadius: 2,
        borderWidth: 3,
      },
    ],
  };

  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top', labels: { usePointStyle: true, padding: 15 } },
    },
    scales: {
      x: { grid: { display: false } },
      y: {
        title: { display: true, text: 'Price ($)' },
        grid: { color: gridColor },
        ticks: {
          callback: function (value) {
            return '$' + (Number(value) / 1000) + 'K';
          },
        },
      },
    },
  };

  return (
    <div className="chart-container" style={{ margin: 0 }}>
      <h4>Average Price Per Unit</h4>
      <FilterBar
        options={[
          { label: 'All', value: 'all' },
          { label: 'U.S.', value: 'us' },
          { label: 'Texas', value: 'texas' },
          { label: 'Houston', value: 'houston' },
        ]}
        active={filter}
        onChange={setFilter}
      />
      <div className="chart-wrapper">
        <Line ref={chartRef} data={data} options={options} />
      </div>
      <p className="chart-source">Source: Colliers, MSCI Real Capital Analytics</p>
    </div>
  );
}

/* ─── 5. Cap Rate ─── */
export function CapRateChart() {
  const [filter, setFilter] = useState('all');
  const chartRef = useRef<ChartJS<'line'>>(null);

  const filterMap: Record<string, number[]> = { us: [0], texas: [1], houston: [2] };

  const updateVisibility = useCallback((f: string) => {
    const chart = chartRef.current;
    if (!chart) return;
    chart.data.datasets.forEach((ds, i) => {
      if (f === 'all') { ds.hidden = false; }
      else { ds.hidden = !filterMap[f]?.includes(i); }
    });
    chart.update();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => { updateVisibility(filter); }, [filter, updateVisibility]);

  const data: ChartData<'line'> = {
    labels: quarterLabels,
    datasets: [
      {
        label: 'U.S.',
        data: [4.8,4.6,4.5,4.3,4.2,4.2,4.3,4.5,4.8,5.1,5.3,5.5,5.6,5.7,5.8,5.8,5.8,5.8,5.8,5.8],
        borderColor: '#718096',
        backgroundColor: 'transparent',
        tension: 0.3,
        pointRadius: 2,
      },
      {
        label: 'Texas',
        data: [4.9,4.7,4.5,4.4,4.3,4.3,4.4,4.6,4.9,5.2,5.4,5.5,5.6,5.7,5.8,5.8,5.8,5.8,5.8,5.8],
        borderColor: sage,
        backgroundColor: 'transparent',
        tension: 0.3,
        pointRadius: 2,
      },
      {
        label: 'Houston',
        data: [5.0,4.8,4.6,4.5,4.4,4.4,4.5,4.7,5.0,5.3,5.5,5.6,5.7,5.8,5.8,5.8,5.8,5.8,5.8,5.9],
        borderColor: rcGreen,
        backgroundColor: 'transparent',
        tension: 0.3,
        pointRadius: 2,
        borderWidth: 3,
      },
    ],
  };

  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top', labels: { usePointStyle: true, padding: 15 } },
    },
    scales: {
      x: { grid: { display: false } },
      y: {
        title: { display: true, text: 'Cap Rate (%)' },
        min: 4.0,
        max: 6.0,
        grid: { color: gridColor },
        ticks: {
          callback: function (value) {
            return Number(value).toFixed(1) + '%';
          },
        },
      },
    },
  };

  return (
    <div className="chart-container" style={{ margin: 0 }}>
      <h4>Average Cap Rate Comparison</h4>
      <FilterBar
        options={[
          { label: 'All', value: 'all' },
          { label: 'U.S.', value: 'us' },
          { label: 'Texas', value: 'texas' },
          { label: 'Houston', value: 'houston' },
        ]}
        active={filter}
        onChange={setFilter}
      />
      <div className="chart-wrapper">
        <Line ref={chartRef} data={data} options={options} />
      </div>
      <p className="chart-source">Source: Colliers, MSCI Real Capital Analytics</p>
    </div>
  );
}
