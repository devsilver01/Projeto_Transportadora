"""
Nome do arquivo: tela_sensores.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime # Importe datetime para a função strftime
from funcional.funcional_arduino_sensores import ler_dados_sensores_simulados, acionar_alarme, controlar_luzes_automatico, acionar_sirene_fumaca

class TelaSensores(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#F0F0F0")
        self.loop_atualizacao = None # Para controlar o loop de atualização

        self.criar_widgets()
        # Não inicia o monitoramento aqui. Ele será chamado pelo MainApplication.mostrar_tela()
        # self.iniciar_monitoramento() 

    def criar_widgets(self):
        lbl_titulo = ttk.Label(self, text="Monitoramento de Sensores (Galpão)", font=("Helvetica", 20, "bold"), background="#F0F0F0", foreground="#333333")
        lbl_titulo.pack(pady=20)

        # Frame para os dados dos sensores
        frame_dados_sensores = ttk.LabelFrame(self, text="Leituras Atuais", padding="15 15 15 15")
        frame_dados_sensores.pack(pady=10, padx=20, fill="x")

        # Labels para exibir os dados dos sensores
        ttk.Label(frame_dados_sensores, text="Presença:", background="#F0F0F0", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.lbl_presenca_valor = ttk.Label(frame_dados_sensores, text="N/A", background="#F0F0F0", font=("Helvetica", 12, "bold"))
        self.lbl_presenca_valor.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.lbl_presenca_status = ttk.Label(frame_dados_sensores, text="Status: Aguardando...", background="#F0F0F0", font=("Helvetica", 10))
        self.lbl_presenca_status.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        ttk.Label(frame_dados_sensores, text="Luminosidade:", background="#F0F0F0", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.lbl_luminosidade_valor = ttk.Label(frame_dados_sensores, text="N/A", background="#F0F0F0", font=("Helvetica", 12, "bold"))
        self.lbl_luminosidade_valor.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.lbl_luminosidade_status = ttk.Label(frame_dados_sensores, text="Status: Aguardando...", background="#F0F0F0", font=("Helvetica", 10))
        self.lbl_luminosidade_status.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        ttk.Label(frame_dados_sensores, text="Temperatura:", background="#F0F0F0", font=("Helvetica", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.lbl_temperatura_valor = ttk.Label(frame_dados_sensores, text="N/A", background="#F0F0F0", font=("Helvetica", 12, "bold"))
        self.lbl_temperatura_valor.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.lbl_temperatura_status = ttk.Label(frame_dados_sensores, text="Status: Aguardando...", background="#F0F0F0", font=("Helvetica", 10))
        self.lbl_temperatura_status.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        
        # Última Atualização
        self.lbl_ultima_atualizacao = ttk.Label(self, text="Última atualização: --:--:--", background="#F0F0F0", font=("Helvetica", 9, "italic"))
        self.lbl_ultima_atualizacao.pack(pady=10)

        # Botão para voltar
        btn_voltar = ttk.Button(self, text="Voltar para o Início", command=self.parar_monitoramento_e_voltar)
        btn_voltar.pack(pady=20)

    def iniciar_monitoramento(self):
        """Inicia o loop de atualização dos dados dos sensores."""
        # Garante que não haja múltiplos loops rodando
        if self.loop_atualizacao:
            self.after_cancel(self.loop_atualizacao)
        self.atualizar_dados_sensores() # Chama a primeira atualização imediatamente
        self.loop_atualizacao = self.after(2000, self.atualizar_dados_sensores) # Configura o loop para atualizar a cada 2 segundos

    def parar_monitoramento(self):
        """Para o loop de atualização dos sensores."""
        if self.loop_atualizacao:
            self.after_cancel(self.loop_atualizacao)
            self.loop_atualizacao = None # Reseta a variável para indicar que o loop não está ativo

    def parar_monitoramento_e_voltar(self):
        """Para o monitoramento e retorna para a tela inicial."""
        self.parar_monitoramento() # Chama o método para parar
        self.controller.mostrar_tela("TelaInicial")

    def atualizar_dados_sensores(self):
        """Atualiza os dados exibidos na tela com base nas leituras simuladas dos sensores."""
        dados = ler_dados_sensores_simulados()
        
        # Atualiza Presença
        self.lbl_presenca_valor.config(text=f"{'Detectado' if dados['presenca'] == 1 else 'Nenhum'}")
        if dados['presenca'] == 1:
            self.lbl_presenca_valor.config(foreground="red")
            self.lbl_presenca_status.config(text="Status: ALARME ATIVADO!", foreground="red")
            acionar_alarme(True)
        else:
            self.lbl_presenca_valor.config(foreground="green")
            self.lbl_presenca_status.config(text="Status: Seguro", foreground="green")
            acionar_alarme(False) # Apenas para o print de desativado

        # Atualiza Luminosidade
        self.lbl_luminosidade_valor.config(text=f"{dados['luminosidade']} LUX")
        luzes_status = controlar_luzes_automatico(dados['luminosidade'])
        if "acesas" in luzes_status:
            self.lbl_luminosidade_status.config(text="Status: Luzes Acionadas", foreground="orange")
        else:
            self.lbl_luminosidade_status.config(text="Status: Luzes Apagadas", foreground="blue")

        # Atualiza Temperatura
        self.lbl_temperatura_valor.config(text=f"{dados['temperatura']} °C")
        sirene_status = acionar_sirene_fumaca(dados['temperatura'])
        if "Ativada" in sirene_status:
            self.lbl_temperatura_status.config(text="Status: SIRENE ATIVADA!", foreground="red")
            self.lbl_temperatura_valor.config(foreground="red")
        else:
            self.lbl_temperatura_status.config(text="Status: Normal", foreground="green")
            self.lbl_temperatura_valor.config(foreground="green")

        # Atualiza o horário da última atualização
        self.lbl_ultima_atualizacao.config(text=f"Última atualização: {datetime.datetime.now().strftime('%H:%M:%S')}")

        # Agenda a próxima atualização (apenas se o monitoramento não foi parado)
        if self.loop_atualizacao is not None: # Verifica se o loop ainda está ativo
            self.loop_atualizacao = self.after(2000, self.atualizar_dados_sensores) # Reagenda a próxima chamada