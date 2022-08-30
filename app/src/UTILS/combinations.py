import itertools

from app.src.UTILS.generic_functions import convert_list_bi_to_unidimensional


def all_combinations(
    any_list=[], split_words=False, min_n_combinations=None, max_n_combinations=None
):

    """

    ESSA FUNÇÃO TEM COMO OBJETIVO GERAR TODAS AS COMBINAÇÕES
    TODAS AS COMBINAÇÕES POSSÍVEIS EM UMA LISTA DE DADOS.

    EX:

    1) anylist: ['a', 'b', 'c']
    2) return: [('a', 'b', 'c'), ('a',), ('b',),
                ('c',), ('a', 'b'), ('a', 'c'),
                ('b', 'c')]

    # Arguments
        any_list              - Required : Qualquer lista (List)
        split_words           - Optional : Parâmetro para verificar se é
                                           necessário realizar o split
                                           dos textos dentro da lista (Boolean)
        min_n_combinations    - Optional : Número mínimo de combinação de palavras.
                                           Caso não seja fornecido um número,
                                           considera-o tamanho da lista (Boolean)
        max_n_combinations    - Optional : Número máximo de combinação de palavras.
                                           Caso não seja fornecido um número,
                                           considera-o tamanho da lista (Boolean)

    # Returns
        combinations          - Required : Combinações da lista (Generator)

    """

    # VERIFICANDO SE O ENVIO É UMA LISTA
    if not isinstance(any_list, list):
        any_list = list(any_list)

    # VERIFICANDO SE É NECESSÁRIO REALIZAR O SPLIT DAS PALAVRAS DENTRO DA LISTA
    if split_words:
        any_list = convert_list_bi_to_unidimensional(
            [str(value).split(" ") for value in any_list]
        )

    # VERIFICANDO A QUANTIDADE DE COMBINAÇÕES - MIN
    if min_n_combinations is None or not isinstance(min_n_combinations, int):
        min_n_combinations = 1

    # VERIFICANDO A QUANTIDADE DE COMBINAÇÕES - MAX
    if max_n_combinations is None or not isinstance(max_n_combinations, int):
        max_n_combinations = len(any_list)

    # OBTENDO AS COMBINAÇÕES
    list_combinations = itertools.chain.from_iterable(
        itertools.combinations(any_list, i)
        for i in range(min_n_combinations, max_n_combinations + 1)
    )

    return list_combinations
