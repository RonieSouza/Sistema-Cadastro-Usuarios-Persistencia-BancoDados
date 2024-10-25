from bancodados import cria_tabelas, conectar
from ferramentas import limpar_tela
from cadastro import finalizar_cadastro
from visualizacao import visualizar_registros
from atualizacao import atualizar_registro
from exclusao import deletar_registro

def menu_principal():

    con = conectar()
    cur = con.cursor()

    cria_tabelas(cur)
    limpar_tela()
    while True:
        print("\n" + "=" * 130)
        print(" " * 50 + "SISTEMA DE GERENCIAMENTO")
        print("=" * 130)
        print("1. 📋 Cadastrar Pessoa")
        print("2. 🔍 Visualizar Registros")
        print("3. ✏️ Atualizar Registro")
        print("4. 🗑️ Deletar Registro")
        print("5. ❌ Sair")
        print("=" * 130)

        escolha = input("Escolha uma opção (1-5): ").strip()

        if escolha == '1':
            print("\n" + "-" * 130)
            print("📋 Cadastrar Pessoa")
            print("-" * 130)
            finalizar_cadastro(cur, con)
        elif escolha == '2':
            print("\n" + "-" * 130)
            print("🔍 Visualizar Registros")
            print("-" * 130)
            visualizar_registros(cur)
        elif escolha == '3':
            print("\n" + "-" * 130)
            print("✏️  Atualizar Registro")
            print("-" * 130)
            visualizar_registros(cur)
            atualizar_registro(cur, con)
        elif escolha == '4':
            print("\n" + "-" * 130)
            print("🗑️  Deletar Registro")
            print("-" * 130)
            visualizar_registros(cur)
            deletar_registro(cur, con)
        elif escolha == '5':
            print("\n" + "=" * 130)
            print("❌ Saindo do sistema... Até logo!")
            print("=" * 130)
            break
        else:
            print("\n❗ Opção inválida. Por favor, escolha uma opção de 1 a 5.")
            print("-" * 130)
    
    con.close()

if __name__ == '__main__':
    menu_principal()