"""

    ORQUESTRA A APLICAÇÃO DE OCR SOBRE UMA IMAGEM.
    OBTÉM CNPJ, MESES E VALORES DE FATURAMENTO.

    O OCR É APLICADO SOBRE A IMAGEM COMPLETA (dir_full_image)
    E SOBRE AS TABELAS (SE ENCONTRADAS) (dir_table_image).


    # Arguments
        dir_full_image              - Required : Caminho ds imagem completa (String)
        dir_table_image             - Required : Caminho dss tabelas encontradas (String)

    # Returns
        validador                   - Required : Validador de execução da função (Boolean)
        retorno_ocr                 - Required : Retorno do OCR (String | Dict)

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "22/03/2022"


from inspect import stack
import re

from dynaconf import settings

import execute_log
from UTILS.image_ocr import ocr_functions
from UTILS.extract_infos import get_matchs_strings, get_matchs_line


class Execute_OCR():

    def __init__(self):

        pass


    def pos_processing_cnpj(text_input, pattern):

        """

            REALIZA O PÓS PROCESSAMENTO (APÓS A OBTENÇÃO DO CNPJ, CASO HAJA NO TEXTO)
            E REALIZA A FORMATAÇÃO:
                1) MANTÉM APENAS OS NÚMEROS
                2) FORMATA O CNPJ COM PADRÃO "00.000.000/0000-00

            # Arguments
                text_input              - Required : CNPJ de input (String)
                pattern                 - Required : Pattern a ser utilizado (String)

            # Returns
                cnpj_result             - Required : CNPJ após formatação (String)

        """

        try:
            # MANTENDO APENAQS OS NÚMEROS DO CNPJ DE INPUT
            text_input_only_numbers = re.sub(pattern=pattern,
                                             repl="",
                                             string=text_input)

            # FORMATANDO O CNPJ OBTIDO
            cnpj_result = "{}.{}.{}/{}-{}".format(text_input_only_numbers[:2],
                                                  text_input_only_numbers[2:5],
                                                  text_input_only_numbers[5:8],
                                                  text_input_only_numbers[8:12],
                                                  text_input_only_numbers[12:])

            return cnpj_result

        except Exception as ex:
            execute_log.error("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

            return text_input


    def pos_processing_faturamento(text_input):

        # MANTENDO APENAS NÚMEROS
        output = [result for result in text_input.split(" ") if result != "R$" and result != "RS"]

        return output


    def execute_pipeline_ocr(self, dir_full_image, dir_table_image):

        """

            ORQUESTRA A APLICAÇÃO DE OCR SOBRE UMA IMAGEM.
            OBTÉM CNPJ, MESES E VALORES DE FATURAMENTO.

            O OCR É APLICADO SOBRE A IMAGEM COMPLETA (dir_full_image)
            E SOBRE AS TABELAS (SE ENCONTRADAS) (dir_table_image).

            # Arguments
                dir_full_image              - Required : Caminho ds imagem completa (String)
                dir_table_image             - Required : Caminho dss tabelas encontradas (String)

            # Returns
                validador                   - Required : Validador de execução da função (Boolean)
                retorno_ocr                 - Required : Retorno do OCR (String | Dict)

        """

        # INICIANDO AS VARIÁVEIS RESULTANTES
        result_ocr = ""
        json_result = {}
        json_result["cnpj"] = ""

        # REALIZANDO O OCR SOBRE A IMAGEM
        result_ocr = ocr_functions(dir_full_image).Orquestra_OCR()

        # OBTENDO - CNPJ
        list_result_cnpj = get_matchs_line(result_ocr, settings.PATTERN_CNPJ)

        # FORMATANDO O RESULTADO OBTIDO - CNPJ
        json_result["cnpj"] = [Execute_OCR.pos_processing_cnpj(value[-1],
                                                               settings.PATTERN_ONLY_NUMBERS) for value in list_result_cnpj]

        return result_ocr, json_result