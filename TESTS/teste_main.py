from main_model import orchestra_extract_table_ocr
from UTILS.base64_encode_decode import image_to_base64

# DEFININDO A IMAGEM A SER UTILIZADA
files = r"C:\Users\Emerson\Desktop\brainIAcs\MASSA_IMAGENS\CARTAS DE FATURAMENTO\Carta5.PNG"

# REALIZANDO O OCR
result = orchestra_extract_table_ocr(image_to_base64(files))

print(result)