import os
import cv2

def find_tables(image):

    # DEFININDO A PROPRIEDADE DE BLUR
    # (DESFOQUE DA IMAGEM COM O OBJETIVO DE REMOÇÃO DE RUÍDOS DA IMAGEM)
    BLUR_KSIZE = (17, 17)

    # DESVIO PADRÃO DO KERNEL AO LONGO DO EIXO X (DIREÇÃO HORIZONTAL)
    STD_DEV_X_DIRECTION = 0

    # DESVIO PADRÃO DO KERNEL AO LONGO DO EIXO Y (DIREÇÃO VERTICAL)
    STD_DEV_Y_DIRECTION = 0

    # DEFININDO A PROPRIEDADE DE THRESHOLD (LIMIAR)
    # VALOR DE PIXEL QUE SERÁ CONVERTIDO, CASO O PIXEL ULTRAPASSE O LIMIAR
    MAX_COLOR_VAL = 255

    # TAMANHO DO KERNEL PARA THRESHOLD
    THRESHOLD_KSIZE = 15

    # VARIÁVEL QUE REPRESENTA A CONSTANTE UTILIZADA NOS MÉTODOS (SUBTRAÍDA DA MÉDIA OU MÉDIA PONDERADA)
    SUBTRACT_FROM_MEAN = -2

    # APLICANDO A TÉCNICA DE BLUR GAUSSIANO
    blurred = cv2.GaussianBlur(image, BLUR_KSIZE, STD_DEV_X_DIRECTION, STD_DEV_Y_DIRECTION)

    img_bin = cv2.adaptiveThreshold(
        ~blurred,
        MAX_COLOR_VAL,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        THRESHOLD_KSIZE,
        SUBTRACT_FROM_MEAN,
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


def main_extract_table(list_result_tables):

    # INICIANDO A VARIÁVEL QUE ARMAZENARÁ OS RESULTADOS (TABELAS ENCONTRADAS)
    results = []

    # PERCORRENDO CADA UMA DAS IMAGENS ENVIADAS
    for file in list_result_tables:

        # OBTENDO O DIRETÓRIO E O NOME DO ARQUIVO
        directory, filename = os.path.split(file)

        # OBTENDO O NOME DO ARQUIVO SEM EXTENSÃO
        filename_without_extension = os.path.splitext(filename)[0]

        # REALIZANDO A LEITURA DA IMAGEM
        # LEITURA EM ESCALA DE CINZA
        image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

        # OBTENDO AS TABELAS CONTIDAS NA IMAGEM
        tables = find_tables(image)
        list_result_tables = []

        # CASO ENCONTROU TABELAS
        if tables:

            # CRIANDO O DIRETÓRIO PARA SALVAR AS TABELAS ENCONTRADAS
            # NOVO_DIRETORIO = DIRETORIO/NOME_DO_ARQUIVO
            os.makedirs(os.path.join(directory, filename_without_extension), exist_ok=True)

            # PERCORRENDO TODAS AS TABELAS ENCONTRADAS
            for i, table in enumerate(tables):

                # DEFININDO O NOME DA TABELA A SER SALVA (FORMATO PNG)
                table_filename = "{}{}{}".format("table_", i, "png")

                # DEFININDO O DIRETÓRIO E NOME DE SAVE
                table_filepath = os.path.join(
                    directory, filename_without_extension, table_filename
                )

                # SALVANDO A IMAGEM
                cv2.imwrite(table_filepath, table)

                # ARMAZENANDO NA LISTA DE TABELAS SALVAS
                # PERMITINDO USO POSTERIOR NO OCR
                list_result_tables.append(table_filepath)

                # ARMAZENANDO O RESULTADO
                # ARQUIVO DE INPUT (file)
                # TABELAS OBTIDAS (list_result_tables)
                results.append((file, list_result_tables))

                print("TABELA - {} SALVA COM SUCESSO".format(len(table_filename)))

    return results
