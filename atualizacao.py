from datetime import datetime
from ferramentas import valida_cpf, valida_email, validar_senha
from re import sub
from getpass import getpass
from hashlib import sha512

def atualizar_nome_completo(cur, id_pessoa):
    novo_nome = input('Informe o novo nome completo (ou deixe vazio para não alterar): ').upper().strip()
    if novo_nome:
        cur.execute('UPDATE pessoa SET nome_completo = ?, data_atualizacao = CURRENT_TIMESTAMP WHERE id_pessoa = ?', (novo_nome, id_pessoa))

def atualizar_data_nascimento(cur, id_pessoa):
    while True:
        nova_data_nascimento = input('Informe a nova data de nascimento (ou deixe vazio para não alterar): ').strip()
        if nova_data_nascimento:
            try:
                data_formatada = str(datetime.strptime(nova_data_nascimento, '%d/%m/%Y').date())
                cur.execute('UPDATE pessoa SET data_nascimento = ?, data_atualizacao = CURRENT_TIMESTAMP WHERE id_pessoa = ?', (data_formatada, id_pessoa))
                break
            except ValueError:
                print("Data inválida. Por favor, use o formato Dia/Mês/Ano.")
        else:
            break

def atualizar_sexo(cur, id_pessoa):
    while True:
        novo_sexo = input('Informe o novo sexo [M] Masculino, [F] Feminino, [O] Outro (ou deixe vazio para não alterar): ').upper().strip()
        if novo_sexo:
            if novo_sexo in ['M', 'F', 'O']:
                sexo_dict = {'M': 'MASCULINO', 'F': 'FEMININO', 'O': 'OUTRO'}
                cur.execute('SELECT id_sexo FROM sexo WHERE descricao = ?;', (sexo_dict[novo_sexo],))
                id_sexo = cur.fetchone()
                if id_sexo:
                    cur.execute('UPDATE pessoa SET id_sexo = ?, data_atualizacao = CURRENT_TIMESTAMP WHERE id_pessoa = ?', (id_sexo[0], id_pessoa))
                    break
                else:
                    print("Sexo inválido.")
            else:
                print("Escolha uma opção válida.")
        else:
            break

def atualizar_cpf(cur, id_pessoa):
    while True:
        novo_cpf = input('Informe o novo CPF (ou deixe vazio para não alterar): ').strip()
        if novo_cpf:
            if valida_cpf(novo_cpf):
                cur.execute("SELECT EXISTS (SELECT 1 FROM documento WHERE documento = ?);", (novo_cpf, ))
                cpf_existe_na_base = cur.fetchone()[0]
                if cpf_existe_na_base:
                    print('CPF já cadastrado.')
                else:
                    cur.execute('UPDATE documento SET documento = ?, data_atualizacao = CURRENT_TIMESTAMP WHERE id_pessoa = ? AND id_tipo_documento = (SELECT id_tipo_documento FROM tipo_documento WHERE descricao = ?);', (novo_cpf, id_pessoa, 'CPF'))
                    break
            else:
                print('CPF inválido. Por favor, informe um CPF válido.')
        else:
            break

def atualizar_email(cur, id_pessoa):
    while True:
        novo_email = input('Informe o novo email (ou deixe vazio para não alterar): ').strip()
        if novo_email:
            if valida_email(novo_email):
                cur.execute('UPDATE contato SET contato = ?, data_atualizacao = CURRENT_TIMESTAMP WHERE id_pessoa = ? AND id_tipo_contato = (SELECT id_tipo_contato FROM tipo_contato WHERE descricao = ?);', (novo_email, id_pessoa, 'EMAIL'))
                break
            else:
                print('Email inválido. Por favor informe um email válido.')
        else:
            break

def atualizar_telefone(cur, id_pessoa):
    while True:
        novo_telefone = sub(r'\D', '', input('Informe o novo telefone (ou deixe vazio para não alterar): '))
        if novo_telefone:
            if 8 <= len(novo_telefone) <= 15:
                cur.execute('UPDATE contato SET contato = ?, data_atualizacao = CURRENT_TIMESTAMP WHERE id_pessoa = ? AND id_tipo_contato = (SELECT id_tipo_contato FROM tipo_contato WHERE descricao = ?);', (novo_telefone, id_pessoa, 'TELEFONE'))
                break
            else:
                print('Telefone inválido. Por favor, informe um telefone válido.')
        else:
            break

def atualizar_usuario(cur, id_pessoa):
    while True:
        novo_usuario = input('Informe o novo usuário (ou deixe vazio para não alterar): ').strip()
        if novo_usuario:
            cur.execute("SELECT EXISTS (SELECT 1 FROM usuario WHERE usuario = ?);", (novo_usuario, ))
            usuario_existe_na_base = cur.fetchone()[0]
            if usuario_existe_na_base:
                print('Usuário já cadastrado. Por favor, tente outro usuário.')
            else:
                cur.execute('UPDATE usuario SET usuario = ?, data_atualizacao = CURRENT_TIMESTAMP WHERE id_pessoa = ?;', (novo_usuario, id_pessoa))
                break
        else:
            break

def atualizar_status(cur, id_pessoa):
    while True:
        novo_status = input('Deseja alterar o status? [A] Ativar / [I] Inativar (ou deixe vazio para não alterar): ').upper().strip()
        if novo_status:       
            if novo_status in ['A', 'I']:
                status_valor = 1 if novo_status == 'A' else 0
                cur.execute('UPDATE usuario SET status = ?, data_atualizacao = CURRENT_TIMESTAMP WHERE id_pessoa = ?;', (status_valor, id_pessoa))
                break
            else:
                print("Escolha uma opção válida.")
        else:
            break

def atualizar_senha(cur, id_pessoa):
    while True:
        texto_informativo_senha = 'A senha deve ter pelo menos 10 caracteres e conter pelo menos uma letra maiúscula, uma letra minúscula, um número e um caractere especial.'
        print(texto_informativo_senha)
        nova_senha = getpass('Informe a nova senha (ou deixe vazio para não alterar): ').strip()
        if nova_senha:       
            confirmacao_nova_senha = getpass('Confirme a nova senha: ').strip()
            nova_senha_confirmada = nova_senha == confirmacao_nova_senha

            if validar_senha(nova_senha) and nova_senha_confirmada:
                senha = sha512(nova_senha.encode('utf-8')).hexdigest()
                cur.execute('UPDATE usuario SET senha = ?, data_atualizacao = CURRENT_TIMESTAMP WHERE id_pessoa = ?;', (senha, id_pessoa))
                break
            else:
                print(f"Senha inválida.")
        else:
            break

def atualizar_registro(cur, con):
    id_pessoa = input("Informe o ID do usuário a ser atualizado: ")
    try:
        id_pessoa = int(id_pessoa)
    except ValueError:
        print("O ID informado deve ser um número válido.")
        return

    cur.execute("SELECT EXISTS (SELECT 1 FROM pessoa WHERE id_pessoa = ?);", (id_pessoa, ))
    id_pessoa_existe = cur.fetchone()[0]
    if id_pessoa_existe:
        atualizar_nome_completo(cur, id_pessoa)
        atualizar_data_nascimento(cur, id_pessoa)
        atualizar_sexo(cur, id_pessoa)
        atualizar_cpf(cur, id_pessoa)
        atualizar_email(cur, id_pessoa)
        atualizar_telefone(cur, id_pessoa)
        atualizar_usuario(cur, id_pessoa)
        atualizar_senha(cur, id_pessoa)
        atualizar_status(cur, id_pessoa)
        con.commit()
        print("Registro atualizado com sucesso.")
    else:
        print('ID informado não existe.')