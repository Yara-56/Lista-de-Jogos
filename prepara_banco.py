import mysql.connector  # Importa o módulo mysql.connector para conexão com o banco de dados MySQL
from mysql.connector import errorcode  # Importa códigos de erro específicos do MySQL
from flask_bcrypt import generate_password_hash  # Importa função para gerar hash de senhas

print("Conectando...")
try:
    # Tenta estabelecer uma conexão com o banco de dados
    conn = mysql.connector.connect(
        host='#',  # Endereço do servidor MySQL
        user='#',  # Nome de usuário do MySQL
        password='#'  # Senha do MySQL
    )
except mysql.connector.Error as err:
    # Trata possíveis erros de conexão
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)

cursor = conn.cursor()  # Cria um cursor para executar comandos SQL

# Remove o banco de dados 'jogoteca' se ele existir
cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")

# Cria um novo banco de dados 'jogoteca'
cursor.execute("CREATE DATABASE `jogoteca`;")

# Seleciona o banco de dados 'jogoteca' para uso
cursor.execute("USE `jogoteca`;")

# Definição das tabelas
TABLES = {}
TABLES['Jogos'] = ('''
    CREATE TABLE `jogos` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `nome` varchar(50) NOT NULL,
    `categoria` varchar(40) NOT NULL,
    `console` varchar(20) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
    CREATE TABLE `usuarios` (
    `nome` varchar(20) NOT NULL,
    `nickname` varchar(8) NOT NULL,
    `senha` varchar(100) NOT NULL,
    PRIMARY KEY (`nickname`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

# Criação das tabelas no banco de dados
for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print('Criando tabela {}:'.format(tabela_nome), end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')

# Inserindo usuários na tabela 'usuarios'
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
    ("Bruno Divino", "BD", generate_password_hash("alohomora").decode('utf-8')),
    ("Camila Ferreira", "Mila", generate_password_hash("paozinho").decode('utf-8')),
    ("Guilherme Louro", "Cake", generate_password_hash("python_eh_vida").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

# Seleciona todos os usuários e exibe-os
cursor.execute('SELECT * FROM jogoteca.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# Inserindo jogos na tabela 'jogos'
jogos_sql = 'INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)'
jogos = [
    ('Tetris', 'Puzzle', 'Atari'),
    ('God of War', 'Hack n Slash', 'PS2'),
    ('Mortal Kombat', 'Luta', 'PS2'),
    ('Valorant', 'FPS', 'PC'),
    ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
    ('Need for Speed', 'Corrida', 'PS2'),
]
cursor.executemany(jogos_sql, jogos)

# Seleciona todos os jogos e exibe-os
cursor.execute('SELECT * FROM jogoteca.jogos')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# Comita as mudanças no banco de dados
conn.commit()

# Fecha o cursor e a conexão com o banco de dados
cursor.close()
conn.close()
