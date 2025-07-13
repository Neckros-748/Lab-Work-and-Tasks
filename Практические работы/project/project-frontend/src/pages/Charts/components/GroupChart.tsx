import React, { useState } from 'react';

import {
	Container, Box, Typography
} from '@mui/material';
import {
	BarChart, LineChart, PieChart
} from '@mui/x-charts';
import { axisClasses } from '@mui/x-charts/ChartsAxis';

import SettingChart from './SettingChart';

type Stats = {
	analytics: {
		avg_sales:   number;
		max_sales:   number;
		min_sales:   number;
		total_sales: number;
	};
	group: string;
};

const labels: Record<string, string> = {
	max_sales:   'Макс. продажи',
	avg_sales:   'Средние продажи',
	min_sales:   'Мин. продажи',
	total_sales: 'Общие продажи',
};

type GroupProps = {
	data: Stats[];
};

function GroupChart({ data }: GroupProps) {

	// Преобразуем данные для диаграммы
	const chartData = data.map(item => ({
		group:       item.group,
		total_sales: item.analytics.total_sales,
		avg_sales:   item.analytics.avg_sales,
		max_sales:   item.analytics.max_sales,
		min_sales:   item.analytics.min_sales,
	}));

	const [series, setSeries] = React.useState({
		'min_sales':   true,
		'avg_sales':   true,
		'max_sales':   true,
		'total_sales': false,
	});

	const [type, setChartType] = React.useState<'bar' | 'line'>('bar');

	let __series__ = Object.entries(series)
		.filter(item => item[1] == true)
		.map(([key]) => ({
			dataKey: key,
			label: labels[key],
		}));

	const setting = {
		yAxis: [{
			label: 'Продажи (млн)',
		}],

		height: 400,
		sx: {
			[`.${axisClasses.left} .${axisClasses.label}`]: {
				transform: 'translate(-10px, 0)',
			},
		},
	};

	return (
		<Container maxWidth="lg">
			<Box sx={{ mb: 3 }}>
				<Typography variant="h5" gutterBottom>
					Статистика по продажам
				</Typography>
				<Typography variant="body1" color="text.secondary">
					Анализ средних, максимальных и минимальных продаж игр
				</Typography>
			</Box>

			<SettingChart
				series={series}
				setSeries={setSeries}
				type={type}
				setChartType={setChartType}
			/>

			{type === 'bar' && (
				<BarChart
					dataset={ chartData }
					series={ __series__ }
					xAxis={[{
						scaleType: 'band', dataKey: 'group'
					}]}
					slotProps={{
						legend: {
							position: { vertical: 'bottom', horizontal: 'center' },
						},
					}}
					barLabel={__series__.length === 1 ? "value" : undefined}
					{...setting}
				/>
			)}

			{type === 'line' && (
				<LineChart
					dataset={ chartData }
					series={ __series__ }
					xAxis={[{
						scaleType: 'band', dataKey: 'group'
					}]}
					slotProps={{
						legend: {
							position: { vertical: 'bottom', horizontal: 'center' },
						},
					}}
					{...setting}
				/>
			)}

		</Container>
	);
}

export default GroupChart;