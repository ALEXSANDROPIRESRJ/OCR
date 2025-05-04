# 🔍 Leitor de Placas Veiculares com OCR

Este projeto realiza a leitura de placas de veículos a partir de imagens, utilizando **EasyOCR** e **OpenCV**. As imagens são pré-processadas para otimizar o reconhecimento óptico de caracteres (OCR) e detectar automaticamente placas no formato brasileiro.

## 📦 Estrutura do Projeto

- `imagens/`: Pasta onde você deve colocar as imagens a serem analisadas.
- `analisadas/`: Pasta onde as imagens processadas serão movidas (opcional, pode ser desativado no código).
- `ocr12.py`: Arquivo principal com toda a lógica de OCR.

## 🧠 Tecnologias Utilizadas

- Python 3.12.1
- EasyOCR
- OpenCV
- NumPy
- Expressões Regulares

## ⚙️ Instalação

```bash
pip install opencv-python
pip install easyocr
pip install numpy
