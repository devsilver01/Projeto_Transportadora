"""
Nome do arquivo: funcional_crud.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import os

# Define o caminho base para a pasta de dados. Volta um nível e entra em 'dados'.
CAMINHO_DADOS = os.path.join(os.path.dirname(__file__), '..', 'dados')

def ler_dados(nome_arquivo):
    """
    Lê os dados de um arquivo TXT e retorna uma lista de dicionários.
    A primeira linha é o cabeçalho.
    """
    caminho_completo = os.path.join(CAMINHO_DADOS, nome_arquivo)
    dados = [] # Lista para guardar todos os registros
    
    # Verifica se o arquivo existe. Se não, retorna uma lista vazia.
    if not os.path.exists(caminho_completo):
        return [] 

    # Abre o arquivo para leitura
    with open(caminho_completo, 'r', encoding='utf-8') as f:
        linhas = f.readlines() # Lê todas as linhas do arquivo
        
        if not linhas: # Se o arquivo estiver vazio, retorna lista vazia
            return [] 

        # A primeira linha é o cabeçalho (nomes das colunas)
        cabecalho = linhas[0].strip().split(';')
        
        # Processa as demais linhas, que são os dados
        for linha in linhas[1:]:
            valores = linha.strip().split(';') # Divide a linha em valores
            # Cria um dicionário para cada linha, combinando cabeçalho e valores
            # Garante que o número de valores corresponde ao cabeçalho.
            if len(valores) == len(cabecalho):
                registro = dict(zip(cabecalho, valores))
                dados.append(registro)
            # Linhas com formato incorreto serão ignoradas silenciosamente para simplicidade
            
    return dados # Retorna a lista de dicionários com os dados

def escrever_dados(nome_arquivo, dados):
    """
    Escreve uma lista de dicionários em um arquivo TXT, sobrescrevendo o conteúdo.
    Assume que 'dados' é uma lista de dicionários onde as chaves são os nomes das colunas.
    """
    caminho_completo = os.path.join(CAMINHO_DADOS, nome_arquivo)
    
    # Mapeia cabeçalhos para cada tipo de arquivo, para garantir que sejam criados corretamente.
    cabecalho_map = {
        'pecas.txt': "ID_Peca;Nome_Peca;Descricao;Quantidade;Localizacao_Estoque",
        'fornecedores.txt': "ID_Fornecedor;Nome_Fornecedor;Contato;Telefone;Email;Endereco_Rua;Endereco_Bairro;Endereco_Cidade",
        'caminhoes.txt': "ID_Caminhao;Marca;Modelo;Ano;Placa;Quilometragem_Atual;Data_Ultima_Manutencao",
        'funcionarios.txt': "ID_Funcionario;Nome_Funcionario;Cargo;Telefone;Email;Endereco_Rua;Endereco_Bairro;Endereco_Cidade",
        'clientes.txt': "ID_Cliente;Nome_Cliente;Contato;Telefone;Email;Endereco_Rua;Endereco_Bairro;Endereco_Cidade",
        'saidas_caminhoes.txt': "ID_Saida;ID_Caminhao;ID_Cliente;Tipo_Carga;Destino;Horario_Saida;Horario_Chegada;Quilometragem_Inicial;Quilometragem_Final",
        'galpoes.txt': "ID_Galpao;Nome_Galpao;Capacidade;Localizacao"
    }
    
    # Se não houver dados, escreve apenas o cabeçalho adequado para o arquivo.
    if not dados:
        cabecalho = cabecalho_map.get(nome_arquivo, "")
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            if cabecalho:
                f.write(cabecalho + '\n')
        return

    # Pega o cabeçalho das chaves do primeiro dicionário na lista de dados.
    cabecalho = ';'.join(dados[0].keys())

    # Abre o arquivo para escrita (sobrescreve o conteúdo existente)
    with open(caminho_completo, 'w', encoding='utf-8') as f:
        f.write(cabecalho + '\n') # Escreve a linha do cabeçalho
        for registro in dados: # Para cada dicionário na lista de dados
            # Pega os valores do dicionário na ordem correta do cabeçalho e os converte para string
            valores = [str(registro.get(chave, '')) for chave in dados[0].keys()]
            f.write(';'.join(valores) + '\n') # Escreve a linha de dados

def adicionar_registro(nome_arquivo, novo_registro):
    """
    Adiciona um novo registro a um arquivo TXT.
    'novo_registro' deve ser um dicionário.
    Retorna True em caso de sucesso, False em caso de falha (simples).
    """
    try:
        dados_existentes = ler_dados(nome_arquivo) # Lê todos os dados atuais
        dados_existentes.append(novo_registro)      # Adiciona o novo registro na lista
        escrever_dados(nome_arquivo, dados_existentes) # Salva a lista atualizada no arquivo
        return True # Indica que a operação foi um sucesso
    except Exception as e:
        print(f"Erro ao adicionar registro em {nome_arquivo}: {e}") # Imprime o erro no console
        return False # Indica que houve uma falha

def atualizar_registro(nome_arquivo, id_chave, id_valor, novos_dados):
    """
    Atualiza um registro existente em um arquivo TXT.
    id_chave: nome da coluna que identifica o registro (ex: 'ID_Peca').
    id_valor: valor do ID do registro a ser atualizado.
    novos_dados: dicionário com os campos a serem atualizados e seus novos valores.
    Retorna True se atualizou, False se não encontrou o registro.
    """
    dados = ler_dados(nome_arquivo) # Lê todos os dados
    encontrado = False
    for i, registro in enumerate(dados): # Percorre cada registro
        # Compara o ID do registro com o ID que queremos atualizar (garante que ambos sejam string)
        if str(registro.get(id_chave)) == str(id_valor):
            # Atualiza os campos do registro com os novos dados
            for chave, valor in novos_dados.items():
                registro[chave] = str(valor) # Converte valor para string para o arquivo TXT
            dados[i] = registro # Atualiza o registro na lista
            encontrado = True
            break # Sai do loop assim que encontra e atualiza
    
    if encontrado: # Se o registro foi encontrado e atualizado
        escrever_dados(nome_arquivo, dados) # Salva a lista atualizada no arquivo
        return True
    return False # Retorna False se o registro não foi encontrado

def deletar_registro(nome_arquivo, id_chave, id_valor):
    """
    Deleta um registro de um arquivo TXT.
    id_chave: nome da coluna que identifica o registro.
    id_valor: valor do ID do registro a ser deletado.
    Retorna True se deletou, False se não encontrou.
    """
    dados = ler_dados(nome_arquivo) # Lê todos os dados
    dados_antes_deletar = len(dados) # Guarda a quantidade de registros antes de deletar
    
    # Cria uma nova lista, excluindo o registro com o ID_valor correspondente
    dados_atualizados = [registro for registro in dados if str(registro.get(id_chave)) != str(id_valor)]
    
    # Se o número de registros diminuiu, significa que um foi deletado
    if len(dados_atualizados) < dados_antes_deletar:
        escrever_dados(nome_arquivo, dados_atualizados) # Salva a nova lista no arquivo
        return True
    return False # Retorna False se o registro não foi encontrado para deletar