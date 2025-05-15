import pandas as pd
import numpy as np
import os

CAMINHO_CASOS = "casos_salvos.xlsx"

# Atributos numéricos e categóricos usados para comparação
ATRIBUTOS_NUMERICOS = ["odometer_value", "year_produced", "engine_capacity", "price_usd"]
ATRIBUTOS_CATEGORICOS = ["manufacturer_name", "model_name", "transmission", "color", "engine_fuel", "body_type", "drivetrain"]


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
    # Calcular min/max por atributo numérico
    min_max = {
        attr: (df[attr].min(), df[attr].max())
        for attr in ATRIBUTOS_NUMERICOS if attr in df
    }

    def normalizar(val1, val2, min_val, max_val):
        try:
            val1 = float(val1)
            val2 = float(val2)
            if max_val == min_val:
                return 1.0
            return 1 - abs(val1 - val2) / (max_val - min_val)
        except (ValueError, TypeError):
            return 0

    similaridades = []

    for _, row in df.iterrows():
        sim = 0
        total_peso = 0

        for atributo, peso in pesos.items():
            if peso == 0 or atributo not in caso_consulta:
                continue

            valor_caso = caso_consulta[atributo]
            valor_row = row.get(atributo)

            if atributo in ATRIBUTOS_NUMERICOS and atributo in min_max:
                min_val, max_val = min_max[atributo]
                sim += peso * normalizar(valor_row, valor_caso, min_val, max_val)
                total_peso += peso
            elif atributo in ATRIBUTOS_CATEGORICOS:
                sim += peso * (1 if str(valor_row).strip().lower() == str(valor_caso).strip().lower() else 0)
                total_peso += peso

        similaridades.append(sim / total_peso if total_peso > 0 else 0)

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
