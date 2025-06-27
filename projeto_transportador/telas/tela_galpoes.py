"""
Nome do arquivo: tela_galpoes.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import tkinter as tk
from tkinter import ttk, messagebox
from funcional.funcional_crud import ler_dados, adicionar_registro, atualizar_registro, deletar_registro

class TelaGalpoes(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#F0F0F0")
        self.nome_arquivo = "galpoes.txt"
        self.id_chave = "ID_Galpao"

        self.criar_widgets()
        self.carregar_galpoes()

    def criar_widgets(self):
        lbl_titulo = ttk.Label(self, text="Controle de Galpões", font=("Helvetica", 20, "bold"), background="#F0F0F0", foreground="#333333")
        lbl_titulo.pack(pady=20)

        frame_entrada = ttk.LabelFrame(self, text="Dados do Galpão", padding="15 15 15 15")
        frame_entrada.pack(pady=10, padx=20, fill="x")

        # Campos de Entrada
        ttk.Label(frame_entrada, text="ID Galpão:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_id = ttk.Entry(frame_entrada, width=30)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entry_id.config(state='readonly')

        ttk.Label(frame_entrada, text="Nome do Galpão:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome = ttk.Entry(frame_entrada, width=30)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Capacidade (m²):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_capacidade = ttk.Entry(frame_entrada, width=30)
        self.entry_capacidade.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Localização:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_localizacao = ttk.Entry(frame_entrada, width=30)
        self.entry_localizacao.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        # Botões de Ação
        frame_botoes = ttk.Frame(self, padding="10")
        frame_botoes.pack(pady=10)

        btn_adicionar = ttk.Button(frame_botoes, text="Adicionar", command=self.adicionar_galpao)
        btn_adicionar.grid(row=0, column=0, padx=5)

        btn_atualizar = ttk.Button(frame_botoes, text="Atualizar", command=self.atualizar_galpao)
        btn_atualizar.grid(row=0, column=1, padx=5)

        btn_deletar = ttk.Button(frame_botoes, text="Deletar", command=self.deletar_galpao)
        btn_deletar.grid(row=0, column=2, padx=5)

        btn_limpar = ttk.Button(frame_botoes, text="Limpar Campos", command=self.limpar_campos)
        btn_limpar.grid(row=0, column=3, padx=5)

        btn_voltar = ttk.Button(self, text="Voltar para o Início", command=lambda: self.controller.mostrar_tela("TelaInicial"))
        btn_voltar.pack(pady=10)

        # Tabela de Galpões (TreeView)
        colunas = ("ID_Galpao", "Nome_Galpao", "Capacidade", "Localizacao")
        self.tree_galpoes = ttk.Treeview(self, columns=colunas, show="headings")
        
        for col in colunas:
            self.tree_galpoes.heading(col, text=col.replace("_", " "))
            self.tree_galpoes.column(col, width=120, anchor="center")
        
        self.tree_galpoes.pack(pady=10, padx=20, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree_galpoes.yview)
        self.tree_galpoes.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree_galpoes.bind("<<TreeviewSelect>>", self.carregar_campos_selecao)

    def gerar_novo_id(self):
        dados = ler_dados(self.nome_arquivo)
        if not dados:
            return "G01" # IDs de galpões podem começar em G01
        max_id_num = 0
        for galpao in dados:
            if galpao.get(self.id_chave, '').startswith('G'):
                try:
                    num = int(galpao[self.id_chave][1:])
                    if num > max_id_num:
                        max_id_num = num
                except ValueError:
                    pass
        return f"G{max_id_num + 1:02d}"

    def carregar_galpoes(self):
        for item in self.tree_galpoes.get_children():
            self.tree_galpoes.delete(item)

        galpoes = ler_dados(self.nome_arquivo)
        for galpao in galpoes:
            self.tree_galpoes.insert("", "end", values=list(galpao.values()))

    def limpar_campos(self):
        self.entry_id.config(state='normal')
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state='readonly')
        self.entry_nome.delete(0, tk.END)
        self.entry_capacidade.delete(0, tk.END)
        self.entry_localizacao.delete(0, tk.END)
    
    def carregar_campos_selecao(self, event):
        selected_item = self.tree_galpoes.selection()
        if not selected_item:
            return

        item_values = self.tree_galpoes.item(selected_item[0], "values")
        
        self.limpar_campos()

        self.entry_id.config(state='normal')
        self.entry_id.insert(0, item_values[0])
        self.entry_id.config(state='readonly')
        
        self.entry_nome.insert(0, item_values[1])
        self.entry_capacidade.insert(0, item_values[2])
        self.entry_localizacao.insert(0, item_values[3])

    def adicionar_galpao(self):
        novo_id = self.gerar_novo_id()
        nome = self.entry_nome.get()
        capacidade = self.entry_capacidade.get()
        localizacao = self.entry_localizacao.get()

        if not all([nome, capacidade, localizacao]):
            messagebox.showwarning("Entrada Inválida", "Todos os campos são obrigatórios.")
            return

        novo_galpao = {
            self.id_chave: novo_id,
            "Nome_Galpao": nome,
            "Capacidade": capacidade,
            "Localizacao": localizacao
        }
        
        adicionar_registro(self.nome_arquivo, novo_galpao)
        messagebox.showinfo("Sucesso", "Galpão adicionado com sucesso!")
        self.limpar_campos()
        self.carregar_galpoes()

    def atualizar_galpao(self):
        id_galpao = self.entry_id.get()
        if not id_galpao:
            messagebox.showwarning("Erro", "Selecione um galpão na tabela para atualizar.")
            return

        nome = self.entry_nome.get()
        capacidade = self.entry_capacidade.get()
        localizacao = self.entry_localizacao.get()

        if not all([nome, capacidade, localizacao]):
            messagebox.showwarning("Entrada Inválida", "Todos os campos são obrigatórios.")
            return

        novos_dados = {
            "Nome_Galpao": nome,
            "Capacidade": capacidade,
            "Localizacao": localizacao
        }

        if atualizar_registro(self.nome_arquivo, self.id_chave, id_galpao, novos_dados):
            messagebox.showinfo("Sucesso", "Galpão atualizado com sucesso!")
            self.limpar_campos()
            self.carregar_galpoes()
        else:
            messagebox.showerror("Erro", "ID do galpão não encontrado.")

    def deletar_galpao(self):
        id_galpao = self.entry_id.get()
        if not id_galpao:
            messagebox.showwarning("Erro", "Selecione um galpão na tabela para deletar.")
            return

        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar o galpão ID: {id_galpao}?"):
            if deletar_registro(self.nome_arquivo, self.id_chave, id_galpao):
                messagebox.showinfo("Sucesso", "Galpão deletado com sucesso!")
                self.limpar_campos()
                self.carregar_galpoes()
            else:
                messagebox.showerror("Erro", "ID do galpão não encontrado.")