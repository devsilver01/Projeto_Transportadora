"""
Nome do arquivo: tela_controle_luzes.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import tkinter as tk
from tkinter import ttk, messagebox
# Importar a função de envio de comando simulado
# Assumindo que você tem um arquivo funcional/funcional_arduino_luzes.py
# com uma função enviar_comando_luz(comando_char)
try:
    from funcional.funcional_arduino_luzes import enviar_comando_luz
except ImportError:
    # Fallback para simulação se o arquivo não for encontrado (para testes independentes)
    print("Aviso: 'funcional/funcional_arduino_luzes.py' não encontrado. Usando simulação interna.")
    def enviar_comando_luz(comando_char):
        print(f"Simulando envio para Arduino: Caractere '{comando_char}' enviado.")
        return True


class TelaControleLuzes(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#F0F0F0") # Cor de fundo padrão

        # Mapeamento interno para determinar status (Ligado/Desligado) a partir do comando
        # Baseado nos seus 'case' do Arduino:
        self.ligar_comandos = {'a', 'c', 'e', 'g', 'i', 'k', 'm', 'o', '1'} # Inclui '1' para ligar tudo
        self.desligar_comandos = {'b', 'd', 'f', 'h', 'j', 'l', 'n', 'p', '0'} # Inclui '0' para desligar tudo

        # Dicionário para armazenar as variáveis de status de cada luz individualmente
        self.light_status_vars = {} 
        self.last_feedback_letter_var = tk.StringVar(value="Nenhum comando enviado") # Variável para exibir a última letra

        self.criar_widgets()

    def criar_widgets(self):
        # Estilos básicos e claros (como definido no main.py simplificado)
        style = ttk.Style()
        style.configure("TLabel", background="#F0F0F0", foreground="#333333")
        style.configure("TButton", font=("Helvetica", 10))
        style.map("TButton", background=[("active", "#cccccc")])
        style.configure("TLabelframe", background="#F0F0F0", foreground="#333333")
        style.configure("TLabelframe.Label", background="#F0F0F0", foreground="#333333")

        lbl_titulo = ttk.Label(self, text="Controle Manual de Luzes", font=("Helvetica", 20, "bold"), background="#F0F0F0", foreground="#333333")
        lbl_titulo.pack(pady=20)

        # Frame para os botões de controle de setores individuais
        frame_controles = ttk.LabelFrame(self, text="Setores", padding="15 15 15 15")
        frame_controles.pack(pady=10, padx=20, fill="x")

        # Botões para cada setor/bloco de luzes (usando as letras exatas para o Arduino)
        self.create_luz_button(frame_controles, "Oficina", "a", "b", 0)
        self.create_luz_button(frame_controles, "Galpão - Bloco 1", "c", "d", 1)
        self.create_luz_button(frame_controles, "Galpão - Bloco 2", "e", "f", 2)
        self.create_luz_button(frame_controles, "Galpão - Bloco 3", "g", "h", 3)
        self.create_luz_button(frame_controles, "Escritório", "i", "j", 4)
        self.create_luz_button(frame_controles, "Corredor", "k", "l", 5) 
        self.create_luz_button(frame_controles, "Área de Serviço", "m", "n", 6)
        self.create_luz_button(frame_controles, "Área Externa", "o", "p", 7)

        # Botões para Ligar Tudo / Desligar Tudo (Controle Geral)
        frame_todos_botoes = ttk.LabelFrame(self, text="Controle Geral", padding="15 15 15 15")
        frame_todos_botoes.pack(pady=10, padx=20, fill="x")

        btn_acender_todos = ttk.Button(frame_todos_botoes, text="Acender Tudo", command=lambda: self.enviar_comando_global('1')) # Envia '1'
        btn_acender_todos.pack(side="left", padx=10, pady=5, expand=True, fill="x")

        btn_apagar_todos = ttk.Button(frame_todos_botoes, text="Apagar Tudo", command=lambda: self.enviar_comando_global('0')) # Envia '0'
        btn_apagar_todos.pack(side="right", padx=10, pady=5, expand=True, fill="x")

        # Label para exibir a última letra de feedback enviada
        lbl_last_feedback = ttk.Label(self, textvariable=self.last_feedback_letter_var, 
                                      font=("Helvetica", 12, "bold"), 
                                      background="#F0F0F0", foreground="#0056A0") 
        lbl_last_feedback.pack(pady=15)

        # Botão Voltar
        btn_voltar = ttk.Button(self, text="Voltar para o Início", command=lambda: self.controller.mostrar_tela("TelaInicial"))
        btn_voltar.pack(pady=20)

    def create_luz_button(self, parent_frame, nome_setor, acender_char, apagar_char, row):
        """
        Cria um par de botões (Acender/Apagar) para um setor de luzes, junto com seu status.
        Args:
            parent_frame: O frame pai para colocar os widgets.
            nome_setor: O nome do setor (ex: "Oficina").
            acender_char: O caractere que acende a luz (ex: 'a').
            apagar_char: O caractere que apaga a luz (ex: 'b').
            row: A linha no grid para posicionar os botões.
        """
        lbl_setor = ttk.Label(parent_frame, text=f"{nome_setor}:", font=("Helvetica", 11))
        lbl_setor.grid(row=row, column=0, padx=5, pady=5, sticky="w")

        status_key = nome_setor.replace(" ", "_").replace("-", "_").lower() 
        
        btn_acender = ttk.Button(parent_frame, text="Acender", 
                                 command=lambda c=acender_char, sk=status_key, ns=nome_setor: self.enviar_comando_individual(c, sk, ns)) 
        btn_acender.grid(row=row, column=1, padx=5, pady=5, sticky="ew")

        btn_apagar = ttk.Button(parent_frame, text="Apagar", 
                                command=lambda c=apagar_char, sk=status_key, ns=nome_setor: self.enviar_comando_individual(c, sk, ns))
        btn_apagar.grid(row=row, column=2, padx=5, pady=5, sticky="ew")
        
        # Cria e armazena a variável de status para este setor de luzes
        status_var = tk.StringVar(value="Desligado")
        self.light_status_vars[status_key] = status_var

        lbl_status = ttk.Label(parent_frame, textvariable=status_var, font=("Helvetica", 10, "italic"), foreground="gray")
        lbl_status.grid(row=row, column=3, padx=5, pady=5, sticky="w")

    def enviar_comando_individual(self, comando_char, status_key, nome_setor):
        """
        Chama a função para enviar o caractere de comando individual ao Arduino simulado, 
        atualiza o status na tela e exibe a letra de feedback.
        """
        if enviar_comando_luz(comando_char): # Envia a letra exata para o Arduino
            feedback_letter = comando_char # A própria letra enviada é o feedback

            status_text = "Desconhecido"
            if comando_char in self.ligar_comandos:
                status_text = "Ligado"
            elif comando_char in self.desligar_comandos:
                status_text = "Desligado"

            full_feedback_message = f"{nome_setor}: {status_text} ({feedback_letter})"

            # Atualiza o status visual do bloco de luz correspondente
            if status_key in self.light_status_vars:
                self.light_status_vars[status_key].set(status_text)
                
            # Atualiza a label geral de última letra enviada
            self.last_feedback_letter_var.set(f"Último comando: {full_feedback_message}")
            
            messagebox.showinfo("Comando Enviado", f"Comando '{comando_char}' enviado (simulado). Status: '{full_feedback_message}'")
        else:
            messagebox.showerror("Erro", "Falha ao enviar comando para controle de luzes.")

    def enviar_comando_global(self, comando_char_global: str):
        """
        Envia um comando global ('0' para desligar tudo, '1' para ligar tudo)
        e atualiza o status de todas as luzes na interface.
        """
        if enviar_comando_luz(comando_char_global): # Envia o comando global ('0' ou '1')
            status_text = "Ligado" if comando_char_global == '1' else "Desligado"
            
            # Atualiza o status de todos os labels de luzes individuais na interface
            for status_var in self.light_status_vars.values():
                status_var.set(status_text)
            
            # Mensagem de feedback global
            action_desc = "Ligar Tudo" if comando_char_global == '1' else "Desligar Tudo"
            full_feedback_message = f"Comando Geral: {action_desc} ({comando_char_global})"
            self.last_feedback_letter_var.set(f"Último comando: {full_feedback_message}")
            
            messagebox.showinfo("Comando Geral Enviado", f"Comando '{comando_char_global}' enviado (simulado). Ação: {action_desc}!")
        else:
            messagebox.showerror("Erro", "Falha ao enviar comando global.")
