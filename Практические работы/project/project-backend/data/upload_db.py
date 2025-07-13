import csv
from project.config import app, db
from project.models import Genre, Platform, VideoGame, SaleGame


def upload_data_from_csv(path):
	db.session.query(SaleGame).delete()
	db.session.query(VideoGame).delete()
	db.session.query(Platform).delete()
	db.session.query(Genre).delete()
	db.session.commit()
	
	genres    = {}
	platforms = {}
	games     = {}
	
	with open(path, 'r', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		# next(reader)
		
		for row in reader:
			# Rank, Name, Platform, Year, Genre, Publisher, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales
			
			# Обработка жанра
			genre_name = row['Genre']
			if genre_name not in genres:
				genre = Genre(genre_name)
				db.session.add(genre)
				db.session.commit()
				genres[genre_name] = genre
			
			# Обработка платформы
			platform_name = row['Platform']
			if platform_name not in platforms:
				platform = Platform(platform_name)
				db.session.add(platform)
				db.session.commit()
				platforms[platform_name] = platform
			
			# Обработка игры
			game_name = row['Name']
			if game_name not in games:
				game = VideoGame(game_name, genres[genre_name].identifier)
				db.session.add(game)
				db.session.commit()
				games[game_name] = game
			
			# Обработка продаж
			sale = SaleGame(
				games[game_name].identifier,
				platforms[platform_name].identifier,
				int(row['Year']) if row['Year'] != "N/A" else None,
				float(row['Global_Sales'])
			)
			db.session.add(sale)
			
			print(row)
		
		db.session.commit()
		print("Данные успешно загружены в базу данных!")


# Загрузка данных в таблицы
upload_data_from_csv("./vgsales.csv")
