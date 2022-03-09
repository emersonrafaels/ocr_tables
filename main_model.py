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


from dynaconf import settings

from execute_extract_table import Extract_Table
from execute_ocr import Execute_OCR
import execute_log

from UTILS.base64_encode_decode import image_to_base64

# INICIANDO OS LOGS DO SISTEMA
execute_log.startLog()

def result_extract_table(files):

    # EXECUTANDO A PIPELINE PARA BUSCA E EXTRAÇÃO DAS TABELAS
    results = Extract_Table().main_extract_table(files)

    for image, tables in results:

        # EXECUTANDO O OCR
        Execute_OCR().execute_pipeline_ocr(image, tables[0])

# DEFININDO A IMAGEM A SER UTILIZADA
files = [r"C:\Users\Emerson\Desktop\brainIAcs\MASSA_IMAGENS\CARTAS DE FATURAMENTO\Carta2.PNG"]

# CONVERTENDO A IMAGEM EM BASE64
files_base64 = [image_to_base64(file) for file in files]

result_extract_table(files)
