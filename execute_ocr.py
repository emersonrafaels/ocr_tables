from inspect import stack
import re

from dynaconf import settings

from UTILS.image_ocr import ocr_functions
from UTILS.extract_infos import get_matchs_strings, get_matchs_line


class Execute_OCR():

    def __init__(self):

        pass


    def pos_processing_cnpj(text_input, pattern):

        # MANTENDO APENAS NÚMEROS
        text_only_numbers = re.sub(pattern=pattern, string=text_input, repl="").strip()

        output = "{}.{}.{}/{}-{}".format(text_only_numbers[:2],
                                         text_only_numbers[2:5],
                                         text_only_numbers[8:12],
                                         text_only_numbers[12:])

        return output


    def pos_processing_faturamento(text_input):

        # MANTENDO APENAS NÚMEROS
        output = [result for result in text_input.split(" ") if result != "R$" and result != "RS"]

        return output


    def orchestra_ocr(dir_image):

        # INICIANDO AS VARIÁVEIS RESULTANTES
        result_ocr = ""
        list_result_cnpj = ""
        json_result = []

        # REALIZANDO O OCR SOBRE A IMAGEM
        result_ocr = ocr_functions.Orquestra_OCR(dir_image)

        # OBTENDO - CNPJ
        list_result_cnpj = get_matchs_line(result_ocr, settings.PATTERN_CNPJ)

        # FORMATANDO O RESULTADO OBTIDO - CNPJ
        cnpj = [Execute_OCR.pos_processing_cnpj(value[0]) for value in list_result_cnpj]

        return result_ocr, cnpj, json_result