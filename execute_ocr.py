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

        try:
            # FORMATANDO O CNPJ OBTIDO
            output = "{}.{}.{}/{}-{}".format(text_input[:2],
                                             text_input[2:5],
                                             text_input[8:12],
                                             text_input[12:])

            return output

        except Exception as ex:
            execute_log.error("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

            return text_input


    def pos_processing_faturamento(text_input):

        # MANTENDO APENAS NÚMEROS
        output = [result for result in text_input.split(" ") if result != "R$" and result != "RS"]

        return output


    def execute_pipeline_ocr(self, dir_full_image, dir_table_image):

        # INICIANDO AS VARIÁVEIS RESULTANTES
        result_ocr = ""
        list_result_cnpj = ""
        json_result = []

        # REALIZANDO O OCR SOBRE A IMAGEM
        result_ocr = ocr_functions(dir_full_image).Orquestra_OCR()

        # OBTENDO - CNPJ
        list_result_cnpj = get_matchs_line(result_ocr, settings.PATTERN_CNPJ)

        # FORMATANDO O RESULTADO OBTIDO - CNPJ
        cnpj = [Execute_OCR.pos_processing_cnpj(value[-1], settings.PATTERN_CNPJ) for value in list_result_cnpj]

        return result_ocr, cnpj, json_result