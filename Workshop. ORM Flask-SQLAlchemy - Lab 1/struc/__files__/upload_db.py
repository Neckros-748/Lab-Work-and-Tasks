from config import db
from models import Country, City, Building
import csv


# Функция для загрузки данных в таблицу Country
def country_upload():
	with open("data/country.csv") as f:
		reader = csv.reader(f)
		next(reader)
		for item in reader:
			new_entry = Country(item[0])
			db.session.add(new_entry)
		db.session.commit()
		print("Данные загружены в таблицу Country.")


# Функция для загрузки данных в таблицу City
def city_upload():
	with open("data/city.csv") as f:
		reader = csv.reader(f)
		next(reader)
		for item in reader:
			new_entry = City(item[0], int(item[1]))
			db.session.add(new_entry)
		db.session.commit()
		print("Данные загружены в таблицу City.")


# Функция для загрузки данных в таблицу Building
def building_upload():
	with open("data/building.csv") as f:
		reader = csv.reader(f)
		next(reader)
		for item in reader:
			new_entry = Building(item[0], int(item[1]), int(item[2]), int(item[3]), float(item[4]))
			db.session.add(new_entry)
		db.session.commit()
		print("Данные загружены в таблицу Building.")


# Функция для вывода данных из таблицы Country
def show_countries():
	query = Country.query.all()
	print(query)


# Функция для вывода данных из таблицы City
def show_cities():
	query = City.query.all()
	print(query)


# Функция для вывода данных из таблицы Building
def show_buildings():
	query = Building.query.all()
	print(query)


# Загрузка данных в таблицы
# country_upload()
# city_upload()
# building_upload()

# Вывод данных из таблиц
show_countries()
show_cities()
show_buildings()
