# app.py
from flask import Flask, render_template
from flask_migrate import Migrate
from models import db
from tasks import tasks_bp  # Importando o Blueprint

def create_app():
    app = Flask(__name__)

    # Configurações do banco de dados (exemplo usando SQLite)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar o banco de dados
    db.init_app(app)

    migrate = Migrate(app, db)

    # Registrar o blueprint com um prefixo de URL
    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    @app.route('/')
    def home():
        return render_template('home.html')

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # db.drop_all()  # Isso vai apagar todas as tabelas
        db.create_all()  # Cria as tabelas, se não existirem
    app.run(debug=True)

