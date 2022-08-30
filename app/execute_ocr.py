"""

    ORQUESTRA A APLICAÇÃO DE OCR SOBRE UMA IMAGEM.
    OBTÉM CNPJ, MESES E VALORES DE FATURAMENTO.

    O OCR É APLICADO SOBRE A IMAGEM COMPLETA (dir_full_image)
    E SOBRE AS TABELAS (SE ENCONTRADAS) (dir_table_image).

    # Arguments
        dir_full_image              - Required : Caminho ds imagem completa (String)
        dir_table_image             - Required : Caminho dss tabelas encontradas (String)

    # Returns
        validator                   - Required : validator de execução da função (Boolean)
        retorno_ocr                 - Required : Retorno do OCR (String | Dict)

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "26/06/2022"


from inspect import stack

from dynaconf import settings

from app import execute_log
from app.src.UTILS.image_ocr import ocr_functions
from app.src.UTILS.generic_functions import drop_duplicates_list, convert_text_unidecode
from app.src.PROCESSINGS.model_pre_processing import Image_Pre_Processing
from app.src.PROCESS_FIELDS.process_cnpj import Execute_Process_CNPJ
from app.src.PROCESS_FIELDS.process_faturamento import (
    Execute_Process_Tabela_Faturamento,
)


class Execute_OCR:
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



    @staticmethod
    def get_list_images(result_tables: dict) -> dict:

        """

        OBTÉM UMA LISTA COM TODAS AS IMAGENS QUE DEVEM SER USADAS NO OCR.

        RECEBE UM DICT CONTENDO DUAS CHAVES:
            1) image_file: imagem original
            2) table: imagem de uma tabela obtida
                pode ser None) para aqueles casos onde não se obteve tabela

        # Arguments
            result_tables           - Required : Imagem e suas tabelas (List)

        # Returns
            dict_result             - Required : Lista de imagens (dict)

        """

        # INICIANDO A LISTA QUE ARMAZENARÁ AS IMAGENS
        dict_result = {}

        try:
            for idx, value in enumerate(result_tables):
                dict_result["IMAGE_ORIGINAL"] = value["image_file"]
                dict_result["TABLE_{}".format(str(idx))] = value["table"]
        except Exception as ex:
            execute_log.error("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return dict_result


    def execute_pipeline_ocr(self, result_tables):

        """

        ORQUESTRA A APLICAÇÃO DE OCR SOBRE UMA IMAGEM.
        OBTÉM CNPJ, MESES E VALORES DE FATURAMENTO.

        O OCR É APLICADO SOBRE A IMAGEM COMPLETA (dir_full_image)
        E SOBRE AS TABELAS (SE ENCONTRADAS) (dir_table_image).

        # Arguments
            result_tables               - Required : Imagem e suas tabelas (List)

        # Returns
            validator                   - Required : validator de execução da função (Boolean)
            result_ocr                  - Required : Retorno do OCR (String | Dict)
            json_result                 - Required : Resultado das informações do DAC (Dict)

        """

        # INICIANDO AS VARIÁVEIS RESULTANTES
        dict_images = {}
        list_result = []
        validator_pre_processing = False

        # OBTENDO A LISTA DE IMAGENS PARA OCR
        dict_all_images = Execute_OCR.get_list_images(result_tables)

        for key_image, image in dict_all_images.items():

            # REALIZANDO O OCR SOBRE A IMAGEM
            text_ocr = ocr_functions(type_return_ocr_input="TEXTO").Orquestra_OCR(
                image
            )

            # SALVANDO O TEXTO OBTIDO
            dict_images[key_image] = text_ocr

            if settings.PRE_PROC_IMAGE:

                # REALIZANDO O PRÉ PROCESSAMENTO DA IMAGEM
                (
                    validator_pre_processing,
                    image_pre_processing,
                ) = Image_Pre_Processing().orchestra_pre_processing(
                    image=image, view_image=settings.VIEW_PRE_PROC_IMAGE
                )

                if validator_pre_processing:

                    # REALIZANDO O OCR SOBRE A IMAGEM
                    text_ocr_pre_processing = ocr_functions(
                        type_return_ocr_input="TEXTO"
                    ).Orquestra_OCR(image_pre_processing)

                    # SALVANDO O TEXTO OBTIDO
                    dict_images[
                        f"PRE_PROCESSING_{key_image}"
                    ] = text_ocr_pre_processing

            for idx, image in enumerate(dict_images):

                # INICIANDO AS VARIÁVEIS DE JSON RESULT
                json_result = {}
                json_result[settings.NAME_FIELD_CNPJ] = ""
                json_result[settings.NAME_FIELD_FATURAMENTO] = ""

                execute_log.info("{} - IMAGEM ATUAL: {}".format(settings.APPNAME, image))

                # FORMATANDO O RESULTADO DO OCR
                result_ocr = convert_text_unidecode(dict_images[image]).upper()

                # OBTENDO - CNPJ
                json_result[settings.NAME_FIELD_CNPJ] = Execute_Process_CNPJ().get_result_cnpjs(
                    text=result_ocr,
                    pattern=settings.PATTERN_CNPJ,
                    range_error_pattern=settings.RANGE_PATTERN_ERROR_CNPJ,
                    words_black_list=settings.WORDS_BLACK_LIST_CNPJ
                    + list(settings.DICT_MONTHS_COMPLETE.keys())
                    + list(settings.DICT_MONTHS_ABREV.keys()),
                )

                # OBTENDO E FORMATANDO - TABELA DE FATURAMENTO
                (
                    json_result[settings.NAME_FIELD_FATURAMENTO],
                    result_years,
                    result_months,
                    result_values_faturamento,
                ) = Execute_Process_Tabela_Faturamento().orchestra_get_table_faturamento(
                    text=result_ocr, pattern=settings.PATTERN_FATURAMENTO_1
                )

                list_result.append({"text": result_ocr, "campos": json_result})

            return list_result
