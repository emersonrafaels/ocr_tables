from app.app import orchestra_extract_table_ocr
from app.src.UTILS.base64_encode_decode import image_to_base64

# DEFININDO A IMAGEM A SER UTILIZADA
files = (
    r"C:\Users\Emerson\Desktop\brainIAcs\MASSA_IMAGENS\CARTAS DE FATURAMENTO\Carta5.PNG"
)

# REALIZANDO O OCR
result = orchestra_extract_table_ocr(image_to_base64(files))

print("TEXTO OBTIDO: {}".format(result["text"]))
print("VALORES OBTIDOS: {}".format(result["campos"]))
