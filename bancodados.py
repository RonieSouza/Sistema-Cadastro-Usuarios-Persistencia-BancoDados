from sqlite3 import connect

def conectar():
    return connect("gestao.db")

def cria_tabelas(cur):
    script_criacao_tabelas = """
    CREATE TABLE IF NOT EXISTS sexo (
        id_sexo INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL UNIQUE,
        data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao DATETIME NULL,
        status INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS tipo_documento (
        id_tipo_documento INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL UNIQUE,
        data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao DATETIME NULL,
        status INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS tipo_contato (
        id_tipo_contato INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL UNIQUE,
        data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao DATETIME NULL,
        status INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS documento (
        id_documento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pessoa INTEGER NOT NULL,
        id_tipo_documento INTEGER NOT NULL,
        documento TEXT NOT NULL,
        data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao DATETIME NULL,
        status INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (id_pessoa) REFERENCES pessoa(id_pessoa),
        FOREIGN KEY (id_tipo_documento) REFERENCES tipo_documento(id_tipo_documento),
        UNIQUE (id_pessoa, id_tipo_documento, documento)
    );

    CREATE TABLE IF NOT EXISTS contato (
        id_contato INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pessoa INTEGER NOT NULL,
        id_tipo_contato INTEGER NOT NULL,
        contato TEXT NOT NULL,
        data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao DATETIME NULL,
        status INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (id_pessoa) REFERENCES pessoa(id_pessoa),
        FOREIGN KEY (id_tipo_contato) REFERENCES tipo_contato(id_tipo_contato),
        UNIQUE (id_pessoa, id_tipo_contato, contato)
    );

    CREATE TABLE IF NOT EXISTS pessoa (
        id_pessoa INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT NOT NULL,
        data_nascimento DATE NOT NULL,
        id_sexo INTEGER NOT NULL,
        data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao DATETIME NULL,
        status INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (id_sexo) REFERENCES sexo(id_sexo)
    );

    CREATE TABLE IF NOT EXISTS usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pessoa INTEGER NOT NULL UNIQUE,
        usuario TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao DATETIME NULL,
        status INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (id_pessoa) REFERENCES pessoa(id_pessoa)
    );

    INSERT OR IGNORE INTO sexo (descricao) VALUES
        ('MASCULINO'),
        ('FEMININO'),
        ('OUTRO'),
        ('NÃO INFORMADO');

    INSERT OR IGNORE INTO tipo_documento (descricao) VALUES
        ('CPF');

    INSERT OR IGNORE INTO tipo_contato (descricao) VALUES
        ('TELEFONE'),
        ('EMAIL');
    """

    cur.executescript(script_criacao_tabelas)