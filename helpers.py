import os  # Importa o módulo os para manipulação de caminhos de arquivos
from jogoteca import app  # Importa a aplicação Flask
from flask_wtf import FlaskForm  # Importa a classe base para formulários do Flask-WTF
from wtforms import StringField, SubmitField, PasswordField, validators  # Importa os campos e validadores do WTForms

# Define o formulário para jogos
class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')

# Define o formulário para usuários
class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')

# Função para recuperar a imagem associada a um jogo
def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo
    return 'capa_padrao.jpg'

# Função para deletar o arquivo de imagem associado a um jogo
def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
