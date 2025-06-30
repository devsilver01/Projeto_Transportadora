"""
Nome do arquivo: funcional_crud.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import os

CAMINHO_DADOS = os.path.join(os.path.dirname(__file__), '..', 'dados')

def ler_dados(nome_arquivo):
    """
    Lê os dados de um arquivo TXT e retorna uma lista de dicionários.
    A primeira linha é o cabeçalho.
    """
    caminho_completo = os.path.join(CAMINHO_DADOS, nome_arquivo)
    dados = []
    
    if not os.path.exists(caminho_completo):
        return [] 

    with open(caminho_completo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
        
        if not linhas:
            return [] 

        cabecalho = linhas[0].strip().split(';')
        
        for linha in linhas[1:]:
            valores = linha.strip().split(';')
            if len(valores) == len(cabecalho):
                registro = dict(zip(cabecalho, valores))
                dados.append(registro)
            
    return dados

def escrever_dados(nome_arquivo, dados):
    """
    Escreve uma lista de dicionários em um arquivo TXT, sobrescrevendo o conteúdo.
    Assume que 'dados' é uma lista de dicionários onde as chaves são os nomes das colunas.
    """
    caminho_completo = os.path.join(CAMINHO_DADOS, nome_arquivo)
    
    cabecalho_map = {
        'pecas.txt': "ID_Peca;Nome_Peca;Descricao;Quantidade;Localizacao_Estoque",
        'fornecedores.txt': "ID_Fornecedor;Nome_Fornecedor;Contato;Telefone;Email;Endereco_Rua;Endereco_Bairro;Endereco_Cidade",
        'caminhoes.txt': "ID_Caminhao;Marca;Modelo;Ano;Placa;Quilometragem_Atual;Data_Ultima_Manutencao",
        'funcionarios.txt': "ID_Funcionario;Nome_Funcionario;Cargo;Telefone;Email;Endereco_Rua;Endereco_Bairro;Endereco_Cidade",
        'clientes.txt': "ID_Cliente;Nome_Cliente;Contato;Telefone;Email;Endereco_Rua;Endereco_Bairro;Endereco_Cidade",
        'saidas_caminhoes.txt': "ID_Saida;ID_Caminhao;ID_Cliente;Tipo_Carga;Destino;Horario_Saida;Horario_Chegada;Quilometragem_Inicial;Quilometragem_Final",
        'galpoes.txt': "ID_Galpao;Nome_Galpao;Capacidade;Localizacao"
    }
    
    if not dados:
        cabecalho = cabecalho_map.get(nome_arquivo, "")
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            if cabecalho:
                f.write(cabecalho + '\n')
        return

    cabecalho = ';'.join(dados[0].keys())

    with open(caminho_completo, 'w', encoding='utf-8') as f:
        f.write(cabecalho + '\n')
        for registro in dados:
            valores = [str(registro.get(chave, '')) for chave in dados[0].keys()]
            f.write(';'.join(valores) + '\n')

def adicionar_registro(nome_arquivo, novo_registro):
    """
    Adiciona um novo registro a um arquivo TXT.
    'novo_registro' deve ser um dicionário.
    Retorna True em caso de sucesso, False em caso de falha.
    """
    try:
        dados_existentes = ler_dados(nome_arquivo)
        dados_existentes.append(novo_registro)
        escrever_dados(nome_arquivo, dados_existentes)
        return True
    except Exception as e:
        print(f"Erro ao adicionar registro em {nome_arquivo}: {e}")
        return False

def atualizar_registro(nome_arquivo, id_chave, id_valor, novos_dados):
    """
    Atualiza um registro existente em um arquivo TXT.
    id_chave: nome da coluna que identifica o registro (ex: 'ID_Peca').
    id_valor: valor do ID do registro a ser atualizado.
    novos_dados: dicionário com os campos a serem atualizados e seus novos valores.
    Retorna True se atualizou, False se não encontrou o registro.
    """
    dados = ler_dados(nome_arquivo)
    encontrado = False
    for i, registro in enumerate(dados):
        if str(registro.get(id_chave)) == str(id_valor):
            for chave, valor in novos_dados.items():
                registro[chave] = str(valor)
            dados[i] = registro
            encontrado = True
            break
    
    if encontrado:
        escrever_dados(nome_arquivo, dados)
        return True
    return False

def deletar_registro(nome_arquivo, id_chave, id_valor):
    """
    Deleta um registro de um arquivo TXT.
    id_chave: nome da coluna que identifica o registro.
    id_valor: valor do ID do registro a ser deletado.
    Retorna True se deletou, False se não encontrou.
    """
    dados = ler_dados(nome_arquivo)
    dados_antes_deletar = len(dados)
    
    dados_atualizados = [registro for registro in dados if str(registro.get(id_chave)) != str(id_valor)]
    
    if len(dados_atualizados) < dados_antes_deletar:
        escrever_dados(nome_arquivo, dados_atualizados)
        return True
    return False