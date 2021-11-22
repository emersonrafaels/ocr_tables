from inspect import stack
import re

from UTILS.image_ocr import ocr_functions


def pos_processing_cnpj(text_input, pattern):

    # MANTENDO APENAS NÚMEROS
    text_only_numbers = re.sub(pattern=pattern, string=text_input, repl="").strip()

    output = "{}.{}.{}/{}-{}".format(text_only_numbers[:2],
                                     text_only_numbers[2:5],
                                     text_only_numbers[8:12],
                                     text_only_numbers[12:])

    return output


def pos_processing_faturamento(text_input):

    # MANTENDO APENAS NÚMEROS
    output = [result for result in text_input.split(" ") if result != "R$" and result != "RS"]

    return output


def get_matchs_line(text, field_pattern, filters_validate=[]):

    """

        FUNÇÃO RESPONSÁVEL POR ORQUESTRAR OS MATCHS
        ANALISANDO LINHA A LINHA

        RECEBE O TEXTO ANALISADO: text
        RECEBE O PATTERN: field_pattern

        # Arguments
            text                  - Required : Texto analisado (String)
            field_pattern         - Required : Pattern a ser utilizado (Regex)
            filters_validate      - Optional : Filtros a validações a serem aplicadas (List)
        # Returns
            matchs_text            - Required : Resultado do modelo com os matchs (List)

    """

    matchs_string = []

    try:
        # SPLITANDO O TEXTO A CADA QUEBRA DE LINHA
        # COM ISSO, OBTEMOS LINHA POR LINHA
        for text_line in text.split("\n"):

            # REALIZANDO O MATCH
            for match in re.finditer(pattern=re.compile(field_pattern, re.IGNORECASE),
                                     string=text_line):

                # REALIZANDO O MATCH
                matchs_string.append([text_line, match.start(), match.end(), match[0]])

    except Exception as ex:
        print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

    return matchs_string