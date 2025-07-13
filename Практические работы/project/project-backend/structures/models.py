from config      import app, db
from flask       import request, jsonify, abort
from models      import Genre, Platform, VideoGame, SaleGame
from marshmallow import ValidationError
from structures.serializers import (
	genre_schema, genres_schema,
	platform_schema, platforms_schema,
	game_schema, games_schema,
	sale_schema, sales_schema
)


class Request:
	@staticmethod
	def get_genres():
		return Genre.query.all()
	
	@staticmethod
	def get_platforms():
		return Platform.query.all()
	
	@staticmethod
	def get_games():
		return VideoGame.query.all()
	
	@staticmethod
	def get_sales():
		return SaleGame.query.all()
	
	@staticmethod
	def get_query_1():
		query = (
			db.session.query(
				VideoGame.name.label("Игра"),
				Genre.name.label("Жанр"),
				db.func.sum(SaleGame.sales).label("Продажи (млн)")
			)
			.join(Genre).join(SaleGame)
			.group_by(VideoGame.name)
			.order_by(db.desc('Продажи (млн)'))
			.limit(10)
		)
		return query
	
	@staticmethod
	def get_query_2():
		query = (
			db.session.query(
				Platform.name.label("Платформа"),
				db.func.sum(SaleGame.sales).label('Продажи (млн)')
			)
			.join(SaleGame)
			.group_by(Platform.name)
			.order_by(db.desc('Продажи (млн)'))
			.limit(5)
		)
		return query
	
	@staticmethod
	def get_query_3():
		query = (
			db.session.query(
				Genre.name.label("Жанр"),
				db.func.avg(SaleGame.sales).label('Средние продажи (млн)')
			)
			.select_from(Genre)
			.join(VideoGame).join(SaleGame)
			.group_by(Genre.name)
			.order_by(db.desc('Средние продажи (млн)'))
		)
		return query
	
	@staticmethod
	def get_query_4():
		query = (
			db.session.query(
				SaleGame.published.label('Год'),
				db.func.sum(SaleGame.sales).label('Продажи (млн)')
			)
			.group_by('Год')
			.order_by('Год')
		)
		return query
	
	@staticmethod
	def get_query_5():
		subquery = (
			db.session.query(
				(db.func.floor(SaleGame.published / 10) * 10).label('Декада'),
				Genre.name.label('Жанр'),
				db.func.sum(SaleGame.sales).label('Продажи (млн)'),
				db.func.rank().over(
					partition_by=(db.func.floor(SaleGame.published / 10) * 10),
					order_by=db.func.sum(SaleGame.sales).desc()
				).label('rank')
			)
			.select_from(SaleGame)
			.join(VideoGame).join(Genre)
			.group_by('Декада', 'Жанр')
			.subquery()
		)
		
		query = (
			db.session.query(
				subquery.c.Декада,
				subquery.c.Жанр,
				subquery.c['Продажи (млн)']
			)
			.filter(subquery.c.rank <= 3)
			.order_by(subquery.c.Декада, subquery.c.rank)
		)
		return query


class API:
	@staticmethod
	def get_genres():
		genres = Genre.query.all()
		return jsonify(genres_schema.dump(genres))
	
	@staticmethod
	def get_genre(id):
		genre = Genre.query.get_or_404(id)
		return jsonify(genre_schema.dump(genre))
	
	@staticmethod
	def add_genre():
		fields = ['name']
		if not request.json or not all(f in request.json for f in fields):
			abort(400)
		try:
			genre = genre_schema.load(request.json)
			db.session.add(genre)
			db.session.commit()
			return jsonify(genre_schema.dump(genre)), 201
		except ValidationError as e:
			return jsonify(e.messages), 400
	
	@staticmethod
	def update_genre(id):
		genre = Genre.query.get_or_404(id)
		try:
			genre = genre_schema.load(request.json, instance=genre, partial=True)
			db.session.commit()
			return jsonify(genre_schema.dump(genre)), 200
		except ValidationError as e:
			db.session.rollback()
			return jsonify(e.messages), 400
	
	@staticmethod
	def delete_genre(id):
		genre = Genre.query.get_or_404(id)
		db.session.delete(genre)
		db.session.commit()
		return jsonify({'result': True})
	
	@staticmethod
	def get_platforms():
		platforms = Platform.query.all()
		return jsonify(platforms_schema.dump(platforms))
	
	@staticmethod
	def get_platform(id):
		platform = Platform.query.get_or_404(id)
		return jsonify(platform_schema.dump(platform))
	
	@staticmethod
	def add_platform():
		fields = ['name']
		if not request.json or not all(f in request.json for f in fields):
			abort(400)
		try:
			platform = platform_schema.load(request.json)
			db.session.add(platform)
			db.session.commit()
			return jsonify(platform_schema.dump(platform)), 201
		except ValidationError as e:
			return jsonify(e.messages), 400
	
	@staticmethod
	def update_platform(id):
		platform = Platform.query.get_or_404(id)
		try:
			platform = platform_schema.load(request.json, instance=platform, partial=True)
			db.session.commit()
			return jsonify(platform_schema.dump(platform)), 200
		except ValidationError as e:
			db.session.rollback()
			return jsonify(e.messages), 400
	
	@staticmethod
	def delete_platform(id):
		platform = Platform.query.get_or_404(id)
		db.session.delete(platform)
		db.session.commit()
		return jsonify({'result': True})
	
	@staticmethod
	def get_games():
		games = VideoGame.query.all()
		return jsonify(games_schema.dump(games))
	
	@staticmethod
	def get_game(id):
		game = VideoGame.query.get_or_404(id)
		return jsonify(game_schema.dump(game))
	
	@staticmethod
	def add_game():
		fields = ['name', 'genre_id']
		if not request.json or not all(f in request.json for f in fields):
			abort(400)
		try:
			if 'genre_id' in request.json:
				genre = Genre.query.get(request.json['genre_id'])
				if not genre:
					return jsonify({"error": "Genre not found"}), 400
			game = game_schema.load(request.json, session=db.session)
			db.session.add(game)
			db.session.commit()
			return jsonify(game_schema.dump(game)), 201
		except ValidationError as e:
			return jsonify(e.messages), 400
	
	@staticmethod
	def update_game(id):
		game = VideoGame.query.get_or_404(id)
		try:
			if 'genre_id' in request.json:
				genre = Genre.query.get(request.json['genre_id'])
				if not genre:
					return jsonify({"error": "Genre not found"}), 400
			
			game = game_schema.load(request.json, instance=game, partial=True)
			db.session.commit()
			return jsonify(game_schema.dump(game)), 200
		except ValidationError as e:
			db.session.rollback()
			return jsonify(e.messages), 400
	
	@staticmethod
	def delete_game(id):
		game = VideoGame.query.get_or_404(id)
		db.session.delete(game)
		db.session.commit()
		return jsonify({'result': True})
	
	@staticmethod
	def get_sales():
		sales = SaleGame.query.all()
		return jsonify(sales_schema.dump(sales))
	
	@staticmethod
	def get_sale(id):
		sale = SaleGame.query.get_or_404(id)
		return jsonify(sale_schema.dump(sale))
	
	@staticmethod
	def add_sale():
		fields = ['game_id', 'platform_id', 'published', 'sales']
		if not request.json or not all(f in request.json for f in fields):
			abort(400)
		try:
			if 'game_id' in request.json:
				genre = VideoGame.query.get(request.json['game_id'])
				if not genre:
					return jsonify({"error": "VideoGame not found"}), 400
			if 'platform_id' in request.json:
				genre = Platform.query.get(request.json['platform_id'])
				if not genre:
					return jsonify({"error": "Platform not found"}), 400
			sale = sale_schema.load(request.json)
			db.session.add(sale)
			db.session.commit()
			return jsonify(sale_schema.dump(sale)), 201
		except ValidationError as e:
			return jsonify(e.messages), 400
	
	@staticmethod
	def update_sale(id):
		sale = SaleGame.query.get_or_404(id)
		try:
			if 'game_id' in request.json:
				genre = VideoGame.query.get(request.json['game_id'])
				if not genre:
					return jsonify({"error": "VideoGame not found"}), 400
			if 'platform_id' in request.json:
				genre = Platform.query.get(request.json['platform_id'])
				if not genre:
					return jsonify({"error": "Platform not found"}), 400
			
			sale = sale_schema.load(request.json, instance=sale, partial=True)
			db.session.commit()
			return jsonify(sale_schema.dump(sale)), 200
		except ValidationError as e:
			db.session.rollback()
			return jsonify(e.messages), 400
	
	@staticmethod
	def delete_sale(id):
		sale = SaleGame.query.get_or_404(id)
		db.session.delete(sale)
		db.session.commit()
		return jsonify({'result': True})
