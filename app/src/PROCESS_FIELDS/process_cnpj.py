"""

    # Arguments
        text                   - Required : Texto a ser analisado (String)
        pattern                - Required : Pattern a ser utilizado para
                                            obtenção dos cnpjs (Regex)
        range_error_pattern    - Optional : Número de erroos
                                            aceitos no pattern (List)
        words_black_list       - Optional : Palavras que não
                                            devem constar na linha (List)
        limit                  - Optional : Quantidade de limites
                                            desejados (Integer)

    # Returns
        result_cnpjs           - Required : CNPJ's obtidos (List)

"""

__version__ = "1.0"
__author__ = "Emerson V. Rafael (EMERVIN)"
__data_atualizacao__ = "26/07/2022"


from inspect import stack
import regex as re

from dynaconf import settings
import numpy as np

from app import execute_log
from app.src.UTILS.extract_infos import get_matchs_line, get_similitary
from app.src.UTILS.generic_functions import remove_line_with_black_list_words, lista_bi_to_uni


class Execute_Process_CNPJ():

    def __init__(self):

        pass


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


    def get_best_match(self, list_cnpjs, limit):

        """

            CLASSE PARA OBTER OS MELHORES MATCHS CONFORME LIMITE

            # Arguments
                list_cnpjs             - Required : Texto a ser analisado (String)
                limit                  - Optional : Quantidade de limites
                                                    desejados (Integer)

            # Returns
                list_best_cnpjs       - Required : CNPJs (List)

        """

        list_best_cnpjs = []

        # PERCORRENDO A LISTA E OBTENDO A SOMA DE FUZZYS
        for value_cnpj in list_cnpjs:
            value_cnpj.append(np.sum(value_cnpj[-1]))

        # REALIZANDO O SORTED E FILTRANDO DE ACORDO COM O LIMIT
        list_best_cnpjs = sorted(list_cnpjs, key=lambda row: row[-1])[:limit]

        return list_best_cnpjs


    def get_result_cnpjs(self, text, pattern,
                         range_error_pattern=[1, 1], words_black_list=[],
                         limit=1):

        """

            CLASSE PARA PROCESSAMENTO DOS CAMPOS DE FORMATO CNPJ.

            POSSUI FUNÇÕES PARA:
                1) FILTRAR LINHAS DO TEXTO QUE CONTÉM PALAVRAS NÃO DESEJADAS
                2) OBTER CNPJS NO TEXTO
                3) OBTER OS CNPJ COM OS MAIORES MATCHS

            # Arguments
                text                   - Required : Texto a ser analisado (String)
                pattern                - Required : Pattern a ser utilizado para
                                                    obtenção dos cnpjs (Regex)
                range_error_pattern    - Optional : Número de erroos
                                                    aceitos no pattern (List)
                words_black_list       - Optional : Palavras que não
                                                    devem constar na linha (List)
                limit                  - Optional : Quantidade de limites
                                                    desejados (Integer)

            # Returns
                result_cnpjs           - Required : CNPJ's obtidos (List)

        """

        # INICIANDO AS VARIÁVEIS
        result_cnpjs = []
        list_cnpjs = []

        # VERIFICANDO SE O RANGE ERROR É UMA LISTA
        if not isinstance(range_error_pattern, list):
            # VERIFICANDO SE O RANGE ERROR PATTERN É UM INTEIRO
            if isinstance(range_error_pattern, int):
                range_error_pattern = [range_error_pattern]
            # VERIFICANDO SE O RANGE ERROR PATTERN É UMA STRING
            elif isinstance(range_error_pattern, str):
                # VERIFICANDO SE O RANGE ERROR PATTERN É UMA STRING
                # QUE PODE SER CONVERTIDA EM NÚMERO
                if range_error_pattern.isdigit():
                    range_error_pattern = [int(range_error_pattern)]
                else:
                    range_error_pattern = [1, 1]
            else:
                range_error_pattern = [1, 1]

        # REALIZANDO A LIMPEZA DO TEXTO, RETIRANDO BLACKLIST
        text = remove_line_with_black_list_words(text=text, list_words=words_black_list)

        try:
            for n_error in np.arange(np.min(range_error_pattern), np.max(range_error_pattern)+1):

                # FORMATANDO O PATTERN
                pattern_error = pattern.replace('n_error', str(n_error))

                # OBTENDO CNPJS
                cnpjs_matchs = get_matchs_line(text=text, field_pattern=pattern_error)

                # SALVANDO A LISTA DE CNPJS
                list_cnpjs += cnpjs_matchs

            # OBTENDO O VALOR COM MELHOR MATCH
            result_cnpjs = Execute_Process_CNPJ.get_best_match(self, list_cnpjs=list_cnpjs, limit=limit)

            # FORMATANDO O RESULTADO OBTIDO - CNPJ
            result_cnpjs = [Execute_Process_CNPJ.pos_processing_cnpj(value[3],
                                                                     settings.PATTERN_ONLY_NUMBERS,
                                                                     validator_only_numbers=settings.CNPJ_ONLY_NUMBERS) for value in result_cnpjs]

        except Exception as ex:
            print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

        return result_cnpjs