from flask_sqlalchemy  import SQLAlchemy
from flask_marshmallow import Marshmallow
from app               import app

# Создаем расширение для работы с базой данных
db = SQLAlchemy()
ma = Marshmallow(app)

# Конфигурация базы данных SQLite
app.config["SQLALCHEMY_DATABASE_URI"]        = "sqlite:///instance/structure.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Инициализация приложения с расширением
db.init_app(app)
