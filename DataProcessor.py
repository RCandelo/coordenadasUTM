import tkinter as tk
from tkinter import ttk
import pandas as pd
from CoordenadasUTM import CoordenadasUTM

class DataProcessor:
    def __init__(self, master):
        self.master = master
        self.mostrando_tabla = False
        self.tree = None

    def procesar_archivo(self, file_path):
        if file_path:
            data_frame = pd.read_excel(file_path)
            if 'CoordenadasX' in data_frame.columns and 'CoordenadasY' in data_frame.columns:
                data_frame['CoordenadasX'] = data_frame['CoordenadasX'].apply(self.realizar_operacion_coordenada)
                data_frame['CoordenadasY'] = data_frame['CoordenadasY'].apply(self.realizar_operacion_coordenada)
                self.convertir_coordenadas(data_frame)
                self.mostrar_tabla(data_frame)
            else:
                print("Las columnas 'CoordenadasX' y 'CoordenadasY' no están presentes en el DataFrame.")
        else:
            print("No se ha seleccionado ningún archivo")

    def realizar_operacion_coordenada(self, valor_celda):
        if isinstance(valor_celda, (int, float)):
            valor_celda = str(valor_celda)
            # Eliminar todos los puntos de las coordenadas
            valor_celda = valor_celda.replace(".", "")
            # Agregar el nuevo punto
            if valor_celda.startswith('1'):
                resultado = valor_celda[:7] + '.' + valor_celda[7:]
            else:
                resultado = valor_celda[:6] + '.' + valor_celda[6:]
            return resultado
        else:
            return "No es un número"

    def convertir_coordenadas(self, data_frame):
        # Iterar sobre cada fila del DataFrame
        for index, row in data_frame.iterrows():
            # Obtener las coordenadas X e Y de la fila actual y convertirlas a números
            coordenada_x = float(row['CoordenadasX'])
            coordenada_y = float(row['CoordenadasY'])
            # Convertir las coordenadas a UTM
            coordenadas = CoordenadasUTM('N', coordenada_x, coordenada_y)
            m, acordEste, n = CoordenadasUTM.calcular_variables_principales('N', coordenada_x, coordenada_y, CoordenadasUTM.calcular_excentricidad_y_radio_curvatura(CoordenadasUTM.calcular_parametros_excentricidad()), CoordenadasUTM.calcular_radioPolar())
            latitud = CoordenadasUTM.calcularLatitud(m)
            longitud = CoordenadasUTM.calcularLongitud(acordEste, n)
            # Crear una nueva columna en el DataFrame con las coordenadas UTM convertidas
            data_frame.at[index, 'Latitud'] = latitud
            data_frame.at[index, 'Longitud'] = longitud


    def mostrar_tabla(self, data_frame):
        if self.tree:
            self.tree.destroy()

        columns = list(data_frame.columns)
        self.tree = ttk.Treeview(self.master, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        for index, row in data_frame.iterrows():
            self.tree.insert("", "end", values=list(row))

        self.tree.pack(expand=True, fill=tk.BOTH)
        self.mostrando_tabla = True
