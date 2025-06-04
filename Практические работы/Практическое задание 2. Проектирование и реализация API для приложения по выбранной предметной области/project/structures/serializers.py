from config import db, ma
from models import Genre, Platform, VideoGame, SaleGame


class GenreSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Genre
		load_instance = True
	
	_links = ma.Hyperlinks(
		{
			"self":       ma.URLFor("get_genre", values=dict(id="<identifier>")),
			"collection": ma.URLFor("get_genres"),
			# 'update':     ma.URLFor('update_genre', values=dict(id="<identifier>")),
			# 'delete':     ma.URLFor('delete_genre', values=dict(id="<identifier>")),
		}
	)


class PlatformSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Platform
		load_instance = True
	
	_links = ma.Hyperlinks(
		{
			"self":       ma.URLFor("get_platform", values=dict(id="<identifier>")),
			"collection": ma.URLFor("get_platforms"),
			# 'update':     ma.URLFor('update_platform', values=dict(id="<identifier>")),
			# 'delete':     ma.URLFor('delete_platform', values=dict(id="<identifier>")),
		}
	)


class VideoGameSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = VideoGame
		load_instance = True
		sqla_session  = db.session

	genre_rel = ma.Nested(GenreSchema())
	genre_id  = ma.auto_field()
	
	_links = ma.Hyperlinks(
		{
			"self":       ma.URLFor("get_game", values=dict(id="<identifier>")),
			"collection": ma.URLFor("get_games"),
			# 'update':     ma.URLFor('update_game', values=dict(id="<identifier>")),
			# 'delete':     ma.URLFor('delete_game', values=dict(id="<identifier>")),
		}
	)


class SaleGameSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model         = SaleGame
		sqla_session  = db.session
		load_instance = True
		ad_instance   = True

	game_rel     = ma.Nested(VideoGameSchema())
	platform_rel = ma.Nested(PlatformSchema())
	game_id      = ma.auto_field()
	platform_id  = ma.auto_field()
	
	_links = ma.Hyperlinks(
		{
			"self":       ma.URLFor("get_sale", values=dict(id="<identifier>")),
			"collection": ma.URLFor("get_sales"),
			# 'update':     ma.URLFor('update_sale', values=dict(id="<identifier>")),
			# 'delete':     ma.URLFor('delete_sale', values=dict(id="<identifier>")),
		}
	)


genre_schema     = GenreSchema()
genres_schema    = GenreSchema(many=True)
platform_schema  = PlatformSchema()
platforms_schema = PlatformSchema(many=True)
game_schema      = VideoGameSchema()
games_schema     = VideoGameSchema(many=True)
sale_schema      = SaleGameSchema()
sales_schema     = SaleGameSchema(many=True)
