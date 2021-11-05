"""

    SERVIÇO PARA REALIZAÇÃO DE EXTRAÇÃO DE TABELAS E OCR SOBRE ELAS.

    1) EXTRAÇÃO DE TABELAS
    2) OCR SOBRE TABELAS

    # Arguments
        object                  - Required : Imagem para aplicação da tabela e OCR (Base64 | Path | Numpy Array)
    # Returns
        output_text             - Required : Textos da tabela após aplicação das
                                             técnicas de pré processamento,
                                             OCR e pós processamento (String)

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "05/11/2021"


from execute_extract_table import Extract_Table

files = [r"C:\Users\Emerson\Desktop\brainIAcs\MASSA_IMAGENS\CARTAS DE FATURAMENTO\Carta1.PNG"]

results = Extract_Table().main_extract_table(files)

for image, tables in results:
    print("\n".join(tables))
