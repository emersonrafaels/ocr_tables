"""

    FUNÇÕES UTEIS PARA PRÉ PROCESSAMENTO DA IMAGEM, ANTES DA APLICAÇÃO DO OCR.

    1. A IMAGEM É LIDA EM ESCALA DE CINZA;
    2. GAUSSIAN BLUR É EXECUTADO PARA REMOVER QUALQUER RUÍDO DISPONÍVEL;
    3. O LIMIAR ADAPTATIVO É APLICADO À IMAGEM BORRADA;
    4. ENCONTRAMOS O CONTORNO CUJA ÁREA É MAIOR, POIS REPRESENTA O QUADRO DO DOCUMENTO;
    5. COM O CONTORNO ENCONTRADO NA ÚLTIMA ETAPA, CRIAMOS UMA MÁSCARA COM A ÁREA REPRESENTADA PELA MOLDURA;
    6. USANDO ESTA MÁSCARA, PODEMOS ENCONTRAR OS QUATRO CANTOS DO DOCUMENTO DE IDENTIFICAÇÃO NA IMAGEM ORIGINAL;
    7. PORTANTO, APLICAMOS DEWARPING E TRANSFORMAMOS NOSSA PERSPECTIVA,
    DE FORMA QUE OS QUATRO CANTOS DO DOCUMENTO SEJAM IGUAIS À IMAGEM.

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
import numpy as np

from UTILS.image_read import read_image_gray


class Image_Pre_Processing(object):

    def __init__(self, blur_ksize=[17, 17], std_dev_x_direction=0,
                 std_dev_y_direction=0, max_color_val=255,
                 threshold_ksize=15, subtract_from_mean=-2):

        # 1 - DEFININDO A PROPRIEDADE DE BLUR
        # (DESFOQUE DA IMAGEM COM O OBJETIVO DE REMOÇÃO DE RUÍDOS DA IMAGEM)
        self.blur_ksize = settings.BLUR_KSIZE

        # 2 - DESVIO PADRÃO DO KERNEL AO LONGO DO EIXO X (DIREÇÃO HORIZONTAL)
        self.std_dev_x_direction = settings.STD_DEV_X_DIRECTION

        # 3 - DESVIO PADRÃO DO KERNEL AO LONGO DO EIXO Y (DIREÇÃO VERTICAL)
        self.std_dev_y_direction = settings.STD_DEV_Y_DIRECTION

        # 4 - DEFININDO A PROPRIEDADE DE THRESHOLD (LIMIAR)
        # VALOR DE PIXEL QUE SERÁ CONVERTIDO, CASO O PIXEL ULTRAPASSE O LIMIAR
        self.max_color_val = settings.MAX_COLOR_VAL

        # 5 - TAMANHO DO KERNEL PARA THRESHOLD
        self.threshold_ksize = settings.THRESHOLD_KSIZE

        # 6 - VARIÁVEL QUE REPRESENTA A CONSTANTE UTILIZADA NOS MÉTODOS (SUBTRAÍDA DA MÉDIA OU MÉDIA PONDERADA)
        self.subtract_from_mean = settings.SUBTRACT_FROM_MEAN


    def find_tables(self, image):

        # APLICANDO A TÉCNICA DE BLUR GAUSSIANO
        blurred = cv2.GaussianBlur(image, self.blur_ksize,
                                   self.std_dev_x_direction,
                                   self.std_dev_y_direction)

        img_bin = cv2.adaptiveThreshold(
            ~blurred,
            self.max_color_val,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            self.threshold_ksize,
            self.subtract_from_mean,
        )
        vertical = horizontal = img_bin.copy()
        SCALE = 5
        image_width, image_height = horizontal.shape
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(image_width / SCALE), 1))
        horizontally_opened = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, horizontal_kernel)
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(image_height / SCALE)))
        vertically_opened = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, vertical_kernel)

        horizontally_dilated = cv2.dilate(horizontally_opened, cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1)))
        vertically_dilated = cv2.dilate(vertically_opened, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 60)))

        mask = horizontally_dilated + vertically_dilated
        contours, heirarchy = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE,
        )

        MIN_TABLE_AREA = 1e5
        contours = [c for c in contours if cv2.contourArea(c) > MIN_TABLE_AREA]
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