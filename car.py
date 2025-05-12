import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Carregar dataset
df = pd.read_excel('carros.xlsx')
# df = pd.read_csv('carros.csv')

# Função para buscar carros semelhantes
def buscar_carros():
    fuel = fuel_type.get()
    transmission_val = transmission.get()
    owner = owner_type.get()
    
    resultado = df.copy()

    if fuel != "Qualquer":
        resultado = resultado[resultado['Fuel_Type'] == fuel]
    if transmission_val != "Qualquer":
        resultado = resultado[resultado['Transmission'] == transmission_val]
    if owner != "Qualquer":
        resultado = resultado[resultado['Owner_Type'] == owner]

    if resultado.empty:
        messagebox.showinfo("Resultado", "Nenhum carro encontrado.")
    else:
        # Mostrar top 5 resultados
        top5 = resultado.head(5)
        output = "\n".join([f"{row['Name']} - {row['Year']} - {row['Kilometers_Driven']} km" 
                            for _, row in top5.iterrows()])
        messagebox.showinfo("Resultados", output)

# Criar janela
root = tk.Tk()
root.title("Sistema RBC de Carros")

# Campos
tk.Label(root, text="Tipo de combustível:").grid(row=0, column=0)
fuel_type = ttk.Combobox(root, values=["Qualquer"] + df['Fuel_Type'].dropna().unique().tolist())
fuel_type.set("Qualquer")
fuel_type.grid(row=0, column=1)

tk.Label(root, text="Transmissão:").grid(row=1, column=0)
transmission = ttk.Combobox(root, values=["Qualquer"] + df['Transmission'].dropna().unique().tolist())
transmission.set("Qualquer")
transmission.grid(row=1, column=1)

tk.Label(root, text="Tipo de proprietário:").grid(row=2, column=0)
owner_type = ttk.Combobox(root, values=["Qualquer"] + df['Owner_Type'].dropna().unique().tolist())
owner_type.set("Qualquer")
owner_type.grid(row=2, column=1)

tk.Button(root, text="Buscar", command=buscar_carros).grid(row=3, column=0, columnspan=2)

root.mainloop()
