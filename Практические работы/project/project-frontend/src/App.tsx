import React                                   from 'react';
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Main        from "./pages/Main/Main";
import GameDetails from './pages/GameDetails/GameDetails';
import GamesTable  from './pages/GamesTable/GamesTable';
import Charts      from './pages/Charts/Charts';

const router = createBrowserRouter([
	{
		element: <Main />,
		path: "/",
	},
	{
		element: <GameDetails />,
		path: "/game/:id",
	},
	{
		element: <GamesTable />,
		path: "/table",
	},
	{
		element: <Charts />,
		path: "/chart",
	},
]);

function App() {
	return (
		<RouterProvider router={router} />
	);
}

export default App;