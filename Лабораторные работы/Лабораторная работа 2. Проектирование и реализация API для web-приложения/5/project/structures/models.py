


# curl -X GET http://localhost:5000/structures/api/v1/buildings
# curl -u student:dvfu -X GET http://localhost:5000/structures/api/v1/buildings

# curl -X GET http://localhost:5000/structures/api/v1/buildings/1
# curl -u student:dvfu -X GET http://localhost:5000/structures/api/v1/buildings/1

# curl -i -H "Content-Type:application/json" --data "{\"title\":\"Пекинская Башня CITIC\",\"type_building_id\":\"1\", \"city_id\":\"23\", \"year\":\"2018\"}" http://localhost:5000/structures/api/v1/buildings
# curl -u student:dvfu -i -H "Content-Type:application/json" --data "{\"title\":\"Пекинская Башня CITIC\",\"type_building_id\":\"1\", \"city_id\":\"23\", \"year\":\"2018\"}" http://localhost:5000/structures/api/v1/buildings

# curl -i -H "Content-Type:application/json" -X PUT -d "{\"height\":500}" http://localhost:5000/structures/api/v1/buildings/65
# curl -u student:dvfu -i -H "Content-Type:application/json" -X PUT -d "{\"height\":500}" http://localhost:5000/structures/api/v1/buildings/65

# curl -X DELETE http://localhost:5000/structures/api/v1/buildings/65
# curl -u student:dvfu -X DELETE http://localhost:5000/structures/api/v1/buildings/65
