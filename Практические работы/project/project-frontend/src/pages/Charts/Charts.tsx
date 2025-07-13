import React, { useState, useEffect } from 'react';

import {
	Select, SelectChangeEvent, Box, Container, FormControl, InputLabel, MenuItem
} from '@mui/material';

import NavBar                                      from '../../components/NavBar';
import GroupChart                                  from './components/GroupChart';
// import { genre_stats, platform_stats, year_stats } from '../../data/grouped_data';

import { getSalesByGenreStats, getSalesByPlatformStats, getSalesByYearStats } from '../../services/api'
import { AnalyticsData }                                                      from '../../services/types'

type tSelect = "genre" | "platform" | "year";



function Charts() {
	const [genre_stats, setGenreStats]       = React.useState<AnalyticsData[]>([]);
	const [platform_stats, setPlatformStats] = React.useState<AnalyticsData[]>([]);
	const [year_stats, setYearStats]         = React.useState<AnalyticsData[]>([]);

	const [group, setGroup]     = React.useState<tSelect>("genre");
	const [data,  setGroupData] = React.useState(genre_stats);

	useEffect(() => {
		getSalesByGenreStats().then((resp) => {
			setGenreStats(resp.data);
			console.log(resp.data);

			setGroupData(resp.data);
		});

		getSalesByPlatformStats().then((resp) => {
			setPlatformStats(resp.data);
			console.log(resp.data);
		});

		getSalesByYearStats().then((resp) => {
			setYearStats(resp.data);
			console.log(resp.data);
		});

	}, []);



	const handleChange = (event: SelectChangeEvent) => {
		const value = event.target.value as tSelect;
		setGroup(value);

		switch(value) {
			case "genre":
				setGroupData(genre_stats);
				break;
			case "platform":
				setGroupData(platform_stats);
				break;
			case "year":
				setGroupData(year_stats);
				break;
		}
	};

	return (
		<div>
			<NavBar active="/chart" />

			<Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
				<FormControl sx={{ minWidth: 200, mb: 3 }}>
					<InputLabel>Группировать по</InputLabel>

					<Select
						id="select-group"
						value={ group }
						label="Группировать по"
						onChange={ handleChange }
					>
						<MenuItem value="genre">Жанру</MenuItem>
						<MenuItem value="platform">Платформе</MenuItem>
						<MenuItem value="year">Году выпуска</MenuItem>
					</Select>
				</FormControl>

				<GroupChart data={data} />
			</Container>
		</div>

	);
};

export default Charts;