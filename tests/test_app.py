from src import models


def test_index_status_200(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'TaskFlow' in response.data


def test_add_task_requires_title(client):
    response = client.post('/add', data={'title': '', 'description': 'Sem título'})
    assert response.status_code == 302
    follow = client.get(response.headers['Location'])
    assert b'O t\xc3\xadtulo da tarefa \xc3\xa9 obrigat\xc3\xb3rio.' in follow.data


def test_create_task(client):
    response = client.post(
        '/add',
        data={
            'title': 'Nova tarefa',
            'description': 'Descrição da tarefa',
            'priority': models.PRIORITY_OPTIONS[2],
        },
    )
    assert response.status_code == 302

    tasks = models.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == 'Nova tarefa'
    assert tasks[0].description == 'Descrição da tarefa'
    assert tasks[0].status == models.STATUS_OPTIONS[0]
    assert tasks[0].priority == models.PRIORITY_OPTIONS[2]


def test_edit_task(client):
    models.create_task('Tarefa editável', 'Descrição antiga', models.PRIORITY_OPTIONS[0])
    task = models.get_all_tasks()[0]
    response = client.post(
        f'/edit/{task.id}',
        data={
            'title': 'Tarefa editada',
            'description': 'Descrição nova',
            'status': models.STATUS_OPTIONS[1],
            'priority': models.PRIORITY_OPTIONS[2],
        },
    )
    assert response.status_code == 302

    updated = models.get_task(task.id)
    assert updated.title == 'Tarefa editada'
    assert updated.description == 'Descrição nova'
    assert updated.status == models.STATUS_OPTIONS[1]
    assert updated.priority == models.PRIORITY_OPTIONS[2]


def test_delete_task(client):
    models.create_task('Tarefa a excluir', 'Descrição')
    task = models.get_all_tasks()[0]
    response = client.post(f'/delete/{task.id}')
    assert response.status_code == 302

    assert models.get_task(task.id) is None
    assert models.get_all_tasks() == []
