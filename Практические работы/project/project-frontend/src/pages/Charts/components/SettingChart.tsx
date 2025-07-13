import {
	FormControl, FormLabel, FormControlLabel, Checkbox, Stack, Divider, RadioGroup, Radio
} from '@mui/material';

type SeriesKeys = 'max_sales' | 'avg_sales' | 'min_sales' | 'total_sales';
type tSeries    = Record<SeriesKeys, boolean>;
type tChart     = 'bar' | 'line';

type Props = {
	series:       tSeries;
	setSeries:    React.Dispatch<React.SetStateAction<tSeries>>;
	type:         tChart;
	setChartType: React.Dispatch<React.SetStateAction<tChart>>;
};

function SettingChart({series, setSeries, type, setChartType}: Props) {
	const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setSeries({
			...series,
			[event.target.name]: event.target.checked,
		});
	};

	const handleChartTypeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		const value = event.target.value as tChart;
		setChartType(value);
	};

	return (
		<Stack
			direction="row"
			justifyContent="center"
			divider={<Divider orientation="vertical" flexItem />}
			spacing={2}
			sx={{ m: "20px 0" }}
		>
			<FormControl>
				<FormLabel id="label-radio-group">
					Тип диаграммы:
				</FormLabel>

				<RadioGroup
					name="group-radio"
					value={ type }
					onChange={ handleChartTypeChange }
				>
					<FormControlLabel
						value="bar"
						control={<Radio />}
						label="Гистограмма"
					/>
					<FormControlLabel
						value="line"
						control={<Radio />}
						label="Линейная"
					/>
				</RadioGroup>
			</FormControl>

			<FormControl>
				<FormLabel id="label-checkbox-group">
					На диаграмме показать:
				</FormLabel>

				<FormControlLabel
					control={
						<Checkbox
							checked={ series["total_sales"] }
							onChange={ handleChange }
							name="total_sales" />
					}
					label="Всего продано (млн)" />
				<FormControlLabel
					control={
						<Checkbox
							checked={ series["max_sales"] }
							onChange={ handleChange }
							name="max_sales" />
					}
					label="Максимальные продажи (млн)" />
				<FormControlLabel
					control={
						<Checkbox
							checked={ series["avg_sales"] }
							onChange={ handleChange }
							name="avg_sales" />
					}
					label="Средние продажи (млн)" />
				<FormControlLabel
					control={
						<Checkbox
							checked={ series["min_sales"] }
							onChange={ handleChange }
							name="min_sales" />
					}
					label="Минимальные продажи (млн)" />
			</FormControl>
		</Stack>
	)
}

export default SettingChart;
