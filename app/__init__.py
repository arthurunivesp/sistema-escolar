from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importar e registrar as rotas
    from .routes import main
    app.register_blueprint(main)

    return app
