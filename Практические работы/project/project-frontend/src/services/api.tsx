import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

// http://127.0.0.1:5000/api/genres
// http://127.0.0.1:5000/api/genres/1
// http://127.0.0.1:5000/api/platforms
// http://127.0.0.1:5000/api/platforms/1
// http://127.0.0.1:5000/api/games
// http://127.0.0.1:5000/api/games/1
// http://127.0.0.1:5000/api/sales
// http://127.0.0.1:5000/api/sales/1

export const getGenres = () => axios.get(`${API_URL}/genres`)
export const getGenre = (id: number) => axios.get(`${API_URL}/genres/${id}`)

export const getPlatforms = () => axios.get(`${API_URL}/platforms`)
export const getPlatform = (id: number) => axios.get(`${API_URL}/platforms/${id}`)

export const getGames = () => axios.get(`${API_URL}/games`)
export const getGame = (id: number) => axios.get(`${API_URL}/games/${id}`)

export const getSales = () => axios.get(`${API_URL}/sales`)
export const getSale = (id: number) => axios.get(`${API_URL}/sales/${id}`)

// http://127.0.0.1:5000/api/analytics/genre_stats
// http://127.0.0.1:5000/api/analytics/platform_stats
// http://127.0.0.1:5000/api/analytics/year_stats
// http://127.0.0.1:5000/api/analytics/top_games/10

export const getSalesByGenreStats = () => axios.get(`${API_URL}/analytics/genre_stats`)
export const getSalesByPlatformStats = () => axios.get(`${API_URL}/analytics/platform_stats`)
export const getSalesByYearStats = () => axios.get(`${API_URL}/analytics/year_stats`)

export const getTopGames = (limit: number) => axios.get(`${API_URL}/analytics/top_games/${limit}`)