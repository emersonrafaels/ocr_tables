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


def main_model(dir_image):

    # INICIANDO O JSON DE RESULTADO
    json_result = {"cnpj": "", "faturamento": ""}

    for file in dir_image:

        # ANALISANDO SE DEVE OCORRER EXTRAÇÃO DE TABELA
        if settings.EXTRACT_TABLE:

            # REALIZANDO A EXTRAÇÃO DA TABELA
            results = Extract_Table().main_extract_table(file)

            # OBTENDO AS TABELAS SALVAS
            for image, tables in results:
                print("\n".join(tables))


        # ENVIANDO A IMAGEM COMPLETA PARA OCR
        result_ocr = Execute_OCR().orchestra_ocr(file)
