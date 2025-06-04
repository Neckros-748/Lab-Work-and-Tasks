from models import Building, TypeBuilding, Country, City
from config import ma, db


class TypeBuildingSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = TypeBuilding


class CountrySchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Country


class CitySchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = City
	country = ma.Nested(CountrySchema())


class BuildingSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model         = Building
		ad_instance   = True
		sqla_session  = db.session
		load_instance = True
	
	type_building    = ma.Nested(TypeBuildingSchema())
	city             = ma.Nested(CitySchema())
	
	type_building_id = ma.auto_field()
	city_id          = ma.auto_field()


building_cschema  = BuildingSchema()
buildings_cschema = BuildingSchema(many=True)
