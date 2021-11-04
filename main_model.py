from execute_extract_table import Extract_Table

files = [r"C:\Users\Emerson\Desktop\brainIAcs\MASSA_IMAGENS\CARTAS DE FATURAMENTO\Carta1.PNG"]

results = Extract_Table().main_extract_table(files)

for image, tables in results:
    print("\n".join(tables))
