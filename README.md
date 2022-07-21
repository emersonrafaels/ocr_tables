<h1 align="center">
    <img alt="OCR TABLES" title="#OCRTABLES" src="./assets/banner.png" />
</h1>

<h4 align="center"> 
	🚧 OCR TABLES 1.0 🚀 em desenvolvimento... 🚧
</h4>

<p align="center">
  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/emersonrafaels/ocr_tables?color=%2304D361">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/emersonrafaels/ocr_tables">

  	
  <a href="https://www.linkedin.com/in/emerson-rafael/">
    <img alt="Siga no Linkedin" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white">
  </a>
	
  
  <a href="https://github.com/emersonrafaels/ocr_tables/commits/main">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/emersonrafaels/ocr_tables">
  </a>

  <img alt="License" src="https://img.shields.io/badge/license-MIT-brightgreen">
   <a href="https://github.com/emersonrafaels/ocr_tables/stargazers">
    <img alt="Stargazers" src="https://img.shields.io/github/stars/emersonrafaels/ocr_tables?style=social">
  </a>
</p>


## 💻 Sobre o projeto

📦 **OCR TABLES** é um projeto para **Extração de tabela contidas em uma imagem e OCR sobre elas**

Atualmente funcionando para:

 1. Único arquivo de imagem
 2. Diretório contendo várias imagens
 3. Arquivo imagem codificado em base64

## 🛠  Tecnologias

As seguintes ferramentas foram usadas na construção do projeto:

- [Python]

## 🚀 Como executar o projeto

1. **Instalando**: pip install -r requirements.txt

Ex: Exemplo de execução:

```python
from main_model import orchestra_extract_table_ocr
from UTILS.base64_encode_decode import image_to_base64

# DEFININDO A IMAGEM A SER UTILIZADA
files = r"C:\Users\Emerson\Desktop\OCRTABLES\Carta5.PNG"

# REALIZANDO O OCR
result = orchestra_extract_table_ocr(image_to_base64(files))

print(result)
```

## ➊ Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas (O download pode ser realizado pela própria página do Python ou Anaconda):
[Python](https://www.anaconda.com/products/individual).

## [≝] Testes
Os testes estão na pasta: **TESTS/***.

## 📝 Licença

Este projeto está sob a licença MIT.

Feito com ❤️ por **Emerson Rafael** 👋🏽 [Entre em contato!](https://www.linkedin.com/in/emerson-rafael/)

[Python]: https://www.python.org/downloads/