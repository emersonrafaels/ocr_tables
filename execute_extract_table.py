"""

    SERVIÇO PARA REALIZAÇÃO DE EXTRAÇÃO DE TABELAS.

    1) APLICA TÉCNICAS DE PRÉ PROCESSAMENTO
    PARA DISTINGUIR TABELA DO RESTANTE DA IMAGEM
    2) ENCONTRANDO TABELAS
        3) EXTRAÇÃO DE TABELAS

    # Arguments
        object                  - Required : Imagem para aplicação da tabela e OCR (Base64 | Path | Numpy Array)
    # Returns
        output_text             - Required : Textos da tabela após aplicação das
                                             técnicas de pré processamento,
                                             OCR e pós processamento (String)

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "22/03/2022"


import os

import cv2
from dynaconf import settings

from model_pre_processing import Image_Pre_Processing
from UTILS.image_read import read_image_gray
import execute_log
from UTILS.base64_encode_decode import isbase64, base64_to_image
from UTILS import generic_functions


class Extract_Table():

    def __init__(self):

        pass


    @staticmethod
    def orchestra_get_files(input_file):

        """

            FUNÇÃO PARA ORQUESTRAR A OBTENÇÃO DOS ARQUIVOS NO QUAL A API DEVE ATUAR.

            PODE SER ENVIADO:
            1) CAMINHO DE UM ARQUIVO ESPECÍFICO
            2) DIRETÓRIO CONTENDO VÁRIOS ARQUIVOS
            3) INPUT EM BASE64

            ESSA FUNÇÃO É RESPONSÁVEL POR CHAMAR A FUNÇÃO DE OBTER TODOS OS ARQUIVOS NO DIRETÓRIO,
            CASO SEJA ENVIADO UM DIRETÓRIO.

            # Arguments
                input_file                       - Required : Caminho do(s) arquivo(s) a serme lidos.
                                                              Pode ser enviado um Path (String) ou Base64 (String)
                input_type                      - Required : Tipo do input (String)

            # Returns
                list_files_result                - Required : Caminho do(s) arquivo(s) listados. (List)

        """

        execute_log.info("INICIANDO PROCESSO DE OBTENÇÃO DO ARQUIVO")

        # INICIANDO A VARIÁVEL QUE ARMAZENARÁ O TIPO DE INPUT
        input_type = None

        # VERIFICANDO SE O ARGUMENTO ENVIADO É UMA BASE64
        validator_base64, result_base64 = isbase64(input_file)

        if validator_base64:

            # O INPUT É UMA BASE64
            # CHAMA-SE AQ FUNÇÃO PARA DECODIFICAR A BASE64

            input_type = "BYTES"

            execute_log.info("INICIANDO PROCESSO DE OBTENÇÃO DO ARQUIVO - {}".format(input_type))

            return input_type, [base64_to_image(result_base64)]

        # VERIFICANDO SE O ARGUMENTO ENVIADO É O CAMINHO DE UM ARQUIVO
        elif str(input_file).find(".") != -1:
            # O INPUT É UM ARQUIVO

            input_type = "ARCHIVE"

            execute_log.info("INICIANDO PROCESSO DE OBTENÇÃO DO ARQUIVO - {}".format(input_type))

            return input_type, [input_file]

        # VERIFICANDO SE O ARGUMENTO ENVIADO É UMA LISTA
        elif isinstance(input_file, list):

            # O RETORNO É BASE64
            input_type = "BYTES"

            execute_log.info("INICIANDO PROCESSO DE OBTENÇÃO DO ARQUIVO - {}".format(input_type))

            return input_type, [base64_to_image(file) for file in input_file if type(file) == bytes]

        else:
            # O INPUT É UM DIRETÓRIO
            # CHAMA-SE A FUNÇÃO PARA OBTER TODOS OS ARQUIVOS NO DIRETÓRIO

            input_type = "DIRECTORY"

            execute_log.info("INICIANDO PROCESSO DE OBTENÇÃO DO ARQUIVO - {}".format(input_type))

            return input_type, generic_functions.get_files_directory(input_file,
                                                                     settings.FORMAT_TYPES_ACCEPTED)


    def main_extract_table(self, input_images):

        """

            ORQUESTRA A OBTENÇÃO DAS TABELAS CONTIDAS NA IMAGEM.

            CASO ENCONTRE AS TABELAS, SALVA CADA UMA DAS IMAGENS
            PERMITINDO A UTILIZAÇÃO NO MODELO DE OCR.

            # Arguments
                input_images            - Required : Lista de imagens para processamento (List)

            # Returns
                results                - Required : Resultado de modelo (List)

        """

        # INICIANDO A VARIÁVEL QUE ARMAZENARÁ OS RESULTADOS (TABELAS ENCONTRADAS)
        results = []

        execute_log.info("INICIANDO FLUXO DE EXTRAÇÃO DE TABELAS")

        # VERIFICANDO O TIPO DE ENVIO
        input_type, list_images = Extract_Table.orchestra_get_files(input_images)

        # PERCORRENDO CADA UMA DAS IMAGENS ENVIADAS
        for image_file in list_images:

            # INICIANDO A VARIÁVEL QUE ARMAZENARÁ OS RESULTADOS (PARA CADA TABELA OBTIDA)
            list_result_tables = []

            # OBTENDO O DIRETÓRIO E O NOME DO ARQUIVO
            directory, filename = generic_functions.get_split_dir(image_file)

            # OBTENDO O NOME DO ARQUIVO SEM EXTENSÃO
            filename_without_extension = os.path.splitext(image_file)[0]

            # REALIZANDO A LEITURA DA IMAGEM
            # LEITURA EM ESCALA DE CINZA
            image = read_image_gray(image_file)

            if image is not None:

                execute_log.info("IMAGEM LIDA COM SUCESSO")

                # OBTENDO AS TABELAS CONTIDAS NA IMAGEM
                tables = Image_Pre_Processing().find_tables(image)

                # CASO ENCONTROU TABELAS
                if len(tables) > 0:

                    # CRIANDO O DIRETÓRIO PARA SALVAR AS TABELAS ENCONTRADAS
                    # NOVO_DIRETORIO = DIRETORIO/NOME_DO_ARQUIVO
                    os.makedirs(os.path.join(directory,
                                             filename_without_extension),
                                exist_ok=True)

                    # PERCORRENDO TODAS AS TABELAS ENCONTRADAS
                    for idx_table, table in enumerate(tables):

                        # DEFININDO O NOME DA TABELA A SER SALVA (FORMATO PNG)
                        table_filename = "{}{}{}".format("table_", idx_table, ".png")

                        # DEFININDO O DIRETÓRIO E NOME DE SAVE
                        table_filepath = os.path.join(
                            directory, filename_without_extension, table_filename
                        )

                        # SALVANDO A IMAGEM
                        cv2.imwrite(table_filepath, table)

                        # ARMAZENANDO NA LISTA DE TABELAS SALVAS
                        # PERMITINDO USO POSTERIOR NO OCR
                        list_result_tables.append(table_filepath)

                        # ARMAZENANDO O RESULTADO
                        # ARQUIVO DE INPUT (file)
                        # TABELAS OBTIDAS (list_result_tables)
                        results.append((image_file, list_result_tables))

                        execute_log.info("TABELA - {} SALVA COM SUCESSO".format(idx_table))

                # CASO NÃO ENCONTROU TABELAS
                else:
                    results.append((image_file, [None]))

            return results
