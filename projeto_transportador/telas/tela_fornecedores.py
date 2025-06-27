"""
Nome do arquivo: tela_fornecedores.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import tkinter as tk
from tkinter import ttk, messagebox
from funcional.funcional_crud import ler_dados, adicionar_registro, atualizar_registro, deletar_registro

class TelaFornecedores(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#F0F0F0")
        self.nome_arquivo = "fornecedores.txt"
        self.id_chave = "ID_Fornecedor"

        self.criar_widgets()
        self.carregar_fornecedores()

    def criar_widgets(self):
        lbl_titulo = ttk.Label(self, text="Gerenciar Fornecedores", font=("Helvetica", 20, "bold"), background="#F0F0F0", foreground="#333333")
        lbl_titulo.pack(pady=20)

        frame_entrada = ttk.LabelFrame(self, text="Dados do Fornecedor", padding="15 15 15 15")
        frame_entrada.pack(pady=10, padx=20, fill="x")

        # Campos de Entrada para Fornecedores
        ttk.Label(frame_entrada, text="ID Fornecedor:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_id = ttk.Entry(frame_entrada, width=30)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entry_id.config(state='readonly')

        ttk.Label(frame_entrada, text="Nome:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome = ttk.Entry(frame_entrada, width=30)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Contato:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_contato = ttk.Entry(frame_entrada, width=30)
        self.entry_contato.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Telefone:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_telefone = ttk.Entry(frame_entrada, width=30)
        self.entry_telefone.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Email:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_email = ttk.Entry(frame_entrada, width=30)
        self.entry_email.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Rua:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_rua = ttk.Entry(frame_entrada, width=30)
        self.entry_rua.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Bairro:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.entry_bairro = ttk.Entry(frame_entrada, width=30)
        self.entry_bairro.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Cidade:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.entry_cidade = ttk.Entry(frame_entrada, width=30)
        self.entry_cidade.grid(row=7, column=1, padx=5, pady=5, sticky="ew")
        
        # Botões de Ação
        frame_botoes = ttk.Frame(self, padding="10")
        frame_botoes.pack(pady=10)

        btn_adicionar = ttk.Button(frame_botoes, text="Adicionar", command=self.adicionar_fornecedor)
        btn_adicionar.grid(row=0, column=0, padx=5)

        btn_atualizar = ttk.Button(frame_botoes, text="Atualizar", command=self.atualizar_fornecedor)
        btn_atualizar.grid(row=0, column=1, padx=5)

        btn_deletar = ttk.Button(frame_botoes, text="Deletar", command=self.deletar_fornecedor)
        btn_deletar.grid(row=0, column=2, padx=5)

        btn_limpar = ttk.Button(frame_botoes, text="Limpar Campos", command=self.limpar_campos)
        btn_limpar.grid(row=0, column=3, padx=5)

        btn_voltar = ttk.Button(self, text="Voltar para o Início", command=lambda: self.controller.mostrar_tela("TelaInicial"))
        btn_voltar.pack(pady=10)

        # Tabela de Fornecedores (TreeView)
        colunas = ("ID_Fornecedor", "Nome_Fornecedor", "Contato", "Telefone", "Email", "Endereco_Rua", "Endereco_Bairro", "Endereco_Cidade")
        self.tree_fornecedores = ttk.Treeview(self, columns=colunas, show="headings")
        
        for col in colunas:
            self.tree_fornecedores.heading(col, text=col.replace("_", " "))
            self.tree_fornecedores.column(col, width=100, anchor="center")
        
        self.tree_fornecedores.pack(pady=10, padx=20, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree_fornecedores.yview)
        self.tree_fornecedores.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree_fornecedores.bind("<<TreeviewSelect>>", self.carregar_campos_selecao)

    def gerar_novo_id(self):
        dados = ler_dados(self.nome_arquivo)
        if not dados:
            return 101 # IDs de fornecedores começam em 101
        max_id = max([int(f.get(self.id_chave, 0)) for f in dados])
        return max_id + 1

    def carregar_fornecedores(self):
        for item in self.tree_fornecedores.get_children():
            self.tree_fornecedores.delete(item)

        fornecedores = ler_dados(self.nome_arquivo)
        for fornecedor in fornecedores:
            self.tree_fornecedores.insert("", "end", values=list(fornecedor.values()))

    def limpar_campos(self):
        self.entry_id.config(state='normal')
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state='readonly')
        self.entry_nome.delete(0, tk.END)
        self.entry_contato.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_rua.delete(0, tk.END)
        self.entry_bairro.delete(0, tk.END)
        self.entry_cidade.delete(0, tk.END)
    
    def carregar_campos_selecao(self, event):
        selected_item = self.tree_fornecedores.selection()
        if not selected_item:
            return

        item_values = self.tree_fornecedores.item(selected_item[0], "values")
        
        self.limpar_campos()

        self.entry_id.config(state='normal')
        self.entry_id.insert(0, item_values[0])
        self.entry_id.config(state='readonly')
        
        self.entry_nome.insert(0, item_values[1])
        self.entry_contato.insert(0, item_values[2])
        self.entry_telefone.insert(0, item_values[3])
        self.entry_email.insert(0, item_values[4])
        self.entry_rua.insert(0, item_values[5])
        self.entry_bairro.insert(0, item_values[6])
        self.entry_cidade.insert(0, item_values[7])

    def adicionar_fornecedor(self):
        novo_id = str(self.gerar_novo_id())
        nome = self.entry_nome.get()
        contato = self.entry_contato.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        rua = self.entry_rua.get()
        bairro = self.entry_bairro.get()
        cidade = self.entry_cidade.get()

        if not nome or not telefone or not cidade:
            messagebox.showwarning("Entrada Inválida", "Nome, Telefone e Cidade são obrigatórios.")
            return

        novo_fornecedor = {
            self.id_chave: novo_id,
            "Nome_Fornecedor": nome,
            "Contato": contato,
            "Telefone": telefone,
            "Email": email,
            "Endereco_Rua": rua,
            "Endereco_Bairro": bairro,
            "Endereco_Cidade": cidade
        }
        
        adicionar_registro(self.nome_arquivo, novo_fornecedor)
        messagebox.showinfo("Sucesso", "Fornecedor adicionado com sucesso!")
        self.limpar_campos()
        self.carregar_fornecedores()

    def atualizar_fornecedor(self):
        id_fornecedor = self.entry_id.get()
        if not id_fornecedor:
            messagebox.showwarning("Erro", "Selecione um fornecedor na tabela para atualizar.")
            return

        nome = self.entry_nome.get()
        contato = self.entry_contato.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        rua = self.entry_rua.get()
        bairro = self.entry_bairro.get()
        cidade = self.entry_cidade.get()

        if not nome or not telefone or not cidade:
            messagebox.showwarning("Entrada Inválida", "Nome, Telefone e Cidade são obrigatórios.")
            return

        novos_dados = {
            "Nome_Fornecedor": nome,
            "Contato": contato,
            "Telefone": telefone,
            "Email": email,
            "Endereco_Rua": rua,
            "Endereco_Bairro": bairro,
            "Endereco_Cidade": cidade
        }

        if atualizar_registro(self.nome_arquivo, self.id_chave, id_fornecedor, novos_dados):
            messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
            self.limpar_campos()
            self.carregar_fornecedores()
        else:
            messagebox.showerror("Erro", "ID do fornecedor não encontrado.")

    def deletar_fornecedor(self):
        id_fornecedor = self.entry_id.get()
        if not id_fornecedor:
            messagebox.showwarning("Erro", "Selecione um fornecedor na tabela para deletar.")
            return

        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar o fornecedor ID: {id_fornecedor}?"):
            if deletar_registro(self.nome_arquivo, self.id_chave, id_fornecedor):
                messagebox.showinfo("Sucesso", "Fornecedor deletado com sucesso!")
                self.limpar_campos()
                self.carregar_fornecedores()
            else:
                messagebox.showerror("Erro", "ID do fornecedor não encontrado.")