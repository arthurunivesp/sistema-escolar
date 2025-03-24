from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "sua_chave_secreta"  # Protege dados da sessão

    # Inicialize o banco de dados
    db.init_app(app)

    # Importar e registrar as rotas
    from .routes import main
    app.register_blueprint(main)

    return app
