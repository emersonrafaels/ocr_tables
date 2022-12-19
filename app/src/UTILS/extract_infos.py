from inspect import stack
import sys
from os import path
from pathlib import Path

import regex as re

try:
    from app.src.UTILS.check_similarity import Check_Similarity
except ModuleNotFoundError:
    sys.path.append(path.join(str(Path(__file__).resolve().parent.parent), "app"))
    from app.src.UTILS.check_similarity import Check_Similarity


def applied_validate_filter(match_analysis, filters_validate):

    """

    VERIFICA SE HÁ FILTROS/VALIDAÇÕES A SEREM APLICADOS NO MATCH DO CAMPO ATUAL.

    EXEMPLOS DE VALIDAÇÕES:

    VALIDAÇÃO DE CPF, VALIDAÇÃO DE CNPJ, VALIDAÇÃO DE IMEI.

    # Arguments
        match_analysis              - Required : Valor para ser
                                                 analisado (String)
        filters_validate            - Required : Filtros ativos para o
                                                 campo atual (List)


    # Returns
        result_filter_validate      - Required : Resultados após aplicação
                                                 dos filtros/validações (Boolean)

    """

    # INICIANDO A VARIÁVEL QUE ARMAZENARÁ O RESULTADO DO FILTRO/VALIDAÇÃO
    result_filter_validate = []

    if False in result_filter_validate:
        return False

    return True


def get_matchs_line(
    text, field_pattern, filters_validate=[], only_one_match_per_line=False
):

    """

    FUNÇÃO RESPONSÁVEL POR ORQUESTRAR OS MATCHS
    ANALISANDO LINHA A LINHA

    RECEBE O TEXTO ANALISADO: text
    RECEBE O PATTERN: field_pattern

    # Arguments
        text                            - Required : Texto analisado (String)
        field_pattern                   - Required : Pattern a ser utilizado (Regex)
        fields_validate                 - Optional : Filtros e validações
                                                     a serem aplicadas (List)
        only_one_match_per_line         - Optional : Se True, retorna
                                                     apenas um append por
                                                     match por linha (Boolean)


    # Returns
        matchs_text      - Required : Resultado do modelo
                                      com os matchs (List)

    """

    matchs_strings = []

    try:
        # SPLITANDO O TEXTO A CADA QUEBRA DE LINHA
        # COM ISSO, OBTEMOS LINHA POR LINHA
        for text_line in text.split("\n"):

            # REALIZANDO O MATCH
            for match in re.finditer(
                pattern=re.compile(field_pattern, re.IGNORECASE), string=text_line
            ):

                # VERIFICANDO SE HÁ FILTROS A SEREM FEITOS
                if applied_validate_filter(match[0], filters_validate):

                    # REALIZANDO O MATCH
                    matchs_strings.append(
                        [
                            text_line,
                            match.start(),
                            match.end(),
                            match[0],
                            match.fuzzy_counts,
                        ]
                    )

                    if only_one_match_per_line:
                        break

    except Exception as ex:
        print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

    return matchs_strings


def get_matchs_strings(text, field_pattern, filters_validate=[]):

    """

    FUNÇÃO RESPONSÁVEL POR ORQUESTRAR OS MATCHS
    ANALISANDO O TEXTO POR COMPLETO.

    RECEBE O TEXTO ANALISADO: text
    RECEBE O PATTERN: field_pattern

    # Arguments
        text             - Required : Texto analisado (String)
        field_pattern    - Required : Pattern a ser utilizado (Regex)
        fields_validate  - Optional : Filtros e validações
                                      a serem aplicadas (List)

    # Returns
        matchs_text      - Required : Resultado do modelo
                                      com os matchs (List)

    """

    matchs_text = []

    try:
        # REALIZANDO O MATCH
        for match in re.finditer(
            pattern=re.compile(field_pattern, re.IGNORECASE), string=text
        ):

            # VERIFICANDO SE HÁ FILTROS A SEREM FEITOS
            if applied_validate_filter(match[0], filters_validate):

                # REALIZANDO O MATCH
                matchs_text.append(
                    [match.start(), match.end(), match[0], match.fuzzy_counts]
                )

    except Exception as ex:
        print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

    return matchs_text


def decorator_valid_similarity(func):

    """

    ORQUESTRA A CHAMADA DA FUNÇÃO DE CÁLCULO DE SIMILARIDADE ITEM A ITEM.

    # Arguments
        search                     - Required : Palavra a ser comparada
                                                ou utilizada como base para obter
                                                as similaridades
                                                dentre as possibilidades (String)

        list_choices               - Required : Palavra ser comparada com a query ou a lista
                                                de palavras a serem comparadas
                                                com a query (String | List)

        percent_match              - Required : Somente serão retornados
                                                os itens acima do
                                                percentual de match (Integer)

        pre_processing             - Optional : Definindo se deve haver
                                                pré processamento (Boolean)

        limit                      - Optional : Limite de resultados
                                                de similaridade (Integer)

    # Returns
        percentual_similarity      - Required : Percentual de similaridade (String | List)

    """

    def valid_value_similarity(
        search, list_choices, percent_match, pre_processing, limit
    ):

        # INICIANDO A VARIÁVEL QUE ARMAZENARÁ O RESULTADO DE SIMILARIDADES
        # APÓS FILTRO POR PERCENTUAL DE MATCH ESPERADO
        result_valid_similarity = []
        validator_similarity = False

        # VALIDANDO O LIMITE ENVIADO
        if limit is False:
            limit = None

        try:
            # OBTENDO AS SIMILARIDADES ENTRE O ITEM PROCURADO E A LISTA DE ITENS
            result_similarity = Check_Similarity.get_values_similarity(
                query=search,
                choices=list_choices,
                pre_processing=pre_processing,
                limit=limit,
            )

            # VALIDANDO OS ITENS QUE ESTÃO ACIMA DO PERCENTUAL DE SIMILARIDADE ENVIADO
            result_valid_similarity = [
                value for value in result_similarity if value[1] > percent_match
            ]

            if len(result_valid_similarity) > 0:
                validator_similarity = True

        except Exception as ex:
            print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

        return validator_similarity, result_valid_similarity

    return valid_value_similarity


@decorator_valid_similarity
def get_similitary():

    pass
