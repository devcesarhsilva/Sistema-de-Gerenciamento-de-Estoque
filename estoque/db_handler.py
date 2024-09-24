import sqlite3
from prettytable import PrettyTable
from datetime import datetime
#Função para conectar ao banco de dados SQlite
def conectar_banco():
    conn = sqlite3.connect('estoque.db')
    return conn
#Função para criar tabelas
def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()

    #Tabela de produtos
    cursor.execute("CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, quantidade INTEGER NOT NULL, preco REAL NOT NULL)")

    #Tabela de transações
    cursor.execute("CREATE TABLE IF NOT EXISTS transacoes (id INTEGER PRIMARY KEY AUTOINCREMENT, produto_id INTEGER, tipo TEXT NOT NULL, quantidade INTEGER NOT NULL, data TEXT NOT NULL, FOREIGN KEY (produto_id) REFERENCES produtos(id))")

    conn.commit()
    conn.close()

    def adicionar_produto(nome, quantidade, preco):
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?,?,?)",
                       (nome, quantidade, preco))
        conn.commit()
        conn.close()
        print(f"Produto' {nome} 'adicionado com sucesso!")

    def exibir_produtos():
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()

        #Criando tabela formatada
        tabela = PrettyTable(['ID', 'Nome', 'Quantidade', 'Preço'])
        for produto in produtos:
            tabela.add_row(produto)

            print(tabela)

            conn.close()

    
    def atualizar_estoque(produto_id, quantidade, tipo):
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (produto_id,))
        resultado = cursor.fetchone()

        if not resultado:
            print('Produto não encontrado!')
            return
        
        nova_quantidade = resultado[0] + quantidade if tipo == 'entrada' else resultado[0] - quantidade
        if nova_quantidade < 0:
            print('Quantidade insuficiente em estoque!')
            return
        
        cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?",
                       (nova_quantidade, produto_id))
        
        #Registrar a transação
        data = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        cursor.execute("INSERT INTO transacoes (produto_id, tipo, quantidade, data) VALUES (?,?,?,?)",
                       (produto_id, tipo, quantidade, data))
        
        conn.commit()
        conn.close()
        print('Estoque atualizado com sucesso!')