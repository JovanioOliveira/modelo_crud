# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    chave = db.Column(db.String(200), nullable=False)
    uf = db.Column(db.String(50), nullable=False)
    gra = db.Column(db.String(50), nullable=False)
    loc = db.Column(db.String(50), nullable=False)
    estacao = db.Column(db.String(50), nullable=False)
    ard = db.Column(db.String(50), nullable=False)
    team = db.Column(db.String(50), nullable=False)
    dc = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    ca20 = db.Column(db.Integer, nullable=False)
    ca50 = db.Column(db.Integer, nullable=False)
    ca100 = db.Column(db.Integer, nullable=False)
    ca200 = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Task {self.team}>'

