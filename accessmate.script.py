import sqlite3
import threading
import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

caminhoBanco = '/home/nti/AccessMate/'

#############################################################
#### Inicializa o display usando o endereco I2C 0x3C
##disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_address=0x3C)
#############################################################

#############################################################
#### 'logo_NTI_UEMG', 128x64px - Ta zoado, tem que arrumar
##logo_NTI_UEMG_byte_array = b'0x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\xff\xff\xff\xff\xff\xff\xff\xf1\xcc\x01\x1f\xff\xff\xff\xfd\xff\xff\xff\xff\xff\xff\xff\xff\xf1\xcc\x01\x1f\xff\xff\xff\xfd\xff\xe0\x00\x00\x7f\xff\xff\xff\xf0\xcf\x8f\x1f\xff\xff\xff\xfd\xff\xc3\xff\xfc\x7f\xff\xff\xff\xf0\x4f\x8f\x1f\xff\xff\xff\xfd\xff\xdf\xff\xfc\x7f\xff\xff\xff\xf2\x4f\x8f\x1f\xff\xff\xff\xfd\xff\x9f\x1f\xc0\x7f\xff\xff\xff\xf3\x0f\x8f\x1f\xff\xff\xff\xfd\xff\x9c\x0f\xa0\x7f\xff\xff\xff\xf3\x0f\x8f\x1f\xff\xff\xff\xfd\xff\x9b\x86\xf0\xff\xff\xff\xff\xf3\x8f\x8f\x1f\xff\xff\xff\xfd\xff\x86\x01\xd8\xff\xff\xff\xff\xf3\xcf\x8f\x1f\xff\xff\xff\xfd\xff\x9c\x0f\x0f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\xb8\x1e\x07\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\xe0\x00\x01\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\xc0\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\x80\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\x80\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\x00\x00\x07\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\x00\x3f\xff\xff\xfe\x40\x27\xdd\x9e\x60\x3c\xf8\x7f\x3f\xfd\xff\x0f\xff\xff\xff\xfe\x40\x37\xdd\xde\x60\x3c\x78\x1e\x3f\xfd\xff\xff\xff\xff\xff\xfe\x7d\xf7\xdd\xde\x7d\xf8\x7b\x9e\x1f\xfd\xff\xff\xff\xff\xff\xfe\x7d\xf7\xdd\xde\x7d\xfb\x79\x3e\xdf\xfd\xff\x76\x33\xb3\x7f\xfe\x7d\xf7\xdd\x9e\x7d\xf3\x38\x1c\xcf\xfd\xff\x76\xf3\x37\xff\xfe\x7d\xf7\xdd\xde\x7d\xf3\x3b\xdc\xcf\xfd\xff\x76\x34\xb6\x7f\xfe\x7d\xf3\x9d\xce\x7d\xe0\x1b\xd8\x07\xfd\xff\x76\xf7\xb7\x7f\xfe\x7d\xf0\x3d\xc0\xfd\xe7\x99\x19\xe7\xfd\xff\xb6\xf7\xb7\x7f\xfe\x7d\xfc\x7d\xe1\xfd\xef\xd8\x33\xe7\xfd\xff\xce\x17\xbc\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#############################################################

#############################################################
#### Configuracao do GPIO
PortaRelay = 23
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(PortaRelay, GPIO.OUT) # O Relay deve estar conectao ao pino PortaRelay
GPIO.output(PortaRelay, GPIO.LOW)
#### Fim Configuracao do GPIO
#############################################################

#############################################################
#### Configuração do teclado matricial
#-- Números dos pinos das linhas
linhas = [12, 16, 20, 21]

#-- Números dos pinos das colunas
colunas = [6, 13, 19, 26]

for j in range(len(colunas)):
    GPIO.setup(colunas[j], GPIO.OUT)
    GPIO.output(colunas[j], 1)

for i in range(len(linhas)):
    GPIO.setup(linhas[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

#-- Mapeamento das teclas do teclado matricial 4x4
teclas = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]
#### Fim Configuração do teclado matricial
#############################################################

#############################################################
#### Banco de Dados
def criar_tabela_estagiarios():
    conn = sqlite3.connect(caminhoBanco + 'estagiarios.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS estagiarios
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT,
                       codigo TEXT,
                       tipo TEXT)''')
    conn.commit()
    conn.close()

def criar_tabela_acessos():
    conn = sqlite3.connect(caminhoBanco + 'estagiarios.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS acessos
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       codigo TEXT,
                       horario DATETIME)''')
    conn.commit()
    conn.close()

def registrar_acesso(codigo):
    conn = sqlite3.connect(caminhoBanco + 'estagiarios.db')
    cursor = conn.cursor()
    horario = time.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("INSERT INTO acessos (codigo, horario) VALUES (?, ?)", (codigo, horario))
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

def listar_estagiarios():
    conn = sqlite3.connect(caminhoBanco + 'estagiarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM estagiarios")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

#### Fim Banco de Dados
#############################################################

#############################################################
#### Funcoes do Display
def display_image_from_byte_array(byte_array):

    # Inicialize o display usando o endereço I2C
    disp.begin()
    disp.clear()
    disp.display()

    # Crie uma imagem PIL a partir do array de bytes
    image = Image.frombytes('1', (128, 64), byte_array)

    # Mostre a imagem no display OLED
    disp.image(image)
    disp.display()

def display_icon(value):
    disp.begin()
    disp.clear()
    disp.display()

    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    draw = ImageDraw.Draw(image)

    if value == 1:
        draw.ellipse((32,16, 96, 48), outline = 255, fill = 0)
        draw.rectangle((62, 16, 66, 48), outline=255, fill=255)

    elif value == 2:
        draw.ellipse((32,16, 96, 48), outline = 255, fill = 0)
        draw.arc((44, 26, 84, 40), 0, 180, fill = 255)
        draw.ellipse((52,24, 56, 28), outline = 255, fill = 255)
        draw.ellipse((72,24, 76, 28), outline = 255, fill = 255)

    elif value == 3:
        draw.ellipse((32,16, 96, 48), outline = 255, fill = 0)
        draw.arc((44, 33, 84, 47), 180, 360, fill = 255)
        draw.ellipse((52,24, 56, 28), outline = 255, fill = 255)
        draw.ellipse((72,24, 76, 28), outline = 255, fill = 255)


    disp.image(image)
    disp.display()
#### Fim Funcoes do Display
#############################################################

#############################################################
#### Funcoes utilitarias
def abrir_fechadura():
    print("Abrindo a Fechadura...")
    GPIO.output(PortaRelay, GPIO.HIGH)
    time.sleep(0.5) # Mantem o relay acionado por meio segundo (aumentar se necessario)
    GPIO.output(PortaRelay, GPIO.LOW)
    print("Fechadura aberta.")

def autorizar(codigo):
    resultado = verificar_estagiario(codigo)
    if resultado:
        #display_icon(2)
        print(f"Estagiário encontrado: {resultado[0]}")
        registrar_acesso(codigo)
        abrir_fechadura()
    else:
        #display_icon(3)
        print("Estagiário não cadastrado.")

    # Espera para voltar o icone default
    time.sleep(3)
    #display_icon(1)

#### Fim Funcoes utilitarias
#############################################################

#############################################################
#### Threads
def read_rfid():
    # cria o objeto para leitura do RFID
    reader = SimpleMFRC522()

    while True:
        try:
            print("Aguardando RFID")
            codigo, text = reader.read()
            print(f"RFID: {codigo}")
            autorizar(codigo)
        finally:
            #GPIO.cleanup()
            print("OK")
            time.sleep(1)


def read_keyboard():
    codigo = ""
    while True:
        time.sleep(0.1)
        for j in range(len(colunas)):
            GPIO.output(colunas[j], 0)
            for i in range(len(linhas)):
                if GPIO.input(linhas[i]) == 0:
                    tecla = teclas[i][j]
                    if tecla == '*':
                        print(f"Entrou com Teclado: {codigo}")
                        autorizar(codigo)
                        codigo = ""
                    else:
                        codigo += tecla
                        print(f"\r{codigo}", end="")
                        time.sleep(0.4)

                    while GPIO.input(linhas[i]) == 0:
                        pass
            GPIO.output(colunas[j], 1)

#### Fim Threads
#############################################################

#############################################################
#### MAIN
def main():
    # Exibe o icone default
    #display_icon(1)

    # Threads para as funcoes de entrada
    rfid_thread = threading.Thread(target=read_rfid)
    keyboard_thread = threading.Thread(target=read_keyboard)

    # Iniciar
    rfid_thread.start()
    keyboard_thread.start()

    # Finalizar
    rfid_thread.join()
    keyboard_thread.join()
#### Fim MAIN
#############################################################

if __name__ == "__main__":
    try:
        criar_tabela_estagiarios()
        criar_tabela_acessos()
        main()
    finally:
        GPIO.cleanup()