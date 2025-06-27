"""
Nome do arquivo: funcional_crud.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import os

# Define o caminho base para a pasta de dados
CAMINHO_DADOS = os.path.join(os.path.dirname(__file__), '..', 'dados')

def ler_dados(nome_arquivo):
    """
    Lê os dados de um arquivo TXT e retorna uma lista de dicionários.
    A primeira linha é considerada o cabeçalho.
    """
    caminho_completo = os.path.join(CAMINHO_DADOS, nome_arquivo)
    dados = []
    if not os.path.exists(caminho_completo):
        return [] # Retorna lista vazia se o arquivo não existe

    with open(caminho_completo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
        if not linhas:
            return [] # Retorna lista vazia se o arquivo está vazio

        cabecalho = linhas[0].strip().split(';')
        for linha in linhas[1:]:
            valores = linha.strip().split(';')
            # Cria um dicionário para cada linha, associando valores ao cabeçalho
            registro = dict(zip(cabecalho, valores))
            dados.append(registro)
    return dados

def escrever_dados(nome_arquivo, dados):
    """
    Escreve uma lista de dicionários no arquivo TXT, sobrescrevendo o conteúdo.
    Assume que 'dados' já está no formato correto (lista de dicionários
    com as chaves correspondentes ao cabeçalho).
    """
    caminho_completo = os.path.join(CAMINHO_DADOS, nome_arquivo)
    
    if not dados: # Se não há dados para escrever, cria um arquivo vazio com cabeçalho
        if nome_arquivo == 'pecas.txt':
            cabecalho = "ID_Peca;Nome_Peca;Descricao;Quantidade;Localizacao_Estoque"
        elif nome_arquivo == 'fornecedores.txt':
            cabecalho = "ID_Fornecedor;Nome_Fornecedor;Contato;Telefone;Email;Endereco_Rua;Endereco_Bairro;Endereco_Cidade"
        elif nome_arquivo == 'caminhoes.txt':
            cabecalho = "ID_Caminhao;Marca;Modelo;Ano;Placa;Quilometragem_Atual;Data_Ultima_Manutencao"
        elif nome_arquivo == 'funcionarios.txt':
            cabecalho = "ID_Funcionario;Nome_Funcionario;Cargo;Telefone;Email;Endereco_Rua;Endereco_Bairro;Endereco_Cidade"
        elif nome_arquivo == 'clientes.txt':
            cabecalho = "ID_Cliente;Nome_Cliente;Contato;Telefone;Email;Endereco_Rua;Endereco_Bairro;Endereco_Cidade"
        elif nome_arquivo == 'saidas_caminhoes.txt':
            cabecalho = "ID_Saida;ID_Caminhao;ID_Cliente;Tipo_Carga;Destino;Horario_Saida;Horario_Chegada;Quilometragem_Inicial;Quilometragem_Final"
        elif nome_arquivo == 'galpoes.txt':
            cabecalho = "ID_Galpao;Nome_Galpao;Capacidade;Localizacao"
        else:
            cabecalho = "" # Caso o arquivo seja desconhecido
            
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            f.write(cabecalho + '\n')
        return

    # Extrai o cabeçalho do primeiro dicionário (assumindo que todos têm as mesmas chaves)
    cabecalho = ';'.join(dados[0].keys())

    with open(caminho_completo, 'w', encoding='utf-8') as f:
        f.write(cabecalho + '\n') # Escreve o cabeçalho
        for registro in dados:
            # Garante que a ordem dos valores é a mesma do cabeçalho
            valores = [str(registro[chave]) for chave in dados[0].keys()]
            f.write(';'.join(valores) + '\n')


def adicionar_registro(nome_arquivo, novo_registro):
    """
    Adiciona um novo registro ao arquivo TXT.
    'novo_registro' deve ser um dicionário com as chaves correspondentes ao cabeçalho.
    """
    dados_existentes = ler_dados(nome_arquivo)
    dados_existentes.append(novo_registro)
    escrever_dados(nome_arquivo, dados_existentes)


def atualizar_registro(nome_arquivo, id_chave, id_valor, novos_dados):
    """
    Atualiza um registro específico em um arquivo TXT.
    id_chave: o nome da chave que contém o ID (ex: 'ID_Peca').
    id_valor: o valor do ID do registro a ser atualizado.
    novos_dados: um dicionário com os novos valores para os campos.
    """
    dados = ler_dados(nome_arquivo)
    encontrado = False
    for i, registro in enumerate(dados):
        if registro.get(id_chave) == id_valor:
            # Atualiza os campos do registro com os novos dados
            for chave, valor in novos_dados.items():
                registro[chave] = valor
            dados[i] = registro
            encontrado = True
            break
    if encontrado:
        escrever_dados(nome_arquivo, dados)
        return True
    return False # Retorna False se o registro não foi encontrado

def deletar_registro(nome_arquivo, id_chave, id_valor):
    """
    Deleta um registro específico de um arquivo TXT.
    id_chave: o nome da chave que contém o ID (ex: 'ID_Peca').
    id_valor: o valor do ID do registro a ser deletado.
    """
    dados = ler_dados(nome_arquivo)
    dados_atualizados = [registro for registro in dados if registro.get(id_chave) != id_valor]
    
    if len(dados_atualizados) < len(dados): # Se o tamanho diminuiu, um registro foi removido
        escrever_dados(nome_arquivo, dados_atualizados)
        return True
    return False # Retorna False se o registro não foi encontrado