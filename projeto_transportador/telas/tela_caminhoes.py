"""
Nome do arquivo: tela_caminhoes.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import tkinter as tk
from tkinter import ttk, messagebox
from funcional.funcional_crud import ler_dados, adicionar_registro, atualizar_registro, deletar_registro

class TelaCaminhoes(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#F0F0F0")
        self.nome_arquivo = "caminhoes.txt"
        self.id_chave = "ID_Caminhao"

        self.criar_widgets()
        self.carregar_caminhoes()

    def criar_widgets(self):
        lbl_titulo = ttk.Label(self, text="Gerenciar Caminhões", font=("Helvetica", 20, "bold"), background="#F0F0F0", foreground="#333333")
        lbl_titulo.pack(pady=20)

        frame_entrada = ttk.LabelFrame(self, text="Dados do Caminhão", padding="15 15 15 15")
        frame_entrada.pack(pady=10, padx=20, fill="x")

        # Campos de Entrada
        ttk.Label(frame_entrada, text="ID Caminhão:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_id = ttk.Entry(frame_entrada, width=30)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entry_id.config(state='readonly')

        ttk.Label(frame_entrada, text="Marca:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_marca = ttk.Entry(frame_entrada, width=30)
        self.entry_marca.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Modelo:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_modelo = ttk.Entry(frame_entrada, width=30)
        self.entry_modelo.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Ano:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_ano = ttk.Entry(frame_entrada, width=30)
        self.entry_ano.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Placa:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_placa = ttk.Entry(frame_entrada, width=30)
        self.entry_placa.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Quilometragem Atual:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_km_atual = ttk.Entry(frame_entrada, width=30)
        self.entry_km_atual.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Data Última Manutenção (AAAA-MM-DD):").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.entry_data_manutencao = ttk.Entry(frame_entrada, width=30)
        self.entry_data_manutencao.grid(row=6, column=1, padx=5, pady=5, sticky="ew")
        
        # Botões de Ação
        frame_botoes = ttk.Frame(self, padding="10")
        frame_botoes.pack(pady=10)

        btn_adicionar = ttk.Button(frame_botoes, text="Adicionar", command=self.adicionar_caminhao)
        btn_adicionar.grid(row=0, column=0, padx=5)

        btn_atualizar = ttk.Button(frame_botoes, text="Atualizar", command=self.atualizar_caminhao)
        btn_atualizar.grid(row=0, column=1, padx=5)

        btn_deletar = ttk.Button(frame_botoes, text="Deletar", command=self.deletar_caminhao)
        btn_deletar.grid(row=0, column=2, padx=5)

        btn_limpar = ttk.Button(frame_botoes, text="Limpar Campos", command=self.limpar_campos)
        btn_limpar.grid(row=0, column=3, padx=5)

        btn_voltar = ttk.Button(self, text="Voltar para o Início", command=lambda: self.controller.mostrar_tela("TelaInicial"))
        btn_voltar.pack(pady=10)

        # Tabela de Caminhões (TreeView)
        colunas = ("ID_Caminhao", "Marca", "Modelo", "Ano", "Placa", "Quilometragem_Atual", "Data_Ultima_Manutencao")
        self.tree_caminhoes = ttk.Treeview(self, columns=colunas, show="headings")
        
        for col in colunas:
            self.tree_caminhoes.heading(col, text=col.replace("_", " "))
            self.tree_caminhoes.column(col, width=120, anchor="center")
        
        self.tree_caminhoes.pack(pady=10, padx=20, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree_caminhoes.yview)
        self.tree_caminhoes.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree_caminhoes.bind("<<TreeviewSelect>>", self.carregar_campos_selecao)

    def gerar_novo_id(self):
        dados = ler_dados(self.nome_arquivo)
        if not dados:
            return "C001"
        # Pega o maior número do ID existente e adiciona 1, formatando para C00X
        max_id_num = 0
        for caminhao in dados:
            if caminhao.get(self.id_chave, '').startswith('C'):
                try:
                    num = int(caminhao[self.id_chave][1:]) # Pega "001" de "C001"
                    if num > max_id_num:
                        max_id_num = num
                except ValueError:
                    pass # Ignora IDs mal formatados
        return f"C{max_id_num + 1:03d}"

    def carregar_caminhoes(self):
        for item in self.tree_caminhoes.get_children():
            self.tree_caminhoes.delete(item)

        caminhoes = ler_dados(self.nome_arquivo)
        for caminhao in caminhoes:
            self.tree_caminhoes.insert("", "end", values=list(caminhao.values()))

    def limpar_campos(self):
        self.entry_id.config(state='normal')
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state='readonly')
        self.entry_marca.delete(0, tk.END)
        self.entry_modelo.delete(0, tk.END)
        self.entry_ano.delete(0, tk.END)
        self.entry_placa.delete(0, tk.END)
        self.entry_km_atual.delete(0, tk.END)
        self.entry_data_manutencao.delete(0, tk.END)
    
    def carregar_campos_selecao(self, event):
        selected_item = self.tree_caminhoes.selection()
        if not selected_item:
            return

        item_values = self.tree_caminhoes.item(selected_item[0], "values")
        
        self.limpar_campos()

        self.entry_id.config(state='normal')
        self.entry_id.insert(0, item_values[0])
        self.entry_id.config(state='readonly')
        
        self.entry_marca.insert(0, item_values[1])
        self.entry_modelo.insert(0, item_values[2])
        self.entry_ano.insert(0, item_values[3])
        self.entry_placa.insert(0, item_values[4])
        self.entry_km_atual.insert(0, item_values[5])
        self.entry_data_manutencao.insert(0, item_values[6])

    def adicionar_caminhao(self):
        novo_id = self.gerar_novo_id()
        marca = self.entry_marca.get()
        modelo = self.entry_modelo.get()
        ano = self.entry_ano.get()
        placa = self.entry_placa.get()
        km_atual = self.entry_km_atual.get()
        data_manutencao = self.entry_data_manutencao.get()

        if not all([marca, modelo, ano, placa, km_atual, data_manutencao]):
            messagebox.showwarning("Entrada Inválida", "Todos os campos são obrigatórios.")
            return

        novo_caminhao = {
            self.id_chave: novo_id,
            "Marca": marca,
            "Modelo": modelo,
            "Ano": ano,
            "Placa": placa,
            "Quilometragem_Atual": km_atual,
            "Data_Ultima_Manutencao": data_manutencao
        }
        
        adicionar_registro(self.nome_arquivo, novo_caminhao)
        messagebox.showinfo("Sucesso", "Caminhão adicionado com sucesso!")
        self.limpar_campos()
        self.carregar_caminhoes()

    def atualizar_caminhao(self):
        id_caminhao = self.entry_id.get()
        if not id_caminhao:
            messagebox.showwarning("Erro", "Selecione um caminhão na tabela para atualizar.")
            return

        marca = self.entry_marca.get()
        modelo = self.entry_modelo.get()
        ano = self.entry_ano.get()
        placa = self.entry_placa.get()
        km_atual = self.entry_km_atual.get()
        data_manutencao = self.entry_data_manutencao.get()

        if not all([marca, modelo, ano, placa, km_atual, data_manutencao]):
            messagebox.showwarning("Entrada Inválida", "Todos os campos são obrigatórios.")
            return

        novos_dados = {
            "Marca": marca,
            "Modelo": modelo,
            "Ano": ano,
            "Placa": placa,
            "Quilometragem_Atual": km_atual,
            "Data_Ultima_Manutencao": data_manutencao
        }

        if atualizar_registro(self.nome_arquivo, self.id_chave, id_caminhao, novos_dados):
            messagebox.showinfo("Sucesso", "Caminhão atualizado com sucesso!")
            self.limpar_campos()
            self.carregar_caminhoes()
        else:
            messagebox.showerror("Erro", "ID do caminhão não encontrado.")

    def deletar_caminhao(self):
        id_caminhao = self.entry_id.get()
        if not id_caminhao:
            messagebox.showwarning("Erro", "Selecione um caminhão na tabela para deletar.")
            return

        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar o caminhão ID: {id_caminhao}?"):
            if deletar_registro(self.nome_arquivo, self.id_chave, id_caminhao):
                messagebox.showinfo("Sucesso", "Caminhão deletado com sucesso!")
                self.limpar_campos()
                self.carregar_caminhoes()
            else:
                messagebox.showerror("Erro", "ID do caminhão não encontrado.")