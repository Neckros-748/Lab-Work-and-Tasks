from config import app, db
from models import TypeBuilding
from sqlalchemy import and_, or_, not_


# Добавление записей в таблицу type_building
def create_records_type_building():
	# Список типов зданий для добавления
	building_types = [
		'Небоскрёб',
		'Антенная мачта',
		'Бетонная башня',
		'Радиомачта',
		'Гиперболоидная башня',
		'Дымовая труба',
		'Решётчатая мачта',
		'Башня',
		'Мост'
	]

	for type_name in building_types:
		db.session.add(TypeBuilding(type_name))

	# Сохранение изменений в базе данных
	db.session.commit()
	print("Записи успешно добавлены в таблицу type_building.")


# Получение записей из таблицы type_building
def read_records_type_building():
	query = TypeBuilding.query.all()
	print(query)

	query = TypeBuilding.query.filter(TypeBuilding.id == 5).all()
	print(query)

	query = TypeBuilding.query.filter(TypeBuilding.name.like("%мачта%")).all()
	print(query)

	query = (TypeBuilding.query.filter(TypeBuilding.name.like("%мачта%")).order_by(TypeBuilding.name.desc()).all())
	print(query)

	query = TypeBuilding.query.filter(and_(TypeBuilding.name.like('%е%'), TypeBuilding.id > 3)).all()
	print(query)


# Обновление записей в таблице type_building
def update_records_type_building():
	TypeBuilding.query.filter(TypeBuilding.name == 'Мост').update({TypeBuilding.name: "Мосты"})
	db.session.commit()

	query = TypeBuilding.query.all()
	print(query)


# Удаление записей из таблицы type_building
def delete_records_type_building():
	TypeBuilding.query.filter(TypeBuilding.id == 9).delete()
	db.session.commit()

	query = TypeBuilding.query.all()
	print(query)


# create_records_type_building()
# read_records_type_building()
# update_records_type_building()
# delete_records_type_building()
