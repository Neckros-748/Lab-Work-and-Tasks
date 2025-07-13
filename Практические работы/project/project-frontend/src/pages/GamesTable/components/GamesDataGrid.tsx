import Container                              from '@mui/material/Container';
import { DataGrid, GridColDef, GridRowsProp } from '@mui/x-data-grid';
import { ruRU }                               from '@mui/x-data-grid/locales';
// import sales                                  from '../../../data/table_data';

import React, { useState, useEffect } from 'react';
import { getSales }                   from '../../../services/api'
import { SaleGame }                   from '../../../services/types'



function GamesDataGrid() {
	const [sales, setSalesData] = React.useState<SaleGame[]>([]);

	useEffect(() => {
		getSales()
			.then((resp) => {
				setSalesData(resp.data);
				console.log(resp.data);
		});
	}, []);



	const rows:    GridRowsProp = sales;
	const columns: GridColDef[] = [
 		{ field: 'identifier', headerName: 'ID', flex: 0.2 },
		{
			field: 'game_name', headerName: 'Название игры', flex: 1,
			valueGetter: (value, row) => {
				if (!row.game_rel.name) {
					return '';
				}
				return row.game_rel.name;
			},
		},
		{
			field: 'game_genre', headerName: 'Жанр', flex: 0.4,
			valueGetter: (value, row) => {
				if (!row.game_rel.genre_rel.name) {
					return '';
				}
				return row.game_rel.genre_rel.name;
			},
		},
		{
			field: 'game_platform', headerName: 'Платформа', flex: 0.4,
			valueGetter: (value, row) => {
				if (!row.platform_rel.name) {
					return '';
				}
				return row.platform_rel.name;
			},
		},
 		{ field: 'published', headerName: 'Год публикации', flex: 0.4 },
 		{ field: 'sales', headerName: 'Продажи (млн)', flex: 0.4 },
	];

	return (
		<Container maxWidth="lg" sx={{height: '700px', mt: '20px'}}>
			<DataGrid
				localeText={ruRU.components.MuiDataGrid.defaultProps.localeText}
				showToolbar={true}
				rows={rows}
				columns={columns}
				getRowId={(row) => row.identifier}
			/>
		</Container>

	);
};

export default GamesDataGrid;