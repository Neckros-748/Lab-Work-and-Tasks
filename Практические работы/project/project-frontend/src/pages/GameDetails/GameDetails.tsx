import React, { useState } from 'react';
import { styled }          from '@mui/material/styles';
import { Link, useParams } from 'react-router-dom';

import {
	Card, CardContent, CardMedia, Typography, Container, Box, Breadcrumbs
} from '@mui/material';

import NavBar from '../../components/NavBar';
import games  from '../../data/games_data';

function GameDetails() {
	const { id } = useParams();
	const game   = games.find(g => g.id === Number(id));

	if (!game) {
		return <div>Игра не найдена</div>;
	}

	return (
		<div>
			<NavBar active="/game/:id" />

			<Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
				<Breadcrumbs separator='>' sx={{ mb: 3 }}>
					<Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
						Главная
					</Link>
					<Typography color="text.primary">{game.game}</Typography>
				</Breadcrumbs>

				<Card sx={{ maxWidth: '100%' }}>
					<Box sx={{
						display:         'flex',
						justifyContent:  'center',
						alignItems:      'center',
						height:          400,
						backgroundColor: '#f5f5f5'
					}}>
						<CardMedia
							component="img"
							sx={{
								maxHeight: '100%',
								maxWidth:  '100%',
								objectFit: 'contain'
							}}
							image={require(`../../data/images/image-${id}.jpg`)}
							alt={game.game}
						/>
					</Box>
					<CardContent>
						<Typography gutterBottom variant="h4" component="div">
							{game.game}
						</Typography>
						<Typography variant="body1" paragraph>
							<strong>Жанр:</strong> {game.genre}
						</Typography>
						<Typography variant="body1" paragraph>
							<strong>Продажи:</strong> {game.total_sales.toFixed(2)} млн
						</Typography>
					</CardContent>
				</Card>
			</Container>
		</div>
	);
};

export default GameDetails;