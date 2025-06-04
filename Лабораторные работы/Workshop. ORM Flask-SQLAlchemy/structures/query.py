from config import app, db
from models import Country, City, Building, TypeBuilding
from sqlalchemy import func, select, desc


# from sqlalchemy import desc


# 1. Вывести информацию о каждом здании: название, тип, страна, город, год, высота.
# Информацию отсортировать по убыванию высоты.
def __task_1():
	result = (
		db.session.query(
			Building.title.label("Название"),
			TypeBuilding.name.label("Тип"),
			Country.name.label("Страна"),
			City.name.label("Город"),
			Building.year.label("Год"),
			Building.height.label("Высота")
		)
		.select_from(Building)
		.join(TypeBuilding, Building.type_building_id == TypeBuilding.id)
		.join(City, Building.city_id == City.id)
		.join(Country, City.country_id == Country.id)
		.order_by(Building.height.desc())
		.all()
	)
	print(result)


# 2. Посчитать максимальную, минимальную и среднюю высоту зданий в каждой стране.
# Информацию отсортировать по названию страны.
def __task_2():
	result = (
		db.session.query(
			Country.name.label("Страна"),
			func.max(Building.height).label('Max высота'),
			func.min(Building.height).label('Min высота'),
			func.round(func.avg(Building.height), 3).label('Avg высота')
		)
		.select_from(Building)
		.join(City, Building.city_id == City.id)
		.join(Country, City.country_id == Country.id)
		.group_by(Country.name)
		.order_by(Country.name)
		.all()
	)
	print(result)


# 3. Посчитать максимальную, минимальную и среднюю высоту зданий по каждому году.
# Информацию отсортировать по возрастанию года.
def __task_3():
	result = (
		db.session.query(
			Building.year.label('Год'),
			func.max(Building.height).label('Max высота'),
			func.min(Building.height).label('Min высота'),
			func.round(func.avg(Building.height), 3).label('Avg высота')
		)
		.group_by(Building.year)
		.order_by(Building.year)
		.all()
	)
	print(result)


# 4. Посчитать максимальную, минимальную и среднюю высоту зданий только для тех
# типов зданий, название которых содержит слово «мачта». Информацию отсортировать по
# убыванию средней высоты.
def __task_4():
	result = (
		db.session.query(
			TypeBuilding.name.label('Тип'),
			func.max(Building.height).label('Max высота'),
			func.min(Building.height).label('Min высота'),
			func.round(func.avg(Building.height), 3).label('Avg высота')
		)
		.join(TypeBuilding, Building.type_building_id == TypeBuilding.id)
		.filter(TypeBuilding.name.like('%мачта%'))
		.group_by(TypeBuilding.name)
		.order_by(desc('Avg высота'))
		.all()
	)
	print(result)


# 5. Посчитать максимальную, минимальную и среднюю высоту зданий для тех стран, в
# которых построено больше одного здания (самостоятельно найти соответствующий метод).
def __task_5():
	# Подзапрос
	# subq = (
	# 	select(City.country_id)
	# 	.join(Building)
	# 	.group_by(City.country_id)
	# 	.having(func.count(Building.id) > 1)
	# )
	
	subq = (
		db.session.query(
			City.country_id
		)
		.join(Building, Building.city_id == City.id)
		.group_by(City.country_id)
		.having(func.count(Building.id) > 1)
		# .subquery()
		# .all()
	)
	
	# Основной запрос
	result = (
		db.session.query(
			Country.name.label("Страна"),
			func.max(Building.height).label('Max высота'),
			func.min(Building.height).label('Min высота'),
			func.round(func.avg(Building.height), 3).label('Avg высота')
		)
		.select_from(Building)
		.filter(Country.id.in_(subq))
		.join(City, Building.city_id == City.id)
		.join(Country, City.country_id == Country.id)
		.group_by(Country.name)
		.order_by(Country.name)
		.all()
	)
	print(result)


__task_1()
__task_2()
__task_3()
__task_4()
__task_5()
