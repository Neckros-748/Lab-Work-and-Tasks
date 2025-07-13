import { Container } from '@mui/material';
import NavBar        from '../../components/NavBar';
import GameGallery   from './components/GameGallery';
import GameContent   from './components/GameContent';

function Main() {
	return (
		<div>
			<NavBar active="/" />

			<Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
				<GameGallery />
				<GameContent />
			</Container>
		</div>
	);
}

export default Main;