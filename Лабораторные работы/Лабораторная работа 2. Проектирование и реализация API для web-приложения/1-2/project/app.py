from flask import Flask, request, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False


@app.route('/')
def hello_world():
	return jsonify({'app': 'Самые высокие здания и сооружения'})


if __name__ == '__main__':
	app.run(debug=True)

import structures.views
