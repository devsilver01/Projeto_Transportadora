"""
Nome do arquivo: funcional_arduino_sensores.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

import random
import time

def ler_dados_sensores_simulados():
    """
    Simula a leitura de dados dos sensores: presença, luminosidade e temperatura.
    Retorna um dicionário com valores fictícios.
    """
    # Sensores de Presença/Distância (1: detectado, 0: não detectado)
    # Vamos simular uma baixa chance de detecção para não acionar o alarme o tempo todo
    presenca = 1 if random.random() < 0.1 else 0 # 10% de chance de detectar presença

    # Luminosidade (0 a 1023, onde 0 é escuro e 1023 é claro)
    luminosidade = random.randint(0, 1023)

    # Temperatura (em Celsius, com variação normal e ocasionalmente alta para fumaça)
    temperatura = random.uniform(20.0, 30.0)
    # 5% de chance de simular alta temperatura para acionar sirene
    if random.random() < 0.05:
        temperatura = random.uniform(40.0, 60.0) # Simula alta temperatura / fumaça

    return {
        "presenca": presenca,
        "luminosidade": int(luminosidade), # Garante que seja inteiro para exibir
        "temperatura": round(temperatura, 1) # Arredonda para uma casa decimal
    }

def acionar_alarme(status):
    """
    Simula o acionamento/desacionamento de um alarme.
    Na vida real, isso enviaria um comando para o Arduino.
    """
    if status:
        print(f"[{time.strftime('%H:%M:%S')}] ALARME ATIVADO: Movimento detectado!")
    else:
        print(f"[{time.strftime('%H:%M:%S')}] ALARME DESATIVADO: Ambiente seguro.")

def controlar_luzes_automatico(luminosidade_atual):
    """
    Simula o controle automático das luzes com base na luminosidade.
    """
    limite_luminosidade = 300 # Valor abaixo do qual as luzes deveriam acender
    if luminosidade_atual < limite_luminosidade:
        print(f"[{time.strftime('%H:%M:%S')}] LUZES ACESAS (AUTOMÁTICO): Luminosidade baixa ({luminosidade_atual}).")
        return "Luzes ligadas"
    else:
        print(f"[{time.strftime('%H:%M:%S')}] LUZES APAGADAS (AUTOMÁTICO): Luminosidade alta ({luminosidade_atual}).")
        return "Luzes apagadas"

def acionar_sirene_fumaca(temperatura_atual):
    """
    Simula o acionamento de uma sirene em caso de alta temperatura (fumaça).
    """
    limite_temperatura_fumaça = 35.0 # Limite para considerar fumaça/incêndio
    if temperatura_atual > limite_temperatura_fumaça:
        print(f"[{time.strftime('%H:%M:%S')}] SIRENE ACIONADA: Alta temperatura detectada ({temperatura_atual}°C)!")
        return "Sirene Ativada"
    else:
        return "Sirene Desativada"