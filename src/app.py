from flask import Flask
from src.database import init_db
from src import routes

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'taskflow-secreto'

# Inicializa o banco de dados SQLite na primeira execução.
init_db()

# Registra as rotas do Blueprint no aplicativo principal.
app.register_blueprint(routes.bp)

if __name__ == '__main__':
    app.run(debug=True)
