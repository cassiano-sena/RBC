import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from rbc import salvar_novo_caso, carregar_casos_salvos, calcular_similaridade, calcular_similaridade_casos, ATRIBUTOS_CATEGORICOS, ATRIBUTOS_NUMERICOS

# Carregar dados
df = pd.read_excel('carros.xlsx')

# Criação da janela principal
root = tk.Tk()
root.title("Sistema RBC de Carros")

# Dicionário de modelos por marca
modelos_por_marca = df.groupby("manufacturer_name")["model_name"].unique().to_dict()

tk.Label(root, text="Modelo:").grid(row=1, column=0)
model_name = ttk.Combobox(root, values=["Qualquer"], width=20)
model_name.set("Qualquer")
model_name.grid(row=1, column=1, columnspan=1)

def atualizar_modelos(event=None):
    marca = manufacturer_name.get()
    if marca != "Qualquer" and marca in modelos_por_marca:
        modelos = sorted(modelos_por_marca[marca])
        model_name['values'] = ["Qualquer"] + modelos
        model_name.set("Qualquer")
    else:
        model_name['values'] = ["Qualquer"]
        model_name.set("Qualquer")

def buscar_carros():
    resultado = df.copy()

    # Filtros categóricos
    filtros = {
        'manufacturer_name': manufacturer_name.get(),
        'model_name': model_name.get(),
        'transmission': transmission.get(),
        'color': color.get(),
        'engine_fuel': engine_fuel.get(),
        'body_type': body_type.get(),
        'drivetrain': drivetrain.get(),
    }

    for coluna, valor in filtros.items():
        if valor != "Qualquer":
            resultado = resultado[resultado[coluna] == valor]

    # Filtros numéricos
    try:
        min_ano = int(year_min.get()) if year_min.get() else resultado['year_produced'].min()
        max_ano = int(year_max.get()) if year_max.get() else resultado['year_produced'].max()
        resultado = resultado[(resultado['year_produced'] >= min_ano) & (resultado['year_produced'] <= max_ano)]

        min_km = int(km_min.get()) if km_min.get() else resultado['odometer_value'].min()
        max_km = int(km_max.get()) if km_max.get() else resultado['odometer_value'].max()
        resultado = resultado[(resultado['odometer_value'] >= min_km) & (resultado['odometer_value'] <= max_km)]

        min_preco = float(preco_min.get()) if preco_min.get() else resultado['price_usd'].min()
        max_preco = float(preco_max.get()) if preco_max.get() else resultado['price_usd'].max()
        resultado = resultado[(resultado['price_usd'] >= min_preco) & (resultado['price_usd'] <= max_preco)]
    except ValueError:
        messagebox.showerror("Erro", "Valores numéricos inválidos.")
        return

    if resultado.empty:
        messagebox.showinfo("Resultado", "Nenhum carro encontrado.")
        return

    # Lê os pesos das entradas (troque nomes das entradas conforme seu código)
    pesos = {
        'price_usd': float(peso_preco_entry.get() or 0),
        'odometer_value': float(peso_km_entry.get() or 0),
        'year_produced': float(peso_ano_entry.get() or 0),
        'manufacturer_name': float(peso_marca_entry.get() or 0),
        'model_name': float(peso_modelo_entry.get() or 0),
        'transmission': float(peso_cambio_entry.get() or 0),
        'color': float(peso_cor_entry.get() or 0),
        'engine_fuel': float(peso_combustivel_entry.get() or 0),
        'body_type': float(peso_carroceria_entry.get() or 0),
        'drivetrain': float(peso_tracao_entry.get() or 0),
    }

    # Caso de consulta para similaridade (preencher com os filtros numéricos e categóricos escolhidos)
    caso_dict = {
        "manufacturer_name": filtros["manufacturer_name"],
        "model_name": filtros["model_name"],
        "transmission": filtros["transmission"],
        "color": filtros["color"],
        "engine_fuel": filtros["engine_fuel"],
        "body_type": filtros["body_type"],
        "drivetrain": filtros["drivetrain"],
        "year_produced": min_ano,
        "odometer_value": min_km,
        "price_usd": min_preco,
    }

    # Importante: calcular similaridade antes de mostrar resultados
    resultado = calcular_similaridade(caso_dict, resultado, pesos)

    # Exibir top 5 ordenado pela similaridade
    top5 = resultado.head(5)
    output = "\n".join([
        f"{row['year_produced']} {row['manufacturer_name']} {row['model_name']} ({row['odometer_value']}km) - US${row['price_usd']:.2f} "
        f"(Similaridade: {row['similaridade']:.2f})"
        for _, row in top5.iterrows()
    ])
    messagebox.showinfo("Resultados", output)

    # Armazena o resultado para exportação
    buscar_carros.resultado_filtrado = resultado

    # Salvar novo caso consultado
    salvar_novo_caso(caso_dict)

    # Sugestão com base em casos salvos (se quiser manter essa parte)
    df_casos = carregar_casos_salvos()
    if not df_casos.empty:
        similares = calcular_similaridade_casos(caso_dict, df_casos)
        if not similares.empty and len(similares) > 1:
            similares = similares.iloc[1:6]
            sugestoes = "\n".join([
                f"{row.get('year_produced', '')} {row.get('manufacturer_name', '')} {row.get('model_name', '')} - US${row.get('price_usd', '')}"
                for _, row in similares.iterrows()
            ])
            messagebox.showinfo("Casos anteriores semelhantes", f"Top 5 casos semelhantes salvos:\n\n{sugestoes}")

# Função para exportar o resultado em CSV/XLSX
def exportar_resultado():
    if hasattr(buscar_carros, 'resultado_filtrado'):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Arquivo Excel", "*.xlsx"), ("CSV", "*.csv")])
        if file_path:
            if file_path.endswith('.csv'):
                buscar_carros.resultado_filtrado.to_csv(file_path, index=False)
            else:
                buscar_carros.resultado_filtrado.to_excel(file_path, index=False)
            messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso.")
    else:
        messagebox.showwarning("Aviso", "Nenhum resultado para salvar.")


# Função para visualizar casos salvos
def visualizar_casos_salvos():
    try:
        df_casos = carregar_casos_salvos()
        if df_casos.empty:
            messagebox.showinfo("Casos Salvos", "Nenhum caso salvo até o momento.")
        else:
            texto = "\n".join([
                f"{row['year_produced']} {row['manufacturer_name']} {row['model_name']} - US${row['price_usd']}"
                for _, row in df_casos.tail(10).iterrows()
            ])
            messagebox.showinfo("Últimos 10 Casos Salvos", texto)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar casos salvos:\n{str(e)}")


# --- INTERFACE ---

def add_combo(label_text, row, column, columnspan, values):
    tk.Label(root, text=label_text).grid(row=row, column=column)
    cb = ttk.Combobox(root, values=["Qualquer"] + sorted(values), width=20)
    cb.set("Qualquer")
    cb.grid(row=row, column=column + 1, columnspan=columnspan)
    return cb

manufacturer_name = add_combo("Marca:", 0, 0, 1, df['manufacturer_name'].dropna().unique())
manufacturer_name.bind("<<ComboboxSelected>>", atualizar_modelos)

model_name = add_combo("Modelo:", 1, 0, 1, [])
transmission = add_combo("Transmissão:", 2, 0, 1, df['transmission'].dropna().unique())
color = add_combo("Cor:", 3, 0, 1, df['color'].dropna().unique())
engine_fuel = add_combo("Combustível:", 4, 0, 1, df['engine_fuel'].dropna().unique())
body_type = add_combo("Carroceria:", 5, 0, 1, df['body_type'].dropna().unique())
drivetrain = add_combo("Tração:", 6, 0, 1, df['drivetrain'].dropna().unique())

# Campos de faixa
tk.Label(root, text="Ano de:").grid(row=0, column=10)
year_min = tk.Entry(root, width=8)
year_min.grid(row=0, column=11)
tk.Label(root, text="até").grid(row=0, column=12)
year_max = tk.Entry(root, width=8)
year_max.grid(row=0, column=13)

tk.Label(root, text="Km de:").grid(row=1, column=10)
km_min = tk.Entry(root, width=8)
km_min.grid(row=1, column=11)
tk.Label(root, text="até").grid(row=1, column=12)
km_max = tk.Entry(root, width=8)
km_max.grid(row=1, column=13)

tk.Label(root, text="Preço de:").grid(row=2, column=10)
preco_min = tk.Entry(root, width=8)
preco_min.grid(row=2, column=11)
tk.Label(root, text="até").grid(row=2, column=12)
preco_max = tk.Entry(root, width=8)
preco_max.grid(row=2, column=13)


year_min.insert(0, "2010")
year_max.insert(0, "2020")
km_min.insert(0, "1000")
km_max.insert(0, "100000")
preco_min.insert(0, "10000")
preco_max.insert(0, "60000")

# Pesos
tk.Label(root, text="Peso Ano:").grid(row=3, column=10)
peso_ano_entry = tk.Entry(root, width=6)
peso_ano_entry.grid(row=3, column=11)

tk.Label(root, text="Peso Km:").grid(row=4, column=10)
peso_km_entry = tk.Entry(root, width=6)
peso_km_entry.grid(row=4, column=11)

tk.Label(root, text="Peso Preço:").grid(row=5, column=10)
peso_preco_entry = tk.Entry(root, width=6)
peso_preco_entry.grid(row=5, column=11)

tk.Label(root, text="Peso Marca:").grid(row=0, column=3)
peso_marca_entry = tk.Entry(root, width=6)
peso_marca_entry.grid(row=0, column=4)

tk.Label(root, text="Peso Modelo:").grid(row=1, column=3)
peso_modelo_entry = tk.Entry(root, width=6)
peso_modelo_entry.grid(row=1, column=4)

tk.Label(root, text="Peso Transmissão:").grid(row=2, column=3)
peso_cambio_entry = tk.Entry(root, width=6)
peso_cambio_entry.grid(row=2, column=4)

tk.Label(root, text="Peso Cor:").grid(row=3, column=3)
peso_cor_entry = tk.Entry(root, width=6)
peso_cor_entry.grid(row=3, column=4)

tk.Label(root, text="Peso Combustível:").grid(row=4, column=3)
peso_combustivel_entry = tk.Entry(root, width=6)
peso_combustivel_entry.grid(row=4, column=4)

tk.Label(root, text="Peso Carroceria:").grid(row=5, column=3)
peso_carroceria_entry = tk.Entry(root, width=6)
peso_carroceria_entry.grid(row=5, column=4)

tk.Label(root, text="Peso Tração:").grid(row=6, column=3)
peso_tracao_entry = tk.Entry(root, width=6)
peso_tracao_entry.grid(row=6, column=4)

peso_preco_entry.insert(0, "0.4")
peso_km_entry.insert(0, "0.3")
peso_ano_entry.insert(0, "0.2")
peso_marca_entry.insert(0, "0.02")
peso_modelo_entry.insert(0, "0.02")
peso_cambio_entry.insert(0, "0.01")
peso_cor_entry.insert(0, "0.01")
peso_combustivel_entry.insert(0, "0.01")
peso_carroceria_entry.insert(0, "0.01")
peso_tracao_entry.insert(0, "0.01")

# Botões
tk.Button(root, text="Buscar", command=buscar_carros).grid(row=13, column=0, columnspan=2, pady=10)
tk.Button(root, text="Exportar Resultado", command=exportar_resultado).grid(row=13, column=2, columnspan=6, pady=10)

root.mainloop()
