from inspect import stack
import re

try:
    from src.UTILS.check_similarity import Check_Similarity
except ModuleNotFoundError:
    sys.path.append(path.join(str(Path(__file__).resolve().parent.parent), "app"))
    from src.UTILS.check_similarity import Check_Similarity


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


def get_matchs_line(text, field_pattern, filters_validate=[]):

    """

        FUNÇÃO RESPONSÁVEL POR ORQUESTRAR OS MATCHS
        ANALISANDO LINHA A LINHA

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

    matchs_strings = []

    try:
        # SPLITANDO O TEXTO A CADA QUEBRA DE LINHA
        # COM ISSO, OBTEMOS LINHA POR LINHA
        for text_line in text.split("\n"):

            # REALIZANDO O MATCH
            for match in re.finditer(pattern=re.compile(field_pattern,
                                                        re.IGNORECASE),
                                     string=text_line):

                # VERIFICANDO SE HÁ FILTROS A SEREM FEITOS
                if applied_validate_filter(match[0], filters_validate):

                    # REALIZANDO O MATCH
                    matchs_strings.append([text_line, match.start(), match.end(), match[0]])

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
        for match in re.finditer(pattern=re.compile(field_pattern,
                                                    re.IGNORECASE),
                                 string=text):

            # VERIFICANDO SE HÁ FILTROS A SEREM FEITOS
            if applied_validate_filter(match[0], filters_validate):

                # REALIZANDO O MATCH
                matchs_text.append([match.start(), match.end(), match[0]])

    except Exception as ex:
        print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

    return matchs_text

