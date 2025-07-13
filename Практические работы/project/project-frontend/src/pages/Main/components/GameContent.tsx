import {
	Typography
} from '@mui/material';

function GameContent() {
	return (
		<div>
			<Typography variant="h6" gutterBottom>
				📌 Практическое задание 3. (React, TypeScript, MUI)

			</Typography>
			<Typography>
				<Typography variant="body1" gutterBottom>
					Используя React, TypeScript, MUI создать сайт для выбранной предметной области, который включает следующие страницы
				</Typography>

				<Typography variant="body2" gutterBottom>
					Главная (уже создана в предыдущем индивидуальном задании).
				</Typography>
				<Typography variant="body2" gutterBottom>
					Страница с таблицей (с возможностью фильтрации, сортировки, управления выводом столбцов).
				</Typography>
				<Typography variant="body2" gutterBottom>
					Динамически создаваемая страница, вызываемая по клику на рисунки.
				</Typography>
				<Typography variant="body2" gutterBottom>
					Страница с графиками по группированным данным.
				</Typography>
			</Typography>
		</div>
	);
};

export default GameContent;