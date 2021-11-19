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
from UTILS.image_view import image_view_functions


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

        # INICIANDO A VARIÁVEL DE RETORNO
        blur = None

        try:
            # APLICANDO A TÉCNICA DE BLUR GAUSSIANO
            blur = cv2.GaussianBlur(img, self.blur_ksize,
                                       self.std_dev_x_direction,
                                       self.std_dev_y_direction)

            print("OCR TABLES - TÉCNICA DE DESFOQUE GAUSSIANO APLICADO COM SUCESSO - {}".format(get_date_time_now("%d/%m/%Y %H:%M:%S")))

            validator = True

        except Exception as ex:
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return validator, blur


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

        # INICIANDO A VARIÁVEL DE RETORNO
        thresh = None

        try:
            thresh = cv2.adaptiveThreshold(~img,
                                            self.max_color_val,
                                            cv2.ADAPTIVE_THRESH_MEAN_C,
                                            cv2.THRESH_BINARY,
                                            self.threshold_ksize,
                                            self.subtract_from_mean)

            print("OCR TABLES - TÉCNICA DE LIMIAR ADAPTATIVO APLICADO COM SUCESSO - {}".format(get_date_time_now("%d/%m/%Y %H:%M:%S")))

            validator = True

        except Exception as ex:
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return validator, thresh


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

        # INICIANDO A VARIÁVEL DE RETORNO
        thresh = None

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

        # INICIANDO A VARIÁVEL DE RETORNO
        horizontally_dilated = vertically_dilated = None

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


    def __get_max_contour(self, img):

        """

            REALIZA A OBTENÇÃO DO CONTORNO DE MAIOR ÁREA DA FIGURA.

            O OBJETIVO É ENCONTRAR O MÁXIMO CONTORNO, PARA OBTER APENAS O DOCUMENTO DE IDENTIIFAÇÃO,
            RETIRANDO POSSÍVEIS OUTROS OBJETOS OU
            CASOS NO QUAL O DOCUMENTO POSSA ESTAR SCANEADO EM UMA FOLHA SULFITE.

            1) OBTÉM TODOS OS CONTORNOS
            2) OBTÉM O CONTORNO DE MÁXIMA ÁREA.

            # Arguments
                img                - Required : Imagem para processamento (Array)

            # Returns
                roi                - Required : Área de interesse (Array)

        """

        # INICIANDO A VARIAVEL QUE ARMAZENARÁ O VALOR DE MÁXIMA ÁREA DE CONTORNO
        roi = max_area = 0

        # INICIANDO O VALIDADOR DA FUNÇÃO
        validator = False

        print("OCR RG - BUSCANDO O DOCUMENTO NA IMAGEM - {}".format(get_date_time_now("%d/%m/%Y %H:%M:%S")))

        try:
            # OBTENDO TODOS OS CONTORNOS
            contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            # PERCORRENDO TODOS OS CONTORNOS
            for contour in contours:

                # OBTENDO O TAMANHO DA ÁREA DO CONTORNO
                area = cv2.contourArea(contour)

                # VERIFICANDO SE O VALOR É MAIOR DO QUE ATUALMENTE É A MÁXIMA ÁREA
                if area > max_area:

                    # CASO VALOR ATUAL SEJA MAIOR QUE A MÁXIMA ÁREA, O VALOR DA MÁXIMA ÁREA É ATUALIZADO
                    max_area = area

                    # ROI ARMAZENA O CONTORNO
                    roi = contour

            validator = True

        except Exception as ex:
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return validator, roi


    def __crop_image_countour(self, img, contour):

        """

            REALIZA O CROP DA IMAGEM ORIGINAL COM BASE NO CONTORNO DE MÁXIMA ÁREA ENCONTRADO.

            # Arguments
                img                 - Required : Imagem para processamento (Array)
                contour             - Required : Valor do contorno da imagem (Array)

            # Returns
                mask                - Required : Imagem com a máscara de contornos (Array)

        """

        # INICIANDO O VALIDADOR DA FUNÇÃO
        validator = False

        # INICIANDO AS VARIÁVEIS QUE ARMAZENARÃO A LISTA DE CONTORNOS NA HORIZONTAL E VERTICAL
        x, y = [], []

        print("OCR RG - CROPPANDO O DOCUMENTO NA IMAGEM - {}".format(get_date_time_now("%d/%m/%Y %H:%M:%S")))

        try:
            for contour_line in contour:
                x.append(contour_line[0][0])
                y.append(contour_line[0][1])

            # OBTENDO OS VALORES MIN E MÁXIMO DE CADA EIXO
            x1, x2, y1, y2 = min(x), max(x), min(y), max(y)

            # APLICANDO O CROP NA IMAGEM
            image_cropped_contour = img[y1:y2, x1:x2]

            validator = True

            print("OCR RG - CROP REALIZADO COM SUCESSO - {}".format(get_date_time_now("%d/%m/%Y %H:%M:%S")))

            return validator, image_cropped_contour

        except Exception as ex:
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return validator, img


    def get_contours(self, img_horizontal, img_vertical):

        """

            REALIZA A OBTENÇÃO DOS CONTORNO DE ÁREA MAIOR QUE A ÁREA MIN DEFINIDA.

            O OBJETIVO É ENCONTRAR OS CONTORNOS, PARA OBTER APENAS TABELAS.

            1) OBTÉM TODOS OS CONTORNOS
            2) APLICA LIMIAR DOS PLANOS DA IMAGEM (ADAPTIVETHRESHOLD)

            # Arguments
                img                    - Required : Imagem para processamento (Array)

            # Returns
                thresh                - Required : Imagem após ambos processamentos (Array)

        """

        # INICIANDO O VALIDADOR DA FUNÇÃO
        validator = False

        # INICIANDO A VARIÁVEL DE RETORNO
        bounding_rects = None

        print(
            "OCR TABLES - OBTENDO AS TABELAS - {}".format(get_date_time_now("%d/%m/%Y %H:%M:%S")))

        try:
            # OBTENDO A MÁSCARA
            mask = img_horizontal + img_vertical

            # OBTENDO OS CONTORNOS
            contours, heirarchy = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE,
            )

            # OBTENDO OS CONTORNOS COM TAMANHO MAIOR QUE DA ÁREA MIN ESPERADA
            contours = [c for c in contours if cv2.contourArea(c) > self.min_table_area]
            perimeter_lengths = [cv2.arcLength(c, True) for c in contours]
            epsilons = [0.1 * p for p in perimeter_lengths]
            approx_polys = [cv2.approxPolyDP(c, e, True) for c, e in zip(contours, epsilons)]
            bounding_rects = [cv2.boundingRect(a) for a in approx_polys]

            validator = True

        except Exception as ex:
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return validator, bounding_rects


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

                validator, contour = Image_Pre_Processing.__get_max_contour(self,
                                                                            preproc_img_blur_thresh)

                if validator:

                    # COM O CONTORNO ENCONTRADO A ÚLTIMA ETAPA, REALIZAMOS O CROP DA IMAGEM
                    validator, image_cropped_contour = self.__crop_image_countour(image, contour)

                    print("FORAM ENCONTRADAS {} TABELAS".format(len(image_cropped_contour)))

                    return image_cropped_contour

        return image