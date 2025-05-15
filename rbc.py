import pandas as pd
import os

CAMINHO_CASOS = "casos_salvos.xlsx"

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
