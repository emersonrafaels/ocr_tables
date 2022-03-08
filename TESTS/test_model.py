from dynaconf import settings

from main_model import main_model
from execute_ocr import Execute_OCR
import execute_log

# DEFININDO A IMAGEM A SER UTILIZADA
files = [r"C:\Users\Emerson\Desktop\brainIAcs\MASSA_IMAGENS\CARTAS DE FATURAMENTO\Carta2.PNG"]

execute_log.startLog()

# ENVIANDO A IMAGEM PARA TESTE
main_model(files)