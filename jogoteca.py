from flask import Flask  # Importa a classe Flask para criar a aplicação
from flask_sqlalchemy import SQLAlchemy  # Importa SQLAlchemy para gerenciamento do banco de dados
from flask_wtf.csrf import CSRFProtect  # Importa CSRFProtect para proteger contra CSRF
from flask_bcrypt import Bcrypt  # Importa Bcrypt para hash de senhas

# Cria a aplicação Flask
app = Flask(__name__)
# Carrega as configurações da aplicação a partir do arquivo config.py
app.config.from_pyfile('config.py')

# Inicializa o banco de dados com a aplicação Flask
db = SQLAlchemy(app)
# Inicializa a proteção CSRF com a aplicação Flask
csrf = CSRFProtect(app)
# Inicializa o Bcrypt com a aplicação Flask para hash de senhas
bcrypt = Bcrypt(app)

# Importa as views dos jogos e dos usuários
from views_game import *
from views_user import *

# Executa a aplicação em modo de depuração se este script for executado diretamente
if __name__ == '__main__':
    app.run(debug=True)
