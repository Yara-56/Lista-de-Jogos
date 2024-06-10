from jogoteca import app, db  # Importa a aplicação Flask e o banco de dados
from flask import render_template, request, redirect, session, flash, url_for  # Importa funções do Flask
from models import Usuarios  # Importa o modelo de Usuários
from helpers import FormularioUsuario  # Importa o formulário de Usuário
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash  # Importa funções para lidar com hash de senhas

bcrypt = Bcrypt(app)  # Inicializa o Bcrypt com a aplicação Flask

@app.route('/login')
def login():
    proxima = request.args.get('proxima')  # Obtém a próxima página a ser acessada após o login
    form = FormularioUsuario()  # Cria uma instância do formulário de usuário
    return render_template('login.html', proxima=proxima, form=form)  # Renderiza a página de login

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)  # Obtém os dados do formulário de usuário

    if not form.validate():  # Verifica se o formulário é válido
        flash('Erro no formulário. Verifique os dados fornecidos.')  # Mostra uma mensagem de erro
        return redirect(url_for('login'))  # Redireciona de volta para a página de login

    nickname = form.nickname.data  # Obtém o nickname do usuário
    print(f"Nickname fornecido: {nickname}")

    usuario = Usuarios.query.filter_by(nickname=nickname).first()  # Consulta o usuário pelo nickname

    if usuario is None:
        flash('Usuário não encontrado.')  # Mostra uma mensagem se o usuário não foi encontrado
        print('Usuário não encontrado no banco de dados.')
        return redirect(url_for('login'))  # Redireciona de volta para a página de login

    print(f"Usuário encontrado: {usuario.nickname}")
    print(f"Hash armazenado: {usuario.senha}")
    print(f"Senha fornecida: {form.senha.data}")

    try:
        if usuario.senha.startswith('$2b$'):  # Verifica se a senha armazenada é um hash bcrypt válido
            if check_password_hash(usuario.senha, form.senha.data):  # Verifica a senha
                session['usuario_logado'] = usuario.nickname  # Define o usuário como logado na sessão
                flash(usuario.nickname + ' logado com sucesso!')  # Mostra uma mensagem de sucesso
                proxima_pagina = request.form.get('proxima', url_for('index'))  # Obtém a próxima página
                return redirect(proxima_pagina)  # Redireciona para a próxima página
            else:
                flash('Senha incorreta.')  # Mostra uma mensagem se a senha estiver incorreta
                return redirect(url_for('login'))  # Redireciona de volta para a página de login
        else:
            if usuario.senha == form.senha.data:  # Se a senha não é um hash bcrypt, verifica como texto puro
                usuario.senha = generate_password_hash(form.senha.data).decode('utf-8')  # Atualiza a senha com um hash bcrypt
                db.session.commit()  # Commit da atualização
                session['usuario_logado'] = usuario.nickname  # Define o usuário como logado na sessão
                flash(usuario.nickname + ' logado com sucesso e senha atualizada!')  # Mostra uma mensagem de sucesso
                proxima_pagina = request.form.get('proxima', url_for('index'))  # Obtém a próxima página
                return redirect(proxima_pagina)  # Redireciona para a próxima página
            else:
                flash('Senha incorreta.')  # Mostra uma mensagem se a senha estiver incorreta
                return redirect(url_for('login'))  # Redireciona de volta para a página de login
    except ValueError as e:
        flash(f"Erro ao verificar a senha: {str(e)}")  # Mostra uma mensagem se houver um erro
        return redirect(url_for('login'))  # Redireciona de volta para a página de login

@app.route('/logout')
def logout():
    session['usuario_logado'] = None  # Define o usuário como deslogado na sessão
    flash('Logout efetuado com sucesso!')  # Mostra uma mensagem de sucesso
    return redirect(url_for('index'))  # Redireciona para a página principal

