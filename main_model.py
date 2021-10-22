from extract_table import main_extract_table

files = [r"C:\Users\Emerson\Desktop\brainIAcs\MASSA_IMAGENS\CARTAS DE FATURAMENTO\Carta1.PNG"]

results = main_extract_table(files)

for image, tables in results:
    print("\n".join(tables))
