"""
Nome do arquivo: funcional_arduino_luzes.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

def enviar_comando_luz(caractere_comando):
    """
    Simula o envio de um caractere para o Arduino para controlar as luzes.
    No uso real, você enviaria este caractere pela porta serial.
    """
    print(f"Simulando envio para Arduino: Caractere '{caractere_comando}' enviado para controlar luzes.")
    return True # Retorna True na simulação para indicar que o "envio" ocorreu