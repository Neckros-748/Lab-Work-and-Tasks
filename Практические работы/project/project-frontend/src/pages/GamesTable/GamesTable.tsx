import { Container } from '@mui/material';
import NavBar        from '../../components/NavBar';
import GamesDataGrid from './components/GamesDataGrid';

function GamesTable() {
	return (
		<div>
			<NavBar active="/table" />

			<Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
				<GamesDataGrid />
			</Container>
		</div>
	);
};

export default GamesTable;