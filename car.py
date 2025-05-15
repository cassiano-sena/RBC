import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

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


# Função para buscar carros com similaridade e filtros por faixa
def buscar_carros():
    resultado = df.copy()

    # Filtros categóricos
    filtros = {
        'manufacturer_name': manufacturer_name.get(),
        'model_name': model_name.get(),
        'transmission': transmission.get(),
        'color': color.get(),
        'engine_fuel': engine_fuel.get(),
        'engine_has_gas': engine_has_gas.get(),
        'engine_type': engine_type.get(),
        'engine_capacity': engine_capacity.get(),
        'body_type': body_type.get(),
        'has_warranty': has_warranty.get(),
        'drivetrain': drivetrain.get(),
        'is_exchangeable': is_exchangeable.get(),
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

    # Similaridade com pesos
    peso_km = float(peso_km_entry.get() or 1)
    peso_ano = float(peso_ano_entry.get() or 1)
    peso_preco = float(peso_preco_entry.get() or 1)

    resultado["similaridade"] = (
        peso_km * (1 - (resultado['odometer_value'] - min_km) / (max_km - min_km + 1)) +
        peso_ano * (1 - (resultado['year_produced'] - min_ano) / (max_ano - min_ano + 1)) +
        peso_preco * (1 - (resultado['price_usd'] - min_preco) / (max_preco - min_preco + 1))
    )

    resultado.sort_values(by="similaridade", ascending=False, inplace=True)

    # Exibir top 5
    top5 = resultado.head(5)
    output = "\n".join([f"{row['year_produced']} {row['manufacturer_name']} {row['model_name']} - US${row['price_usd']}" 
                        for _, row in top5.iterrows()])
    messagebox.showinfo("Resultados", output)

    # Armazena o resultado para exportação
    buscar_carros.resultado_filtrado = resultado

# Função para salvar em CSV/XLSX
def salvar_resultado():
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

# --- INTERFACE ---

def add_combo(label_text, row, column, columnspan, values):
    tk.Label(root, text=label_text).grid(row=row, column=column)
    cb = ttk.Combobox(root, values=["Qualquer"] + sorted(values), width=20)
    cb.set("Qualquer")
    cb.grid(row=row, column=column + 1, columnspan=columnspan)
    return cb

manufacturer_name = add_combo("Marca:", 0, 0, 1, df['manufacturer_name'].dropna().unique())
manufacturer_name.bind("<<ComboboxSelected>>", atualizar_modelos)

# model_name = add_combo("Modelo:", 1, 0, 1, df['model_name'].dropna().unique())
model_name = add_combo("Modelo:", 1, 0, 1, [])

transmission = add_combo("Transmissão:", 2, 0, 1, df['transmission'].dropna().unique())
color = add_combo("Cor:", 3, 0, 1, df['color'].dropna().unique())
engine_fuel = add_combo("Combustível:", 4, 0, 1, df['engine_fuel'].dropna().unique())
engine_has_gas = add_combo("Tem gás:", 5, 0, 1, df['engine_has_gas'].dropna().unique())
engine_type = add_combo("Tipo do motor:", 6, 0, 1, df['engine_type'].dropna().unique())
engine_capacity = add_combo("Motor (L):", 7, 0, 1, df['engine_capacity'].dropna().unique())
body_type = add_combo("Carroceria:", 8, 0, 1, df['body_type'].dropna().unique())
has_warranty = add_combo("Garantia:", 9, 0, 1, df['has_warranty'].dropna().unique())
drivetrain = add_combo("Tração:", 10, 0, 1, df['drivetrain'].dropna().unique())
is_exchangeable = add_combo("Aceita troca:", 11, 0, 1, df['is_exchangeable'].dropna().unique())

# Campos de faixa
tk.Label(root, text="Ano de:").grid(row=0, column=3)
year_min = tk.Entry(root, width=8)
year_min.grid(row=0, column=4)
tk.Label(root, text="até").grid(row=0, column=5)
year_max = tk.Entry(root, width=8)
year_max.grid(row=0, column=6)

tk.Label(root, text="Km de:").grid(row=1, column=3)
km_min = tk.Entry(root, width=8)
km_min.grid(row=1, column=4)
tk.Label(root, text="até").grid(row=1, column=5)
km_max = tk.Entry(root, width=8)
km_max.grid(row=1, column=6)

tk.Label(root, text="Preço de:").grid(row=2, column=3)
preco_min = tk.Entry(root, width=8)
preco_min.grid(row=2, column=4)
tk.Label(root, text="até").grid(row=2, column=5)
preco_max = tk.Entry(root, width=8)
preco_max.grid(row=2, column=6)

# Pesos
tk.Label(root, text="Peso Km:").grid(row=4, column=3)
peso_km_entry = tk.Entry(root, width=6)
peso_km_entry.insert(0, "1")
peso_km_entry.grid(row=4, column=4)

tk.Label(root, text="Peso Ano:").grid(row=5, column=3)
peso_ano_entry = tk.Entry(root, width=6)
peso_ano_entry.insert(0, "1")
peso_ano_entry.grid(row=5, column=4)

tk.Label(root, text="Peso Preço:").grid(row=6, column=3)
peso_preco_entry = tk.Entry(root, width=6)
peso_preco_entry.insert(0, "1")
peso_preco_entry.grid(row=6, column=4)

# Botões
tk.Button(root, text="Buscar", command=buscar_carros).grid(row=13, column=0, columnspan=2, pady=10)
tk.Button(root, text="Salvar Resultado", command=salvar_resultado).grid(row=13, column=2, columnspan=2, pady=10)

root.mainloop()
