"""
Nome do arquivo: tela_saidas.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import tkinter as tk
from tkinter import ttk, messagebox
from funcional.funcional_crud import ler_dados, adicionar_registro, atualizar_registro, deletar_registro
import datetime # Para gerar o horário da saída

class TelaSaidas(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#F0F0F0")
        self.nome_arquivo = "saidas_caminhoes.txt"
        self.id_chave = "ID_Saida"

        self.criar_widgets()
        self.carregar_saidas()

    def criar_widgets(self):
        lbl_titulo = ttk.Label(self, text="Registro de Saídas de Caminhões", font=("Helvetica", 20, "bold"), background="#F0F0F0", foreground="#333333")
        lbl_titulo.pack(pady=20)

        frame_entrada = ttk.LabelFrame(self, text="Dados da Saída", padding="15 15 15 15")
        frame_entrada.pack(pady=10, padx=20, fill="x")

        # Campos de Entrada para Saídas
        ttk.Label(frame_entrada, text="ID Saída:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_id = ttk.Entry(frame_entrada, width=30)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entry_id.config(state='readonly')

        ttk.Label(frame_entrada, text="ID Caminhão:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_id_caminhao = ttk.Entry(frame_entrada, width=30)
        self.entry_id_caminhao.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="ID Cliente:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_id_cliente = ttk.Entry(frame_entrada, width=30)
        self.entry_id_cliente.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Tipo de Carga:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_tipo_carga = ttk.Entry(frame_entrada, width=30)
        self.entry_tipo_carga.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Destino:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_destino = ttk.Entry(frame_entrada, width=30)
        self.entry_destino.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(frame_entrada, text="Horário Saída (AAAA-MM-DD HH:MM):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_horario_saida = ttk.Entry(frame_entrada, width=30)
        self.entry_horario_saida.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Horário Chegada (AAAA-MM-DD HH:MM):").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.entry_horario_chegada = ttk.Entry(frame_entrada, width=30)
        self.entry_horario_chegada.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Quilometragem Inicial:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.entry_km_inicial = ttk.Entry(frame_entrada, width=30)
        self.entry_km_inicial.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Quilometragem Final:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.entry_km_final = ttk.Entry(frame_entrada, width=30)
        self.entry_km_final.grid(row=8, column=1, padx=5, pady=5, sticky="ew")


        # Botões de Ação
        frame_botoes = ttk.Frame(self, padding="10")
        frame_botoes.pack(pady=10)

        btn_adicionar = ttk.Button(frame_botoes, text="Adicionar", command=self.adicionar_saida)
        btn_adicionar.grid(row=0, column=0, padx=5)

        btn_atualizar = ttk.Button(frame_botoes, text="Atualizar", command=self.atualizar_saida)
        btn_atualizar.grid(row=0, column=1, padx=5)

        btn_deletar = ttk.Button(frame_botoes, text="Deletar", command=self.deletar_saida)
        btn_deletar.grid(row=0, column=2, padx=5)

        btn_limpar = ttk.Button(frame_botoes, text="Limpar Campos", command=self.limpar_campos)
        btn_limpar.grid(row=0, column=3, padx=5)

        btn_voltar = ttk.Button(self, text="Voltar para o Início", command=lambda: self.controller.mostrar_tela("TelaInicial"))
        btn_voltar.pack(pady=10)

        # Tabela de Saídas (TreeView)
        colunas = ("ID_Saida", "ID_Caminhao", "ID_Cliente", "Tipo_Carga", "Destino", "Horario_Saida", "Horario_Chegada", "Quilometragem_Inicial", "Quilometragem_Final")
        self.tree_saidas = ttk.Treeview(self, columns=colunas, show="headings")
        
        for col in colunas:
            self.tree_saidas.heading(col, text=col.replace("_", " "))
            self.tree_saidas.column(col, width=100, anchor="center")
        
        # Ajustes de largura para colunas específicas
        self.tree_saidas.column("ID_Saida", width=60)
        self.tree_saidas.column("Horario_Saida", width=150)
        self.tree_saidas.column("Horario_Chegada", width=150)
        self.tree_saidas.column("Quilometragem_Inicial", width=120)
        self.tree_saidas.column("Quilometragem_Final", width=120)

        self.tree_saidas.pack(pady=10, padx=20, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree_saidas.yview)
        self.tree_saidas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree_saidas.bind("<<TreeviewSelect>>", self.carregar_campos_selecao)

    def gerar_novo_id(self):
        dados = ler_dados(self.nome_arquivo)
        if not dados:
            return 1
        # IDs de saída são numéricos simples
        max_id = max([int(s.get(self.id_chave, 0).replace('S', '')) for s in dados if s.get(self.id_chave, 'S').startswith('S')]) # Extrai o número do ID (S001 -> 1)
        return max_id + 1

    def carregar_saidas(self):
        for item in self.tree_saidas.get_children():
            self.tree_saidas.delete(item)

        saidas = ler_dados(self.nome_arquivo)
        for saida in saidas:
            self.tree_saidas.insert("", "end", values=list(saida.values()))

    def limpar_campos(self):
        self.entry_id.config(state='normal')
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state='readonly')
        self.entry_id_caminhao.delete(0, tk.END)
        self.entry_id_cliente.delete(0, tk.END)
        self.entry_tipo_carga.delete(0, tk.END)
        self.entry_destino.delete(0, tk.END)
        self.entry_horario_saida.delete(0, tk.END)
        self.entry_horario_chegada.delete(0, tk.END)
        self.entry_km_inicial.delete(0, tk.END)
        self.entry_km_final.delete(0, tk.END)
    
    def carregar_campos_selecao(self, event):
        selected_item = self.tree_saidas.selection()
        if not selected_item:
            return

        item_values = self.tree_saidas.item(selected_item[0], "values")
        
        self.limpar_campos()

        self.entry_id.config(state='normal')
        self.entry_id.insert(0, item_values[0])
        self.entry_id.config(state='readonly')
        
        self.entry_id_caminhao.insert(0, item_values[1])
        self.entry_id_cliente.insert(0, item_values[2])
        self.entry_tipo_carga.insert(0, item_values[3])
        self.entry_destino.insert(0, item_values[4])
        self.entry_horario_saida.insert(0, item_values[5])
        self.entry_horario_chegada.insert(0, item_values[6])
        self.entry_km_inicial.insert(0, item_values[7])
        self.entry_km_final.insert(0, item_values[8])

    def adicionar_saida(self):
        novo_id_num = self.gerar_novo_id()
        novo_id = f"S{novo_id_num:03d}" # Formata como S001, S002, etc.

        id_caminhao = self.entry_id_caminhao.get()
        id_cliente = self.entry_id_cliente.get()
        tipo_carga = self.entry_tipo_carga.get()
        destino = self.entry_destino.get()
        horario_saida = self.entry_horario_saida.get()
        horario_chegada = self.entry_horario_chegada.get()
        km_inicial = self.entry_km_inicial.get()
        km_final = self.entry_km_final.get()

        if not all([id_caminhao, id_cliente, tipo_carga, destino, horario_saida, km_inicial]):
            messagebox.showwarning("Entrada Inválida", "Campos 'ID Caminhão', 'ID Cliente', 'Tipo Carga', 'Destino', 'Horário Saída' e 'Quilometragem Inicial' são obrigatórios.")
            return

        # Preenche horário de saída se vazio (pode ser automático)
        if not horario_saida:
            horario_saida = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            self.entry_horario_saida.delete(0, tk.END)
            self.entry_horario_saida.insert(0, horario_saida)
            
        nova_saida = {
            self.id_chave: novo_id,
            "ID_Caminhao": id_caminhao,
            "ID_Cliente": id_cliente,
            "Tipo_Carga": tipo_carga,
            "Destino": destino,
            "Horario_Saida": horario_saida,
            "Horario_Chegada": horario_chegada,
            "Quilometragem_Inicial": km_inicial,
            "Quilometragem_Final": km_final
        }
        
        adicionar_registro(self.nome_arquivo, nova_saida)
        messagebox.showinfo("Sucesso", "Saída registrada com sucesso!")
        self.limpar_campos()
        self.carregar_saidas()

    def atualizar_saida(self):
        id_saida = self.entry_id.get()
        if not id_saida:
            messagebox.showwarning("Erro", "Selecione uma saída na tabela para atualizar.")
            return

        id_caminhao = self.entry_id_caminhao.get()
        id_cliente = self.entry_id_cliente.get()
        tipo_carga = self.entry_tipo_carga.get()
        destino = self.entry_destino.get()
        horario_saida = self.entry_horario_saida.get()
        horario_chegada = self.entry_horario_chegada.get()
        km_inicial = self.entry_km_inicial.get()
        km_final = self.entry_km_final.get()

        if not all([id_caminhao, id_cliente, tipo_carga, destino, horario_saida, km_inicial]):
            messagebox.showwarning("Entrada Inválida", "Campos obrigatórios não podem ser vazios.")
            return

        novos_dados = {
            "ID_Caminhao": id_caminhao,
            "ID_Cliente": id_cliente,
            "Tipo_Carga": tipo_carga,
            "Destino": destino,
            "Horario_Saida": horario_saida,
            "Horario_Chegada": horario_chegada,
            "Quilometragem_Inicial": km_inicial,
            "Quilometragem_Final": km_final
        }

        if atualizar_registro(self.nome_arquivo, self.id_chave, id_saida, novos_dados):
            messagebox.showinfo("Sucesso", "Saída atualizada com sucesso!")
            self.limpar_campos()
            self.carregar_saidas()
        else:
            messagebox.showerror("Erro", "ID da saída não encontrado.")

    def deletar_saida(self):
        id_saida = self.entry_id.get()
        if not id_saida:
            messagebox.showwarning("Erro", "Selecione uma saída na tabela para deletar.")
            return

        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar a saída ID: {id_saida}?"):
            if deletar_registro(self.nome_arquivo, self.id_chave, id_saida):
                messagebox.showinfo("Sucesso", "Saída deletada com sucesso!")
                self.limpar_campos()
                self.carregar_saidas()
            else:
                messagebox.showerror("Erro", "ID da saída não encontrado.")