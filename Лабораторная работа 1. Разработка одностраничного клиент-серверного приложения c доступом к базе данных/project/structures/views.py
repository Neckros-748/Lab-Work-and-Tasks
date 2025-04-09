from app import app
from flask import render_template
from structures.models import get_all_buildings, get_stats_buildings, get_stats_country, get_stats_year, get_buildings


@app.route('/')
def index():

	[all_buildings_head, all_buildings_body] = get_all_buildings()
	[stats_buildings_head, stats_buildings_body] = get_stats_buildings()
	[stats_country_head, stats_country_body] = get_stats_country()
	[stats_year_head, stats_year_body] = get_stats_year()
	[buildings_head, buildings_body] = get_buildings(2000, 2018)
	
	html = render_template(
		'index.html',
		all_buildings_head=all_buildings_head,
		all_buildings_body=all_buildings_body,
		stats_buildings_head=stats_buildings_head,
		stats_buildings_body=stats_buildings_body,
		stats_country_head=stats_country_head,
		stats_country_body=stats_country_body,
		stats_year_head=stats_year_head,
		stats_year_body=stats_year_body,
		buildings_head=buildings_head,
		buildings_body=buildings_body,
	)

	return html
