"""

    CLASSE PARA PROCESSAMENTO DOS CAMPOS DE FORMATO FATURAMENTO.

    POSSUI FUNÇÕES PARA:
        1) FILTRAR LINHAS DO TEXTO QUE CONTÉM PALAVRAS NÃO DESEJADAS
        2) OBTER A TABELA DE FATURAMENTO NO TEXTO
        3) REALIZAR MELHORIA DO OCR COM SIMILARIDADES

    # Arguments
        text                   - Required : Texto a ser analisado (String)
        pattern                - Required : Pattern a ser utilizado para
                                            obtenção dos cnpjs (Regex)
        words_black_list       - Optional : Palavras que não
                                            devem constar na linha (List)
        limit                  - Optional : Quantidade de limites
                                            desejados (Integer)

    # Returns
        cnpjs                  - Required : CNPJ's (List)

"""

__version__ = "1.0"
__author__ = "Emerson V. Rafael (EMERVIN)"
__data_atualizacao__ = "28/07/2022"


from inspect import stack
import regex as re

from dynaconf import settings
import numpy as np

from app import execute_log
from app.src.UTILS.extract_infos import get_matchs_line, get_similitary
from app.src.UTILS.generic_functions import (remove_line_with_black_list_words,
                                             lista_bi_to_uni,
                                             verify_find_intersection)


class Execute_Process_Tabela_Faturamento():

    def __init__(self):

        pass


    def get_similarity_months(self, values_table, list_months):

        """

            OBTÉM OS VALORES SIMILARES DE MÊS

            OBTÉM O VALOR DE MÁXIMA SIMILARIDADE ENTRE OCR E LISTA DE MESES POSSIVEIS.

            # Arguments
                values_table            - Required : Tabela de faturamento
                                                     obtida no OCR (Dict)
                list_months             - Required : Lista de meses possíveis (List)

            # Returns
                values_table_similarity - Required : Tabela de faturamento
                                                     após realização de matchs
                                                     de similaridade (Dict)

        """

        # PERCORRENDO CADA VALOR DA TABELA
        for key in values_table:
            result_similarity = get_similitary(values_table[key]["mes"],
                                               self.list_values_months,
                                               self.default_percent_match,
                                               self.similarity_pre_processing,
                                               self.limit_result_best_similar)

            print(result_similarity)

            values_table[key]["mes"] = result_similarity

        return values_table


    @staticmethod
    def get_result_faturamento_format_dict_list(list_result_faturamento, pattern=None):

        """

            REALIZA A SEPARAÇÃO DA LISTA DE FATURAMENTO EM:
                1) ANOS (result_years)
                2) MESES (result_months)
                3) VALORES DE FATURAMENTO (result_values_faturamento)

            AO FINAL, REALIZA A UNIFICAÇÃO DAS LISTAS EM UM LISTA.

            O RESULTADO FINAL TEM O FORMATO:
                'tabela_valores': {0: ['OUTUBRO', '2016', '298.320,00'], 0: ['DEZEMBRO', '2016', '300.320,00']}

            # Arguments
                list_result_faturamento         - Required : Lista com os
                                                             valores de faturamento (List)
                pattern                         - Required : Pattern de formatação ser utilizado (String)

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

            # CONVERTENDO MULTIDIMENSIONAL LIST TO DICT
            result_values_faturamentos_dict = {index: list(value) for index,
                                                                      value in enumerate(list(zip(result_years,
                                                                                                  result_months,
                                                                                                  result_values_faturamentos)))}

        except Exception as ex:
            execute_log.error("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return result_values_faturamentos_dict, result_years, result_months, result_values_faturamentos


    @staticmethod
    def get_result_faturamento_format_dict_dict(list_result_faturamento, pattern=None):

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
                pattern                         - Required : Pattern de formatação ser utilizado (String)

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

            # CONVERTENDO MULTIDIMENSIONAL LIST TO DICT
            result_values_faturamentos_dict = {index: list(value) for index,
                                                                      value in enumerate(list(zip(result_years,
                                                                                                  result_months,
                                                                                                  result_values_faturamentos)))}

        except Exception as ex:
            execute_log.error("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return result_values_faturamentos_dict, result_years, result_months, result_values_faturamentos


    @staticmethod
    def filter_values_table_faturamento(list_values, filters_validate):

        pass


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

        # FILTRANDO RESULTADOS QUE POSSUEM MESES
        list_filter_result = [value[0] for value in list_result_faturamento if
                              verify_find_intersection(value[0], self.list_values_months)]

        return list_filter_result


    def pos_processing_faturamento(self):

        """

            FUNÇÃO RESPONSÁVEL POR FORMATAR A LISTA DE POSSÍVEIS VALORES DE FATURAMENTO
            REALIZANDO A OBTENÇÃO DAS INFORMAÇÕES DE:

                1) MÊS
                2) ANO
                3) FATURAMENTO

            # Arguments

            # Returns

        """

        pass


    def orchestra_get_table_faturamento(self, text_input):

        # INICIANDO O VALIDADOR
        validator = False

        # INICIANDO AS VARIÁVEIS DE JSON RESULT
        json_result = {}
        json_result["cnpj_cliente"] = ""
        json_result["tabela_valores"] = ""

        # OBTENDO A TABELA DE FATURAMENTO
        result_table = Execute_Process_Tabela_Faturamento.get_table_faturamento(self, text_input)

        # REALIZANDO O PÓS PROCESSAMENTO DA TABELA DE FATURAMENTO
        Execute_Process_Tabela_Faturamento.pos_processing_faturamento(self, result_table)

        # FORMATANDO O RESULTADO OBTIDO - TABELA DE FATURAMENTO
        json_result["tabela_valores"], \
        result_years, \
        result_months, \
        result_values_faturamento = Execute_Process_Tabela_Faturamento.get_result_faturamento(result_table,
                                                                                              settings.REGEX_ONLY_LETTERS_NUMBERS_DOT_BARS_DASHES_COMMA)

        return json_result["tabela_valores"], \
               result_years, \
               result_months, \
               result_values_faturamento