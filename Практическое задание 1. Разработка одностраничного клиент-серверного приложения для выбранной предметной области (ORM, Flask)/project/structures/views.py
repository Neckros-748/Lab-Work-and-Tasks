from config import app, db
from flask import render_template
from models import Genre, Platform, VideoGame, SaleGame
# from sqlalchemy import distinct, over


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
