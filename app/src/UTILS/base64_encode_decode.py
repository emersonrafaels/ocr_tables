"""

    FUNÇÕES UTEIS PARA CODIFICAÇÃO E DECODIFICAÇÃO DE BASE64.

    A SAÍDA DA DECODIFICAÇÃO É NO FORMATO ARQUIVO IMAGEM (SALVO NA PASTA RAIZ).

    # Arguments
        file_base64                - Required : Input no formato Base64 (BASE64)

    # Returns
        built_pdf                  - Required : Caminho/Nome do arquivo gerado (String)

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "08/03/2022"


import base64
from inspect import stack
import mimetypes
from tempfile import NamedTemporaryFile

import magic

from app import execute_log


def base64_get_extension(file_base64_decode: bytes) -> str:

    """

     ESSA FUNÇÃO RETORNA O TIPO DA IMAGEM DECODIFICADA DO BASE64.

     PARA OBTER A EXTENSÃO UTILIZA-SE O MIMETYPE:
        Adivinha a extensão de um arquivo com base em seu tipo MIME, fornecido por tipo .
        O valor de retorno é uma string que fornece uma
        extensão de nome de arquivo, incluindo o ponto inicial ( '.')

     # Arguments
        file_base64_decode          - Required : Input no formato Base64 Decodificado (Stromg)

    # Returns
        extension                  - Required : Extensão da imagem decodificada (String)

    """

    extension = None

    try:
        # OBTENDO A EXTENSÃO
        mime_type = magic.from_buffer(file_base64_decode, mime=True)
        extension = mimetypes.guess_extension(mime_type)

    except Exception as ex:
        execute_log.error("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))

    return extension


def isbase64(input_file: bytes) -> bool:

    """

     VERIFICA SE UM VALOR É UMA BASE64.

     FUNCIONA PARA VALORES EM FORMATO:
        1) BYTES
        2) STRING

     # Arguments
        input_file                 - Required : Valor a ser verificado (Bytes | String)

    # Returns
        verificator                - Required : Verificador de base64 (Boolean)

    """

    try:
        # VERIFICANDO SE O ENVIADO ESTÁ EM FORMATO STRING
        if isinstance(input_file, str):

            # CONVERTENDO A STRING EM BYTES
            input_file_bytes = bytes(input_file, "ascii")

        # VERIFICANDO SE O ENVIADO ESTÁ EM FORMATO DE BYTES
        elif isinstance(input_file, bytes):

            # MANTENDO EM BYTES
            input_file_bytes = input_file

        else:
            raise ValueError("Argument must be string or bytes")

        return (
            base64.b64encode(base64.b64decode(input_file_bytes)) == input_file_bytes,
            input_file_bytes,
        )

    except Exception:
        return False, None


def base64_to_image(file_base64: bytes) -> str:

    """

     ESSA FUNÇÃO TEM COMO OBJETIVO, CONVERTER FORMATO DE INPUT (BASE64) -> IMAGE (PNG)

     O ARQUIVO OBTIDO (PNG) É SALVO NA MÁQUINA QUE ESTÁ EXECUTANDO O MODELO.

     # Arguments
        file_base64                - Required : Input no formato Base64 (BASE64)

    # Returns
        built_image                - Required : Caminho/Nome do arquivo gerado (String)

    """

    # INICIANDO O NOME E DIR DE SAVE DO ARQUIVO RESULTANTE
    # CONVERSÃO BASE64 TO IMAGE
    built_image = None

    try:
        # DECODOFICANDO A BASE64
        result_decode = base64.b64decode(file_base64.decode())

        execute_log.info("BASE64 DECODIFICADA COM SUCESSO")

        # OBTENDO A EXTENSÃO DO ARQUIVO
        extension = base64_get_extension(result_decode)

        execute_log.info("BASE64 - EXTENSÃO: {}".format(extension))

        # REALIZANDO A ABERTURA DE UM ARQUIVO (QUE SERÁ ESCRITO NA MÁQUINA)
        with NamedTemporaryFile(suffix=extension, delete=False) as temp_file:

            try:
                temp_file.write(result_decode)

                # SOBREESCREVENDO O VALOR DO BUILT_IMAGE
                built_image = temp_file.name

                execute_log.info("ARQUIVO SALVO EM: {}".format(built_image))

            except Exception as ex:
                execute_log.error("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))

    except Exception as ex:
        execute_log.error("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))

    return built_image


def image_to_base64(file_image: str) -> bytes:

    """

     ESSA FUNÇÃO TEM COMO OBJETIVO, CONVERTER FORMATO DE INPUT (PNG) -> BASE64

     O ARQUIVO OBTIDO (PNG) É SALVO NA MÁQUINA QUE ESTÁ EXECUTANDO O MODELO.

     # Arguments
        file_image                - Required : Caminho do arquivo
                                               no formato imagem (String)

    # Returns
        built_base64              - Required : Valor no formato Base64 (BASE64)

    """

    # INICIANDO A VARIÁVEL QUE RECEBERÁ O VALOR DA BASE64
    built_base64 = None

    try:
        # DECODOFICANDO A BASE64, ARMAZENANDO-O NO OBJETO ABERTO
        # ESCREVENDO NA MÁQUINA
        built_base64 = base64.b64encode(open(file_image, "rb").read())

    except Exception as ex:
        execute_log.error("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

    return built_base64
