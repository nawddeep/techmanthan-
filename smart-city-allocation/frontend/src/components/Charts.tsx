"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";

interface ChartsProps {
  history: {
    time: string;
    traffic: number;
    waste: number;
  }[];
}

export default function Charts({ history }: ChartsProps) {
  // Use recharts to generate a simple trend line
  return (
    <div className="glass-panel p-6 h-[400px] flex flex-col">
      <h2 className="text-lg font-semibold tracking-wide text-slate-200 uppercase mb-6">Live City Metrics Trend</h2>
      
      <div className="flex-1 w-full -ml-4">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={history}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
            <XAxis 
              dataKey="time" 
              stroke="#64748b" 
              fontSize={12} 
              tickLine={false} 
              axisLine={false} 
            />
            <YAxis 
              stroke="#64748b" 
              fontSize={12} 
              tickLine={false} 
              axisLine={false} 
              domain={[0, 100]}
            />
            <Tooltip 
              contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }}
              itemStyle={{ color: '#e2e8f0' }}
            />
            <Legend verticalAlign="top" height={36} wrapperStyle={{ fontSize: '12px', color: '#94a3b8' }} iconType="circle" />
            <Line 
              type="monotone" 
              dataKey="traffic" 
              stroke="#3B82F6" 
              strokeWidth={3}
              dot={false}
              activeDot={{ r: 6 }}
              name="Traffic Level"
            />
            <Line 
              type="monotone" 
              dataKey="waste" 
              stroke="#22C55E" 
              strokeWidth={3}
              dot={false}
              activeDot={{ r: 6 }}
              name="Waste Fill %"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
