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
from UTILS.image_view import image_view_functions


class Extract_Table():

    def __init__(self):

        pass


    def main_extract_table(self, dir_image):

        # INICIANDO A VARIÁVEL QUE ARMAZENARÁ OS RESULTADOS (TABELAS ENCONTRADAS)
        results = []

        # INICIANDO A VARIÁVEL QUE ARMAZENARÁ OS RESULTADOS (PARA CADA TABELA OBTIDA)
        list_result_tables = []

        # OBTENDO O DIRETÓRIO E O NOME DO ARQUIVO
        directory, filename = generic_functions.get_split_dir(dir_image)

        # OBTENDO O NOME DO ARQUIVO SEM EXTENSÃO
        filename_without_extension = os.path.splitext(filename)[0]

        # REALIZANDO A LEITURA DA IMAGEM
        # LEITURA EM ESCALA DE CINZA
        image = read_image_gray(dir_image)

        # OBTENDO AS TABELAS CONTIDAS NA IMAGEM
        tables = Image_Pre_Processing().find_tables(image)

        # CASO ENCONTROU TABELAS
        if len(tables) > 0:

            # CRIANDO O DIRETÓRIO PARA SALVAR AS TABELAS ENCONTRADAS
            # NOVO_DIRETORIO = DIRETORIO/NOME_DO_ARQUIVO
            os.makedirs(os.path.join(directory, filename_without_extension), exist_ok=True)

            # PERCORRENDO TODAS AS TABELAS ENCONTRADAS
            for i, table in enumerate(tables):

                # DEFININDO O NOME DA TABELA A SER SALVA (FORMATO PNG)
                table_filename = "{}{}{}".format("table_", i, ".png")

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
                results.append((dir_image, list_result_tables))

                print("TABELA - {} SALVA COM SUCESSO".format(len(table_filename)))

        return results
