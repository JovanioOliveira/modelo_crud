# tasks.py
from flask import Blueprint, render_template, request, redirect, url_for, send_file
from datetime import datetime
import csv
from sqlalchemy import func
from models import Task, db  # Importando o modelo Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@tasks_bp.route('/export')
def export():
    tasks = Task.query.all()
    with open('tasks.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'team', 'dc', 'ca20', 'ca50', 'ca100', 'ca200', 'total', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            writer.writerow({
                'id': task.id,
                'team': task.team,
                'dc': task.dc,
                'ca20': task.ca20,
                'ca50': task.ca50,
                'ca100': task.ca100,
                'ca200': task.ca200,
                'total': task.total,
                'date': task.date
            })
    return send_file('tasks.csv', as_attachment=True)

@tasks_bp.route('/export_summary')
def export_summary():
    summary = db.session.query(
        Task.dc,
        Task.status,
        func.sum(Task.ca20).label('total_ca20'),
        func.sum(Task.ca50).label('total_ca50'),
        func.sum(Task.ca100).label('total_ca100'),
        func.sum(Task.ca200).label('total_ca200'),
        func.sum(Task.total).label('total_sum')
    ).group_by(Task.dc, Task.status).all()

    with open('summary.csv', 'w', newline='') as csvfile:
        fieldnames = ['dc', 'status', 'total_ca20', 'total_ca50', 'total_ca100', 'total_ca200', 'total_sum']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in summary:
            writer.writerow({
                'dc': row.dc,
                'status': row.status,
                'total_ca20': row.total_ca20,
                'total_ca50': row.total_ca50,
                'total_ca100': row.total_ca100,
                'total_ca200': row.total_ca200,
                'total_sum': row.total_sum
            })

    return send_file('summary.csv', as_attachment=True)

@tasks_bp.route('/save_summary')
def save_summary():
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

    return redirect(url_for('tasks.index'))

@tasks_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        date = request.form['date']
        tipo = request.form['tipo']
        uf = request.form['uf']
        gra = request.form['gra']
        loc = request.form['loc']
        estacao = request.form['estacao']
        ard = request.form['ard']
        chave = f"{uf}-{loc}-{estacao}-{ard}"
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
        
        # Atualiza os arquivos imediatamente após salvar o novo item
        update_tasks_csv()
        update_summary_csv()

        return redirect(url_for('tasks.add_more'))
    return render_template('create.html')

def update_tasks_csv():
    tasks = Task.query.all()
    with open('tasks.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'team', 'ca20', 'ca50', 'ca100', 'ca200', 'total', 'date']
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

def update_summary_csv():
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

@tasks_bp.route('/update/<int:id>', methods=['GET', 'POST'])
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
        
        # Atualiza os arquivos imediatamente após a atualização
        update_tasks_csv()
        update_summary_csv()
        
        return redirect(url_for('tasks.index'))
    
    # Converte a data para o formato datetime se necessário
    if isinstance(task.date, str):
        task.date = datetime.strptime(task.date, '%Y-%m-%d')  # Converte a string para datetime
    
    return render_template('update.html', task=task)

@tasks_bp.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/add_more')
def add_more():
    return render_template('add_more.html')

@tasks_bp.route('/search', methods=['GET', 'POST'])
def search_dc():
    if request.method == 'POST':
        dc_number = request.form['dc']
        
        # Obter as tarefas correspondentes ao DC
        results = Task.query.filter_by(dc=dc_number).all()
        
        # Obter o resumo do DC
        summary = db.session.query(
            Task.dc,
            func.sum(Task.ca20).label('total_ca20'),
            func.sum(Task.ca50).label('total_ca50'),
            func.sum(Task.ca100).label('total_ca100'),
            func.sum(Task.ca200).label('total_ca200'),
            func.sum(Task.total).label('total_sum')
        ).filter(Task.dc == dc_number).group_by(Task.dc).first()
        
        return render_template('pesquisar.html', results=results, summary=summary)
    
    return render_template('pesquisar.html')






