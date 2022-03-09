"""

    SERVIÇO PARA REALIZAÇÃO DE EXTRAÇÃO DE TABELAS.

    1) APLICA TÉCNICAS DE PRÉ PROCESSAMENTO [
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
__data_atualizacao__ = "15/12/2021"


import os

import cv2
from dynaconf import settings

from model_pre_processing import Image_Pre_Processing
from UTILS.image_read import read_image_gray
from UTILS import generic_functions
import execute_log

from UTILS.base64_encode_decode import base64_to_image


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

            # Returns
                list_files_result                - Required : Caminho do(s) arquivo(s) listados. (List)

        """

        # VERIFICANDO SE O ARGUMENTO ENVIADO É UMA BASE64
        if type(input_file) == bytes:
            # O INPUT É UMA BASE64
            # CHAMA-SE AQ FUNÇÃO PARA DECODIFICAR A BASE64
            return [base64_to_image(input_file)]

        # VERIFICANDO SE O ARGUMENTO ENVIADO É O CAMINHO DE UM ARQUIVO
        elif str(input_file).find(".") != -1:
            # O INPUT É UM ARQUIVO
            return [input_file]

        else:
            # O INPUT É UM DIRETÓRIO
            # CHAMA-SE A FUNÇÃO PARA OBTER TODOS OS ARQUIVOS NO DIRETÓRIO
            return generic_functions.get_files_directory


    def main_extract_table(self, list_images):

        """

            ORQUESTRA A OBTENÇÃO DAS TABELAS CONTIDAS NA IMAGEM.

            CASO ENCONTRE AS TABELAS, SALVA CADA UMA DAS IMAGENS
            PERMITINDO A UTILIZAÇÃO NO MODELO DE OCR.

            # Arguments
                list_images            - Required : Lista de imagens para processamento (List)

            # Returns
                results                - Required : Resultado de modelo (List)

        """

        # INICIANDO A VARIÁVEL QUE ARMAZENARÁ OS RESULTADOS (TABELAS ENCONTRADAS)
        results = []

        # PERCORRENDO CADA UMA DAS IMAGENS ENVIADAS
        for file in list_images:

            # INICIANDO A VARIÁVEL QUE ARMAZENARÁ OS RESULTADOS (PARA CADA TABELA OBTIDA)
            list_result_tables = []

            # OBTENDO O DIRETÓRIO E O NOME DO ARQUIVO
            directory, filename = generic_functions.get_split_dir(file)

            # OBTENDO O NOME DO ARQUIVO SEM EXTENSÃO
            filename_without_extension = os.path.splitext(filename)[0]

            # VERIFICANDO O TIPO DE ENVIO
            images = Extract_Table.orchestra_get_files(file)

            for image_file in images:

                # REALIZANDO A LEITURA DA IMAGEM
                # LEITURA EM ESCALA DE CINZA
                image = read_image_gray(file)

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
                        results.append((file, list_result_tables))

                        execute_log.info("TABELA - {} SALVA COM SUCESSO".format(idx_table))

        return results
