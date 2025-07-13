import React, { useState } from 'react';
import { styled }          from '@mui/material/styles';
import { Link }            from 'react-router-dom';

import {
	AppBar, Toolbar, Container, Box, Typography, Drawer, IconButton, Button, MenuItem
} from '@mui/material';
import MenuIcon         from '@mui/icons-material/Menu';
import CloseRoundedIcon from '@mui/icons-material/CloseRounded';




const Title       = "Самые высокие здания и сооружения";
const NavBarItems = [
    { name: 'Главная',     path: '/',         display: true  },
    { name: 'Таблица игр', path: '/table',    display: true  },
    { name: 'Графики',     path: '/chart',    display: true  },
    { name: 'Детали игры', path: '/game/:id', display: false },
];

interface Props {
    active: string;
}



const StyledToolbar = styled(Toolbar)(({ theme }) => ({
    display:        'flex',
    alignItems:     'center',
    justifyContent: 'space-between',
    flexShrink:     0,
    borderRadius:   `calc(${theme.shape.borderRadius}px + 8px)`,
    border:         '1px solid',
    borderColor:    theme.palette.divider,
    padding:        '8px 12px',
}));

const StyledMenuItem = styled(MenuItem)(({ theme }) => ({
    '&.active': {
        backgroundColor: theme.palette.info.main,
        color:           theme.palette.info.contrastText,
    },
	'&.active:hover': {
		backgroundColor: theme.palette.info.main,
		color:           theme.palette.info.contrastText,
	},
}));

const NavLink = styled(Link)(({ theme }) => ({
    textDecoration: 'none',
    color:          'inherit',
    '&.active button': {
        backgroundColor: theme.palette.primary.main,
        color:           theme.palette.primary.contrastText,
    }
}));



function NavBar(props: Props) {
    const [open, setOpen] = React.useState(false);

    const toggleDrawer = (open: boolean) => () => {
        setOpen(open);
    };



    // Функция для фильтрации элементов навигации
    const getVisibleItems = () => {
        return NavBarItems.filter(item =>
            item.display || props.active === item.path
        );
    };

    const visibleItems = getVisibleItems();



    return (
        <AppBar position="static" sx={{ boxShadow: 0, bgcolor: 'transparent', mt: '28px' }}>
            <Container maxWidth="lg">
                <StyledToolbar>

                    <NavLink to="/">
                        <Typography variant="h6" sx={{ color: '#5d8aa8' }}>
                            {Title}
                        </Typography>
                    </NavLink>

                    <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 1 }}>
                        {visibleItems.map((item) => (
                            <NavLink
                                className={props.active === item.path ? 'active' : ''} to={item.path}
                            >
                                <Button
                                    variant={props.active === item.path ? 'contained' : 'text'} color="info" size="medium"
                                >
                                    {item.name}
                                </Button>
                            </NavLink>
                        ))}
                    </Box>

					<Box sx={{ display: { xs: 'flex', md: 'none' }}}>
						<IconButton
							aria-label="Menu button" onClick={toggleDrawer(true)}
						>
							<MenuIcon />
						</IconButton>

                        <Drawer
                            anchor="top" open={open} onClose={toggleDrawer(false)}
                        >
                            <Box>
                                <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
									<IconButton onClick={toggleDrawer(false)}>
										<CloseRoundedIcon />
									</IconButton>
                                </Box>

                                <Box sx={{ p: 2 }}>
                                    {visibleItems.map((item) => (
                                        <NavLink
                                            to={item.path} onClick={toggleDrawer(false)}
                                        >
                                            <StyledMenuItem
                                            	className={props.active === item.path ? 'active' : ''}
                                            >
                                                {item.name}
                                            </StyledMenuItem>
                                        </NavLink>
                                    ))}
                                </Box>
                            </Box>
                        </Drawer>
                    </Box>

                </StyledToolbar>
            </Container>
        </AppBar>
    );
}

export default NavBar;