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
from src.UTILS.image_ocr import ocr_functions
from src.UTILS.extract_infos import get_matchs_line, get_similarity
from src.UTILS.generic_functions import convert_text_unidecode, verify_find_intersection


class Execute_OCR():

    def __init__(self):

        # 1 - OBTENDO A LISTA DE MESES
        self.list_values_months_abrev = list(settings.DICT_MONTHS_ABREV.keys())
        self.list_values_months_complete = list(settings.DICT_MONTHS_COMPLETE.keys())
        self.list_values_months = self.list_values_months_abrev + self.list_values_months_complete

        # 2 - INICIANDO OS PERCENTUAIS DE MATCH
        self.default_percent_match = settings.DEFAULT_PERCENTUAL_MATCH

        # 3 - DEFININDO SE DEVE HAVER PRÉ PROCESSAMENTO DOS ITENS ANTES DO CÁLCULO DE SEMELHANÇA
        self.similarity_pre_processing = settings.DEFAULT_PRE_PROCESSING

        # 4 - INICIANDO A VARIÁVEL QUE CONTÉM O LIMIT NA CHAMADA DE MÁXIMAS SIMILARIDADES
        self.limit_result_best_similar = settings.DEFAULT_LIMIT_RESULT_BEST_SIMILAR


    @staticmethod
    def pos_processing_cnpj(text_input, pattern, validator_only_numbers=False):

        """

            FORMATA O CNPJ OBTIDO DA CARTA DE FATURAMENTO

            # Arguments
                text_input                - Required : Texto de input (String)
                pattern                   - Required : Pattern de formatação a ser utilizado (String)
                validator_only_numbers    - Optional : Caso True, retorna o CNPJ apenas de forma numérica.
                                                       Sem utilizar '-', '.', '/'. (Boolean)

            # Returns
                result_cnpj             - Required : Resultado da formatação (String)

        """

        try:
            # MANTENDO APENAQS OS NÚMEROS DO CNPJ DE INPUT
            text_input_only_numbers = re.sub(pattern=pattern,
                                             repl="",
                                             string=text_input)

            if not validator_only_numbers:

                # FORMATANDO O CNPJ OBTIDO
                result_cnpj = "{}.{}.{}/{}-{}".format(text_input_only_numbers[:2],
                                                      text_input_only_numbers[2:5],
                                                      text_input_only_numbers[5:8],
                                                      text_input_only_numbers[8:12],
                                                      text_input_only_numbers[12:])

                return result_cnpj

            else:
                return text_input_only_numbers

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

        # INICIANDO A VARIÁVEL CONTENDO A LISTA DE RESULTADO
        list_filter_result = []

        # OBTENDO - FATURAMENTO - FORMA 1
        list_result_faturamento = get_matchs_line(text_input, settings.PATTERN_FATURAMENTO_1)

        if list_result_faturamento:

            # FILTRANDO RESULTADOS QUE POSSUEM MESES
            list_filter_result = [value[0] for value in list_result_faturamento if verify_find_intersection(value[0],
                                                                                                            self.list_values_months)]

            if list_filter_result:

                return list_filter_result

        if not list_filter_result:

            # FILTRANDO RESULTADOS QUE POSSUEM MESES
            list_filter_result = [value for value in text_input.split("\n") if verify_find_intersection(value,
                                                                                                        self.list_values_months_complete)]

        return list_filter_result


    def pos_processing_faturamento(self, list_result_faturamento):

        """

            FUNÇÃO RESPONSÁVEL POR FORMATAR A LISTA DE POSSÍVEIS VALORES DE FATURAMENTO
            REALIZANDO A OBTENÇÃO DAS INFORMAÇÕES DE:
                1) MÊS
                2) ANO
                3) FATURAMENTO

            # Arguments
                list_result_faturamento                      - Required : Lista com os
                                                                          valores de faturamento (List)

            # Returns
                list_result_faturamento_formatted            - Required : Resultado de faturamento
                                                                          após formatação (List)

        """

        # DADO UMA LISTA DE VALORES, BUSCAMOS OBTER:
            # 1) UM VALOR MÊS DESSA LISTA (HÁ A LISTA DE MESES POSSÍVEIS)
            # 2) UM ANO DESSA LISTA (4 NÚMEROS, ENTRE 1900 E 2500)
            # 3) VALORES DE FATURAMENTO (NÚMEROS, COM VALORES ACIMA DE 2500)

        # PERCORRENDO CADA UM DOS VALORES DA LISTA
        for value in list_result_faturamento:

            # CAPTURANDO O VALOR DE MÊS
            result_month = [month for month in self.list_values_months_complete if value.find(month)!=-1]

            # CAPTURANDO O VALOR DE ANO
            result_year = re.match(pattern=settings.REGEX_DATE_VALID, string=value)

        print(result_month)


    @staticmethod
    def get_result_faturamento(list_result_faturamento, pattern=None):

        """

            REALIZA A SEPARAÇÃO DA LISTA DE FATURAMENTO EM:
                1) ANOS (result_years)
                2) MESES (result_months)
                3) VALORES DE FATURAMENTO (result_values_faturamento)

            AO FINAL, REALIZA A UNIFICAÇÃO DAS LISTAS EM UM DICT.

            O RESULTADO FINAL TEM O FORMATO:
                'tabela_valores': {0: ['OUTUBRO', '2016', '298.320,00'], 0: ['DEZEMBRO', '2016', '300.320,00']}

            # Arguments
                list_result_faturamento         - Required : Lista com os
                                                             valores de faturamento (List)

            # Returns
                result_years                    - Required : Resultado contendo os anos obtidos (String)
                result_months                   - Required : Resultado contendo os meses obtidos (String)
                result_values_faturamentos      - Required : Resultado contendo os faturamentos obtidos (String)
                result_values_faturamentos_dict - Required : Resultando zipando os
                                                             resultados de ano, mes e valores (Dict)

        """

        # INICIALIZANDO AS LISTAS RESULTADOS
        result_years = []
        result_months = []
        result_values_faturamentos = []
        result_values_faturamentos_dict = {}

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

            result_values_faturamentos_dict = {index: list(value) for index,
                                                                      value in enumerate(list(zip(result_years,
                                                                                                  result_months,
                                                                                                  result_values_faturamentos)))}

        except Exception as ex:
            execute_log.error("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return result_values_faturamentos_dict, result_years, result_months, result_values_faturamentos


    @staticmethod
    def get_result_faturamento_alternate_format(list_result_faturamento, pattern=None):

        """

            REALIZA A SEPARAÇÃO DA LISTA DE FATURAMENTO EM:
                1) ANOS (result_years)
                2) MESES (result_months)
                3) VALORES DE FATURAMENTO (result_values_faturamento)

            AO FINAL, REALIZA A UNIFICAÇÃO DAS LISTAS EM UM DICT.

            O RESULTADO FINAL TEM O FORMATO:
                'tabela_valores': [{'mes': 'OUTUBRO', 'ano': '2016', 'valor': '298.320,00'}, {'mes': 'DEZEMBRO', 'ano': '2016', 'valor': '300.320,00'}]

            # Arguments
                list_result_faturamento         - Required : Lista com os
                                                             valores de faturamento (List)

            # Returns
                result_years                    - Required : Resultado contendo os anos obtidos (String)
                result_months                   - Required : Resultado contendo os meses obtidos (String)
                result_values_faturamentos      - Required : Resultado contendo os faturamentos obtidos (String)
                result_values_faturamentos_list - Required : Resultando zipando os
                                                             resultados de ano, mes e valores (List)

        """

        # INICIALIZANDO AS LISTAS RESULTADOS
        result_years = []
        result_months = []
        result_values_faturamentos = []
        result_values_faturamentos_list = {}

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

                result_values_faturamentos_list.append(dict(mes=result_years[-1],
                                                            ano=result_months[-1],
                                                            valor=result_values_faturamentos[-1]))

        except Exception as ex:
            execute_log.error("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return result_values_faturamentos_list, result_years, result_months, result_values_faturamentos


    def execute_pipeline_ocr(self, result_tables):

        """

            ORQUESTRA A APLICAÇÃO DE OCR SOBRE UMA IMAGEM.
            OBTÉM CNPJ, MESES E VALORES DE FATURAMENTO.

            O OCR É APLICADO SOBRE A IMAGEM COMPLETA (dir_full_image)
            E SOBRE AS TABELAS (SE ENCONTRADAS) (dir_table_image).

            # Arguments
                result_tables               - Required : Imagem e suas tabelas (List)

            # Returns
                validador                   - Required : Validador de execução da função (Boolean)
                result_ocr                  - Required : Retorno do OCR (String | Dict)
                json_result                 - Required : Resultado das informações do DAC (Dict)

        """

        # INICIANDO AS VARIÁVEIS RESULTANTES
        result_ocr = ""
        json_result = {}
        json_result["cnpj_cliente"] = ""
        json_result["tabela_valores"] = ""

        for result in result_tables:

            # REALIZANDO O OCR SOBRE A IMAGEM
            result_ocr = ocr_functions(result["image_file"]).Orquestra_OCR()

            # FORMATANDO O RESULTADO DO OCR
            result_ocr = convert_text_unidecode(result_ocr).upper()

            # OBTENDO - CNPJ
            list_result_cnpj = get_matchs_line(result_ocr, settings.PATTERN_CNPJ)

            # FORMATANDO O RESULTADO OBTIDO - CNPJ
            json_result["cnpj_cliente"] = [Execute_OCR.pos_processing_cnpj(value[-1],
                                                                           settings.PATTERN_ONLY_NUMBERS, validator_only_numbers=settings.CNPJ_ONLY_NUMBERS) for value in list_result_cnpj]

            # OBTENDO A TABELA DE FATURAMENTO
            result_table = Execute_OCR.get_table_faturamento(self, result_ocr)

            # REALIZANDO O PÓS PROCESSAMENTO DA TABELA DE FATURAMENTO
            Execute_OCR.pos_processing_faturamento(self, result_table)

            # FORMATANDO O RESULTADO OBTIDO - TABELA DE FATURAMENTO
            json_result["tabela_valores"], \
            result_years, \
            result_months, \
            result_values_faturamento = Execute_OCR.get_result_faturamento(result_table,
                                                                           settings.REGEX_ONLY_LETTERS_NUMBERS_DOT_BARS_DASHES_COMMA)

        return result_ocr, json_result