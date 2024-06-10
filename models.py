from jogoteca import db

from jogoteca import db  # Importa o banco de dados da aplicação jogoteca

# Define a tabela 'Jogos' no banco de dados
class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Coluna 'id' é chave primária e auto-incrementada
    nome = db.Column(db.String(50), nullable=False)  # Coluna 'nome' com máximo de 50 caracteres, não pode ser nula
    categoria = db.Column(db.String(40), nullable=False)  # Coluna 'categoria' com máximo de 40 caracteres, não pode ser nula
    console = db.Column(db.String(20), nullable=False)  # Coluna 'console' com máximo de 20 caracteres, não pode ser nula

    # Representação do objeto como string para fins de depuração
    def __repr__(self):
        return '<Name %r>' % self.nome

# Define a tabela 'Usuarios' no banco de dados
class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)  # Coluna 'nickname' é chave primária, máximo de 8 caracteres
    nome = db.Column(db.String(20), nullable=False)  # Coluna 'nome' com máximo de 20 caracteres, não pode ser nula
    senha = db.Column(db.String(100), nullable=False)  # Coluna 'senha' com máximo de 100 caracteres, não pode ser nula

    # Representação do objeto como string para fins de depuração
    def __repr__(self):
        return '<Name %r>' % self.nome
