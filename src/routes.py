from flask import Blueprint, render_template, request, redirect, url_for, flash
from src import models

bp = Blueprint('tasks', __name__)


@bp.route('/')
def index():
    tasks = models.get_all_tasks()
    edit_id = request.args.get('edit')
    edit_task = models.get_task(int(edit_id)) if edit_id else None
    return render_template('index.html', tasks=tasks, edit_task=edit_task, status_options=models.STATUS_OPTIONS)


@bp.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    if not title:
        flash('O título da tarefa é obrigatório.', 'error')
        return redirect(url_for('tasks.index'))

    models.create_task(title, description)
    flash('Tarefa criada com sucesso.', 'success')
    return redirect(url_for('tasks.index'))


@bp.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    status = request.form.get('status', models.STATUS_OPTIONS[0])
    if not title:
        flash('O título da tarefa é obrigatório.', 'error')
        return redirect(url_for('tasks.index', edit=task_id))

    models.update_task(task_id, title, description, status)
    flash('Tarefa atualizada com sucesso.', 'success')
    return redirect(url_for('tasks.index'))


@bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    models.delete_task(task_id)
    flash('Tarefa removida com sucesso.', 'success')
    return redirect(url_for('tasks.index'))


@bp.route('/status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    status = request.form.get('status', models.STATUS_OPTIONS[0])
    if status not in models.STATUS_OPTIONS:
        status = models.STATUS_OPTIONS[0]
    models.change_status(task_id, status)
    flash('Status da tarefa atualizado.', 'success')
    return redirect(url_for('tasks.index'))
