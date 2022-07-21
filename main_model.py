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
__data_atualizacao__ = "22/03/2022"


from dynaconf import settings

from execute_extract_table import Extract_Table
from execute_ocr import Execute_OCR
import execute_log

def orchestra_extract_table_ocr(files):

    # INICIANDO OS LOGS DO SISTEMA
    execute_log.startLog()

    # INICIANDO AS VARIÁVEIS QUE ARMAZENARÃO OS RESULTADOS
    result_ocr = ""
    json_result = {}

    # EXECUTANDO A PIPELINE PARA BUSCA E EXTRAÇÃO DAS TABELAS
    results = Extract_Table().main_extract_table(files)

    for image, tables in results:

        # EXECUTANDO O OCR
        result_ocr, json_result = Execute_OCR().execute_pipeline_ocr(image, tables[0])

        print("RESULTADO OBTIDO:\n{}".format(result_ocr))
        print("JSON_RESULT:\n{}".format(json_result))


    return result_ocr, json_result
