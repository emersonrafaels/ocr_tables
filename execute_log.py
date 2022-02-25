"""

    O LOG É UM MEIO DE RASTREAR EVENTOS QUE ACONTECEM QUANDO ALGUM SOFTWARE É
    EXECUTADO.

    A BIBLIOTECA LOGGING POSSUI COMO DEFAULT, OS SEGUINTES LOG LEVELS:

    DEBUG - INFORMAÇÕES MAIS DETALHADAS, QUANDO ESTAMOS BUSCANDO PROBLEMAS
    INFO - CONFIRMAR QUE AS COISAS ESTÃO FUNCIONANDO COMO ESPERADO
    WARNING - INFORMAÇÃO DE QUE ALGO INESPERADO ACONTECEU (MAS TUDO FUNCIONA BEM)
    ERROR - QUANDO ALGO INESPERADO OCORRE E O PROGRAMA NÃO CONSEGUE EXECUTAR ALGO
    CRITICAL - UM ERRO GRAVE QUE IMPEDIU O SISTEMA DE EXECUTAR ALGO

    # Arguments

    # Returns

"""

__version__ = "2.0"
__author__ = """Patricia Catandi (CATANDI) & Oscar Bedoya (BEDOYAO) & Edson Mano (EDDANSA) &
                Lucas Menegheso (MENEFAR) & Fabio Andre Sonza (SONZAFA) & 
                Rafael Barbosa Ferreira (RBFRDTH) & Felipe Gomes Luttzolff (LUTTZOL) &
                Emerson V. Rafael (EMERVIN) & Henrique Fantinatti (HENRFAN)"""

from datetime import datetime
from inspect import stack
import logging
from os import path
import time

from dynaconf import settings

from UTILS.generic_functions import get_date_time_now, create_path, verify_exists


def configure_logging():

    """

        CONFIGURANDO OS LOGS (LOGGING).

        DOIS LOGS SERÃO CONFIGURADOS:
            - MANIPULADORES DE LOGS - ARQUIVO DE LOG
            - MANIPULADORES DE LOGS - CONSOLE (TELA DO USUÁRIO)

        # Arguments

        # Returns
            validador            - Required : Validador da função (Boolean)

    """

    # INICIANDO O VALIDADOR DA FUNÇÃO
    validador = False

    # CONFIGURAÇÕES DE LOG
    try:
        if settings.APPNAME not in settings.LOGGERS.keys():

            # CRIANDO O LOGGER
            logger = logging.getLogger(settings.APPNAME)

            # DEFININDO O LEVEL PARA LOGS
            # LOGS ACIMA DESSE LEVEL SERÃO REGISTRADOS
            logger.setLevel(settings.LOGLEVEL)

            if not len(logger.handlers):

                # DEFININDO O LOCAL DO ARQUIVO DE LOG
                dir_filename = path.join(settings.DIR_SAVE_LOGS, settings.LOG_FILENAME)

                # CRIANDO OS MANIPULADORES DE LOGS - ARQUIVO DE LOG
                fh = logging.FileHandler(dir_filename)
                fh.setLevel(settings.LOGLEVEL_FILE)

                # CRIANDO OS MANIPULADORES DE LOGS - CONSOLE (TELA DO USUÁRIO)
                ch = logging.StreamHandler()
                ch.setLevel(settings.LOGLEVEL_CONSOLE)

                # CRIANDO OS FORMATOS DE LOGS
                formatter_f = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')
                formatter_c = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

                # ATRIBUINDO OS FORMATOS DE LOGS PARA CADA UM DOS HANDLERS
                fh.setFormatter(formatter_f)
                ch.setFormatter(formatter_c)

                # ADICIONANDO OS HANDLERS AO LOGGER (QUE CONTERÁ DOIS HANDLERS)
                logger.addHandler(fh)
                logger.addHandler(ch)

            settings.LOGGERS[settings.APPNAME] = logger

            validador = True

    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))

    return validador


def startLog():

    """

        CONFIGURANDO OS LOGS (LOGGING).

        DOIS LOGS SERÃO CONFIGURADOS:
            - MANIPULADORES DE LOGS - ARQUIVO DE LOG
            - MANIPULADORES DE LOGS - CONSOLE (TELA DO USUÁRIO)

        # Arguments

        # Returns
            validador            - Required : Validador da função (Boolean)

    """

    # INICIANDO O VALIDADOR DA FUNÇÃO
    validador = False

    # VERIFICANDO SE O DIRETÓRIO DE SAVE DOS LOGS EXISTE
    validador = verify_exists(settings.DIR_SAVE_LOGS)

    if validador is False:

        # CRIANDO O DIRETÓRIO DE SAVE DOS LOGS
        validador = create_path(settings.DIR_SAVE_LOGS)

    if validador:

        # CONFIGURANDO O USO DA LOGGING (REGISTRANDO NO ARQUIVO DE LOG E NO CONSOLE)
        validador = configure_logging()

    return validador


def on_log(origin: str, msg: str, image: str, idt: str):

    """

        REALIZANDO O REGISTRO DE INÍCIO DOS LOGS

        # Arguments
            origin               - Required : Origem dos logs (String)
            msg                  - Required : Mensagem do log (String)
            image                - Required : Image atual (String)
            idt                  - Required : Identificação da chamada (String)

        # Returns
            validador            - Required : Validador da função (Boolean)

    """

    try:
        # OBTENDO O LOGGER
        logger = logging.getLogger(settings.APPNAME)

        # REGISTRANDO O LOG - LOGGING
        logger.info("INÍCIO DO PROCESSAMENTO - {}".format(msg))

    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))



def start(origin: str, msg: str, image: str, idt: str):

    """

        REALIZANDO REGISTRO DE START

        # Arguments
            origin               - Required : Origem dos logs (String)
            msg                  - Required : Mensagem do log (String)
            image                - Required : Image atual (String)
            idt                  - Required : Identificação da chamada (String)

        # Returns
            validador            - Required : Validador da função (Boolean)

    """

    try:
        # OBTENDO O LOGGER
        logger = logging.getLogger(settings.APPNAME)

        # REGISTRANDO O LOG - LOGGING
        logger.error("START - {}".format(msg))

    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))


def end(origin: str, msg: str, image: str, idt: str, start_time: float):

    """

        REALIZANDO REGISTRO DE ERRO

        # Arguments
            origin               - Required : Origem dos logs (String)
            msg                  - Required : Mensagem do log (String)
            image                - Required : Image atual (String)
            idt                  - Required : Identificação da chamada (String)

        # Returns
            validador            - Required : Validador da função (Boolean)

    """

    try:
        # OBTENDO O LOGGER
        logger = logging.getLogger(settings.APPNAME)

        # REGISTRANDO O LOG - LOGGING
        logger.info("FIM DO PROCESSAMENTO - {}".format(msg))

    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))


def error(origin: str, msg: str, image: str, idt: str):

    """

        REALIZANDO REGISTRO DE ERRO

        # Arguments
            origin               - Required : Origem dos logs (String)
            msg                  - Required : Mensagem do log (String)
            image                - Required : Image atual (String)
            idt                  - Required : Identificação da chamada (String)

        # Returns
            validador            - Required : Validador da função (Boolean)

    """

    try:
        # OBTENDO O LOGGER
        logger = logging.getLogger(settings.APPNAME)

        # REGISTRANDO O LOG - LOGGING
        logger.error("{}".format(msg))

    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))


def warnings(origin: str, msg: str, image: str, idt: str):

    """

        REALIZANDO O REGISTRO DE WARNINGS

        # Arguments
            origin               - Required : Origem dos logs (String)
            msg                  - Required : Mensagem do log (String)
            image                - Required : Image atual (String)
            idt                  - Required : Identificação da chamada (String)

        # Returns
            validador            - Required : Validador da função (Boolean)

    """

    try:
        # OBTENDO O LOGGER
        logger = logging.getLogger(settings.APPNAME)

        # REGISTRANDO O LOG - LOGGING
        logger.warning("{}".format(msg))

    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))


def info(origin: str, msg: str, image: str, idt: str):

    """

        REALIZANDO REGISTRO DE INFORMAÇÕES

        # Arguments
            origin               - Required : Origem dos logs (String)
            msg                  - Required : Mensagem do log (String)
            image                - Required : Image atual (String)
            idt                  - Required : Identificação da chamada (String)

        # Returns
            validador            - Required : Validador da função (Boolean)

    """

    try:
        # OBTENDO O LOGGER
        logger = logging.getLogger(settings.APPNAME)

        # REGISTRANDO O LOG - LOGGING
        logger.info("{}".format(msg))

    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))