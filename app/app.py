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


import sys
from os import path
from pathlib import Path

from dynaconf import settings
from pydantic import validate_arguments

try:
    from app.src.CONFIG import config
    from app.execute_extract_table import Extract_Table
    from app.execute_ocr import Execute_OCR
    from app.src.UTILS.image_read import read_image_gray
    from app import execute_log
except ModuleNotFoundError:
    sys.path.append(path.join(str(Path(__file__).resolve().parent.parent), "app"))
    from app.src.CONFIG import config
    from app.execute_extract_table import Extract_Table
    from app.src.UTILS.image_read import read_image_gray
    from app.execute_ocr import Execute_OCR
    from app import execute_log


@validate_arguments
def orchestra_extract_table_ocr(files: bytes = None):

    # INICIANDO OS LOGS DO SISTEMA
    execute_log.startLog()

    # INICIANDO AS VARIÁVEIS QUE ARMAZENARÃO OS RESULTADOS
    results = ""
    json_result = {}

    if files is not None:

        # VALIDANDO SE DEVE HAVER EXTRAÇÃO DAS TABELAS
        if settings.VALIDATOR_EXTRACT_TABLE:

            # EXECUTANDO A PIPELINE PARA BUSCA E EXTRAÇÃO DAS TABELAS
            results = Extract_Table().main_extract_table(files)

        else:
            results.append({"image_file": read_image_gray(Extract_Table().orchestra_get_files(files)[-1]),
                            "table": None})

        # EXECUTANDO O OCR
        json_result = Execute_OCR().execute_pipeline_ocr(results)[0]

    return json_result
