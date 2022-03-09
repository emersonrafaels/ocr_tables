"""

    FUNÇÕES GENÉRICAS UTILIZANDO PYTHON.

    # Arguments

    # Returns


"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "04/07/2021"


import datetime
from inspect import stack
from os import path, makedirs, walk
import time

import pandas as pd


def verify_exists(dir):

    """

        FUNÇÃO PARA VERIFICAR SE UM DIRETÓRIO (PATH) EXISTE.

        # Arguments
            dir                  - Required : Diretório a ser verificado (String)

        # Returns
            validador            - Required : Validador da função (Boolean)

    """

    # INICIANDO O VALIDADOR DA FUNÇÃO
    validador = False

    try:
        validador = path.exists(dir)
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))

    return validador


def get_files_directory(directory, format_types_accepted):

    """

        FUNÇÃO PARA OBTER OS ARQUIVOS EM UM DETERMINADO DIRETÓRIO
        FILTRANDO APENAS OS ARQUIVOS DOS FORMATOS ACEITOS POR ESSA API

        # Arguments
            directory                    - Required : Caminho/Diretório para obter os arquivos (String)
            format_types_accepted        - Required : Tipos de arquivos aceitos (List)

        # Returns
            list_archives_accepted       - Required : Caminho dos arquivos listados (List)

    """

    # INICIANDO A VARIÁVEL QUE ARMAZENARÁ O RESULTADO
    list_archives_accepted = []

    try:
        # OBTENDO A LISTA DE ARQUIVOS CONTIDOS NO DIRETÓRIO
        for root in walk(directory):
            for dir in root:
                for files in dir:
                    if path.splitext(files)[1] in format_types_accepted:
                        list_archives_accepted.append(path.join(root[0], files))

    except Exception as ex:
        print(f"ERRO NA FUNÇÃO {stack()[0][3]} - {ex}")

    return list_archives_accepted


def create_path(dir):

    """

        FUNÇÃO PARA CRIAR UM DIRETÓRIO (PATH).

        # Arguments
            dir                  - Required : Diretório a ser criado (String)

        # Returns
            validador            - Required : Validador da função (Boolean)

    """

    # INICIANDO O VALIDADOR DA FUNÇÃO
    validador = False

    try:
       # REALIZANDO A CRIAÇÃO DO DIRETÓRIO
       makedirs(dir)

       validador = True
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))

    return validador


def converte_int(valor_para_converter):

    """

        FUNÇÃO GENÉRICA PARA CONVERTER UM VALOR PARA FORMATO INTEIRO.


        # Arguments
            valor_para_converter              - Required : Valor para converter (Object)

        # Returns
            valor_para_converter              - Required : Valor após conversão (Integer)

    """

    try:
        if isinstance(valor_para_converter, int):
            return valor_para_converter
        else:
            return int(valor_para_converter)
    except Exception as ex:
        print(ex)
        return None


def get_split_dir(dir):

    """

        USADO PARA DIVIDIR O NOME DO CAMINHO EM UM PAR DE CABEÇA E CAUDA.
        AQUI, CAUDA É O ÚLTIMO COMPONENTE DO NOME DO CAMINHO E CABEÇA É TUDO QUE LEVA A ISSO.

        EX: nome do caminho = '/home/User/Desktop/file.txt'
        CABEÇA: '/home/User/Desktop'
        CAUDA: 'file.txt'


        # Arguments
            dir                 - Required : Caminho a ser splitado (String)

        # Returns
            directory           - Required : Cabeça do diretório (String)
            filename            - Required : Cauda do diretório (String)

    """

    # INICIANDO AS VARIÁVEIS A SEREM OBTIDAS
    directory = filename = None

    try:
        directory, filename = path.split(dir)
    except Exception as ex:
        print(ex)

    return directory, filename


def read_csv(data_dir):

    """

        REALIZA LEITURA DA BASE (CSV)

        # Arguments
            data_dir                      - Required : Diretório da base a ser lida (String)

        # Returns
            validador                     - Required : Validação da função (Boolean)
            dataframe                     - Required : Base lida (DataFrame)

    """

    # INICIANDO O VALIDADOR
    validador = False

    # INICIANDO O DATAFRAME DE RESULTADO DA LEITURA
    dataframe = pd.DataFrame()

    try:
        dataframe = pd.read_csv(data_dir, encoding='utf-8')

        validador = True
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

    return validador, dataframe


def save_excel(dataframe_to_save, data_dir):

    """

        REALIZA SAVE DA BASE (CSV)

        # Arguments
            dataframe_to_save             - Required : Base a ser salva (DataFrame)
            data_dir                      - Required : Diretório da base a ser salva (String)

        # Returns
            validador                     - Required : Validação da função (Boolean)

    """

    # INICIANDO O VALIDADOR
    validador = False

    try:
        dataframe_to_save.to_excel(data_dir, index=None)

        validador = True
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

    return validador


def get_date_time_now(return_type):

    """

        OBTÉM TODOS OS POSSÍVEIS RETORNOS DE DATA E TEMPO.

        # Arguments
            return_type                    - Required : Formato de retorno. (String)

        # Returns

    """

    """%d/%m/%Y %H:%M:%S | %Y-%m-%d %H:%M:%S
    Dia: %d
    Mês: %
    Ano: %Y
    Data: %Y/%m/%d

    Hora: %H
    Minuto: %M
    Segundo: %S"""

    try:
        ts = time.time()
        stfim = datetime.datetime.fromtimestamp(ts).strftime(return_type)

        return stfim
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))
        return datetime.datetime.now()

