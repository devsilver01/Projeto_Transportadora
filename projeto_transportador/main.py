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

        # --- CONFIGURAÇÃO SIMPLIFICADA DO TEMA ---
        style = ttk.Style(self)
        style.theme_use('clam') # Usando 'clam' como base simples

        # Estilos básicos e claros
        style.configure(".", background="#F0F0F0", foreground="#333333") # Fundo claro geral
        style.configure("TLabel", background="#F0F0F0", foreground="#333333")
        style.configure("Titulo.TLabel", font=("Helvetica", 24, "bold"), background="#F0F0F0", foreground="#0056A0") # Azul para destaque
        style.configure("Subtitulo.TLabel", font=("Helvetica", 20, "bold"), background="#F0F0F0", foreground="#0056A0")

        style.configure("TButton", font=("Helvetica", 11, "bold"), background="#007ACC", foreground="white", padding=10, relief="flat")
        style.map("TButton", background=[("active", "#0056A0"), ("pressed", "#003A60")])

        style.configure("TEntry", fieldbackground="white", foreground="black", bordercolor="#CCCCCC")
        style.configure("TLabelframe", background="#F0F0F0", foreground="#333333", bordercolor="#CCCCCC")
        style.configure("TLabelframe.Label", background="#F0F0F0", foreground="#333333")

        style.configure("Treeview", background="white", foreground="black", fieldbackground="white", bordercolor="#CCCCCC")
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#DDDDDD", foreground="#333333")
        style.map("Treeview", background=[("selected", "#B0D0F0")], foreground=[("selected", "black")]) # Seleção em azul claro

        style.configure("Vertical.TScrollbar", background="#DDDDDD", troughcolor="#F0F0F0")
        # --- FIM DA CONFIGURAÇÃO SIMPLIFICADA DO TEMA ---


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
