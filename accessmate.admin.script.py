import sqlite3
import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522

caminhoBanco = '/home/nti/AccessMate/'

# cria o objeto para leitura do RFID
reader = SimpleMFRC522()

# Configuracao do GPIO
PortaRelay = 23
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(PortaRelay, GPIO.OUT) # O Relay deve estar conectao ao pino PortaRelay
GPIO.output(PortaRelay, GPIO.LOW)

# Configuração do teclado matricial
linhas = [6, 13, 19, 26]  # Números dos pinos das linhas
colunas = [12, 16, 20, 21]  # Números dos pinos das colunas

for j in range(len(colunas)):
    GPIO.setup(colunas[j], GPIO.OUT)
    GPIO.output(colunas[j], 1)

for i in range(len(linhas)):
    GPIO.setup(linhas[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Mapeamento das teclas do teclado matricial 4x4
teclas = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# Função para ler o teclado matricial até que o asterisco seja pressionado
def ler_teclado_ate_asterisco(mensagem):
    print(mensagem)
    digitado = ""
    while True:
        for j in range(len(colunas)):
            GPIO.output(colunas[j], 0)
            for i in range(len(linhas)):
                if GPIO.input(linhas[i]) == 0:
                    tecla = teclas[i][j]
                    if tecla == '*':
                        return digitado
                    else:
                        digitado += tecla
                    while GPIO.input(linhas[i]) == 0:
                        pass
            GPIO.output(colunas[j], 1)

# Função para ler o teclado matricial
def ler_teclado(mensagem):
    print(mensagem)
    tecla = None
    while True:
        for j in range(len(colunas)):
            GPIO.output(colunas[j], 0)
            for i in range(len(linhas)):
                if GPIO.input(linhas[i]) == 0:
                    tecla = i * len(colunas) + j + 1  # 1-16
                    while GPIO.input(linhas[i]) == 0:
                        pass
                    return tecla
            GPIO.output(colunas[j], 1)

def criar_tabela():
    conn = sqlite3.connect('estagiarios.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS estagiarios
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT,
                       codigo TEXT,
                       tipo TEXT)''')
    conn.commit()
    conn.close()

def cadastrar_estagiario(nome, codigo, tipo):
    if verificar_estagiario(codigo):
        Imprimir("Codigo ja cadastrado. Tente novamente.")
        return False

    conn = sqlite3.connect(caminhoBanco + 'estagiarios.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO estagiarios (nome, codigo, tipo) VALUES (?, ?, ?)", (nome, codigo, tipo))
    conn.commit()
    conn.close()

def verificar_estagiario(codigo):
    print(f"O codigo foi: {codigo}")
    #return False
    conn = sqlite3.connect(caminhoBanco + 'estagiarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM estagiarios WHERE codigo=?", (codigo,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def excluir_estagiario(codigo):
    conn = sqlite3.connect(caminhoBanco + 'estagiarios.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM estagiarios WHERE codigo=?", (codigo,))
    conn.commit()
    conn.close()

def listar_estagiarios():
    conn = sqlite3.connect(caminhoBanco + 'estagiarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, nome FROM estagiarios")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def listar_acessos():
    conn = sqlite3.connect(caminhoBanco + 'estagiarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT acessos.codigo, estagiarios.nome, acessos.horario FROM acessos INNER JOIN estagiarios ON acessos.codigo = estagiarios.codigo;")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def abrir_fechadura():
    print("Abrindo a Fechadura...")
    GPIO.output(PortaRelay, GPIO.HIGH)
    time.sleep(0.5) # Mantem o relay acionado por meio segundo (aumentar se necessario)
    GPIO.output(PortaRelay, GPIO.LOW)
    print("Fechadura aberta.")

def main():
    criar_tabela()
    while True:
        print("Menu Principal")
        print("1) Cadastrar Estagiário")
        print("2) Verificar Estagiário")
        print("3) Excluir Estagiário")
        print("4) Listar Estagiários Cadastrados")
        print("5) Listar Acessos")
        print("6) Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("1) RFID")
            print("2) Senha")
            print("3) Voltar")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                print("Aproxime a TAG ou Cartao: ")
                codigo, text = reader.read()
                print("RFID: ", codigo)
                nome = input("Digite o nome do estagiário: ")
                cadastrar_estagiario(nome, codigo, 'RDID')
            elif escolha == '2':
                codigo = input("Digite a senha: ")
                nome = input("Digite o nome do estagiário: ")
                cadastrar_estagiario(nome, codigo, 'Senha')
            elif escolha == '3':
                continue

        elif opcao == '2':
            #codigo = input("Digite o código RFID ou a senha: ")
            print("Aguardando entrada do teclado matricial...")
            codigo = str(ler_teclado_ate_asterisco("Informe o codigo:"))

            resultado = verificar_estagiario(codigo)
            if resultado:
                print(f"Estagiário encontrado: {resultado[0]}")
                abrir_fechadura()
            else:
                print("Estagiário não cadastrado.")

        elif opcao == '3':
            codigo = input("Digite o código RFID ou a senha: ")
            resultado = verificar_estagiario(codigo)
            if resultado:
                print(f"Estagiário encontrado: {resultado[0]}")
                confirmacao = input("Deseja realmente excluir? (S/N): ")
                if confirmacao.upper() == 'S':
                    excluir_estagiario(codigo)

        elif opcao == '4':
            estagiarios = listar_estagiarios()
            print("Estagiários Cadastrados:")
            for estagiario in estagiarios:
                print(estagiario[0] + ' - ' + estagiario[1])

        elif opcao == '5':
            acessos = listar_acessos()
            print("Acessos:")
            for registro in acessos:
                print(registro[0] + ' - ' + registro[1] + ' - ' + registro[2])

        elif opcao == '6':
            break

if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()