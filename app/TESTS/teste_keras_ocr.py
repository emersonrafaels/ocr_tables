import keras_ocr


def get_text(predictions):

    """

    APÓS A REALIZAÇÃO DO OCR COMPLETO (POR BOUNDING BOX),
    UTILIZANDO O KERAS_OCR
    ESSA FUNÇÃO CONCATENA O TEXTO, RESULTANDO EM UMA ÚNICA STRING.

    CONVERTE O RESULTADO DO OCR COMPLETO (IMAGE DATA)
    EM UM FORMATO LEGÍVEL:
        1) TEXT: STRING CONTENDO O TEXTO DO OCR OBTIDO
        2) PREDICTIONS: List CONTENDO AS INFORMAÇÕES DO OCR (List)

    # Arguments
        predictions                   - Required : Informações obtidas no OCR (List)
    # Returns
        text_result                   - Required : Texto resultante (String)
        predictions                   - Required : Informações obtidas no OCR (List)

    """

    x_max = 0
    temp_str = ""
    text = ""

    for value in predictions:
        x_max_local = value[1][:, 0].max()
        if x_max_local > x_max:
            x_max = x_max_local
            temp_str = temp_str + " " + value[0]
        else:
            x_max = 0
            temp_str = temp_str + "\n"
            text += temp_str
            temp_str = ""

    return text, predictions


# keras-ocr will automatically download pretrained
# weights for the detector and recognizer.
pipeline = keras_ocr.pipeline.Pipeline()

# Get a set of three example images
images = [
    r"C:\Users\Emerson\Desktop\brainIAcs\MASSA_IMAGENS\CARTAS DE FATURAMENTO\Carta5.PNG"
]

# Each list of predictions in prediction_groups is a list of
# (word, box) tuples.
prediction_groups = pipeline.recognize(images)

# looping in predictions
text = get_text(prediction_groups[0])

print(text)
