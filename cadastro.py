import sqlite3
import tkinter as tk

# Criar a conexão com o banco de dados
conn = sqlite3.connect('estoque.db')

# Criar a tabela de produtos
conn.execute('''CREATE TABLE IF NOT EXISTS estoque
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             ITEM TEXT NOT NULL,
             DESCRICAO TEXT NOT NULL,
             QUANTIDADE REAL NOT NULL,
             UNIDADE TEXT NOT NULL,
             PRECO_UNIT REAL NOT NULL,
             PRECO_TOTAL REAL NOT NULL);''')

# Função para inserir um novo produto no banco de dados
def adicionar_produto():
    item = item_entry.get()
    descricao = descricao_entry.get()
    quantidade = quantidade_entry.get()
    unidade = unidade_entry.get()
    preco_unit = preco_unit_entry.get()
    preco_total = float(quantidade) * float(preco_unit)
    conn.execute("INSERT INTO estoque (ITEM, DESCRICAO, QUANTIDADE, UNIDADE, PRECO_UNIT, PRECO_TOTAL) VALUES (?, ?, ?, ?, ?, ?)",
                 (item, descricao, quantidade, unidade, preco_unit, preco_total))
    conn.commit()
    atualizar_tabela()

# Função para excluir um produto do banco de dados
def excluir_produto():
    item = item_entry.get()
    conn.execute("DELETE FROM estoque WHERE ITEM=?", (item,))
    conn.commit()
    atualizar_tabela()

# Função para atualizar a tabela de produtos na tela
def atualizar_tabela():
    cursor = conn.execute("SELECT * FROM estoque")
    i = 0
    for row in cursor:
        for j in range(len(row)):
            cell = tk.Entry(master, width=15)
            cell.grid(row=i+1, column=j)
            cell.insert(0, row[j])
        i += 1

# Criação da janela principal
master = tk.Tk()

# Criação dos campos de entrada
item_label = tk.Label(master, text="Item")
item_label.grid(row=0, column=0)
item_entry = tk.Entry(master)
item_entry.grid(row=0, column=1)

descricao_label = tk.Label(master, text="Descrição")
descricao_label.grid(row=0, column=2)
descricao_entry = tk.Entry(master)
descricao_entry.grid(row=0, column=3)

quantidade_label = tk.Label(master, text="Quantidade")
quantidade_label.grid(row=0, column=4)
quantidade_entry = tk.Entry(master)
quantidade_entry.grid(row=0, column=5)

unidade_label = tk.Label(master, text="Unidade")
unidade_label.grid(row=0, column=6)
unidade_entry = tk.Entry(master)
unidade_entry.grid(row=0, column=7)

preco_unit_label = tk.Label(master, text="Preço Unitário")
preco_unit_label.grid(row=0, column=8)
preco_unit_entry = tk.Entry(master)
preco_unit_entry.grid(row=0, column=9)

# C
adicionar_button = tk.Button(master, text="Adicionar", command=adicionar_produto)
adicionar_button.grid(row=0, column=10)

excluir_button = tk.Button(master, text="Excluir", command=excluir_produto)
excluir_button.grid(row=0, column=11)

item_header = tk.Label(master, text="Item")
item_header.grid(row=1, column=0)
descricao_header = tk.Label(master, text="Descrição")
descricao_header.grid(row=1, column=1)
quantidade_header = tk.Label(master, text="Quantidade")
quantidade_header.grid(row=1, column=2)
unidade_header = tk.Label(master, text="Unidade")
unidade_header.grid(row=1, column=3)
preco_unit_header = tk.Label(master, text="Preço Unitário")
preco_unit_header.grid(row=1, column=4)
preco_total_header = tk.Label(master, text="Preço Total")
preco_total_header.grid(row=1, column=5)

atualizar_tabela()
tk.mainloop()
conn.close()