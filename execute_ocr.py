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
from UTILS.generic_functions import convert_text_unidecode, verify_find_intersection


class Execute_OCR():

    def __init__(self):

        # 1 - OBTENDO A LISTA DE MESES
        self.list_values_months = list(settings.DICT_MONTHS_ABREV.keys()) + list(settings.DICT_MONTHS_COMPLETE.keys())


    @staticmethod
    def pos_processing_cnpj(text_input, pattern):

        """

            FORMATA O CNPJ OBTIDO DA CARTA DE FATURAMENTO

            # Arguments
                text_input              - Required : Texto de input (String)
                pattern                 - Required : Pattern de formatação a ser utilizado (String)

            # Returns
                result_cnpj             - Required : Resultado da formatação (String)

        """

        try:
            # MANTENDO APENAQS OS NÚMEROS DO CNPJ DE INPUT
            text_input_only_numbers = re.sub(pattern=pattern,
                                             repl="",
                                             string=text_input)

            # FORMATANDO O CNPJ OBTIDO
            result_cnpj = "{}.{}.{}/{}-{}".format(text_input_only_numbers[:2],
                                                  text_input_only_numbers[2:5],
                                                  text_input_only_numbers[5:8],
                                                  text_input_only_numbers[8:12],
                                                  text_input_only_numbers[12:])

            return result_cnpj

        except Exception as ex:
            execute_log.error("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

            return text_input


    def get_table_faturamento(self, text_input):

        """

            OBTÉM OS VALORES DA TABELA DE FATURAMENTO

            # Arguments
                text_input                - Required : Texto de input (String)

            # Returns
                result_faturamento        - Required : Resultado do faturamento (String)

        """

        # OBTENDO - FATURAMENTO - FORMA 1
        list_result_faturamento = get_matchs_line(text_input, settings.PATTERN_FATURAMENTO_1)

        # FILTANDO FATURAMENTOS QUE POSSUEM MESES OU FORMATO DE ANO (XXXX)
        list_filter_result = [value[0] for value in list_result_faturamento if verify_find_intersection(value[0],
                                                                                                     self.list_values_months)]

        return list_filter_result


    @staticmethod
    def pos_processing_faturamento(list_result_faturamento, pattern=None):

        """

            REALIZA A SEPARAÇÃO DA LISTA DE FATURAMENTO EM:
                1) ANOS (result_years)
                2) MESES (result_months)
                3) VALORES DE FATURAMENTO (result_values_faturamento)

            # Arguments
                list_result_faturamento         - Required : Lista com os
                                                             valores de faturamento (List)
                 pattern                        - Required : Pattern de formatação a ser utilizado (String)

            # Returns
                result_years                    - Required : Resultado contendo os anos obtidos (String)
                result_months                   - Required : Resultado contendo os meses obtidos (String)
                result_values_faturamentos      - Required : Resultado contendo os faturamentos obtidos (String)

        """

        # INICIALIZANDO AS LISTAS RESULTADOS
        result_years = []
        result_months = []
        result_values_faturamentos = []

        try:
            # PERCORRENDO CADA UM DOS FATURAMENTOS OBTIDOS
            for value in list_result_faturamento:

                if pattern:
                    # MANTENDO APENAQS OS NÚMEROS DO CNPJ DE INPUT
                    value = re.sub(pattern=pattern, repl="", string=value)

                # RETIRANDO ESPAÇOS A MAIS
                value = " ".join(filter(lambda x: x, value.split(' ')))

                # SEPARANDO OS VALORES OBIDOS POR ESPAÇO
                result_split = value.split(" ")

                # ADICIONANDO O RESULTADO DO SPLIT
                result_years.append(result_split[0])
                result_months.append(result_split[1])
                result_values_faturamentos.append(result_split[-1])

        except Exception as ex:
            execute_log.error("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return result_years, result_months, result_values_faturamentos


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
        json_result["faturamento"] = ""

        # REALIZANDO O OCR SOBRE A IMAGEM
        result_ocr = ocr_functions(dir_full_image).Orquestra_OCR()

        # FORMATANDO O RESULTADO DO OCR
        result_ocr = convert_text_unidecode(result_ocr).upper()

        # OBTENDO - CNPJ
        list_result_cnpj = get_matchs_line(result_ocr, settings.PATTERN_CNPJ)

        # FORMATANDO O RESULTADO OBTIDO - CNPJ
        json_result["cnpj"] = [Execute_OCR.pos_processing_cnpj(value[-1],
                                                               settings.PATTERN_ONLY_NUMBERS) for value in list_result_cnpj]

        # OBTENDO A TABELA DE FATURAMENTO
        json_result["faturamento"] = Execute_OCR.get_table_faturamento(self, result_ocr)

        # FORMATANDO O RESULTADO OBTIDO - TABELA DE FATURAMENTO
        result_years, result_months, result_values_faturamento = Execute_OCR.pos_processing_faturamento(json_result["faturamento"],
                                                                                                        settings.REGEX_ONLY_LETTERS_NUMBERS_DOT_BARS_DASHES_COMMA)

        return result_ocr, json_result