"""

    FUNÇÕES UTEIS PARA PRÉ PROCESSAMENTO DA IMAGEM, ANTES DA APLICAÇÃO DO OCR.

    1. A IMAGEM É LIDA EM ESCALA DE CINZA;
    2. GAUSSIAN BLUR É EXECUTADO PARA REMOVER QUALQUER RUÍDO DISPONÍVEL;
    3. O LIMIAR ADAPTATIVO É APLICADO À IMAGEM BORRADA;
    4. APLICA-SE TRANSFORMAÇÕES MORFOLÓGICAS PARA DILATAÇÃO DA IMAGEM.
    5. ENCONTRAMOS OS CONTORNOS CUJA ÁREA SÃO MAIORES QUE UMA MÍNIMA ÁREA DEFINIDA.
    6. COM O CONTORNO ENCONTRADO NA ÚLTIMA ETAPA, CRIAMOS UMA MÁSCARA COM A ÁREA REPRESENTADA PELA MOLDURA;
    7. USANDO ESTA MÁSCARA, PODEMOS ENCONTRAR OS QUATRO CANTOS DO DOCUMENTO DE IDENTIFICAÇÃO NA IMAGEM ORIGINAL;

    # Arguments
        object                  - Required : Imagem para aplicação do OCR (Base64 | Path | Numpy Array)
    # Returns
        output_rg               - Required : Textos dos campos do RG após aplicação das
                                             técnicas de pré processamento,
                                             OCR e pós processamento (String)

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "16/10/2021"

from inspect import stack

import cv2
from dynaconf import settings

from UTILS.generic_functions import get_date_time_now


class Image_Pre_Processing(object):

    def __init__(self,
                 blur_ksize=settings.BLUR_KSIZE,
                 std_dev_x_direction=settings.STD_DEV_X_DIRECTION,
                 std_dev_y_direction=settings.STD_DEV_Y_DIRECTION,
                 max_color_val=settings.MAX_COLOR_VAL,
                 threshold_ksize=settings.THRESHOLD_KSIZE,
                 subtract_from_mean=settings.SUBTRACT_FROM_MEAN,
                 scale=settings.SCALE,
                 min_table_area=settings.MIN_TABLE_AREA):

        # 1 - DEFININDO A PROPRIEDADE DE BLUR
        # (DESFOQUE DA IMAGEM COM O OBJETIVO DE REMOÇÃO DE RUÍDOS DA IMAGEM)
        self.blur_ksize = blur_ksize

        # 2 - DESVIO PADRÃO DO KERNEL AO LONGO DO EIXO X (DIREÇÃO HORIZONTAL)
        self.std_dev_x_direction = std_dev_x_direction

        # 3 - DESVIO PADRÃO DO KERNEL AO LONGO DO EIXO Y (DIREÇÃO VERTICAL)
        self.std_dev_y_direction = std_dev_y_direction

        # 4 - DEFININDO A PROPRIEDADE DE THRESHOLD (LIMIAR)
        # VALOR DE PIXEL QUE SERÁ CONVERTIDO, CASO O PIXEL ULTRAPASSE O LIMIAR
        self.max_color_val = max_color_val

        # 5 - TAMANHO DO KERNEL PARA THRESHOLD
        self.threshold_ksize = threshold_ksize

        # 6 - VARIÁVEL QUE REPRESENTA A CONSTANTE UTILIZADA NOS MÉTODOS (SUBTRAÍDA DA MÉDIA OU MÉDIA PONDERADA)
        self.subtract_from_mean = subtract_from_mean

        # 7 - REALIZANDO O PARÂMETRO DA ESCALA
        self.scale = scale

        # 8 - DEFININDO O TAMANHO MIN DE ÁREA DA TABELA
        self.min_table_area = min_table_area


    def smoothing_blurring(self, img):

        """

            O DESFOQUE GAUSSIANO É SEMELHANTE AO DESFOQUE MÉDIO,
            MAS EM VEZ DE USAR UMA MÉDIA SIMPLES,
            ESTAMOS USANDO UMA MÉDIA PONDERADA,
            ONDE OS PIXELS DA VIZINHANÇA QUE ESTÃO MAIS PRÓXIMOS DO PIXEL CENTRAL
            CONTRIBUEM COM MAIS “PESO” PARA A MÉDIA.

            A SUAVIZAÇÃO GAUSSIANA É USADA PARA REMOVER O RUÍDO QUE
            SEGUE APROXIMADAMENTE UMA DISTRIBUIÇÃO GAUSSIANA.

            O RESULTADO FINAL É QUE NOSSA IMAGEM FICA MENOS DESFOCADA,
            PORÉM MAIS "DESFOCADA NATURALMENTE".. ALÉM DISSO, COM BASE NESSA PONDERAÇÃO,
            SEREMOS CAPAZES DE PRESERVAR MAIS AS BORDAS EM NOSSA
            IMAGEM EM COMPARAÇÃO COM A SUAVIZAÇÃO MÉDIA.

            # Arguments
                img                    - Required : Imagem para processamento (Array)

            # Returns
                blur                   - Required : Imagem após processamento do desfoque (Array)

        """

        # INICIANDO O VALIDADOR DA FUNÇÃO
        validator = False

        try:
            # APLICANDO A TÉCNICA DE BLUR GAUSSIANO
            blur = cv2.GaussianBlur(img, self.blur_ksize,
                                       self.std_dev_x_direction,
                                       self.std_dev_y_direction)

            print("OCR TABLES - TÉCNICA DE DESFOQUE GAUSSIANO APLICADO COM SUCESSO - {}".format(get_date_time_now("%d/%m/%Y %H:%M:%S")))

            validator = True

            return validator, blur

        except Exception as ex:
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return validator, img


    def threshold_image(self, img):

        """

            O LIMIAR ADAPTATIVO CONSIDERA UM PEQUENO CONJUNTO
            DE PIXELS VIZINHOS POR VEZ, CALCULA T PARA
            AQUELA REGIÃO LOCAL ESPECÍFICA E, EM SEGUIDA, REALIZA A SEGMENTAÇÃO.

            O SEGUNDO PARÂMETRO DA FUNÇÃO É O VALOR DO LIMITE DE SAÍDA, OU SEJA, PIXEL <= T TORNARA-SE ESSE VALOR DE PIXEL.
                EX: SE PIXEL <= T, o PIXEL TORNA-SE BRANCO (255)

            O TERCEIRO ARGUMENTO É O MÉTODO DE LIMIAR ADAPTATIVO. AQUI NÓS
            FORNECEMOS UM VALOR DE CV2.ADAPTIVE_THRESH_GAUSSIAN_C
            PARA INDICAR QUE ESTAMOS USANDO A MÉDIA GAUSSIANA DA VIZINHANÇA
            LOCAL DO PIXEL PARA CALCULAR NOSSO VALOR LIMITE DE T.

            O QUARTO VALOR É O MÉTODO DE LIMIAR, AQUI PASSAMOS UM VALOR
            DE CV2.THRESH_BINARY_INV PARA INDICAR QUE QUALQUER VALOR DE PIXEL QUE PASSE NO
            TESTE DE LIMITE TERÁ UM VALOR DE SAÍDA DE 0. CASO CONTRÁRIO, TERÁ UM VALOR DE 255.

            O QUINTO PARÂMETRO É O TAMANHO DE NOSSA VIZINHANÇA DE PIXEL,
            AQUI VOCÊ PODE VER QUE IREMOS CALCULAR O VALOR MÉDIO DA INTENSIDADE
            DO PIXEL EM TONS DE CINZA DE CADA SUB-REGIÃO 11 × 11 NA IMAGEM PARA CALCULAR NOSSO VALOR LIMITE.

            O ARGUMENTO FINAL PARA CV2.ADAPTIVETHRESHOLD É A CONSTANTE C
            QUE PERMITE SIMPLESMENTE AJUSTAR O VALOR LIMITE.

            # Arguments
                img                    - Required : Imagem para processamento (Array)

            # Returns
                thresh                 - Required : Imagem após processamento do limiar (Array)

        """

        # INICIANDO O VALIDADOR DA FUNÇÃO
        validator = False

        try:
            thresh = cv2.adaptiveThreshold(~img,
                                            self.max_color_val,
                                            cv2.ADAPTIVE_THRESH_MEAN_C,
                                            cv2.THRESH_BINARY,
                                            self.threshold_ksize,
                                            self.subtract_from_mean)

            print("OCR TABLES - TÉCNICA DE LIMIAR ADAPTATIVO APLICADO COM SUCESSO - {}".format(get_date_time_now("%d/%m/%Y %H:%M:%S")))

            validator = True

            return validator, thresh

        except Exception as ex:
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return validator, img


    def preprocess_blur_threshold_img(self, img):

        """

            REALIZA A ORQUESTRAÇÃO DE DUAS TÉCNICAS DE PRÉ PROCESSAMENTO DA IMAGEM.

            1) APLICA AS TÉCNICAS DE DESFOQUE (GAUSSIANBLUR)
            2) APLICA LIMIAR DOS PLANOS DA IMAGEM (ADAPTIVETHRESHOLD)

            # Arguments
                img                    - Required : Imagem para processamento (Array)

            # Returns
                thresh                - Required : Imagem após ambos processamentos (Array)

        """

        # INICIANDO O VALIDADOR DA FUNÇÃO
        validator = False

        print("OCR TABLES - INICIANDO O PRÉ PROCESSAMENTO DA IMAGEM - {}".format(get_date_time_now("%d/%m/%Y %H:%M:%S")))

        try:
            # REALIZANDO O DESFOQUE GAUSSIANO
            validator, blur = Image_Pre_Processing.smoothing_blurring(self, img)

            if validator:

                # APLICANDO O LIMIAR PARA MELHOR SEPARAÇÃO DE PLANO PRINCIPAL E FUNDO
                validator, thresh = Image_Pre_Processing.threshold_image(self, blur)

        except Exception as ex:
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return validator, thresh


    def preprocess_morfo_transformations(self, image):

        # INICIANDO O VALIDADOR DA FUNÇÃO
        validator = False

        print(
            "OCR TABLES - TÉCNICA DE TRANSFORMAÇÕES MORFOLÓGICAS - {}".format(get_date_time_now("%d/%m/%Y %H:%M:%S")))

        try:
            # OBTENDO O COMPRIMENTO E AMPLITUDE DA IMAGEM
            image_width, image_height = image.shape

            # REALIZANDO AS OPERAÇÕES NA ESTRUTURA HORIZONTAL DA IMAGEM
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(image_width / self.scale), 1))
            horizontally_opened = cv2.morphologyEx(image, cv2.MORPH_OPEN, horizontal_kernel)

            # REALIZANDO AS OPERAÇÕES NA ESTRUTURA VERTICAL DA IMAGEM
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(image_height / self.scale)))
            vertically_opened = cv2.morphologyEx(image, cv2.MORPH_OPEN, vertical_kernel)

            # REALIZANDO A OPERAÇÃO DE DILATAÇÃO
            horizontally_dilated = cv2.dilate(horizontally_opened, cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1)))
            vertically_dilated = cv2.dilate(vertically_opened, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 60)))

            validator = True

        except Exception as ex:
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return validator, horizontally_dilated, vertically_dilated


    def find_tables(self, image):

        # REALIZANDO O PRÉ PROCESSAMENTO DA IMAGEM COM BLURRING
        validator, preproc_img_blur_thresh = Image_Pre_Processing.preprocess_blur_threshold_img(self,
                                                                                                image)

        if validator:

            # REALIZANDO A CÓPIA DA IMAGEM
            vertical = horizontal = preproc_img_blur_thresh.copy()

            # APLICANDO TRANSFORMAÇÕES MORFOLÓGICAS
            validator, horizontally_dilated, vertically_dilated = Image_Pre_Processing.preprocess_morfo_transformations(self,
                                                                                                                        preproc_img_blur_thresh)

            if validator:

                # OBTENDO A MÁSCARA E OBTENDO OS CONTORNOS
                mask = horizontally_dilated + vertically_dilated
                contours, heirarchy = cv2.findContours(
                    mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE,
                )

                # OBTENDO OS CONTORNOS COM TAMANHO MAIOR QUE DA ÁREA MIN ESPERADA
                contours = [c for c in contours if cv2.contourArea(c) > self.min_table_area]
                perimeter_lengths = [cv2.arcLength(c, True) for c in contours]
                epsilons = [0.1 * p for p in perimeter_lengths]
                approx_polys = [cv2.approxPolyDP(c, e, True) for c, e in zip(contours, epsilons)]
                bounding_rects = [cv2.boundingRect(a) for a in approx_polys]

                # The link where a lot of this code was borrowed from recommends an
                # additional step to check the number of "joints" inside this bounding rectangle.
                # A table should have a lot of intersections. We might have a rectangular image
                # here though which would only have 4 intersections, 1 at each corner.
                # Leaving that step as a future TODO if it is ever necessary.
                images = [image[y:y+h, x:x+w] for x, y, w, h in bounding_rects]

                print("FORAM ENCONTRADAS {} TABELAS".format(len(images)))

        return images