"""
Nome do arquivo: tela_pecas.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import tkinter as tk
from tkinter import ttk, messagebox
from funcional.funcional_crud import ler_dados, adicionar_registro, atualizar_registro, deletar_registro

class TelaPecas(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Cor de fundo padrão para as telas (poderia vir de uma configuração global ou ser #F0F0F0)
        self.configure(bg="#F0F0F0") 
        # Nome do arquivo TXT. ESSENCIAL que inclua .txt
        self.nome_arquivo = "pecas.txt" 
        self.id_chave = "ID_Peca" # Nome da chave ID para esta tabela

        self.criar_widgets()
        self.carregar_pecas() # Carrega os dados na tabela ao iniciar a tela

    def criar_widgets(self):
        # Título da Tela
        # Usando estilo padrão para simplicidade.
        # Se quiser tema escuro, adicione 'style="Subtitulo.TLabel"' e configure no main.py
        lbl_titulo = ttk.Label(self, text="Gerenciar Peças", font=("Helvetica", 20, "bold"), background="#F0F0F0", foreground="#333333")
        lbl_titulo.pack(pady=20)

        # Frame de Entrada de Dados (caixa com título para organizar os campos)
        frame_entrada = ttk.LabelFrame(self, text="Dados da Peça", padding="15")
        frame_entrada.pack(pady=10, padx=20, fill="x")

        # Estilo básico para os widgets dentro desta tela
        # Removido estilos complexos para simplicidade
        style = ttk.Style()
        style.configure("TLabel", background="#F0F0F0", font=("Helvetica", 10))
        style.configure("TEntry", font=("Helvetica", 10))
        style.configure("TButton", font=("Helvetica", 10))
        style.map("TButton", background=[("active", "#cccccc")]) # Efeito ao passar o mouse

        # Campos de Entrada (Entry) e seus rótulos (Label)
        ttk.Label(frame_entrada, text="ID da Peça:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_id = ttk.Entry(frame_entrada, width=30)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entry_id.config(state='readonly') # ID não pode ser digitado, apenas visualizado/selecionado

        ttk.Label(frame_entrada, text="Nome da Peça:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome = ttk.Entry(frame_entrada, width=30)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Descrição:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_descricao = ttk.Entry(frame_entrada, width=30)
        self.entry_descricao.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Quantidade:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_quantidade = ttk.Entry(frame_entrada, width=30)
        self.entry_quantidade.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_entrada, text="Localização:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_localizacao = ttk.Entry(frame_entrada, width=30)
        self.entry_localizacao.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Botões de Ação (Adicionar, Atualizar, Deletar, Limpar)
        frame_botoes = ttk.Frame(self, padding="10")
        frame_botoes.pack(pady=10)

        btn_adicionar = ttk.Button(frame_botoes, text="Adicionar", command=self.adicionar_peca)
        btn_adicionar.grid(row=0, column=0, padx=5)

        btn_atualizar = ttk.Button(frame_botoes, text="Atualizar", command=self.atualizar_peca)
        btn_atualizar.grid(row=0, column=1, padx=5)

        btn_deletar = ttk.Button(frame_botoes, text="Deletar", command=self.deletar_peca)
        btn_deletar.grid(row=0, column=2, padx=5)

        btn_limpar = ttk.Button(frame_botoes, text="Limpar Campos", command=self.limpar_campos)
        btn_limpar.grid(row=0, column=3, padx=5)

        # Botão para voltar para a tela inicial
        btn_voltar = ttk.Button(self, text="Voltar para o Início", command=lambda: self.controller.mostrar_tela("TelaInicial"))
        btn_voltar.pack(pady=10)

        # Tabela de Peças (Treeview) para exibir os dados
        colunas = ("ID_Peca", "Nome_Peca", "Descricao", "Quantidade", "Localizacao_Estoque")
        self.tree_pecas = ttk.Treeview(self, columns=colunas, show="headings")
        
        # Configura os cabeçalhos da tabela
        for col in colunas:
            self.tree_pecas.heading(col, text=col.replace("_", " ")) # Troca '_' por espaço
            self.tree_pecas.column(col, width=100, anchor="center") # Largura e alinhamento
        
        # Ajustes de largura para colunas específicas
        self.tree_pecas.column("ID_Peca", width=70)
        self.tree_pecas.column("Nome_Peca", width=120)
        self.tree_pecas.column("Descricao", width=200)

        self.tree_pecas.pack(pady=10, padx=20, fill="both", expand=True) # Empacota a tabela

        # Barra de rolagem vertical para a tabela
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree_pecas.yview)
        self.tree_pecas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Configura a seleção de linha na tabela para preencher os campos de entrada
        self.tree_pecas.bind("<<TreeviewSelect>>", self.carregar_campos_selecao)

    def gerar_novo_id(self): 
        """Gera um novo ID para a peça, sequencialmente."""
        dados = ler_dados(self.nome_arquivo) # Lê os dados existentes
        if not dados:
            return 1 # Se não há dados, começa com 1
        # Encontra o maior ID existente e adiciona 1
        # Garante que p.get(self.id_chave, '0') seja tratado como string antes de verificar isdigit()
        max_id = max([int(str(p.get(self.id_chave, '0'))) if str(p.get(self.id_chave, '0')).isdigit() else 0 for p in dados])
        return max_id + 1

    def carregar_pecas(self):
        """Carrega e exibe as peças na tabela."""
        # Limpa todos os itens da tabela antes de recarregar
        for item in self.tree_pecas.get_children():
            self.tree_pecas.delete(item)

        pecas = ler_dados(self.nome_arquivo) # Lê as peças do arquivo TXT
        for peca in pecas:
            # Insere cada peça na tabela. Todos os valores são convertidos para string.
            self.tree_pecas.insert("", "end", values=[str(v) for v in peca.values()])

    def limpar_campos(self):
        """Limpa todos os campos de entrada da tela."""
        self.entry_id.config(state='normal') # Habilita temporariamente para limpar
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state='readonly') # Volta para somente leitura
        
        self.entry_nome.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.entry_localizacao.delete(0, tk.END)
    
    def carregar_campos_selecao(self, event):
        """Preenche os campos de entrada com os dados da linha selecionada na tabela."""
        selected_item = self.tree_pecas.selection() # Pega o item selecionado
        if not selected_item: # Se nada foi selecionado, não faz nada
            return

        item_values = self.tree_pecas.item(selected_item[0], "values") # Pega os valores do item
        
        self.limpar_campos() # Limpa os campos antes de preencher

        self.entry_id.config(state='normal')
        self.entry_id.insert(0, item_values[0])
        self.entry_id.config(state='readonly') # ID continua somente leitura
        
        self.entry_nome.insert(0, item_values[1])
        self.entry_descricao.insert(0, item_values[2])
        self.entry_quantidade.insert(0, item_values[3])
        self.entry_localizacao.insert(0, item_values[4])

    def adicionar_peca(self):
        """Adiciona uma nova peça ao arquivo TXT."""
        novo_id = str(self.gerar_novo_id()) # Gera um novo ID e converte para string
        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get()
        quantidade = self.entry_quantidade.get() # Pega a quantidade como string
        localizacao = self.entry_localizacao.get()

        # Validação básica: verifica se campos obrigatórios não estão vazios
        if not nome or not quantidade or not localizacao:
            messagebox.showwarning("Entrada Inválida", "Nome, Quantidade e Localização são obrigatórios.")
            return
        
        # REMOVIDO: a tentativa de converter quantidade para int, para simplicidade com TXT.
        # Todos os dados serão salvos como string.

        nova_peca = {
            self.id_chave: novo_id,
            "Nome_Peca": nome,
            "Descricao": descricao,
            "Quantidade": quantidade, # Salva como string diretamente
            "Localizacao_Estoque": localizacao
        }
        
        # Chama a função do funcional_crud para adicionar.
        # Ela agora retorna True/False.
        if adicionar_registro(self.nome_arquivo, nova_peca):
            messagebox.showinfo("Sucesso", "Peça adicionada com sucesso!")
            self.limpar_campos() # Limpa os campos após adicionar
            self.carregar_pecas() # Recarrega a tabela para mostrar a nova peça
        else:
            messagebox.showerror("Erro", "Não foi possível adicionar a peça.") # Mensagem de erro simples


    def atualizar_peca(self):
        """Atualiza uma peça existente no arquivo TXT."""
        id_peca = self.entry_id.get() # Pega o ID do campo (que foi preenchido pela seleção)
        if not id_peca:
            messagebox.showwarning("Erro", "Selecione uma peça na tabela para atualizar.")
            return

        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get()
        quantidade = self.entry_quantidade.get() # Pega a quantidade como string
        localizacao = self.entry_localizacao.get()

        if not nome or not quantidade or not localizacao:
            messagebox.showwarning("Entrada Inválida", "Nome, Quantidade e Localização são obrigatórios.")
            return

        # REMOVIDO: a tentativa de converter quantidade para int.
        # Todos os dados serão salvos como string.

        novos_dados = {
            "Nome_Peca": nome,
            "Descricao": descricao,
            "Quantidade": quantidade, # Salva como string diretamente
            "Localizacao_Estoque": localizacao
        }

        # Chama a função do funcional_crud para atualizar
        if atualizar_registro(self.nome_arquivo, self.id_chave, id_peca, novos_dados):
            messagebox.showinfo("Sucesso", "Peça atualizada com sucesso!")
            self.limpar_campos() # Limpa os campos após atualizar
            self.carregar_pecas() # Recarrega a tabela
        else:
            messagebox.showerror("Erro", "ID da peça não encontrado ou erro na atualização.")

    def deletar_peca(self):
        """Deleta uma peça do arquivo TXT."""
        id_peca = self.entry_id.get() # Pega o ID do campo
        if not id_peca:
            messagebox.showwarning("Erro", "Selecione uma peça na tabela para deletar.")
            return

        # Pede confirmação ao usuário antes de deletar
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar a peça ID: {id_peca}?"):
            # Chama a função do funcional_crud para deletar
            if deletar_registro(self.nome_arquivo, self.id_chave, id_peca):
                messagebox.showinfo("Sucesso", "Peça deletada com sucesso!")
                self.limpar_campos() # Limpa os campos
                self.carregar_pecas() # Recarrega a tabela
            else:
                messagebox.showerror("Erro", "ID da peça não encontrado ou erro na exclusão.")