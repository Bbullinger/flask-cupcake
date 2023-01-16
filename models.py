"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from secret import my_password


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///baked_goods"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = my_password
    return app


def connect_db(app):
    db = SQLAlchemy(app)
    db.app = app
    db.init_app(app)

    with app.app_context():
        db.create_all()
        return db


app = create_app()
db = connect_db(app)


class Cupcake(db.Model):
    """Cupcake"""

    __tablename__ = "cupcakes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image_url = db.Column(
        db.Text, nullable=False, default="https://tinyurl.com/demo-cupcake"
    )


# take info from Cupcake model and serialize so it can be jsonified
#######Could this also work on a class method?########


def serialize_cupcake(self):
    return {
        "id": self.id,
        "flavor": self.flavor,
        "size": self.size,
        "rating": self.rating,
        "image_url": self.image_url,
    }
