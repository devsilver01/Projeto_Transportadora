"""
Nome do arquivo: tela_funcionarios.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import tkinter as tk
from tkinter import ttk, messagebox
from funcional.funcional_crud import ler_dados, adicionar_registro, atualizar_registro, deletar_registro

class TelaFuncionarios(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#F0F0F0")
        self.nome_arquivo = "funcionarios.txt"
        self.id_chave = "ID_Funcionario"

        self.criar_widgets()
        self.carregar_funcionarios()

    def criar_widgets(self):
        lbl_titulo = ttk.Label(self, text="Gerenciar Funcionários", font=("Helvetica", 20, "bold"), background="#F0F0F0", foreground="#333333")
        lbl_titulo.pack(pady=20)

        frame_entrada = ttk.LabelFrame(self, text="Dados do Funcionário", padding="15 15 15 15")
        frame_entrada.pack(pady=10, padx=20, fill="x")

        # Campos de Entrada
        ttk.Label(frame_entrada, text="ID Funcionário:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_id = ttk.Entry(frame_entrada, width=30)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entry_id.config(state='readonly')

        ttk.Label(frame_entrada, text="Nome:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome = ttk.Entry(frame_entrada, width=30)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Cargo:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_cargo = ttk.Entry(frame_entrada, width=30)
        self.entry_cargo.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

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

        btn_adicionar = ttk.Button(frame_botoes, text="Adicionar", command=self.adicionar_funcionario)
        btn_adicionar.grid(row=0, column=0, padx=5)

        btn_atualizar = ttk.Button(frame_botoes, text="Atualizar", command=self.atualizar_funcionario)
        btn_atualizar.grid(row=0, column=1, padx=5)

        btn_deletar = ttk.Button(frame_botoes, text="Deletar", command=self.deletar_funcionario)
        btn_deletar.grid(row=0, column=2, padx=5)

        btn_limpar = ttk.Button(frame_botoes, text="Limpar Campos", command=self.limpar_campos)
        btn_limpar.grid(row=0, column=3, padx=5)

        btn_voltar = ttk.Button(self, text="Voltar para o Início", command=lambda: self.controller.mostrar_tela("TelaInicial"))
        btn_voltar.pack(pady=10)

        # Tabela de Funcionários (TreeView)
        colunas = ("ID_Funcionario", "Nome_Funcionario", "Cargo", "Telefone", "Email", "Endereco_Rua", "Endereco_Bairro", "Endereco_Cidade")
        self.tree_funcionarios = ttk.Treeview(self, columns=colunas, show="headings")
        
        for col in colunas:
            self.tree_funcionarios.heading(col, text=col.replace("_", " "))
            self.tree_funcionarios.column(col, width=100, anchor="center")
        
        self.tree_funcionarios.pack(pady=10, padx=20, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree_funcionarios.yview)
        self.tree_funcionarios.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree_funcionarios.bind("<<TreeviewSelect>>", self.carregar_campos_selecao)

    def gerar_novo_id(self):
        dados = ler_dados(self.nome_arquivo)
        if not dados:
            return "F001" # IDs de funcionários podem começar em F001
        max_id_num = 0
        for func in dados:
            if func.get(self.id_chave, '').startswith('F'):
                try:
                    num = int(func[self.id_chave][1:])
                    if num > max_id_num:
                        max_id_num = num
                except ValueError:
                    pass
        return f"F{max_id_num + 1:03d}"

    def carregar_funcionarios(self):
        for item in self.tree_funcionarios.get_children():
            self.tree_funcionarios.delete(item)

        funcionarios = ler_dados(self.nome_arquivo)
        for func in funcionarios:
            self.tree_funcionarios.insert("", "end", values=list(func.values()))

    def limpar_campos(self):
        self.entry_id.config(state='normal')
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state='readonly')
        self.entry_nome.delete(0, tk.END)
        self.entry_cargo.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_rua.delete(0, tk.END)
        self.entry_bairro.delete(0, tk.END)
        self.entry_cidade.delete(0, tk.END)
    
    def carregar_campos_selecao(self, event):
        selected_item = self.tree_funcionarios.selection()
        if not selected_item:
            return

        item_values = self.tree_funcionarios.item(selected_item[0], "values")
        
        self.limpar_campos()

        self.entry_id.config(state='normal')
        self.entry_id.insert(0, item_values[0])
        self.entry_id.config(state='readonly')
        
        self.entry_nome.insert(0, item_values[1])
        self.entry_cargo.insert(0, item_values[2])
        self.entry_telefone.insert(0, item_values[3])
        self.entry_email.insert(0, item_values[4])
        self.entry_rua.insert(0, item_values[5])
        self.entry_bairro.insert(0, item_values[6])
        self.entry_cidade.insert(0, item_values[7])

    def adicionar_funcionario(self):
        novo_id = self.gerar_novo_id()
        nome = self.entry_nome.get()
        cargo = self.entry_cargo.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        rua = self.entry_rua.get()
        bairro = self.entry_bairro.get()
        cidade = self.entry_cidade.get()

        if not all([nome, cargo, telefone, cidade]):
            messagebox.showwarning("Entrada Inválida", "Nome, Cargo, Telefone e Cidade são obrigatórios.")
            return

        novo_funcionario = {
            self.id_chave: novo_id,
            "Nome_Funcionario": nome,
            "Cargo": cargo,
            "Telefone": telefone,
            "Email": email,
            "Endereco_Rua": rua,
            "Endereco_Bairro": bairro,
            "Endereco_Cidade": cidade
        }
        
        adicionar_registro(self.nome_arquivo, novo_funcionario)
        messagebox.showinfo("Sucesso", "Funcionário adicionado com sucesso!")
        self.limpar_campos()
        self.carregar_funcionarios()

    def atualizar_funcionario(self):
        id_funcionario = self.entry_id.get()
        if not id_funcionario:
            messagebox.showwarning("Erro", "Selecione um funcionário na tabela para atualizar.")
            return

        nome = self.entry_nome.get()
        cargo = self.entry_cargo.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        rua = self.entry_rua.get()
        bairro = self.entry_bairro.get()
        cidade = self.entry_cidade.get()

        if not all([nome, cargo, telefone, cidade]):
            messagebox.showwarning("Entrada Inválida", "Nome, Cargo, Telefone e Cidade são obrigatórios.")
            return

        novos_dados = {
            "Nome_Funcionario": nome,
            "Cargo": cargo,
            "Telefone": telefone,
            "Email": email,
            "Endereco_Rua": rua,
            "Endereco_Bairro": bairro,
            "Endereco_Cidade": cidade
        }

        if atualizar_registro(self.nome_arquivo, self.id_chave, id_funcionario, novos_dados):
            messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
            self.limpar_campos()
            self.carregar_funcionarios()
        else:
            messagebox.showerror("Erro", "ID do funcionário não encontrado.")

    def deletar_funcionario(self):
        id_funcionario = self.entry_id.get()
        if not id_funcionario:
            messagebox.showwarning("Erro", "Selecione um funcionário na tabela para deletar.")
            return

        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar o funcionário ID: {id_funcionario}?"):
            if deletar_registro(self.nome_arquivo, self.id_chave, id_funcionario):
                messagebox.showinfo("Sucesso", "Funcionário deletado com sucesso!")
                self.limpar_campos()
                self.carregar_funcionarios()
            else:
                messagebox.showerror("Erro", "ID do funcionário não encontrado.")