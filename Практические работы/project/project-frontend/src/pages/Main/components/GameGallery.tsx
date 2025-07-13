import React, { useState, useEffect } from 'react';
import { styled }                     from '@mui/material/styles';
import { Link }                       from 'react-router-dom';

import {
	Box, ImageList, ImageListItem, ImageListItemBar
} from '@mui/material';

import games from '../../../data/games_data';

function GameGallery() {
	return (
		<Box sx={{ width: '100%', height: 'auto', overflowY: 'hidden', m: '20px auto' }}>
			<ImageList
				variant="masonry"
				sx={{
					columnCount: {
						sm: '2 !important',
						md: '3 !important',
						lg: '4 !important',
					},
				}}
				gap={8}
			>
				{games.map((game) => (
					<Link key={game.id} to={`/game/${game.id}`}>
						<ImageListItem>
							<img
								src={require(`../../../data/images/image-${game.id}.jpg`)}
								alt={game.game}
								loading="lazy"
								style={{ borderRadius: '4px' }}
							/>
							<ImageListItemBar position="bottom" title={game.game} />
						</ImageListItem>
					</Link>
				))}
			</ImageList>
		</Box>
	);
}

export default GameGallery;