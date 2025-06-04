from app import app
from flask import Flask, request, jsonify, abort, make_response, render_template, url_for
from config import db
from models import Genre, Platform, VideoGame, SaleGame
# from structures.serializers import buildings_cschema, building_cschema
from sqlalchemy import distinct, over, func
from structures.serializers import (
	genre_schema, genres_schema,
	platform_schema, platforms_schema,
	game_schema, games_schema,
	sale_schema, sales_schema
)
from marshmallow import ValidationError


@app.route('/')
def index():
	# Основные данные из таблиц
	genres = Genre.query.all()
	platforms = Platform.query.all()
	games = VideoGame.query.all()
	sales = SaleGame.query.all()
	
	# Запросы для отображения
	query1 = (
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
	
	query2 = (
		db.session.query(
			Platform.name.label("Платформа"),
			db.func.sum(SaleGame.sales).label('Продажи (млн)')
		)
		.join(SaleGame)
		.group_by(Platform.name)
		.order_by(db.desc('Продажи (млн)'))
		.limit(5)
	)
	
	query3 = (
		db.session.query(
			Genre.name.label("Жанр"),
			db.func.avg(SaleGame.sales).label('Средние продажи (млн)')
		)
		.select_from(Genre)
		.join(VideoGame).join(SaleGame)
		.group_by(Genre.name)
		.order_by(db.desc('Средние продажи (млн)'))
	)
	
	query4 = (
		db.session.query(
			SaleGame.published.label('Год'),
			db.func.sum(SaleGame.sales).label('Продажи (млн)')
		)
		.group_by('Год')
		.order_by('Год')
	)
	
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
	
	query5 = (
		db.session.query(
			subquery.c.Декада,
			subquery.c.Жанр,
			subquery.c['Продажи (млн)']
		)
		.filter(subquery.c.rank <= 3)
		.order_by(subquery.c.Декада, subquery.c.rank)
	)
	
	html = render_template(
		'index.html',
		genres=genres,
		platforms=platforms,
		games=games,
		sales=sales,
		
		query1=[query1.statement.columns.keys(), query1.all()],
		query2=[query2.statement.columns.keys(), query2.all()],
		query3=[query3.statement.columns.keys(), query3.all()],
		query4=[query4.statement.columns.keys(), query4.all()],
		query5=[query5.statement.columns.keys(), query5.all()],
	)
	return html


# ================================================================================
# GENRE
#
# curl -X GET http://127.0.0.1:5000/api/genres
# curl -X GET http://127.0.0.1:5000/api/genres/1
# curl -X POST -H "Content-Type: application/json" -d "{\"name\": \"Test\"}" http://localhost:5000/api/genres
# curl -X PUT -H "Content-Type: application/json" -d "{\"name\": \"Testing\"}" http://localhost:5000/api/genres/13
# curl -X DELETE http://localhost:5000/api/genres/13
# ================================================================================

@app.route('/api/genres', methods=['GET'])
def get_genres():
	genres = Genre.query.all()
	return jsonify(genres_schema.dump(genres))


@app.route('/api/genres/<int:id>', methods=['GET'])
def get_genre(id):
	genre = Genre.query.get_or_404(id)
	return jsonify(genre_schema.dump(genre))


@app.route('/api/genres', methods=['POST'])
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


@app.route('/api/genres/<int:id>', methods=['PUT'])
def update_genre(id):
	genre = Genre.query.get_or_404(id)
	try:
		genre = genre_schema.load(request.json, instance=genre, partial=True)
		db.session.commit()
		return jsonify(genre_schema.dump(genre)), 200
	except ValidationError as e:
		db.session.rollback()
		return jsonify(e.messages), 400


@app.route('/api/genres/<int:id>', methods=['DELETE'])
def delete_genre(id):
	genre = Genre.query.get_or_404(id)
	db.session.delete(genre)
	db.session.commit()
	return jsonify({'result': True})


# ================================================================================
# PLATFORM
#
# curl -X GET http://127.0.0.1:5000/api/platforms
# curl -X GET http://127.0.0.1:5000/api/platforms/1
# curl -X POST -H "Content-Type: application/json" -d "{\"name\": \"Test\"}" http://localhost:5000/api/platforms
# curl -X PUT -H "Content-Type: application/json" -d "{\"name\": \"Testing\"}" http://localhost:5000/api/platforms/26
# curl -X DELETE http://localhost:5000/api/platforms/26
# ================================================================================

@app.route('/api/platforms', methods=['GET'])
def get_platforms():
	platforms = Platform.query.all()
	return jsonify(platforms_schema.dump(platforms))


@app.route('/api/platforms/<int:id>', methods=['GET'])
def get_platform(id):
	platform = Platform.query.get_or_404(id)
	return jsonify(platform_schema.dump(platform))


@app.route('/api/platforms', methods=['POST'])
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


@app.route('/api/platforms/<int:id>', methods=['PUT'])
def update_platform(id):
	platform = Platform.query.get_or_404(id)
	try:
		platform = platform_schema.load(request.json, instance=platform, partial=True)
		db.session.commit()
		return jsonify(platform_schema.dump(platform)), 200
	except ValidationError as e:
		db.session.rollback()
		return jsonify(e.messages), 400


@app.route('/api/platforms/<int:id>', methods=['DELETE'])
def delete_platform(id):
	platform = Platform.query.get_or_404(id)
	db.session.delete(platform)
	db.session.commit()
	return jsonify({'result': True})


# ================================================================================
# VIDEO GAME
#
# curl -X GET http://127.0.0.1:5000/api/games
# curl -X GET http://127.0.0.1:5000/api/games/1
# curl -X POST -H "Content-Type: application/json" -d "{\"name\": \"Test\", \"genre_id\": 1}" http://localhost:5000/api/games
# curl -X PUT -H "Content-Type: application/json" -d "{\"name\": \"Testing\"}" http://localhost:5000/api/games/1568
# curl -X DELETE http://localhost:5000/api/games/1568
# ================================================================================

@app.route('/api/games', methods=['GET'])
def get_games():
	games = VideoGame.query.all()
	return jsonify(games_schema.dump(games))


@app.route('/api/games/<int:id>', methods=['GET'])
def get_game(id):
	game = VideoGame.query.get_or_404(id)
	return jsonify(game_schema.dump(game))


@app.route('/api/games', methods=['POST'])
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


@app.route('/api/games/<int:id>', methods=['PUT'])
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


@app.route('/api/games/<int:id>', methods=['DELETE'])
def delete_game(id):
	game = VideoGame.query.get_or_404(id)
	db.session.delete(game)
	db.session.commit()
	return jsonify({'result': True})


# ================================================================================
# SALE GAME
#
# curl -X GET http://127.0.0.1:5000/api/sales
# curl -X GET http://127.0.0.1:5000/api/sales/1
# curl -X POST -H "Content-Type: application/json" -d "{\"game_id\": 1, \"platform_id\": 1, \"published\": 2020, \"sales\": 2.5}" http://localhost:5000/api/sales
# curl -X PUT -H "Content-Type: application/json" -d "{\"sales\": 5.0}" http://localhost:5000/api/sales/2000
# curl -X DELETE http://localhost:5000/api/sales/2000
# ================================================================================

@app.route('/api/sales', methods=['GET'])
def get_sales():
	sales = SaleGame.query.all()
	return jsonify(sales_schema.dump(sales))


@app.route('/api/sales/<int:id>', methods=['GET'])
def get_sale(id):
	sale = SaleGame.query.get_or_404(id)
	return jsonify(sale_schema.dump(sale))


@app.route('/api/sales', methods=['POST'])
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


@app.route('/api/sales/<int:id>', methods=['PUT'])
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


@app.route('/api/sales/<int:id>', methods=['DELETE'])
def delete_sale(id):
	sale = SaleGame.query.get_or_404(id)
	db.session.delete(sale)
	db.session.commit()
	return jsonify({'result': True})


# ================================================================================
# Максимальное, минимальное, среднее значение по группированным данным
#
# curl -X GET http://127.0.0.1:5000/api/analytics/sales_by_genre
# curl -X GET http://127.0.0.1:5000/api/analytics/sales_by_platform
# curl -X GET http://127.0.0.1:5000/api/analytics/top_games/5
# ================================================================================

@app.route('/api/analytics/sales_by_genre', methods=['GET'])
def sales_by_genre():
	results = (
		db.session.query(
			Genre.name,
			db.func.sum(SaleGame.sales).label('total_sales'),
			db.func.avg(SaleGame.sales).label('avg_sales'),
			db.func.max(SaleGame.sales).label('max_sales'),
			db.func.min(SaleGame.sales).label('min_sales')
		)
		.join(VideoGame, VideoGame.genre_id == Genre.identifier)
		.join(SaleGame, SaleGame.game_id == VideoGame.identifier)
		.group_by(Genre.name)
		.all()
	)
	return jsonify([{
		'genre': r[0],
		'analytics': {
			'total_sales': r[1],
			'avg_sales': r[2],
			'max_sales': r[3],
			'min_sales': r[4]
		}
	} for r in results])


@app.route('/api/analytics/sales_by_platform', methods=['GET'])
def sales_by_platform():
	results = (
		db.session.query(
			Platform.name,
			db.func.sum(SaleGame.sales).label('total_sales'),
			db.func.avg(SaleGame.sales).label('avg_sales'),
			db.func.max(SaleGame.sales).label('max_sales'),
			db.func.min(SaleGame.sales).label('min_sales')
		)
		.join(SaleGame, SaleGame.platform_id == Platform.identifier)
		.group_by(Platform.name)
		.all()
	)
	
	return jsonify([{
		'platform': r[0],
		'analytics': {
			'total_sales': r[1],
			'avg_sales': r[2],
			'max_sales': r[3],
			'min_sales': r[4]
		}
	} for r in results])


@app.route('/api/analytics/top_games/<int:limit>', methods=['GET'])
def top_games(limit):
	results = (
		db.session.query(
			VideoGame.name,
			Genre.name.label('genre'),
			db.func.sum(SaleGame.sales).label('total_sales')
		)
		.join(Genre, VideoGame.genre_id == Genre.identifier)
		.join(SaleGame, SaleGame.game_id == VideoGame.identifier)
		.group_by(VideoGame.name, Genre.name)
		.order_by(db.desc('total_sales'))
		.limit(limit)
		.all()
	)
	
	return jsonify([{
		'game': r[0],
		'genre': r[1],
		'total_sales': r[2]
	} for r in results])
