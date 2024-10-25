from tabulate import tabulate

def visualizar_registros(cur):
    query = """
    select
        pes.id_pessoa														as id
        , pes.nome_completo													as nome_completo
        , pes.data_nascimento												as data_nascimento
        , sex.descricao														as sexo
        , doc.documento														as cpf
        , max(case when tip.descricao = 'EMAIL' then cont.contato end) 		as email
        , max(case when tip.descricao = 'TELEFONE' then cont.contato end) 	as telefone
        , usr.usuario														as usuario
        , case when usr.status then 'ATIVO' else 'INATIVO' end				as status
    from
        usuario as usr
        join
            pessoa as pes
            on usr.id_pessoa = pes.id_pessoa
        join
            sexo as sex
            on pes.id_sexo = sex.id_sexo
        join
            documento as doc
            on pes.id_pessoa = doc.id_pessoa
        join
            contato as cont
            on pes.id_pessoa = cont.id_pessoa
        join
            tipo_contato as tip
            on cont.id_tipo_contato = tip.id_tipo_contato
    group by
        usr.id_usuario;
    """
    
    cur.execute(query)
    registros = cur.fetchall()
    
    headers = ["ID", "Nome Completo", "Data de Nascimento", "Sexo", "CPF", "Email", "Telefone", "Usuário", "Status"]
    
    print(tabulate(registros, headers=headers, tablefmt="fancy_grid"))