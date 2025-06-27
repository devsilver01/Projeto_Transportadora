"""
Nome do arquivo: tela_pecas.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import tkinter as tk
from tkinter import ttk, messagebox
from funcional.funcional_crud import ler_dados, adicionar_registro, atualizar_registro, deletar_registro

class TelaPecas(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#F0F0F0")
        self.nome_arquivo = "pecas.txt"
        self.id_chave = "ID_Peca"

        self.criar_widgets()
        self.carregar_pecas()

    def criar_widgets(self):
        # Título da Tela
        lbl_titulo = ttk.Label(self, text="Gerenciar Peças", font=("Helvetica", 20, "bold"), background="#F0F0F0", foreground="#333333")
        lbl_titulo.pack(pady=20)

        # Frame de Entrada de Dados
        frame_entrada = ttk.LabelFrame(self, text="Dados da Peça", padding="15 15 15 15")
        frame_entrada.pack(pady=10, padx=20, fill="x")

        # Estilo para labels e entries
        style = ttk.Style()
        style.configure("TLabel", background="#F0F0F0", font=("Helvetica", 10))
        style.configure("TEntry", font=("Helvetica", 10))
        style.configure("TButton", font=("Helvetica", 10))
        style.map("TButton", background=[("active", "#cccccc")])


        # Campos de Entrada
        # ID_Peca
        ttk.Label(frame_entrada, text="ID da Peça:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_id = ttk.Entry(frame_entrada, width=30)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entry_id.config(state='readonly') # ID será gerado automaticamente ou pego da tabela

        # Nome_Peca
        ttk.Label(frame_entrada, text="Nome da Peça:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome = ttk.Entry(frame_entrada, width=30)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Descricao
        ttk.Label(frame_entrada, text="Descrição:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_descricao = ttk.Entry(frame_entrada, width=30)
        self.entry_descricao.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Quantidade
        ttk.Label(frame_entrada, text="Quantidade:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_quantidade = ttk.Entry(frame_entrada, width=30)
        self.entry_quantidade.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Localizacao_Estoque
        ttk.Label(frame_entrada, text="Localização:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_localizacao = ttk.Entry(frame_entrada, width=30)
        self.entry_localizacao.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Botões de Ação
        frame_botoes = ttk.Frame(self, padding="10")
        frame_botoes.pack(pady=10)

        btn_adicionar = ttk.Button(frame_botoes, text="Adicionar", command=self.adicionar_peca)
        btn_adicionar.grid(row=0, column=0, padx=5)

        btn_atualizar = ttk.Button(frame_botoes, text="Atualizar", command=self.atualizar_peca)
        btn_atualizar.grid(row=0, column=1, padx=5)

        btn_deletar = ttk.Button(frame_botoes, text="Deletar", command=self.deletar_peca)
        btn_deletar.grid(row=0, column=2, padx=5)

        btn_limpar = ttk.Button(frame_botoes, text="Limpar Campos", command=self.limpar_campos)
        btn_limpar.grid(row=0, column=3, padx=5)

        btn_voltar = ttk.Button(self, text="Voltar para o Início", command=lambda: self.controller.mostrar_tela("TelaInicial"))
        btn_voltar.pack(pady=10)

        # Tabela de Peças (TreeView)
        colunas = ("ID_Peca", "Nome_Peca", "Descricao", "Quantidade", "Localizacao_Estoque")
        self.tree_pecas = ttk.Treeview(self, columns=colunas, show="headings")
        
        # Define os cabeçalhos das colunas
        for col in colunas:
            self.tree_pecas.heading(col, text=col.replace("_", " "))
            self.tree_pecas.column(col, width=100, anchor="center")
        
        # Ajustes de largura específicos
        self.tree_pecas.column("ID_Peca", width=70)
        self.tree_pecas.column("Nome_Peca", width=120)
        self.tree_pecas.column("Descricao", width=200)

        self.tree_pecas.pack(pady=10, padx=20, fill="both", expand=True)

        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree_pecas.yview)
        self.tree_pecas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Bind de seleção na tabela
        self.tree_pecas.bind("<<TreeviewSelect>>", self.carregar_campos_selecao)

    def gerar_novo_id(self):
        dados = ler_dados(self.nome_arquivo)
        if not dados:
            return 1
        # Pega o maior ID_Peca existente e adiciona 1
        max_id = max([int(p.get(self.id_chave, 0)) for p in dados])
        return max_id + 1

    def carregar_pecas(self):
        # Limpa a tabela
        for item in self.tree_pecas.get_children():
            self.tree_pecas.delete(item)

        pecas = ler_dados(self.nome_arquivo)
        for peca in pecas:
            # Adiciona cada peça na tabela
            self.tree_pecas.insert("", "end", values=list(peca.values()))

    def limpar_campos(self):
        self.entry_id.config(state='normal')
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state='readonly')
        self.entry_nome.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.entry_localizacao.delete(0, tk.END)
    
    def carregar_campos_selecao(self, event):
        selected_item = self.tree_pecas.selection()
        if not selected_item:
            return

        item_values = self.tree_pecas.item(selected_item[0], "values")
        
        self.limpar_campos() # Limpa antes de preencher

        self.entry_id.config(state='normal')
        self.entry_id.insert(0, item_values[0])
        self.entry_id.config(state='readonly')
        
        self.entry_nome.insert(0, item_values[1])
        self.entry_descricao.insert(0, item_values[2])
        self.entry_quantidade.insert(0, item_values[3])
        self.entry_localizacao.insert(0, item_values[4])

    def adicionar_peca(self):
        # ID é gerado automaticamente
        novo_id = str(self.generar_novo_id())
        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get()
        quantidade = self.entry_quantidade.get()
        localizacao = self.entry_localizacao.get()

        if not nome or not quantidade or not localizacao:
            messagebox.showwarning("Entrada Inválida", "Nome, Quantidade e Localização são obrigatórios.")
            return

        nova_peca = {
            self.id_chave: novo_id,
            "Nome_Peca": nome,
            "Descricao": descricao,
            "Quantidade": quantidade,
            "Localizacao_Estoque": localizacao
        }
        
        adicionar_registro(self.nome_arquivo, nova_peca)
        messagebox.showinfo("Sucesso", "Peça adicionada com sucesso!")
        self.limpar_campos()
        self.carregar_pecas()

    def atualizar_peca(self):
        id_peca = self.entry_id.get()
        if not id_peca:
            messagebox.showwarning("Erro", "Selecione uma peça na tabela para atualizar.")
            return

        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get()
        quantidade = self.entry_quantidade.get()
        localizacao = self.entry_localizacao.get()

        if not nome or not quantidade or not localizacao:
            messagebox.showwarning("Entrada Inválida", "Nome, Quantidade e Localização são obrigatórios.")
            return

        novos_dados = {
            "Nome_Peca": nome,
            "Descricao": descricao,
            "Quantidade": quantidade,
            "Localizacao_Estoque": localizacao
        }

        if atualizar_registro(self.nome_arquivo, self.id_chave, id_peca, novos_dados):
            messagebox.showinfo("Sucesso", "Peça atualizada com sucesso!")
            self.limpar_campos()
            self.carregar_pecas()
        else:
            messagebox.showerror("Erro", "ID da peça não encontrado.")

    def deletar_peca(self):
        id_peca = self.entry_id.get()
        if not id_peca:
            messagebox.showwarning("Erro", "Selecione uma peça na tabela para deletar.")
            return

        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar a peça ID: {id_peca}?"):
            if deletar_registro(self.nome_arquivo, self.id_chave, id_peca):
                messagebox.showinfo("Sucesso", "Peça deletada com sucesso!")
                self.limpar_campos()
                self.carregar_pecas()
            else:
                messagebox.showerror("Erro", "ID da peça não encontrado.")