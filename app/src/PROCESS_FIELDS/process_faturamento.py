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
__data_atualizacao__ = "23/08/2022"


from inspect import stack
import itertools
import regex as re

from dynaconf import settings
from typing import Union

from app import execute_log
from app.src.UTILS.combinations import all_combinations
from app.src.UTILS.extract_infos import (get_matchs_line,
                                         get_matchs_strings,
                                         get_similitary)
from app.src.UTILS.generic_functions import (
    verify_find_intersection,
    has_number,
)


class Execute_Process_Tabela_Faturamento:
    def __init__(self):

        # 1 - OBTENDO A LISTA DE MESES
        self.list_values_months_abrev = list(settings.DICT_MONTHS_ABREV.keys())
        self.list_values_months_complete = list(settings.DICT_MONTHS_COMPLETE.keys())
        self.list_values_months = (
            self.list_values_months_abrev + self.list_values_months_complete
        )

        # 2 - INICIANDO OS PERCENTUAIS DE MATCH
        self.default_percent_match = settings.DEFAULT_PERCENTUAL_MATCH

        # 3 - DEFININDO SE DEVE HAVER PRÉ PROCESSAMENTO DOS ITENS ANTES DO CÁLCULO DE SEMELHANÇA
        self.similarity_pre_processing = settings.DEFAULT_PRE_PROCESSING

        # 4 - INICIANDO A VARIÁVEL QUE CONTÉM O LIMIT NA CHAMADA DE MÁXIMAS SIMILARIDADES
        self.limit_result_best_similar = settings.DEFAULT_LIMIT_RESULT_BEST_SIMILAR

    def get_similarity_months(self, value_table, list_months):

        """

        OBTÉM OS VALORES SIMILARES DE MÊS

        OBTÉM O VALOR DE MÁXIMA SIMILARIDADE ENTRE OCR E LISTA DE MESES POSSIVEIS.

        # Arguments
            value_table             - Required : Valor a ser validado (String)
            list_months             - Required : Lista de meses possíveis (List)

        # Returns
            values_table_similarity - Required : Tabela de faturamento
                                                 após realização de matchs
                                                 de similaridade (Dict)

        """

        # MANTENDO APENAS PARTE TEXTUAL
        value_table_letters = re.sub(
            pattern=settings.PATTERN_ONLY_LETTERS, string=str(value_table), repl=""
        ).strip()

        # REALIZANDO COMBINÇÃO DE PALAVRAS
        combinations = list(
            all_combinations(
                any_list=[value_table_letters],
                split_words=True,
                min_n_combinations=1,
                max_n_combinations=len(value_table_letters.split()),
            )
        )

        for combination in combinations:

            # UNIFICANDO AS PALAVRAS EM UMA ÚNICA STRING
            combination_str = " ".join([value for value in combination])

            # MANTENDO APENAS A PARTE TEXTUAL
            combination_str = re.sub(
                pattern=settings.PATTERN_ONLY_LETTERS,
                string=str(combination_str),
                repl="",
            )

            if combination_str.strip() != "":

                # PERCORRENDO CADA VALOR DA TABELA
                result_similarity = get_similitary(
                    combination_str,
                    list_months,
                    self.default_percent_match,
                    self.similarity_pre_processing,
                    self.limit_result_best_similar,
                )

                if result_similarity[0]:

                    return True

        return False

    def valid_has_monetary_value(self, value_table, regex_money):

        """

        VALIDA SE UMA STRING CONTÉM VALORES MONETÁRIOS.

        PARA VALIDAÇÃO, REALIZA APLICAÇÃO DE REGEX SOBRE A STRING.

        # Arguments
            value_table           - Required : Valor a ser analisado (String)
            regex_money           - Required : Expressão para valores monetários (Regex)

        # Returns:
            validator_money      - Required : validator se
                                              possui valor monetário (Boolean)

        """

        # VERIFICANDO SE HÁ UM VALOR MONETÁRIO
        value_table_money = get_matchs_line(text=value_table, field_pattern=regex_money)

        if value_table_money:
            return True

        return False

    @staticmethod
    def get_month_year_faturamento(values_faturamento: Union[tuple, list]) -> list:

        """

        REALIZA A SEPARAÇÃO DA LISTA DE FATURAMENTO EM:
            1) ANOS (result_years)
            2) MESES (result_months)
            3) VALORES DE FATURAMENTO (result_values_faturamento)


        # Arguments
            values_faturamento              - Required : Lista com os
                                                         valores de faturamento (List)

        # Returns
            result_year                    - Required : Resultado contendo os anos obtidos (String)
            result_month                   - Required : Resultado contendo os meses obtidos (String)
            result_faturamento             - Required : Resultado contendo os faturamentos obtidos (String)

        """

        result_month = result_year = result_faturamento = ""

        # OBTENDO O MÊS
        result_pattern_month = get_matchs_strings(text=values_faturamento,
                                                  field_pattern=settings.PATTERN_FATURAMENTO_1)

        if result_pattern_month:
            result_month = values_faturamento[values_faturamento.find(result_pattern_month[0][2]):].split(" ")[0]

            values_faturamento = values_faturamento.replace(result_month, " ")

        # OBTENDO O ANO
        result_pattern_year = get_matchs_strings(text=values_faturamento,
                                                 field_pattern=settings.PATTERN_YEAR)

        if result_pattern_year:
            result_year = values_faturamento[values_faturamento.find(result_pattern_year[0][2]):].split(" ")[0]

            values_faturamento = values_faturamento.replace(result_year, " ")

        # OBTENDO O VALOR
        result_faturamento = values_faturamento.strip().replace(" ", ".")

        return [result_month, result_year, result_faturamento]

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
                value = " ".join(filter(lambda x: x, value.split(" ")))

                # SEPARANDO OS VALORES OBIDOS POR ESPAÇO
                result_split = Execute_Process_Tabela_Faturamento.get_month_year_faturamento(values_faturamento=value)

                # ADICIONANDO O RESULTADO DO SPLIT
                result_years.append(result_split[0])
                result_months.append(result_split[1])
                result_values_faturamentos.append(result_split[-1])

            # CONVERTENDO MULTIDIMENSIONAL LIST TO DICT
            result_values_faturamentos_dict = {
                index: list(value)
                for index, value in enumerate(
                    list(zip(result_years, result_months, result_values_faturamentos))
                )
            }

        except Exception as ex:
            execute_log.error("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return (
            result_values_faturamentos_dict,
            result_years,
            result_months,
            result_values_faturamentos,
        )

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
                    # MANTENDO APENAS LETRAS, NÚMEROS,
                    # PONTUAÇÕES E CARACTERES ESPECIAIS DESEJADOS
                    value = re.sub(pattern=pattern, repl="", string=value)

                # SEPARANDO OS VALORES OBTIDOS POR ESPAÇO
                result_split = value.split(" ")

                # ADICIONANDO O RESULTADO DO SPLIT
                result_years.append(result_split[0])
                result_months.append(result_split[1])
                result_values_faturamentos.append(result_split[-1])

            # CONVERTENDO MULTIDIMENSIONAL LIST TO DICT
            result_values_faturamentos_dict = {
                index: list(value)
                for index, value in enumerate(
                    list(zip(result_years, result_months, result_values_faturamentos))
                )
            }

        except Exception as ex:
            execute_log.error("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return (
            result_values_faturamentos_dict,
            result_years,
            result_months,
            result_values_faturamentos,
        )

    @staticmethod
    def filter_values_table_faturamento(list_values, filters_validate):

        pass

    def get_table_faturamento(self, text_input, pattern):

        """

        OBTÉM OS VALORES DA TABELA DE FATURAMENTO

        # Arguments
            text_input                - Required : Texto de input (String)
            pattern                   - Required : Pattern a ser utilizado para
                                                   obtenção da tabela de faturamento (Regex)

        # Returns
            result_faturamento        - Required : Resultado do faturamento (String)

        """

        # INICIANDO A VARIÁVEL CONTENDO A LISTA DE RESULTADO
        list_filter_result = []

        # OBTENDO - FATURAMENTO - FORMA 1 - PATTERMS
        list_result_faturamento = get_matchs_line(
            text=text_input, field_pattern=pattern, only_one_match_per_line=True
        )

        # OBTENDO - FATURAMENTO - FORMA 2
        # FILTRANDO RESULTADOS QUE POSSUEM MESES
        # FILTRANDO RESULTADOS QUE POSSUEM NÚMEROS
        list_filter_result = [
            value[0]
            for value in list_result_faturamento
            if (
                verify_find_intersection(value[0], self.list_values_months)
                and has_number(value[0])
            )
        ]

        return list_filter_result

    def pos_processing_faturamento(self,
                                   table_faturamento,
                                   pattern_faturamento_valid_caracters):

        """

        FUNÇÃO RESPONSÁVEL POR FORMATAR A LISTA DE POSSÍVEIS VALORES DE FATURAMENTO
        REALIZANDO A OBTENÇÃO DAS INFORMAÇÕES DE:

            1) MÊS
            2) ANO
            3) FATURAMENTO

        # Arguments
            table                                  - Required : Tabela de faturamento (List)
            pattern_faturamento_valid_caracters    - Required : Pattern ds caracteres
                                                                validos no pattern (Regex)

        # Returns
            table_result                          - Required : Tabela após processamentos
                                                               de similaridade (List)

        """

        # INICIANDO A LISTA FINAL
        table_result = []

        # PERCORRENDO CADA UM DOS VALORES DA TABELA DE FATURAMENTO
        for value_faturamento in table_faturamento:

            # MANTENDO APENAS OS CARACTERES ACEITOS NO CAMPO DE FATURAMENTO
            # MANTENDO APENAQS OS NÚMEROS DO CNPJ DE INPUT
            value_faturamento = re.sub(pattern=pattern_faturamento_valid_caracters,
                                       repl="",
                                       string=value_faturamento)

            # ETAPA 1 - VALIDANDO AS LINHAS QUE POSSUEM MESES VÁLIDOS
            validator_function_month = (
                Execute_Process_Tabela_Faturamento.get_similarity_months(
                    self,
                    value_table=value_faturamento,
                    list_months=self.list_values_months,
                )
            )

            # ETAPA 2 - VALIDANDO SE HÁ VALORES MONETÁRIO
            validator_function_monetary = (
                Execute_Process_Tabela_Faturamento.valid_has_monetary_value(
                    self,
                    value_table=value_faturamento,
                    regex_money=settings.PATTERN_MONEY,
                )
            )

            if False not in itertools.chain(
                [validator_function_month], [validator_function_monetary]
            ):
                # SALVANDO COMO LISTA FINAL
                table_result.append(value_faturamento)

        return table_result

    def orchestra_get_table_faturamento(self, text, pattern):

        """

        CLASSE PARA PROCESSAMENTO DOS CAMPOS DA TABELA DE FATURAMENTO.

        POSSUI FUNÇÕES PARA:
            1) OBTER TABELA DE FATURAMENTO
            2) OBTER OS CAMPOS MESES, ANOS E VALORES

        # Arguments
            text                   - Required : Texto a ser analisado (String)
            pattern                - Required : Pattern a ser utilizado para
                                                obtenção da tabela
                                                de faturamento (Regex)

        # Returns
            result_years                    - Required : Resultado contendo os anos obtidos (String)
            result_months                   - Required : Resultado contendo os meses obtidos (String)
            result_values_faturamentos      - Required : Resultado contendo os faturamentos obtidos (String)
            result_values_faturamentos_dict - Required : Resultando zipando os
                                                         resultados de ano, mes e valores (Dict)

        """

        # INICIANDO O validator
        validator = False

        # INICIANDO AS VARIÁVEIS DE JSON RESULT
        json_result = {}
        json_result["cnpj_cliente"] = ""
        json_result["tabela_valores"] = ""

        # OBTENDO A TABELA DE FATURAMENTO
        result_table = Execute_Process_Tabela_Faturamento.get_table_faturamento(
            self, text, pattern
        )

        # REALIZANDO O PÓS PROCESSAMENTO DA TABELA DE FATURAMENTO
        result_table = Execute_Process_Tabela_Faturamento.pos_processing_faturamento(
            self, table_faturamento=result_table,
            pattern_faturamento_valid_caracters=settings.PATTERN_DIF_LETTERS_NUMBERS_DOT_COMMA
        )

        # FORMATANDO O RESULTADO OBTIDO - TABELA DE FATURAMENTO
        (
            json_result["tabela_valores"],
            result_years,
            result_months,
            result_values_faturamento,
        ) = Execute_Process_Tabela_Faturamento.get_result_faturamento_format_dict_dict(
            result_table, settings.PATTERN_ONLY_LETTERS_NUMBERS_DOT_BARS_DASHES_COMMA
        )

        return (
            json_result["tabela_valores"],
            result_years,
            result_months,
            result_values_faturamento,
        )
