from app import app, auth
from flask import Flask, request, jsonify, abort, make_response
from config import db
from models import Country, City, Building, TypeBuilding
from sqlalchemy import func
from structures.serializers import buildings_cschema, building_cschema


# Вспомогательная функция для сериализации
# def serialize_building(building):
# 	if not building:
# 		return None
#
# 	result = {
# 		"id": building.id,
# 		"title": building.title,
# 		"year": building.year,
# 		"height": building.height,
# 		"type": {
# 			"id": building.type_building.id if building.type_building else None,
# 			"name": building.type_building.name if building.type_building else None
# 		},
# 		"location": {
# 			"city": {
# 				"id": building.city.id if building.city else None,
# 				"name": building.city.name if building.city else None
# 			},
# 			"country": {
# 				"id": building.city.country.id if building.city and building.city.country else None,
# 				"name": building.city.country.name if building.city and building.city.country else None
# 			}
# 		}
# 	}
# 	return result


@app.errorhandler(400)
def missing_fields(error):
	return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


# curl -X GET http://localhost:5000/structures/api/v1/buildings
# curl -u student:dvfu -X GET http://localhost:5000/structures/api/v1/buildings
@app.route('/structures/api/v1/buildings', methods=['GET'])
@auth.login_required
def get_buildings():
	buildings = Building.query.all()
	return jsonify({"buildings": buildings_cschema.dump(buildings)})
	# return jsonify({"buildings": [serialize_building(b) for b in buildings]})


# curl -X GET http://localhost:5000/structures/api/v1/buildings/1
# curl -u student:dvfu -X GET http://localhost:5000/structures/api/v1/buildings/1
@app.route('/structures/api/v1/buildings/<int:building_id>', methods=['GET'])
@auth.login_required
def get_building(building_id):
	building = Building.query.filter(Building.id == building_id).one_or_none()
	if building is None:
		abort(404)
	return jsonify({"building": buildings_cschema.dump(building, many=False)})
	# return jsonify({"building": serialize_building(building)})


# curl -i -H "Content-Type:application/json" --data "{\"title\":\"Пекинская Башня CITIC\",\"type_building_id\":\"1\", \"city_id\":\"23\", \"year\":\"2018\"}" http://localhost:5000/structures/api/v1/buildings
# curl -u student:dvfu -i -H "Content-Type:application/json" --data "{\"title\":\"Пекинская Башня CITIC\",\"type_building_id\":\"1\", \"city_id\":\"23\", \"year\":\"2018\"}" http://localhost:5000/structures/api/v1/buildings
@app.route('/structures/api/v1/buildings', methods=['POST'])
@auth.login_required
def create_building():
	required_fields = ['title', 'type_building_id', 'city_id']  # , 'year', 'height'
	if not request.json or not all(field in request.get_json() for field in required_fields):
		abort(400)
	
	data = request.get_json()
	if 'height' not in request.json:
		data['height'] = 0
	if 'year' not in request.json:
		data['year'] = 2000
	try:
		building = building_cschema.load(data, session=db.session)
		db.session.add(building)
		db.session.commit()
		
		return jsonify({'building': building_cschema.dump(building)}), 201
		# return jsonify({'building': serialize_building(new_building)}), 201
	except Exception as e:
		db.session.rollback()
		return jsonify({"error": str(e)})


# curl -i -H "Content-Type:application/json" -X PUT -d "{\"height\":500}" http://localhost:5000/structures/api/v1/buildings/65
# curl -u student:dvfu -i -H "Content-Type:application/json" -X PUT -d "{\"height\":500}" http://localhost:5000/structures/api/v1/buildings/65
@app.route('/structures/api/v1/buildings/<int:building_id>', methods=['PUT'])
@auth.login_required
def update_building(building_id):
	building = Building.query.filter(Building.id == building_id).one_or_none()
	if building is None or not request.json:
		abort(404)
		
	if 'title' in request.json and type(request.json['title']) is not str:
		abort(400)
	if 'type_building_id' in request.json and type(request.json['type_building_id']) is not int:
		abort(400)
	if 'city_id' in request.json and type(request.json['city_id']) is not int:
		abort(400)
	if 'year' in request.json and type(request.json['year']) is not int:
		abort(400)
	if 'height' in request.json and type(request.json['height']) is not int:
		abort(400)
	
	data = request.get_json()
	try:
		updated_data = building_cschema.load(data, partial=True, instance=building, session=db.session)
		db.session.commit()

		return jsonify({'building': building_cschema.dump(updated_data)}), 200
	except Exception as e:
		db.session.rollback()
		return jsonify({"error": str(e)})


# curl -X DELETE http://localhost:5000/structures/api/v1/buildings/65
# curl -u student:dvfu -X DELETE http://localhost:5000/structures/api/v1/buildings/65
@app.route('/structures/api/v1/buildings/<int:building_id>', methods=['DELETE'])
@auth.login_required
def delete_building(building_id):
	building = Building.query.filter(Building.id == building_id).one_or_none()
	if building is None:
		abort(404)
	try:
		db.session.delete(building)
		db.session.commit()
		return jsonify({'result': True})
	except Exception as e:
		db.session.rollback()
		return jsonify({"error": str(e)})
