from config import db
from models import Country, City, Building, TypeBuilding
from sqlalchemy import func


def get_all_buildings():
	query = (
		db.session.query(
			Building.title.label("Здание"),
			TypeBuilding.name.label("Тип"),
			Country.name.label("Страна"),
			City.name.label("Город"),
			Building.year.label("Год"),
			Building.height.label("Высота")
		)
		.select_from(Building)
		.join(TypeBuilding)
		.join(City)
		.join(Country)
	)
	return [query.statement.columns.keys(), query.all()]


def get_stats_buildings():
	query = (
		db.session.query(
			TypeBuilding.name.label("Тип"),
			func.max(Building.height).label('Максимальная высота'),
			func.min(Building.height).label('Минимальная высота'),
			func.round(func.avg(Building.height), 1).label("Средняя высота")
		)
		.select_from(Building)
		.join(TypeBuilding)
		.group_by(TypeBuilding.name)
	)
	return [query.statement.columns.keys(), query.all()]


def get_stats_country():
	query = (
		db.session.query(
			Country.name.label("Страна"),
			func.max(Building.height).label('Максимальная высота'),
			func.min(Building.height).label('Минимальная высота'),
			func.round(func.avg(Building.height), 1).label("Средняя высота")
		)
		.select_from(Building)
		.join(City)
		.join(Country)
		.group_by(Country.name)
	)
	return [query.statement.columns.keys(), query.all()]


def get_stats_year():
	query = (
		db.session.query(
			Building.year.label("Год"),
			func.max(Building.height).label('Максимальная высота'),
			func.min(Building.height).label('Минимальная высота'),
			func.round(func.avg(Building.height), 1).label("Средняя высота")
		)
		.select_from(Building)
		.group_by(Building.year)
	)
	return [query.statement.columns.keys(), query.all()]


def get_buildings(start_year, end_year):
	query = (
		db.session.query(
			Building.title.label("Здание"),
			TypeBuilding.name.label("Тип"),
			Country.name.label("Страна"),
			City.name.label("Город"),
			Building.year.label("Год"),
			Building.height.label("Высота")
		)
		.select_from(Building)
		.join(TypeBuilding)
		.join(City)
		.join(Country)
		.filter(Building.year.between(start_year, end_year))
		.order_by(Building.year)
	)
	return [query.statement.columns.keys(), query.all()]
