from flask import render_template, request, redirect, session, flash, url_for, send_from_directory  # Importa funções Flask
from jogoteca import app, db  # Importa a aplicação e o banco de dados
from models import Jogos  # Importa o modelo de Jogos
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo  # Importa funções auxiliares e o formulário de jogos
import time  # Importa a biblioteca time para trabalhar com timestamps

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)  # Consulta todos os jogos ordenados por id
    return render_template('lista.html', titulo='Jogos', jogos=lista)  # Renderiza a página de lista de jogos

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:  # Verifica se o usuário está logado
        return redirect(url_for('login', proxima=url_for('novo')))  # Redireciona para a página de login se não estiver logado
    form = FormularioJogo()  # Cria uma instância do formulário de jogos
    return render_template('novo.html', titulo='Novo Jogo', form=form)  # Renderiza a página de novo jogo

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioJogo(request.form)  # Obtém os dados do formulário

    if not form.validate_on_submit():  # Verifica se o formulário é válido
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    jogo = Jogos.query.filter_by(nome=nome).first()  # Verifica se o jogo já existe

    if jogo:
        flash('Jogo já existente!')  # Mostra uma mensagem se o jogo já existe
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)  # Cria uma nova instância de Jogos
    db.session.add(novo_jogo)  # Adiciona o novo jogo ao banco de dados
    db.session.commit()  # Commit das mudanças

    arquivo = request.files['arquivo']  # Obtém o arquivo enviado
    upload_path = app.config['UPLOAD_PATH']  # Obtém o caminho de upload
    timestamp = time.time()  # Gera um timestamp
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')  # Salva o arquivo com o nome especificado

    return redirect(url_for('index'))  # Redireciona para a página principal

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:  # Verifica se o usuário está logado
        return redirect(url_for('login', proxima=url_for('editar', id=id)))  # Redireciona para a página de login se não estiver logado
    jogo = Jogos.query.filter_by(id=id).first()  # Obtém o jogo pelo id
    form = FormularioJogo()  # Cria uma instância do formulário de jogos
    form.nome.data = jogo.nome  # Preenche o formulário com os dados do jogo
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    capa_jogo = recupera_imagem(id)  # Obtém a imagem do jogo
    return render_template('editar.html', titulo='Editando Jogo', id=id, capa_jogo=capa_jogo, form=form)  # Renderiza a página de edição de jogos

@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioJogo(request.form)  # Obtém os dados do formulário

    if form.validate_on_submit():  # Verifica se o formulário é válido
        jogo = Jogos.query.filter_by(id=request.form['id']).first()  # Obtém o jogo pelo id
        jogo.nome = form.nome.data  # Atualiza os dados do jogo
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add(jogo)  # Adiciona as mudanças ao banco de dados
        db.session.commit()  # Commit das mudanças

        arquivo = request.files['arquivo']  # Obtém o arquivo enviado
        upload_path = app.config['UPLOAD_PATH']  # Obtém o caminho de upload
        timestamp = time.time()  # Gera um timestamp
        deleta_arquivo(request.form['id'])  # Deleta o arquivo antigo
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')  # Salva o novo arquivo

    return redirect(url_for('index'))  # Redireciona para a página principal

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:  # Verifica se o usuário está logado
        return redirect(url_for('login'))  # Redireciona para a página de login se não estiver logado

    Jogos.query.filter_by(id=id).delete()  # Deleta o jogo pelo id
    db.session.commit()  # Commit das mudanças
    flash('Jogo deletado com sucesso!')  # Mostra uma mensagem de sucesso

    return redirect(url_for('index'))  # Redireciona para a página principal

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)  # Envia o arquivo da pasta de uploads
