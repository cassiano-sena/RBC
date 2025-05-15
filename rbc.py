import pandas as pd
import numpy as np
import os

CAMINHO_CASOS = "casos_salvos.xlsx"

# Atributos numéricos e categóricos usados para comparação
ATRIBUTOS_NUMERICOS = ["price_usd", "year_produced", "odometer_value"]
ATRIBUTOS_CATEGORICOS = ["manufacturer_name", "model_name", "engine_fuel", "transmission", "color"]


def carregar_casos_salvos():
    """Carrega os casos anteriores de um arquivo"""
    if os.path.exists(CAMINHO_CASOS):
        return pd.read_excel(CAMINHO_CASOS)
    else:
        return pd.DataFrame()



def salvar_novo_caso(caso_dict):
    """Salva um novo caso fornecido como dicionário"""
    df_casos = carregar_casos_salvos()
    novo_caso_df = pd.DataFrame([caso_dict])
    df_casos = pd.concat([df_casos, novo_caso_df], ignore_index=True)
    df_casos.to_excel(CAMINHO_CASOS, index=False)



def calcular_similaridade(caso_consulta, df, pesos):
    def normalizar(val1, val2):
        try:
            val1 = float(val1)
            val2 = float(val2)
            return 1 - abs(val1 - val2) / (abs(val2) + 1)
        except (ValueError, TypeError):
            return 0

    similaridades = []

    for _, row in df.iterrows():
        sim = 0

        for atributo, peso in pesos.items():
            if peso == 0 or atributo not in caso_consulta:
                continue

            valor_caso = caso_consulta[atributo]
            valor_row = row.get(atributo)

            if atributo in ATRIBUTOS_NUMERICOS:
                sim += peso * normalizar(valor_row, valor_caso)
            elif atributo in ATRIBUTOS_CATEGORICOS:
                sim += peso * (1 if str(valor_row).strip().lower() == str(valor_caso).strip().lower() else 0)

        similaridades.append(sim)

    df = df.copy()
    df["similaridade"] = similaridades
    return df.sort_values(by="similaridade", ascending=False)




def calcular_similaridade_casos(caso_atual_dict, df_casos):
    """Compara o caso atual com os casos salvos, retornando ordenado por similaridade"""

    def similaridade(caso_linha):
        score = 0
        total = 0
        for campo in ["year_produced", "odometer_value", "price_usd"]:
            try:
                val1 = float(caso_atual_dict.get(campo, 0))
                val2 = float(caso_linha.get(campo, 0))
                diff = abs(val1 - val2)
                score += 1 / (1 + diff)
                total += 1
            except:
                pass
        return score / total if total > 0 else 0

    if df_casos.empty:
        return df_casos

    df_casos = df_casos.copy()
    df_casos["similaridade"] = df_casos.apply(similaridade, axis=1)
    return df_casos.sort_values(by="similaridade", ascending=False)
