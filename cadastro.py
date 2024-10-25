from datetime import datetime
from re import sub
from hashlib import sha512
from ferramentas import valida_cpf, validar_senha, valida_email, consulta_contatos_cadastrados

def cadastrar_pessoa(cur) -> int:
    while True:
        nome_completo_informado = input('Informe o nome completo: ').upper().strip()
        
        if nome_completo_informado:
            data_nascimento = cadastrar_data_nascimento()
            sexo = cadastrar_sexo(cur)
            cur.execute('INSERT INTO pessoa (nome_completo, data_nascimento, id_sexo) VALUES (?, ?, ?)', (nome_completo_informado, data_nascimento, sexo))
            cur.execute('SELECT last_insert_rowid();')
            id_pessoa = cur.fetchone()[0]
            break
    return id_pessoa

def cadastrar_data_nascimento() -> str:
    while True:
        informa_data_nascimento = input('Informe a data de nascimento (Dia/Mês/Ano): ').strip()
        try:
            data_formatada = str(datetime.strptime(informa_data_nascimento, '%d/%m/%Y').date())
            break
        except ValueError:
            print("Data inválida. Por favor, use o formato Dia/Mês/Ano.")
    return data_formatada

def cadastrar_sexo(cur) -> int:
    informar_sexo = input('Informe o sexo: [M] Masculino, [F] Feminino, [O] Outro ').upper().strip()

    cur.execute('SELECT id_sexo, descricao FROM sexo WHERE status = 1;')
    opcoes_sexo = cur.fetchall()

    if informar_sexo == 'M':
        id_sexo = [id for id, sexo in opcoes_sexo if sexo == 'MASCULINO']
    elif informar_sexo == 'F':
        id_sexo = [id for id, sexo in opcoes_sexo if sexo == 'FEMININO']
    elif informar_sexo == 'O':
        id_sexo = [id for id, sexo in opcoes_sexo if sexo == 'OUTRO']
    else:
        id_sexo = [id for id, sexo in opcoes_sexo if sexo == 'NÃO INFORMADO']
    
    return id_sexo[0]

def cadastrar_cpf(cur, id_pessoa):
    while True:  
        cpf_informado = sub(r'\D', '', input('Informe o CPF: '))
        if valida_cpf(cpf_informado):

            cur.execute("SELECT EXISTS (SELECT 1 FROM documento WHERE documento = ? and status = 1);", (cpf_informado,))
            cpf_existe_na_base = cur.fetchone()[0]
            if cpf_existe_na_base:
                print('CPF já cadastrado.')
            else:
                cur.execute("SELECT id_tipo_documento FROM tipo_documento WHERE status = 1 AND descricao = 'CPF';")
                id_tipo_documento = cur.fetchone()[0]
                cur.execute('INSERT INTO documento (id_pessoa, id_tipo_documento, documento) VALUES (?, ?, ?)', (id_pessoa, id_tipo_documento, cpf_informado))
                break
        else:
            print('CPF inválido. Por favor, informe um CPF válido.')

def cadastrar_telefone(cur, id_pessoa):
    while True:
        telefone_informado = sub(r'\D', '', input('Informe o telefone: '))
        if 8 <= len(telefone_informado) <= 15:

            contatos_cadastrados = consulta_contatos_cadastrados(cur, 'TELEFONE')
            lista_contatos_cadastrados = contatos_cadastrados[0]
            id_tipo_contato = contatos_cadastrados[1]

            if (id_pessoa, telefone_informado) in lista_contatos_cadastrados:
                print('Telefone já cadastrado para essa pessoa.')
            else:
                cur.execute('INSERT INTO contato (id_pessoa, id_tipo_contato, contato) VALUES (?, ?, ?)', (id_pessoa, id_tipo_contato, telefone_informado))
                break
        else:
            print('Telefone inválido. Por favor, informe um telefone válido.')

def cadastrar_email(cur, id_pessoa):
    while True:
        email_informado = input('Informe o email: ').strip()
        if valida_email(email_informado):

            contatos_cadastrados = consulta_contatos_cadastrados(cur, 'EMAIL')
            lista_contatos_cadastrados = contatos_cadastrados[0]
            id_tipo_contato = contatos_cadastrados[1]

            if (id_pessoa, email_informado) in lista_contatos_cadastrados:
                print('Email já cadastrado para essa pessoa.')
            else:
                cur.execute('INSERT INTO contato (id_pessoa, id_tipo_contato, contato) VALUES (?, ?, ?)', (id_pessoa, id_tipo_contato, email_informado))
                break
        else:
            print('Email inválido. Por favor informe um email válido.')

def cadastrar_senha() -> str:
    while True:
        texto_informativo_senha = 'A senha deve ter pelo menos 10 caracteres e conter pelo menos uma letra maiúscula, uma letra minúscula, um número e um caractere especial.'
        print(texto_informativo_senha)
        senha_informada = input("Digite a senha: ")
    
        if validar_senha(senha_informada):
            senha = sha512(senha_informada.encode('utf-8')).hexdigest()
            break
        else:
            print(f"Senha inválida. {texto_informativo_senha}")

    return senha

def cadastrar_usuario(cur, id_pessoa):
    while True:
        usuario_informado = input('Informe o usuário: ').strip()
        if usuario_informado:

            cur.execute("SELECT EXISTS (SELECT 1 FROM usuario WHERE status = 1 and usuario = ?);", (usuario_informado,))
            usuario_existe_na_base = cur.fetchone()[0]

            if usuario_existe_na_base:
                print('Usuário já cadastrado. Por favor, tente outro usuário.')
            else:
                senha = cadastrar_senha()
                cur.execute('INSERT INTO usuario (id_pessoa, usuario, senha) VALUES (?, ?, ?)', (id_pessoa, usuario_informado, senha))
                break

def finalizar_cadastro(cur, con):
    try:
        id_pessoa = cadastrar_pessoa(cur)
        cadastrar_cpf(cur, id_pessoa)
        cadastrar_telefone(cur, id_pessoa)
        cadastrar_email(cur, id_pessoa)
        cadastrar_usuario(cur, id_pessoa)
        con.commit()
        print('Cadastro Realizado com Sucesso.')
    except Exception as e:
        print(f"Erro ao finalizar cadastro: {str(e)}")
        con.rollback()