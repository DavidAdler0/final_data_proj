from flask import Flask
from blueprints.map import map_bp
from blueprints.analysis import analysis_bp
from services.data_service import init_first_data, init_second_data
from db import db



def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:1234@localhost:5433/final_data_proj'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config["DEBUG"] = True


    db.init_app(app)
    app.register_blueprint(analysis_bp, url_prefix='/analysis')
    app.register_blueprint(map_bp, url_prefix='/map')
    return app


def init_db(app):
    try:
        with app.app_context():
            db.drop_all()
            print("droped all tables")
            db.create_all()
            print("Tables created successfully")
            init_first_data()
            print("initalized first csv")
            init_second_data()
            print("initalized second csv")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise
    return app

if __name__ == '__main__':

    app = create_app()
    # app = init_db(app)
    app.run()