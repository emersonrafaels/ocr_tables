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
__data_atualizacao__ = "26/06/2022"


from inspect import stack
import regex as re

from dynaconf import settings

from app import execute_log
from app.src.UTILS.image_ocr import ocr_functions
from app.src.UTILS.extract_infos import get_matchs_line, get_similitary
from app.src.UTILS.generic_functions import convert_text_unidecode, verify_find_intersection
from app.src.PROCESSINGS.model_pre_processing import Image_Pre_Processing
from app.src.PROCESS_FIELDS.process_cnpj import Execute_Process_CNPJ


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
        list_filter_result = [value[0] for value in list_result_faturamento if verify_find_intersection(value[0], self.list_values_months)]

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
        dict_images = {}
        list_result = []
        validator_pre_processing = False

        for result in result_tables:

            # REALIZANDO O OCR SOBRE A IMAGEM
            text_ocr = ocr_functions(type_return_ocr_input="TEXTO").Orquestra_OCR(result["image_file"])

            # SALVANDO O TEXTO OBTIDO
            dict_images["IMG_ORIGINAL"] = text_ocr

            if settings.PRE_PROC_IMAGE:
                # REALIZANDO O PRÉ PROCESSAMENTO DA IMAGEM
                validator_pre_processing, image_pre_processing = Image_Pre_Processing().orchestra_pre_processing(result["image_file"])

                if validator_pre_processing:

                    # REALIZANDO O OCR SOBRE A IMAGEM
                    text_ocr_pre_processing = ocr_functions(type_return_ocr_input="TEXTO").Orquestra_OCR(image_pre_processing)

                    # SALVANDO O TEXTO OBTIDO
                    dict_images["PRE_PROCESSING"] = text_ocr_pre_processing

            for idx, image in enumerate(dict_images):

                # INICIANDO AS VARIÁVEIS DE JSON RESULT
                json_result = {}
                json_result["cnpj_cliente"] = ""
                json_result["tabela_valores"] = ""

                execute_log.info("{} - IMAGEM ATUAL: {}".format(settings.APPNAME, image))

                # FORMATANDO O RESULTADO DO OCR
                result_ocr = convert_text_unidecode(dict_images[image]).upper()

                # OBTENDO - CNPJ
                json_result["cnpj_cliente"] = Execute_Process_CNPJ().get_result_cnpjs(text=result_ocr,
                                                                                      pattern=settings.PATTERN_CNPJ,
                                                                                      range_error_pattern=settings.RANGE_PATTERN_ERROR_CNPJ,
                                                                                      words_black_list=settings.WORDS_BLACK_LIST_CNPJ +
                                                                                            list(settings.DICT_MONTHS_COMPLETE.keys()) +
                                                                                            list(settings.DICT_MONTHS_ABREV.keys()))


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

                list_result.append(json_result)

        return result_ocr, list_result