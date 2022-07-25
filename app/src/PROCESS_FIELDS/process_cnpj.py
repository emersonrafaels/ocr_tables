"""

    CLASSE PARA PROCESSAMENTO DOS CAMPOS DE FORMATO CNPJ.

    POSSUI FUNÇÕES PARA:
        1) OBTER CNPJS NO TEXTO

    # Arguments
        text                   - Required : Texto a ser analisado (String)
        pattern_cnpj           - Required : Pattern a ser utilizado para
                                            obtenção dos cnpjs (Regex)

    # Returns
        cnpj                  - Required : CNPJ (String)

"""

__version__ = "1.0"
__author__ = "Emerson V. Rafael (EMERVIN)"
__data_atualizacao__ = "22/07/2022"


from inspect import stack

import execute_log
from src.UTILS.extract_infos import get_matchs_line, get_similitary


class Execute_Process_CNPJ():

    def __init__(self):

        pass


    def get_result_cnpjs(self, text, pattern_cnpj):

        """

            CLASSE PARA PROCESSAMENTO DOS CAMPOS DE FORMATO CNPJ.

            POSSUI FUNÇÕES PARA:
                1) OBTER CNPJS NO TEXTO

            # Arguments
                text                   - Required : Texto a ser analisado (String)
                pattern_cnpj           - Required : Pattern a ser utilizado para
                                                    obtenção dos cnpjs (Regex)

            # Returns
                cnpj                  - Required : CNPJ (String)

        """

        # INICIANDO AS VARIÁVEIS
        cnpjs = []

        try:
            # OBTENDO CNPJS
            cnpjs = get_matchs_line(text=text, field_pattern=pattern_cnpj)

        except Exception as ex:
            print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

        return cnpjs