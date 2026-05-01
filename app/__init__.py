from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()

mongo = PyMongo()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "iocl-dms-dev-secret")
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/iocl_dms")

    mongo.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.dealers import dealers_bp
    from app.routes.inventory import inventory_bp
    from app.routes.orders import orders_bp
    from app.routes.sales import sales_bp
    from app.routes.complaints import complaints_bp
    from app.routes.reports import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(dealers_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(complaints_bp)
    app.register_blueprint(reports_bp)

    return app
