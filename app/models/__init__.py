import os
from flask import Flask, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.routes.auth_routes import auth_bp
from app.routes.cost_report_routes import cost_bp
from app.api import api_bp

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "devkey")
    database_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    if not database_url:
        raise ValueError("[ERROR] DATABASE_URL no configurada.")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(cost_bp)
    app.register_blueprint(api_bp, url_prefix="/api")  # prefijo opcional

    # Ruta principal
    @app.route("/")
    def home():
        if session.get("autenticado") and session.get("es_admin"):
            return redirect(url_for("cost_report.procesar_costos"))
        return redirect(url_for("auth.verificar_pin"))

    # Log en vez de print
    app.logger.info(f"Base de datos conectada: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    return app

