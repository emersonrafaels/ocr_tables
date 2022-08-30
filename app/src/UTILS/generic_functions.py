"""

    FUNÇÕES GENÉRICAS UTILIZANDO PYTHON.

    # Arguments

    # Returns


"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "04/07/2021"


from collections import OrderedDict
import datetime
from inspect import stack
from os import path, makedirs, walk, getcwd
import time
from typing import Union
from unidecode import unidecode
import re


import pandas as pd
from numpy import array


def verify_exists(dir: str) -> bool:

    """

    FUNÇÃO PARA VERIFICAR SE UM DIRETÓRIO (PATH) EXISTE.

    # Arguments
        dir                  - Required : Diretório a ser verificado (String)

    # Returns
        validator            - Required : validator da função (Boolean)

    """

    # INICIANDO O validator DA FUNÇÃO
    validator = False

    try:
        validator = path.exists(dir)
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))

    return validator


def get_files_directory(
    directory: str, format_types_accepted: Union[tuple, list]
) -> list:

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
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))

    return list_archives_accepted


def create_path(dir: str) -> bool:

    """

    FUNÇÃO PARA CRIAR UM DIRETÓRIO (PATH).

    # Arguments
        dir                  - Required : Diretório a ser criado (String)

    # Returns
        validator            - Required : validator da função (Boolean)

    """

    # INICIANDO O validator DA FUNÇÃO
    validator = False

    try:
        # REALIZANDO A CRIAÇÃO DO DIRETÓRIO
        makedirs(dir)

        validator = True
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))

    return validator


def converte_int(valor_para_converter: Union[str, int]) -> int:

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


def convert_list_bi_to_unidimensional(list_bid: Union[tuple, list]) -> list:

    """

    FUNÇÃO QUE PERMITE A CONVERSÃO DE UMA LISTA BIDIMENSIONAL PARA UMA LISTA SIMPLES.

    # Arguments
        list_bid           - Required : Lista Bidimensional. (List)

    # Returns
        list_uni_result    - Required : Lista Unidimensional. (List)

    """

    list_uni_result = []

    try:
        for list_uni in list_bid:
            for value in list_uni:
                list_uni_result.append(value)

    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))
        list_uni_result = list_bid

    return list_uni_result


def drop_duplicates_list(list_values: list) -> list:

    """

    REMOVE DUPLICIDADES EM UMA LISTA DE VALORES

    # Arguments
        list_values                - Required : Lista de input. (List)

    # Returns
        list_without_duplicates    - Required : Lista sem duplicidades. (List)

    """

    if not isinstance(list_values, (tuple, list)):

        list_values = list_values.split()

    return list(OrderedDict.fromkeys(list_values))


def has_number(value_test: str) -> bool:

    """

    FUNÇÃO QUE ANALISA SE HÁ NÚMEROS EM UMA STRING

    # Arguments
        value_test         - Required : String a ser testada. (String)

    # Returns
        list_uni_result    - Required : Lista Unidimensional. (List)

    """

    # OBTENDO O PATTERN DE APENAS NÚMEROS
    pattern_number = "[^\d]"

    try:
        # REALIZANDO A VERIFICAÇÃO
        if len(re.sub(pattern=pattern_number, string=str(value_test), repl="")) > 0:
            # A STRING POSSUI NÚMEROS
            return True
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

    return False


def get_split_dir(dir: str) -> [str, str]:

    """

    USADO PARA DIVIDIR O NOME DO CAMINHO EM UM PAR DE CABEÇA E CAUDA.
    AQUI, CAUDA É O ÚLTIMO COMPONENTE DO NOME DO CAMINHO E CABEÇA É TUDO QUE LEVA A ISSO.

    EX: nome do caminho = '/home/User/Desktop/file.txt'
    CABEÇA: '/home/User/Desktop'
    CAUDA: 'file.txt'

    * O DIR PODE SER UMA BASE64

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


def read_csv(data_dir: str) -> [bool, pd.DataFrame]:

    """

    REALIZA LEITURA DA BASE (CSV)

    # Arguments
        data_dir                      - Required : Diretório da base a ser lida (String)

    # Returns
        validator                     - Required : Validação da função (Boolean)
        dataframe                     - Required : Base lida (DataFrame)

    """

    # INICIANDO O validator
    validator = False

    # INICIANDO O DATAFRAME DE RESULTADO DA LEITURA
    dataframe = pd.DataFrame()

    try:
        dataframe = pd.read_csv(data_dir, encoding="utf-8")

        validator = True
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

    return validator, dataframe


def save_excel(dataframe_to_save: pd.DataFrame, data_dir: str) -> bool:

    """

    REALIZA SAVE DA BASE (CSV)

    # Arguments
        dataframe_to_save             - Required : Base a ser salva (DataFrame)
        data_dir                      - Required : Diretório da base a ser salva (String)

    # Returns
        validator                     - Required : Validação da função (Boolean)

    """

    # INICIANDO O validator
    validator = False

    try:
        dataframe_to_save.to_excel(data_dir, index=None)

        validator = True
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

    return validator


def get_date_time_now(return_type: str) -> str:

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


def order_list_with_arguments(
    list_values: Union[tuple, list], number_column_order: int = 1, limit: int = 1
) -> list:

    """

    FUNÇÃO PARA ORDENAR UMA LISTA E OBTER UM NÚMERO (LIMIT) DE ARGUMENTOS.

        1) ORDENA A LISTA USANDO UM DOS SEUS ARGUMENTOS (number_column_order)
        2) FILTRA A LISTA DE ACORDO COM UM NÚMERO DESEJADO DE ELEMENTOS (limit)

    # Arguments
        list_values                  - Required : Lista de valores para processar (List)
        number_column_order          - Optional : Qual o argumento deve ser usado
                                                  como parâmetro de ordenação (Integer)
        limit                        - Optional : Número desejado de argumentos
                                                  para retorno da função (Integer)

    # Returns
        return_list                 - Required : Lista resultado (List)

    """

    # INICIANDO A LISTA DE VARIÁVEL QUE ARMAZENARÁ OS INDEX RESULTANTES
    list_idx = []

    # VERIFICANDO SE O ARGUMENTO DE ORDENAÇÃO É UM NÚMERO INTEIRO
    if isinstance(number_column_order, str):
        if number_column_order.isdigit():
            number_column_order = int(number_column_order)
        else:
            number_column_order = 1

    # VERIFICANDO SE O VALOR DE LIMIT É UM NÚMERO INTEIRO
    if isinstance(limit, str):
        if limit.isdigit():
            limit = int(limit)
        else:
            limit = 1

    # ORDENANDO POR UM DOS VALORES DE ARGUMENTOS DA LISTA
    # FILTRANDO DE ACORDO COM O LIMITE DESEJADO
    list_result_filter = sorted(
        list_values, key=lambda row: (row[number_column_order]), reverse=True
    )[:limit]

    # PERCORRENDO A LISTA DE RESULTADOS, PARA FILTAR NA LISTA ORIGINAL
    # O OBJETIVO É MANTER NA LISTA ORIGINAL (MANTENDO A ORDEM DELA)
    for value in list_result_filter:
        list_idx.append(list_values.index(value))

    # MANTENDO APENAS OS IDX DESEJADOS
    return_list = array(list_values, dtype=object)[list_idx]

    # RETORNANDO O RESULTADO
    return return_list


def remove_line_with_black_list_words(
    text: str, list_words: list = [], mode: str = "FIND"
) -> str:

    """

    FUNÇÃO PARA REMOVER LINHAS QUE CONTÉM PALAVRAS NÃO DESEJADAS

    HÁ DOIS MODOS DE BUSCA:
        EQUAL - A PALAVRA ESTÁ EXATAMENTE IGUAL
        FIND - A PALAVRA ESTÁ PARCIALMENTE IGUAL

    # Arguments
        text                  - Required : Texto a ser analisado (String)
        list_words            - Optional : Lista de palavras a serem buscadas (List)
        mode                  - Optional : Modo de busca da palavra (String)

    # Returns
        return_text          - Required : Texto resultante após a análise (String)

    """

    # INICIANDO O validator
    validator = False

    return_text = ""

    for line in text.split("\n"):

        validator = False

        # PERCORRENDO TODAS AS PALAVRAS DA BLACK LIST
        for value in list_words:

            if mode == "FIND":

                if line.find(value) != -1:
                    # A PALAVRA FOI ENCONTRADA
                    validator = True
                    break

            else:

                if value in line.split(" "):
                    # A PALAVRA FOI ENCONTRADA
                    validator = True
                    break

        if validator is False:
            # A PALAVRA NÃO FOI ENCONTRADA
            return_text = return_text + "\n" + line

    # RETORNANDO O TEXTO FINAL
    return return_text


def verify_find_intersection(data_verified: str, data_lists: list) -> bool:

    """

    FUNÇÃO PARA VERIFICAR SE UM DADO (DATA_VERIFIED) ESTÁ CONTIDO
    EM QUALQUER ELEMENTO DE UMA LISTA DE DADOS.

    ESSA VERIFICAÇÃO É REALIZADA UTILIZANDO PARTE DA STRING,
    NESSE CASO, UTILIZA-SE O MÉTODO 'FIND'.

    # Arguments
        data_verified               - Required : Dado a ser verificado (String)
        data_lists                  - Required : Lista de dados (List)

    # Returns
        validator                   - Required : validator da função (String)

    """

    # INICIANDO O validator DA FUNÇÃO
    validator = False

    try:
        # PERCORRENDO TODOS OS DADOS DA LISTA DE DADOS
        for value in data_lists:

            # VERIFICANDO SE O VALOR A SER VERIFICADO ESTÁ CONTIDO NA LISTA DE DADOS
            # ESSA VERIFICAÇÃO É REALIZADA UTILIZANDO PARTE DA STRING
            # NESSE CASO, UTILIZA-SE O MÉTODO 'FIND'
            if data_verified.find(value) != -1 and data_verified != "":
                validator = True
                break

    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

    return validator


def convert_text_unidecode(text: str) -> str:

    """

    TRANSFORMA O TEXTO PURO EM FORMATO UNIDECODE (SEM ACENTOS).

    # Arguments
        text                    - Required : Texto a ser convertido. (String)

    # Returns
        text_unidecode          - Required : Texto após conversão. (String)

    """

    try:
        return unidecode(text)
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))
        return text
