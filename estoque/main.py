import db_handler as db

def menu():
    print('=== Sistema de Gerenciamento de Estoque ===')
    print('1. Adicionar Produto')
    print('2. Exibir Produtos')
    print('3. Atualizar Estoque (Entrada/Saída)')
    print('4. Sair')

while True:
    menu()
    escolha = input('Escolha uma opção: ')

    if escolha == '1':
        nome = input('Nome do Produto: ')
        quantidade = int(input('Quantidade inicial: '))
        preco = float(input('Preço: '))
        db.adicionar_produto(nome, quantidade, preco)

    elif escolha == '2':
        db.exibir_produtos()

    elif escolha == '3':
        produto_id = int(input('ID do Produto: '))
        tipo = input('Tipo (Entrada/Saída): ').lower()
        quantidade = int(input('Quantidade: '))
        db.atualizar_estoque(produto_id, quantidade, tipo)

    elif escolha == '4':
        print('Saindo...')
        break
    else:
        print('Opção Inválida!')