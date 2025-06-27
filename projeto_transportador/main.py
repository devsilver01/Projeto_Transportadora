"""
Nome do arquivo: main.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import tkinter as tk
from tkinter import ttk, messagebox

# Importa as telas
from telas.tela_inicial import TelaInicial
from telas.tela_pecas import TelaPecas
from telas.tela_fornecedores import TelaFornecedores
from telas.tela_caminhoes import TelaCaminhoes
from telas.tela_funcionarios import TelaFuncionarios
from telas.tela_clientes import TelaClientes
from telas.tela_saidas import TelaSaidas
from telas.tela_galpoes import TelaGalpoes
from telas.tela_sensores import TelaSensores
from telas.tela_controle_luzes import TelaControleLuzes

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("TruckFlow Pro - Gerenciamento de Transportadora")
        self.geometry("1000x700") 
        self.minsize(800, 600) 

        # --- AQUI É ONDE VOCÊ MUDA O TEMA ---
        style = ttk.Style(self)
        # Tente diferentes temas: 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative', 'winnative'
        # Em alguns sistemas operacionais, 'clam' ou 'alt' podem oferecer mais personalização de cores.
        style.theme_use('clam') 
        # --- FIM DA MUDANÇA DE TEMA ---

        # Container onde as diferentes telas serão empilhadas
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.active_frame_name = None 
        
        for F in (TelaInicial, TelaPecas, TelaFornecedores, TelaCaminhoes, 
                  TelaFuncionarios, TelaClientes, TelaSaidas, TelaGalpoes, 
                  TelaSensores, TelaControleLuzes):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela("TelaInicial")

    def mostrar_tela(self, page_name):
        if self.active_frame_name == "TelaSensores" and page_name != "TelaSensores":
            sensor_frame = self.frames["TelaSensores"]
            if hasattr(sensor_frame, 'parar_monitoramento'):
                sensor_frame.parar_monitoramento()
        
        self.active_frame_name = page_name

        frame = self.frames[page_name]
        frame.tkraise()
        
        display_name = page_name.replace('Tela', '')
        if display_name == 'Pecas': display_name = 'Peças'
        elif display_name == 'Saidas': display_name = 'Saídas'
        elif display_name == 'Galpoes': display_name = 'Galpões'
        display_name = ''.join([' ' + char if char.isupper() else char for char in display_name]).strip()
        self.title(f"TruckFlow Pro - {display_name}")

        if page_name == "TelaSensores":
            if hasattr(frame, 'iniciar_monitoramento'):
                frame.iniciar_monitoramento()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()