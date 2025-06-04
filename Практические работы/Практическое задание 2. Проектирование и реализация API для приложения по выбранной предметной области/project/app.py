from flask import Flask

app = Flask(__name__)
app.json.ensure_ascii = False

if __name__ == '__main__':
    app.run(debug=True)

import structures.views
