"""
Nome do arquivo: tela_inicial.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import tkinter as tk
from tkinter import ttk

class TelaInicial(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#F0F0F0") # Cor de fundo leve

        self.criar_widgets()

    def criar_widgets(self):
        # Título do Aplicativo
        lbl_titulo = ttk.Label(self, text="TruckFlow Pro", font=("Helvetica", 24, "bold"), background="#F0F0F0", foreground="#333333")
        lbl_titulo.pack(pady=30)

        # Frame para os botões
        frame_botoes = ttk.Frame(self, padding="20 20 20 20")
        frame_botoes.pack(pady=10)
        
        # Estilo para os botões
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10, background="#4CAF50", foreground="white") # Exemplo de cor para o botão
        style.map("TButton", background=[("active", "#45a049")]) # Cor ao passar o mouse

        # Botões de Navegação
        btn_pecas = ttk.Button(frame_botoes, text="Gerenciar Peças", command=lambda: self.controller.mostrar_tela("TelaPecas"))
        btn_pecas.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        btn_fornecedores = ttk.Button(frame_botoes, text="Gerenciar Fornecedores", command=lambda: self.controller.mostrar_tela("TelaFornecedores"))
        btn_fornecedores.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        btn_caminhoes = ttk.Button(frame_botoes, text="Gerenciar Caminhões", command=lambda: self.controller.mostrar_tela("TelaCaminhoes"))
        btn_caminhoes.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        btn_funcionarios = ttk.Button(frame_botoes, text="Gerenciar Funcionários", command=lambda: self.controller.mostrar_tela("TelaFuncionarios"))
        btn_funcionarios.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        btn_clientes = ttk.Button(frame_botoes, text="Gerenciar Clientes", command=lambda: self.controller.mostrar_tela("TelaClientes"))
        btn_clientes.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        btn_saidas = ttk.Button(frame_botoes, text="Registro de Saídas", command=lambda: self.controller.mostrar_tela("TelaSaidas"))
        btn_saidas.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        btn_galpoes = ttk.Button(frame_botoes, text="Controle de Galpões", command=lambda: self.controller.mostrar_tela("TelaGalpoes"))
        btn_galpoes.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        btn_sensores = ttk.Button(frame_botoes, text="Monitoramento de Sensores", command=lambda: self.controller.mostrar_tela("TelaSensores"))
        btn_sensores.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        btn_controle_luzes = ttk.Button(frame_botoes, text="Controle de Luzes", command=lambda: self.controller.mostrar_tela("TelaControleLuzes"))
        btn_controle_luzes.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Configura as colunas para expandir igualmente
        frame_botoes.grid_columnconfigure(0, weight=1)
        frame_botoes.grid_columnconfigure(1, weight=1)