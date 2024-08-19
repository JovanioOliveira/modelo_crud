from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import csv
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    chave = db.Column(db.String(200), nullable=False)  # Nova coluna adicionada
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

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def home_redirect():
    return redirect(url_for('home'))

@app.route('/index')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/export')
def export():
    tasks = Task.query.all()
    with open('tasks.csv', 'w', newline='') as csvfile:
        fieldnames = ['id','team', 'ca20', 'ca50', 'ca100', 'ca200', 'total', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for task in tasks:
            writer.writerow({
                'id': task.id,
                'team': task.team,
                'ca20': task.ca20,
                'ca50': task.ca50,
                'ca100': task.ca100,
                'ca200': task.ca200,
                'total': task.total,
                'date': task.date
            })

    return send_file('tasks.csv', as_attachment=True)

@app.route('/export_summary')
def export_summary():
    summary = db.session.query(
        Task.date,
        func.sum(Task.ca20).label('total_ca20'),
        func.sum(Task.ca50).label('total_ca50'),
        func.sum(Task.ca100).label('total_ca100'),
        func.sum(Task.ca200).label('total_ca200'),
        func.sum(Task.total).label('total_sum')
    ).group_by(Task.date).all()

    with open('summary.csv', 'w', newline='') as csvfile:
        fieldnames = ['date', 'total_ca20', 'total_ca50', 'total_ca100', 'total_ca200', 'total_sum']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in summary:
            writer.writerow({
                'date': row.date,
                'total_ca20': row.total_ca20,
                'total_ca50': row.total_ca50,
                'total_ca100': row.total_ca100,
                'total_ca200': row.total_ca200,
                'total_sum': row.total_sum
            })

    return send_file('summary.csv', as_attachment=True)

@app.route('/download_summary')
def download_summary():
    return send_file('summary.csv', as_attachment=True)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        date = request.form['date']
        tipo = request.form['tipo']
        uf = request.form['uf']
        gra = request.form['gra']
        loc = request.form['loc']
        estacao = request.form['estacao']
        ard = request.form['ard']
        chave = f"{uf}-{loc}-{estacao}-{ard}"  # Gerando o valor da coluna CHAVE
        team = request.form['team']
        dc = request.form['dc']
        status = request.form['status']
        ca20 = int(request.form['ca20'])
        ca50 = int(request.form['ca50'])
        ca100 = int(request.form['ca100'])
        ca200 = int(request.form['ca200'])
        total = ca20 + ca50 + ca100 + ca200
        new_task = Task(date=date, tipo=tipo, chave=chave, uf=uf, gra=gra, loc=loc, estacao=estacao, ard=ard,
                        team=team, dc=dc, status=status, ca20=ca20, ca50=ca50, ca100=ca100, ca200=ca200, total=total)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/add_more')
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.date = request.form['date']
        task.tipo = request.form['tipo']
        task.uf = request.form['uf']
        task.gra = request.form['gra']
        task.loc = request.form['loc']
        task.estacao = request.form['estacao']
        task.ard = request.form['ard']
        task.chave = f"{task.uf}-{task.loc}-{task.estacao}-{task.ard}"  # Atualizando o valor da coluna CHAVE
        task.team = request.form['team']
        task.dc = request.form['dc']
        task.status = request.form['status']
        task.ca20 = int(request.form['ca20'])
        task.ca50 = int(request.form['ca50'])
        task.ca100 = int(request.form['ca100'])
        task.ca200 = int(request.form['ca200'])
        task.total = task.ca20 + task.ca50 + task.ca100 + task.ca200
        db.session.commit()
        return redirect('/')
    return render_template('update.html', task=task)


@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/add_more')
def add_more():
    return render_template('add_more.html')

if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()  # Isso vai apagar todas as tabelas
        db.create_all()  # Isso vai recriar todas as tabelas com as novas colunas
    app.run(debug=True)

