def deletar_registro(cur, con):
    id_pessoa = input("Informe o ID do usuário a ser deletado: ")
    try:
        id_pessoa = int(id_pessoa)
    except ValueError:
        print("O ID informado deve ser um número válido.")
        return

    cur.execute("SELECT EXISTS (SELECT 1 FROM pessoa WHERE id_pessoa = ?);", (id_pessoa, ))
    id_pessoa_existe = cur.fetchone()[0]

    if id_pessoa_existe:
        while True:
            confirmacao_delete = input(f'Deseja deletar o usuário ID {id_pessoa}? [S] Sim ou [N] Não\n').upper()
            if confirmacao_delete in ['S', 'N']:
                break
            else:
                print("Por favor, digite 'S' para Sim ou 'N' para Não.")
        
        if confirmacao_delete == 'S':
            try:
                cur.execute("DELETE FROM usuario WHERE id_pessoa = ?", (id_pessoa,))
                cur.execute("DELETE FROM contato WHERE id_pessoa = ?", (id_pessoa,))
                cur.execute("DELETE FROM documento WHERE id_pessoa = ?", (id_pessoa,))
                cur.execute("DELETE FROM pessoa WHERE id_pessoa = ?", (id_pessoa,))
                print("Registro deletado com sucesso.")
            except Exception as e:
                print(f"Erro ao deletar registro: {str(e)}")
            finally:
                con.commit()
    else:
        print('ID informado não existe.')