# pylint: disable=line-too-long
"""
Escriba el código que ejecute la acción solicitada.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envíos
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`
    * `Mode_of_Shipment`
    * `Customer_rating`
    * `Weight_in_gms`
    """

    def obtener_datos():
        return pd.read_csv("files/input/shipping-data.csv")

    datos = obtener_datos()

    #almacen
    def graficar_almacen(info):
        fig, ax = plt.subplots()
        valores = info["Warehouse_block"].value_counts().sort_index()
        ax.bar(valores.index, valores.values, color="cornflowerblue", edgecolor="black")
        ax.set_title("Distribución por Almacén")
        ax.set_xlabel("Bloque")
        ax.set_ylabel("Cantidad")
        ax.spines[['top', 'right']].set_visible(False)
        fig.tight_layout()
        fig.savefig("docs/shipping_per_warehouse.png")
        plt.close(fig)

    # envio
    def graficar_modo_envio(info):
        fig, ax = plt.subplots()
        conteo = info["Mode_of_Shipment"].value_counts()
        colores = plt.get_cmap("Set2").colors[:len(conteo)]
        ax.pie(conteo, labels=conteo.index, colors=colores, startangle=0,
               autopct="%1.1f%%", wedgeprops=dict(width=0.3))
        ax.set_title("Modos de Envío")
        fig.savefig("docs/mode_of_shipment.png")
        plt.close(fig)

    # figura de rating
    def graficar_rating(info):
        agrupado = info.groupby("Mode_of_Shipment")["Customer_rating"].agg(["mean", "min", "max"])
        fig, ax = plt.subplots()
        rango = agrupado["max"] - agrupado["min"]
        colores = ["tab:green" if val >= 3 else "tab:red" for val in agrupado["mean"]]

        ax.barh(agrupado.index, rango, left=agrupado["min"], color="lightgray", height=0.7)
        ax.barh(agrupado.index, agrupado["mean"] - agrupado["min"], left=agrupado["min"], color=colores, height=0.4)
        ax.set_title("Calificación Promedio por Modo")
        ax.set_xlabel("Puntaje")
        ax.spines[['top', 'right']].set_visible(False)
        fig.tight_layout()
        fig.savefig("docs/average_customer_rating.png")
        plt.close(fig)

    # figura de peso
    def graficar_peso(info):
        fig, ax = plt.subplots()
        ax.hist(info["Weight_in_gms"], bins=20, color="darkorange", edgecolor="white")
        ax.set_title("Histograma del Peso")
        ax.set_xlabel("Peso en gramos")
        ax.set_ylabel("Frecuencia")
        ax.spines[['top', 'right']].set_visible(False)
        fig.tight_layout()
        fig.savefig("docs/weight_distribution.png")
        plt.close(fig)

    graficar_almacen(datos)
    graficar_modo_envio(datos)
    graficar_rating(datos)
    graficar_peso(datos)

    html = """<!DOCTYPE html>
<html>
  <body>
    <h1>Shipping Dashboard Example</h1>
    <div style="width:45%;float:left">
      <img src="shipping_per_warehouse.png" alt="Fig 1">
      <img src="mode_of_shipment.png"     alt="Fig 2">
    </div>
    <div style="width:45%;float:left">
      <img src="average_customer_rating.png" alt="Fig 3">
      <img src="weight_distribution.png"     alt="Fig 4">
    </div>
  </body>
</html>"""

    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    pregunta_01()
