from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)

import structures.views
