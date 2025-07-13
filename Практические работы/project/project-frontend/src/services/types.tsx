export interface Genre {
	identifier: number;
	name:       string;
}

export interface Platform {
	identifier: number;
	name:       string;
}

export interface VideoGame {
	identifier: number;
	name:       string;
	genre_id:   number;
	genre_rel?: Genre;
}

export interface SaleGame {
	identifier:    number;
	game_id:       number;
	game_rel?:     VideoGame;
	platform_id:   number;
	platform_rel?: Platform;
	published:     number;
	sales:         number;
}

export interface AnalyticsData {
	group: string;
	analytics: {
		total_sales: number;
		avg_sales:   number;
		max_sales:   number;
		min_sales:   number;
	}
}