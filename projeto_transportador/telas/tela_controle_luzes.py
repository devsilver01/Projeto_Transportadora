"""
Nome do arquivo: tela_controle_luzes.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import tkinter as tk
from tkinter import ttk, messagebox
from funcional.funcional_arduino_luzes import enviar_comando_luz

class TelaControleLuzes(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#F0F0F0")

        self.criar_widgets()

    def criar_widgets(self):
        lbl_titulo = ttk.Label(self, text="Controle Manual de Luzes", font=("Helvetica", 20, "bold"), background="#F0F0F0", foreground="#333333")
        lbl_titulo.pack(pady=20)

        # Frame para os botões de controle
        frame_controles = ttk.LabelFrame(self, text="Setores", padding="15 15 15 15")
        frame_controles.pack(pady=10, padx=20, fill="x")

        # Botões para cada setor/bloco de luzes
        # Oficina
        self.create_luz_button(frame_controles, "Oficina", "O", 0)

        # Galpão (3 blocos)
        self.create_luz_button(frame_controles, "Galpão - Bloco 1", "G1", 1)
        self.create_luz_button(frame_controles, "Galpão - Bloco 2", "G2", 2)
        self.create_luz_button(frame_controles, "Galpão - Bloco 3", "G3", 3)

        # Escritório
        self.create_luz_button(frame_controles, "Escritório", "E", 4)

        # Corredor
        self.create_luz_button(frame_controles, "Corredor", "C", 5)

        # Área de Serviço
        self.create_luz_button(frame_controles, "Área de Serviço", "S", 6)

        # Área Externa
        self.create_luz_button(frame_controles, "Área Externa", "X", 7)

        # Botão Voltar
        btn_voltar = ttk.Button(self, text="Voltar para o Início", command=lambda: self.controller.mostrar_tela("TelaInicial"))
        btn_voltar.pack(pady=20)

    def create_luz_button(self, parent_frame, nome_setor, prefixo_comando, row):
        """
        Cria um par de botões (Acender/Apagar) para um setor de luzes.
        """
        lbl_setor = ttk.Label(parent_frame, text=f"{nome_setor}:", background="#F0F0F0", font=("Helvetica", 11))
        lbl_setor.grid(row=row, column=0, padx=5, pady=5, sticky="w")

        btn_acender = ttk.Button(parent_frame, text="Acender", 
                                 command=lambda: self.enviar_comando(f"{prefixo_comando}1")) # Ex: O1 para Oficina Ligar
        btn_acender.grid(row=row, column=1, padx=5, pady=5, sticky="ew")

        btn_apagar = ttk.Button(parent_frame, text="Apagar", 
                                command=lambda: self.enviar_comando(f"{prefixo_comando}0")) # Ex: O0 para Oficina Desligar
        btn_apagar.grid(row=row, column=2, padx=5, pady=5, sticky="ew")
        
        # Adiciona um status para cada luz, para feedback visual
        status_var = tk.StringVar(value="Desligado")
        lbl_status = ttk.Label(parent_frame, textvariable=status_var, background="#F0F0F0", font=("Helvetica", 10, "italic"), foreground="gray")
        lbl_status.grid(row=row, column=3, padx=5, pady=5, sticky="w")
        
        # Armazena a variável de status para poder atualizá-la
        setattr(self, f"status_{prefixo_comando.lower()}", status_var)

    def enviar_comando(self, comando):
        """
        Chama a função para enviar o comando ao Arduino simulado e atualiza o status.
        """
        if enviar_comando_luz(comando):
            messagebox.showinfo("Comando Enviado", f"Comando '{comando}' para controle de luzes enviado (simulado).")
            # Atualiza o status visual
            prefixo = comando[:-1].lower()
            status_var = getattr(self, f"status_{prefixo}")
            if comando.endswith("1"):
                status_var.set("Ligado")
                messagebox.showinfo("Status Luz", f"Luz {prefixo.upper()} ligada.")
            else:
                status_var.set("Desligado")
                messagebox.showinfo("Status Luz", f"Luz {prefixo.upper()} desligada.")
        else:
            messagebox.showerror("Erro", "Falha ao enviar comando para controle de luzes.")