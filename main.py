# this is part of the BudgetSys project.
#
# Release: v1.0-test1
#
# Copyright (c) 2023  Juan Bindez  <juanbindez780@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#  
# repo: https://github.com/juanBindez



import tkinter as tk
import sqlite3
from tkinter import ttk
import subprocess

from reportlab.pdfgen import canvas







# Conectar ao banco de dados
conn = sqlite3.connect('estoque.db')
c = conn.cursor()

# Criar nova janela para a pesquisa de produtos
pesquisa_window = tk.Tk()
pesquisa_window.title("Pesquisa de produtos")
pesquisa_window.geometry("600x400")



def create_pdf():
    image = tk.PhotoImage(width=pesquisa_window.winfo_width(), height=pesquisa_window.winfo_height())
    # renderiza a janela no objeto PhotoImage
    pesquisa_window.update()
    image = image.subsample(2) # reduz a resolução da imagem pela metade para salvar mais rapidamente

    # salva a imagem em formato PNG
    image.write("screenshot.png", format="png")




# Função para pesquisar o produto
def pesquisar_produto():
    # Limpar a tabela existente
    for row in tabela.get_children():
        tabela.delete(row)
    
    # Recuperar a palavra-chave da pesquisa
    keyword = entrada_pesquisa.get()
    
    # Pesquisar no banco de dados
    c.execute("SELECT * FROM estoque WHERE ITEM LIKE ?", ('%'+keyword+'%',))
    rows = c.fetchall()
    
    # Adicionar os resultados na tabela
    for row in rows:
        tabela.insert('', 'end', values=row[1:])
    
    # Calcular o valor total dos produtos encontrados
    total = sum([float(row[5])*int(row[3]) for row in rows])
    total_label.configure(text="Valor total: R$ {:.2f}".format(total))
    








# Função para selecionar um produto
def selecionar_produto():
    # Recuperar a linha selecionada na tabela
    selected_item = tabela.focus()
    
    # Verificar se um item foi selecionado
    if selected_item:
        # Recuperar as informações do produto selecionado
        item, descricao, quantidade, unidade, preco_unitario, preco_total = tabela.item(selected_item, 'values')
        
        # Criar uma nova janela para exibir as informações do produto
        detalhes_window = tk.Toplevel(pesquisa_window)
        detalhes_window.title("Detalhes do produto")
        detalhes_window.geometry("400x200")
        
        # Adicionar as informações do produto na janela
        item_label = tk.Label(detalhes_window, text="Item: {}".format(item))
        item_label.pack()
        
        descricao_label = tk.Label(detalhes_window, text="Descrição: {}".format(descricao))
        descricao_label.pack()
        
        quantidade_label = tk.Label(detalhes_window, text="Quantidade: {}".format(quantidade))
        quantidade_label.pack()
        
        unidade_label = tk.Label(detalhes_window, text="Unidade: {}".format(unidade))
        unidade_label.pack()
        
        preco_unitario_label = tk.Label(detalhes_window, text="Preço unitário: R$ {:.2f}".format(float(preco_unitario)))
        preco_unitario_label.pack()
        
        preco_total_label = tk.Label(detalhes_window, text="Preço total: R$ {:.2f}".format(float(preco_total)))
        preco_total_label.pack()
        








# Adicionar campo de pesquisa e botão de pesquisa
entrada_pesquisa = tk.Entry(pesquisa_window)
entrada_pesquisa.grid(row=0, column=0)

botao_pesquisar = tk.Button(pesquisa_window, text="Pesquisar",
                            command=pesquisar_produto)
botao_pesquisar.place(x=500, y=0)

# Adicionar tabela para exibir os resultados da pesquisa
tabela = tk.ttk.Treeview(pesquisa_window, columns=('Item', 'Descrição', 'Quantidade', 'Unidade', 'Preço Unitário', 'Preço Total'))
tabela.grid(row=4, column=0, columnspan=2)

tabela.heading('Item', text='Item')
tabela.heading('Descrição', text='Descrição')
tabela.heading('Quantidade', text='Quantidade')
tabela.heading('Unidade', text='Unidade')
tabela.heading('Preço Unitário', text='Preço Unitário')
tabela.heading('Preço Total', text='Preço Total')

vsb = tk.ttk.Scrollbar(pesquisa_window, orient="vertical", command=tabela.yview)
vsb.grid(row=1, column=2, sticky='ns')
tabela.configure(yscrollcommand=vsb.set)

botao_selecionar = tk.Button(pesquisa_window, text="Selecionar",
command=selecionar_produto)
botao_selecionar.grid(row=2, column=0)

total_label = tk.Label(pesquisa_window, text="")
total_label.grid(row=2, column=1)




tk.Button(pesquisa_window, text="save", command=create_pdf).place(x=45, y=0) 


pesquisa_window.mainloop()
