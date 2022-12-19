from os import path
import sys
from pathlib import Path

sys.path.append(path.join(str(Path(__file__).resolve().parent.parent), "app"))

import pandas as pd

from app.src.UTILS.extract_infos import (
    get_similitary
)


df = pd.read_excel(r'C:\Users\Emerson\Desktop\brainIAcs\OCR_TABLES\app\src\RESULTADOS\EX_RESULTADOS.xlsx',
                   engine='openpyxl')

dict_months = {"VL01": "JANEIRO",
               "VL02": "FEVEREIRO",
               "VL03": "MARÇO",
               "VL04": "ABRIL",
               "VL05": "MAIO",
               "VL06": "JUNHO",
               "VL07": "JULHO",
               "VL08": "AGOSTO",
               "VL09": "SETEMBRO",
               "VL10": "OUTUBRO",
               "VL11": "NOVEMBRO",
               "VL12": "DEZEMBRO"}

def generate_gab_ocr():

    # PERCORRENDO CADA UMA DAS IMAGENS
    for imagem in df["LISTA_IMAGEM"].unique():

        # FILTRANDO O DATAFRAME DA IMAGEM ATUAL
        df_actual = df[df["LISTA_IMAGEM"] == imagem]

        # VERIFICANDO A QUANTIDADE DE MATCHS BOTH
        years_both = list(df_actual[df_actual["_merge"] == "both"]["ANO_GAB"])

        # FILTRANDO OS ANOS BOTH
        df_actual_years_both = df_actual[df_actual["ANO_GAB"].isin(years_both)]

        # INICIANDO A LISTA DE RESULTADO
        list_result = []

        # PERCORRENDO CADA ANO BOTH
        for year in years_both:

            # FILTRANDO O ANO ATUAL
            df_filter_year = df_actual_years_both[df_actual_years_both["ANO_GAB"] == year]

            result_list_year = [{row[month_gab], row[month_ocr]} for month_gab, month_ocr in dict_months.items() for idx, row in
             df_filter_year.iterrows() if month_ocr in row.keys()]

            result_dict_year = {year: result_list_year}

            list_result.append(result_dict_year)

    return list_result


def calculate_metric(result_gab_ocr):

    print(result_gab_ocr)


list_result_gab_ocr = generate_gab_ocr()

calculate_metric(list_result_gab_ocr)