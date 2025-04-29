import cv2
import easyocr
import numpy as np
import re
import time
import os
import shutil
import warnings

# Início da contagem de tempo
inicio_total = time.time()
warnings.filterwarnings("ignore")

# Caminhos
pasta_entrada = r'C:/Users/fadami/Documents/OCRDOZERO/imagens'
pasta_saida = r'C:/Users/fadami/Documents/OCRDOZERO/analisadas'
os.makedirs(pasta_saida, exist_ok=True)

# Inicializa o EasyOCR uma vez (muito mais eficiente)
reader = easyocr.Reader(['en', 'pt'], gpu=False)

# Função: Pré-processamento da imagem
def preprocessar_imagem(imagem):
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    imagem_ampliada = cv2.resize(imagem_cinza, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    return imagem_ampliada

# Função: Realizar OCR usando EasyOCR
def realizar_ocr_easyocr(imagem):
    return reader.readtext(imagem, detail=0, width_ths=0.5, paragraph=False)

# Função: Limpar o texto OCR
def limpar_texto_ocr(texto):
    return re.sub(r'[^A-Z0-9]', '', texto.upper())

# Função: Encontrar padrões de placas
def encontrar_placas(texto):
    padrao = re.compile(r'[A-Z]{3}\d[A-Z]\d{2}|[A-Z]{3}\d{4}')
    return padrao.findall(texto)

# Função: Validar formato da placa
def validar_placa(placa):
    return bool(re.match(r'^[A-Z]{3}\d{4}$', placa) or re.match(r'^[A-Z]{3}\d[A-Z]\d{2}$', placa))

# Lista de imagens válidas na pasta de entrada
extensoes_validas = ['.jpg', '.jpeg', '.png', '.bmp']
imagens = [f for f in os.listdir(pasta_entrada) if os.path.splitext(f)[1].lower() in extensoes_validas]

print(f"🔍 Imagens encontradas: {len(imagens)}")

# Processamento das imagens
for nome_arquivo in imagens:
    caminho_imagem = os.path.join(pasta_entrada, nome_arquivo)

    if not os.path.exists(caminho_imagem):
        print(f"❌ Imagem não encontrada: {caminho_imagem}")
        continue

    print(f"\n📷 Processando: {nome_arquivo}")

    imagem = cv2.imread(caminho_imagem)
    if imagem is None:
        print("⚠️ Erro ao carregar imagem. Pulando...")
        continue

    imagem_processada = preprocessar_imagem(imagem)

    # OCR
    inicio_ocr = time.time()
    ocr_bruto = realizar_ocr_easyocr(imagem_processada)
    fim_ocr = time.time()

    texto_bruto = ''.join(ocr_bruto)
    texto_limpo = limpar_texto_ocr(texto_bruto)

    print("Texto bruto do OCR:", texto_bruto)
    print("Texto limpo:", texto_limpo)

    placas_detectadas = encontrar_placas(texto_limpo)
    placas_validas = list(set([p for p in placas_detectadas if validar_placa(p)]))

    if placas_validas:
        print("✅ Placas válidas detectadas:")
        for placa in placas_validas:
            print("-", placa)
    else:
        print("🚫 Nenhuma placa válida detectada.")

    fim_total = time.time()
    print(f"⏱ Tempo OCR: {fim_ocr - inicio_ocr:.2f} s")
    print(f"⏱ Tempo total: {fim_total - inicio_total:.2f} s")

    # Move imagem processada para a pasta de saída
    # caminho_destino = os.path.join(pasta_saida, nome_arquivo)
    # try:
    #    shutil.move(caminho_imagem, caminho_destino)
    #    print(f"📁 Imagem movida para: {caminho_destino}")
    # except FileNotFoundError:
    #    print(f"❌ Arquivo não encontrado ao tentar mover: {caminho_imagem}")
    # Pirão