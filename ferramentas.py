from re import fullmatch
import os
from email_validator import validate_email, EmailNotValidError

def valida_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def valida_cpf(cpf: str) -> bool:
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # CPF deve ter 11 dígitos
    if len(cpf) != 11 or cpf == cpf[0] * len(cpf):
        return False

    # Cálculo do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    primeiro_digito = 11 - (soma % 11)
    primeiro_digito = 0 if primeiro_digito >= 10 else primeiro_digito

    if primeiro_digito != int(cpf[9]):
        return False

    # Cálculo do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    segundo_digito = 11 - (soma % 11)
    segundo_digito = 0 if segundo_digito >= 10 else segundo_digito

    return segundo_digito == int(cpf[10])

def validar_senha(senha) -> bool:
    padrao = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+={}[\]|\\:;"\'<>,.?/~`])[A-Za-z\d!@#$%^&*()_\-+={}[\]|\\:;"\'<>,.?/~`]{10,}$'
    return bool(fullmatch(padrao, senha))

def consulta_contatos_cadastrados(cur, tipo_contato) -> tuple:
    cur.execute("""
                                select
                                    con.id_pessoa
                                    , con.contato
                                    , tip.id_tipo_contato 
                                from
                                    contato as con
                                    right join
                                        tipo_contato as tip
                                        on con.id_tipo_contato = tip.id_tipo_contato
										and con.status = 1
                                where
                                    tip.descricao = ?;
                """, (tipo_contato,)
                )
    
    contatos_cadastrados = cur.fetchall()
    lista_contatos = [(i,j) for i, j, _ in contatos_cadastrados]
    id_tipo_contato = contatos_cadastrados[0][2]

    return lista_contatos, id_tipo_contato

def limpar_tela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')