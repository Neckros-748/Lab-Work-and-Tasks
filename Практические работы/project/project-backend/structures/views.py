from config import app, db
from flask  import jsonify, render_template
from models import Genre, Platform, VideoGame, SaleGame

import structures.models as mdl


@app.route('/')
def index():
	genres    = mdl.Request.get_genres()
	platforms = mdl.Request.get_platforms()
	games     = mdl.Request.get_games()
	sales     = mdl.Request.get_sales()
	
	# Запросы для отображения
	query1 = mdl.Request.get_query_1()
	query2 = mdl.Request.get_query_2()
	query3 = mdl.Request.get_query_3()
	query4 = mdl.Request.get_query_4()
	query5 = mdl.Request.get_query_5()
	
	html = render_template(
		'index.html',
		genres=   genres,
		platforms=platforms,
		games=    games,
		sales=    sales,
		
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
	return mdl.API.get_genres()


@app.route('/api/genres/<int:id>', methods=['GET'])
def get_genre(id):
	return mdl.API.get_genre(id)


@app.route('/api/genres', methods=['POST'])
def add_genre():
	return mdl.API.add_genre()


@app.route('/api/genres/<int:id>', methods=['PUT'])
def update_genre(id):
	return mdl.API.update_genre(id)


@app.route('/api/genres/<int:id>', methods=['DELETE'])
def delete_genre(id):
	return mdl.API.delete_genre(id)


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
	return mdl.API.get_platforms()


@app.route('/api/platforms/<int:id>', methods=['GET'])
def get_platform(id):
	return mdl.API.get_platform(id)


@app.route('/api/platforms', methods=['POST'])
def add_platform():
	return mdl.API.add_platform()


@app.route('/api/platforms/<int:id>', methods=['PUT'])
def update_platform(id):
	return mdl.API.update_platform(id)


@app.route('/api/platforms/<int:id>', methods=['DELETE'])
def delete_platform(id):
	return mdl.API.delete_platform(id)


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
	return mdl.API.get_games()


@app.route('/api/games/<int:id>', methods=['GET'])
def get_game(id):
	return mdl.API.get_game(id)


@app.route('/api/games', methods=['POST'])
def add_game():
	return mdl.API.add_game()


@app.route('/api/games/<int:id>', methods=['PUT'])
def update_game(id):
	return mdl.API.update_game(id)


@app.route('/api/games/<int:id>', methods=['DELETE'])
def delete_game(id):
	return mdl.API.delete_game(id)


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
	return mdl.API.get_sales()


@app.route('/api/sales/<int:id>', methods=['GET'])
def get_sale(id):
	return mdl.API.get_sale(id)


@app.route('/api/sales', methods=['POST'])
def add_sale():
	return mdl.API.add_sale()


@app.route('/api/sales/<int:id>', methods=['PUT'])
def update_sale(id):
	return mdl.API.update_sale(id)


@app.route('/api/sales/<int:id>', methods=['DELETE'])
def delete_sale(id):
	return mdl.API.delete_sale(id)


# ================================================================================
# Максимальное, минимальное, среднее значение по группированным данным
#
# curl -X GET http://127.0.0.1:5000/api/analytics/genre_stats
# curl -X GET http://127.0.0.1:5000/api/analytics/platform_stats
# curl -X GET http://127.0.0.1:5000/api/analytics/year_stats
# curl -X GET http://127.0.0.1:5000/api/analytics/top_games/5
# ================================================================================

@app.route('/api/analytics/genre_stats', methods=['GET'])
def genre_stats():
	stats = (
		db.session.query(
			Genre.name.label('genre'),
			db.func.sum(SaleGame.sales).label('total_sales'),
			db.func.max(SaleGame.sales).label('max_sales'),
			db.func.min(SaleGame.sales).label('min_sales'),
			db.func.avg(SaleGame.sales).label('avg_sales')
		)
		.join(VideoGame, VideoGame.genre_id == Genre.identifier)
		.join(SaleGame,  SaleGame.game_id == VideoGame.identifier)
		.group_by(Genre.name)
		.all()
	)
	return jsonify([{
		'group':           r[0],
		'analytics': {
			'total_sales': r[1],
			'max_sales':   r[2],
			'min_sales':   r[3],
			'avg_sales':   r[4],
		}
	} for r in stats])


@app.route('/api/analytics/platform_stats', methods=['GET'])
def platform_stats():
	stats = (
		db.session.query(
			Platform.name.label('platform'),
			db.func.sum(SaleGame.sales).label('total_sales'),
			db.func.max(SaleGame.sales).label('max_sales'),
			db.func.min(SaleGame.sales).label('min_sales'),
			db.func.avg(SaleGame.sales).label('avg_sales')
		)
		.join(SaleGame, SaleGame.platform_id == Platform.identifier)
		.group_by(Platform.name)
		.all()
	)
	return jsonify([{
		'group':           r[0],
		'analytics': {
			'total_sales': r[1],
			'max_sales':   r[2],
			'min_sales':   r[3],
			'avg_sales':   r[4],
		}
	} for r in stats])


@app.route('/api/analytics/year_stats', methods=['GET'])
def year_stats():
	stats = (
		db.session.query(
			SaleGame.published.label('year'),
			db.func.sum(SaleGame.sales).label('total_sales'),
			db.func.max(SaleGame.sales).label('max_sales'),
			db.func.min(SaleGame.sales).label('min_sales'),
			db.func.avg(SaleGame.sales).label('avg_sales')
		)
		.filter(SaleGame.published.isnot(None))
		.group_by(SaleGame.published)
		.order_by(SaleGame.published)
		.all()
	)
	return jsonify([{
		'group':           str(r[0]),
		'analytics': {
			'total_sales': r[1],
			'max_sales':   r[2],
			'min_sales':   r[3],
			'avg_sales':   r[4],
		}
	} for r in stats])


@app.route('/api/analytics/top_games/<int:limit>', methods=['GET'])
def top_games(limit):
	results = (
		db.session.query(
			VideoGame.name,
			VideoGame.identifier,
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
		'game':        r[0],
		'id':          r[1],
		'genre':       r[2],
		'total_sales': r[3]
	} for r in results])
