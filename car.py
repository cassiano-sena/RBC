import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Carregar dataset
df = pd.read_excel('carros.xlsx')
# df = pd.read_csv('carros.csv')

# Função para buscar carros semelhantes
def buscar_carros():
    manufacturer_name_val = manufacturer_name.get()
    model_name_val = model_name.get()
    transmission_val = transmission.get()
    color_val = color.get()
    odometer_value_val = odometer_value.get()
    year_produced_val = year_produced.get()
    engine_fuel_val = engine_fuel.get()
    engine_has_gas_val = engine_has_gas.get()
    engine_type_val = engine_type.get()
    engine_capacity_val = engine_capacity.get()
    body_type_val = body_type.get()
    has_warranty_val = has_warranty.get()
    drivetrain_val = drivetrain.get()
    price_usd_val = price_usd.get()
    is_exchangeable_val = manufacturer_name.get()
    
    resultado = df.copy()
    if manufacturer_name_val != "Qualquer":
        resultado = resultado[resultado['manufacturer_name'] == manufacturer_name_val]
    if model_name_val != "Qualquer":
        resultado = resultado[resultado['model_name'] == model_name_val]
    if transmission_val != "Qualquer":
        resultado = resultado[resultado['transmission'] == transmission_val]
    if color_val != "Qualquer":
        resultado = resultado[resultado['color'] == color_val]
    if odometer_value_val != "Qualquer":
        resultado = resultado[resultado['odometer_value'] == odometer_value_val]
    if year_produced_val != "Qualquer":
        resultado = resultado[resultado['year_produced'] == year_produced_val]
    if engine_fuel_val != "Qualquer":
        resultado = resultado[resultado['engine_fuel'] == engine_fuel_val]
    if engine_has_gas_val != "Qualquer":
        resultado = resultado[resultado['engine_has_gas'] == engine_has_gas_val]
    if engine_type_val != "Qualquer":
        resultado = resultado[resultado['engine_type'] == engine_type_val]
    if engine_capacity_val != "Qualquer":
        resultado = resultado[resultado['engine_capacity'] == engine_capacity_val]
    if body_type_val != "Qualquer":
        resultado = resultado[resultado['body_type'] == body_type_val]
    if has_warranty_val != "Qualquer":
        resultado = resultado[resultado['has_warranty'] == has_warranty_val]
    if drivetrain_val != "Qualquer":
        resultado = resultado[resultado['drivetrain'] == drivetrain_val]
    if price_usd_val != "Qualquer":
            resultado = resultado[resultado['price_usd'] == price_usd_val]
    if is_exchangeable_val != "Qualquer":
        resultado = resultado[resultado['is_exchangeable'] == is_exchangeable_val]

    if resultado.empty:
        messagebox.showinfo("Resultado", "Nenhum carro encontrado.")
    else:
        # Mostrar top 5 resultados
        top5 = resultado.head(5)
        output = "\n".join([f"{row['year_produced']} {row['manufacturer_name']} {row['model_name']} - {row['odometer_value']} km" 
                            for _, row in top5.iterrows()])
        messagebox.showinfo("Resultados", output)

# Criar janela
root = tk.Tk()
root.title("Sistema RBC de Carros")

# Campos
tk.Label(root, text="Marca:").grid(row=0, column=0)
manufacturer_name = ttk.Combobox(root, values=["Qualquer"] + df['manufacturer_name'].dropna().unique().tolist())
manufacturer_name.set("Qualquer")
manufacturer_name.grid(row=0, column=1)

tk.Label(root, text="Modelo:").grid(row=1, column=0)
model_name = ttk.Combobox(root, values=["Qualquer"] + df['model_name'].dropna().unique().tolist())
model_name.set("Qualquer")
model_name.grid(row=1, column=1)

tk.Label(root, text="Transmissão:").grid(row=2, column=0)
transmission = ttk.Combobox(root, values=["Qualquer"] + df['transmission'].dropna().unique().tolist())
transmission.set("Qualquer")
transmission.grid(row=2, column=1)

tk.Label(root, text="Cor:").grid(row=3, column=0)
color = ttk.Combobox(root, values=["Qualquer"] + df['color'].dropna().unique().tolist())
color.set("Qualquer")
color.grid(row=3, column=1)

tk.Label(root, text="Km:").grid(row=4, column=0)
odometer_value = ttk.Combobox(root, values=["Qualquer"] + df['odometer_value'].dropna().unique().tolist())
odometer_value.set("Qualquer")
odometer_value.grid(row=4, column=1)

tk.Label(root, text="Ano:").grid(row=5, column=0)
year_produced = ttk.Combobox(root, values=["Qualquer"] + df['year_produced'].dropna().unique().tolist())
year_produced.set("Qualquer")
year_produced.grid(row=5, column=1)

tk.Label(root, text="Tipo de combustível:").grid(row=6, column=0)
engine_fuel = ttk.Combobox(root, values=["Qualquer"] + df['engine_fuel'].dropna().unique().tolist())
engine_fuel.set("Qualquer")
engine_fuel.grid(row=6, column=1)

tk.Label(root, text="Possui combustível:").grid(row=7, column=0)
engine_has_gas = ttk.Combobox(root, values=["Qualquer"] + df['engine_has_gas'].dropna().unique().tolist())
engine_has_gas.set("Qualquer")
engine_has_gas.grid(row=7, column=1)

tk.Label(root, text="Tipo do Motor:").grid(row=8, column=0)
engine_type = ttk.Combobox(root, values=["Qualquer"] + df['engine_type'].dropna().unique().tolist())
engine_type.set("Qualquer")
engine_type.grid(row=8, column=1)

tk.Label(root, text="Litragem:").grid(row=9, column=0)
engine_capacity = ttk.Combobox(root, values=["Qualquer"] + df['engine_capacity'].dropna().unique().tolist())
engine_capacity.set("Qualquer")
engine_capacity.grid(row=9, column=1)

tk.Label(root, text="Carroceria:").grid(row=10, column=0)
body_type = ttk.Combobox(root, values=["Qualquer"] + df['body_type'].dropna().unique().tolist())
body_type.set("Qualquer")
body_type.grid(row=10, column=1)

tk.Label(root, text="Segurado:").grid(row=11, column=0)
has_warranty = ttk.Combobox(root, values=["Qualquer"] + df['has_warranty'].dropna().unique().tolist())
has_warranty.set("Qualquer")
has_warranty.grid(row=11, column=1)

tk.Label(root, text="Tração:").grid(row=12, column=0)
drivetrain = ttk.Combobox(root, values=["Qualquer"] + df['drivetrain'].dropna().unique().tolist())
drivetrain.set("Qualquer")
drivetrain.grid(row=12, column=1)

tk.Label(root, text="Preço:").grid(row=13, column=0)
price_usd = ttk.Combobox(root, values=["Qualquer"] + df['price_usd'].dropna().unique().tolist())
price_usd.set("Qualquer")
price_usd.grid(row=13, column=1)

tk.Label(root, text="Aceita troca:").grid(row=14, column=0)
is_exchangeable = ttk.Combobox(root, values=["Qualquer"] + df['is_exchangeable'].dropna().unique().tolist())
is_exchangeable.set("Qualquer")
is_exchangeable.grid(row=14, column=1)

tk.Button(root, text="Buscar", command=buscar_carros).grid(row=16, column=0, columnspan=2)

root.mainloop()
