import os  # Importa o módulo os para manipulação de caminhos de arquivos

# Chave secreta para a aplicação Flask, usada para manter os dados da sessão segura
SECRET_KEY = 'alura'

# Configuração da URI do banco de dados SQLAlchemy para conectar a um banco de dados MySQL
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='#',
        senha='#',
        servidor='localhost',
        database='jogoteca'
    )

# Caminho de upload de arquivos, definido como o diretório "uploads" no mesmo local do script atual
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
