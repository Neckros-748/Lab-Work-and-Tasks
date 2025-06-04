from config import app, db


class Genre(db.Model):
	__tablename__ = 'Жанр'
	identifier    = db.Column('ID',       db.Integer, primary_key=True)
	name          = db.Column('Название', db.String(50), nullable=False)
	games         = db.relationship('VideoGame', cascade="all, delete")
	
	def __init__(self, name):
		self.name = name
	
	def __repr__(self):
		return f'ID: {self.identifier}, Название: {self.name}\n'
class Platform(db.Model):
	__tablename__ = 'Платформа'
	identifier    = db.Column('ID',       db.Integer, primary_key=True)
	name          = db.Column('Название', db.String(50), nullable=False)
	sales         = db.relationship('SaleGame', cascade="all, delete")
	
	def __init__(self, name):
		self.name = name
	
	def __repr__(self):
		return f'ID: {self.identifier}, Название: {self.name}\n'


class VideoGame(db.Model):
	__tablename__ = 'Игра'
	identifier    = db.Column('ID',       db.Integer, primary_key=True)
	name          = db.Column('Название', db.String(100), nullable=False)
	genre_id      = db.Column('Жанр',     db.Integer, db.ForeignKey('Жанр.ID'))
	genre_rel     = db.relationship("Genre",    back_populates="games")
	sales         = db.relationship('SaleGame', cascade="all, delete")
	
	def __init__(self, name, genre_id):
		self.name     = name
		self.genre_id = genre_id
	
	def __repr__(self):
		return f'ID: {self.identifier}, Название: {self.name}, Жанр (ID): {self.genre_id}\n'


class SaleGame(db.Model):
	__tablename__ = 'Продажи игры'
	identifier    = db.Column('ID',             db.Integer, primary_key=True)
	game_id       = db.Column('Игра',           db.Integer, db.ForeignKey('Игра.ID'))
	platform_id   = db.Column('Платформа',      db.Integer, db.ForeignKey('Платформа.ID'))
	published     = db.Column('Год публикации', db.Integer, nullable=True)
	sales         = db.Column('Общие продажи',  db.Float, nullable=False)
	game_rel      = db.relationship("VideoGame", back_populates="sales")
	platform_rel  = db.relationship("Platform",  back_populates="sales")

	def __init__(self, game_id, platform_id, published, sales):
		self.game_id     = game_id
		self.platform_id = platform_id
		self.published   = published
		self.sales       = sales

	def __repr__(self):
		return f'ID: {self.identifier}, Игра (ID): {self.game_id}, Платформа (ID): {self.platform_id}, Дата: {self.datePublished}, Продажи: {self.globalSales}\n'


# Создание базы данных
app.app_context().push()

with app.app_context():
	db.create_all()
