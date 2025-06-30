"""
Nome do arquivo: tela_controle_luzes.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import tkinter as tk
from tkinter import ttk, messagebox
try:
    from funcional.funcional_arduino_luzes import enviar_comando_luz
except ImportError:
    print("Aviso: 'funcional/funcional_arduino_luzes.py' não encontrado. Usando simulação interna.")
    def enviar_comando_luz(comando_char):
        print(f"Simulando envio para Arduino: Caractere '{comando_char}' enviado.")
        return True


class TelaControleLuzes(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#F0F0F0")

        self.ligar_comandos = {'a', 'c', 'e', 'g', 'i', 'k', 'm', 'o', '1'}
        self.desligar_comandos = {'b', 'd', 'f', 'h', 'j', 'l', 'n', 'p', '0'}

        self.light_status_vars = {} 
        self.last_feedback_letter_var = tk.StringVar(value="Nenhum comando enviado")

        self.criar_widgets()

    def criar_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", background="#F0F0F0", foreground="#333333")
        
        style.theme_use("clam") 
        
        style.configure("TButton", 
                        font=("Helvetica", 8),
                        background="#007BFF",
                        foreground="white",
                        borderwidth=1,
                        focusthickness=3,
                        focuscolor="none")
        style.map("TButton", 
                  background=[("active", "#0056b3"),
                              ("pressed", "#004085")],
                  foreground=[("active", "white"),
                              ("pressed", "white")])

        style.configure("AcenderTudo.TButton", 
                        font=("Helvetica", 8),
                        background="#28a745",
                        foreground="white",
                        borderwidth=1,
                        focusthickness=3,
                        focuscolor="none")
        style.map("AcenderTudo.TButton", 
                  background=[("active", "#218838"), 
                              ("pressed", "#1e7e34")],
                  foreground=[("active", "white"),
                              ("pressed", "white")])

        style.configure("ApagarTudo.TButton", 
                        font=("Helvetica", 8),
                        background="#dc3545",
                        foreground="white",
                        borderwidth=1,
                        focusthickness=3,
                        focuscolor="none")
        style.map("ApagarTudo.TButton", 
                  background=[("active", "#c82333"), 
                              ("pressed", "#bd2130")],
                  foreground=[("active", "white"),
                              ("pressed", "white")])

        style.configure("TLabelframe", background="#F0F0F0", foreground="#333333")
        style.configure("TLabelframe.Label", background="#F0F0F0", foreground="#333333")

        lbl_titulo = ttk.Label(self, text="Controle Manual de Luzes", font=("Helvetica", 20, "bold"), background="#F0F0F0", foreground="#333333")
        lbl_titulo.pack(pady=20)

        frame_controles = ttk.LabelFrame(self, text="Setores", padding="15 15 15 15")
        frame_controles.pack(pady=10, padx=20, fill="x", expand=True)

        frame_controles.grid_columnconfigure(0, weight=1)
        frame_controles.grid_columnconfigure(1, weight=1)
        frame_controles.grid_columnconfigure(2, weight=1) 
        frame_controles.grid_columnconfigure(3, weight=1) 
        frame_controles.grid_columnconfigure(4, weight=1) 
        frame_controles.grid_columnconfigure(5, weight=1)
        frame_controles.grid_columnconfigure(6, weight=1)

        self.create_luz_button_grid(frame_controles, "Oficina", "a", "b", 0, 0) 
        self.create_luz_button_grid(frame_controles, "Galpão - Bloco 1", "c", "d", 1, 0)
        self.create_luz_button_grid(frame_controles, "Galpão - Bloco 2", "e", "f", 2, 0)
        self.create_luz_button_grid(frame_controles, "Galpão - Bloco 3", "g", "h", 3, 0)

        self.create_luz_button_grid(frame_controles, "Escritório", "i", "j", 0, 4) 
        self.create_luz_button_grid(frame_controles, "Corredor", "k", "l", 1, 4) 
        self.create_luz_button_grid(frame_controles, "Área de Serviço", "m", "n", 2, 4)
        self.create_luz_button_grid(frame_controles, "Área Externa", "o", "p", 3, 4)

        frame_todos_botoes = ttk.LabelFrame(self, text="Controle Geral", padding="15 15 15 15")
        frame_todos_botoes.pack(pady=10, padx=20, fill="x", expand=True)

        btn_acender_todos = ttk.Button(frame_todos_botoes, text="Acender Tudo", 
                                        command=lambda: self.enviar_comando_global('1'),
                                        style="AcenderTudo.TButton")
        btn_acender_todos.pack(side="left", padx=5, pady=3, expand=True, fill="x")

        btn_apagar_todos = ttk.Button(frame_todos_botoes, text="Apagar Tudo", 
                                       command=lambda: self.enviar_comando_global('0'),
                                       style="ApagarTudo.TButton")
        btn_apagar_todos.pack(side="right", padx=5, pady=3, expand=True, fill="x")

        lbl_last_feedback = ttk.Label(self, textvariable=self.last_feedback_letter_var, 
                                      font=("Helvetica", 12, "bold"), 
                                      background="#F0F0F0", foreground="#0056A0") 
        lbl_last_feedback.pack(pady=15)

        btn_voltar = ttk.Button(self, text="Voltar para o Início", command=lambda: self.controller.mostrar_tela("TelaInicial"))
        btn_voltar.pack(pady=20, padx=20, fill="x")

    def create_luz_button_grid(self, parent_frame, nome_setor, acender_char, apagar_char, row, col_offset):
        """Cria um par de botões (Acender/Apagar) para um setor de luzes, junto com seu status,
        posicionando-os usando grid com um offset de coluna.
        """
        lbl_setor = ttk.Label(parent_frame, text=f"{nome_setor}:", font=("Helvetica", 10))
        lbl_setor.grid(row=row, column=col_offset, padx=(5, 2), pady=3, sticky="w")

        status_key = nome_setor.replace(" ", "_").replace("-", "_").lower() 
        
        btn_acender = ttk.Button(parent_frame, text="Acender", 
                                 command=lambda c=acender_char, sk=status_key, ns=nome_setor: self.enviar_comando_individual(c, sk, ns)) 
        btn_acender.grid(row=row, column=col_offset + 1, padx=2, pady=3, sticky="ew")

        btn_apagar = ttk.Button(parent_frame, text="Apagar", 
                                command=lambda c=apagar_char, sk=status_key, ns=nome_setor: self.enviar_comando_individual(c, sk, ns))
        btn_apagar.grid(row=row, column=col_offset + 2, padx=2, pady=3, sticky="ew")
        
        status_var = tk.StringVar(value="Desligado")
        self.light_status_vars[status_key] = status_var

        lbl_status = ttk.Label(parent_frame, textvariable=status_var, font=("Helvetica", 9, "italic"), foreground="gray")
        lbl_status.grid(row=row, column=col_offset + 3, padx=(2, 5), pady=3, sticky="w")

    def enviar_comando_individual(self, comando_char, status_key, nome_setor):
        """Chama a função para enviar o caractere de comando individual ao Arduino simulado, 
        atualiza o status na tela e exibe a letra de feedback.
        """
        if enviar_comando_luz(comando_char):
            feedback_letter = comando_char

            status_text = "Desconhecido"
            if comando_char in self.ligar_comandos:
                status_text = "Ligado"
            elif comando_char in self.desligar_comandos:
                status_text = "Desligado"

            full_feedback_message = f"{nome_setor}: {status_text} ({feedback_letter})"

            if status_key in self.light_status_vars:
                self.light_status_vars[status_key].set(status_text)
                
            self.last_feedback_letter_var.set(f"Último comando: {full_feedback_message}")
            
            messagebox.showinfo("Comando Enviado", f"Comando '{comando_char}' enviado (simulado). Status: '{full_feedback_message}'")
        else:
            messagebox.showerror("Erro", "Falha ao enviar comando para controle de luzes.")

    def enviar_comando_global(self, comando_char_global: str):
        """Envia um comando global ('0' para desligar tudo, '1' para ligar tudo)
        e atualiza o status de todas as luzes na interface.
        """
        if enviar_comando_luz(comando_char_global):
            status_text = "Ligado" if comando_char_global == '1' else "Desligado"
            
            for status_var in self.light_status_vars.values():
                status_var.set(status_text)
            
            action_desc = "Ligar Tudo" if comando_char_global == '1' else "Desligar Tudo"
            full_feedback_message = f"Comando Geral: {action_desc} ({comando_char_global})"
            self.last_feedback_letter_var.set(f"Último comando: {full_feedback_message}")
            
            messagebox.showinfo("Comando Geral Enviado", f"Comando '{comando_char_global}' enviado (simulado). Ação: {action_desc}!")
        else:
            messagebox.showerror("Erro", "Falha ao enviar comando global.")