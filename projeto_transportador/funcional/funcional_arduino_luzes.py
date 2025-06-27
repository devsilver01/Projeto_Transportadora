"""
Nome do arquivo: funcional_arduino_luzes.py
Equipe: Breno Vidal, Silvestre Ferreira, Rafael Vitor, Maria Luiza, Luis Felipe.
Turma: 91164
Semestre: 2025.1
"""

# Nota: Para a comunicação real com o Arduino, você precisaria do módulo `serial`
# import serial
# ser = None # Variável global para a porta serial

# Função para iniciar a comunicação serial (opcional, para teste real)
# def iniciar_serial(porta='/dev/ttyACM0', baud_rate=9600):
#     global ser
#     try:
#         ser = serial.Serial(porta, baud_rate, timeout=1)
#         print(f"Conectado ao Arduino na porta {porta} com {baud_rate} bps.")
#         return True
#     except serial.SerialException as e:
#         print(f"Erro ao conectar ao Arduino: {e}")
#         return False

# Função para fechar a comunicação serial (opcional, para teste real)
# def fechar_serial():
#     global ser
#     if ser and ser.is_open:
#         ser.close()
#         print("Conexão serial com Arduino fechada.")

def enviar_comando_luz(caractere_comando):
    """
    Simula o envio de um caractere para o Arduino para controlar as luzes.
    No uso real, você enviaria este caractere pela porta serial.
    """
    print(f"Simulando envio para Arduino: Caractere '{caractere_comando}' enviado para controlar luzes.")
    # Implementação real (descomente e configure se for testar com Arduino físico):
    # global ser
    # if ser and ser.is_open:
    #     try:
    #         ser.write(caractere_comando.encode())
    #         print(f"Comando '{caractere_comando}' enviado via serial.")
    #         return True
    #     except Exception as e:
    #         print(f"Erro ao enviar comando serial: {e}")
    #         return False
    # else:
    #     print("Porta serial não está aberta para enviar comando.")
    #     return False
    return True # Retorna True na simulação para indicar que o "envio" ocorreu