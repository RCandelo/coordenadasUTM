import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from DataProcessor  import DataProcessor
from FileLoader import FileLoader




class MainFrame:
    def __init__(self, master):
        self.master = master
        self.master.title("MANEJAR EXCEL")

        self.data_processor = DataProcessor(master)
        self.file_loader = FileLoader(self.data_processor.procesar_archivo)

        self.setup_gui()

    def setup_gui(self):
        lbl_agregar_excel = tk.Label(self.master, text="Seleccionar archivo Excel:")
        lbl_agregar_excel.pack(pady=10)

        txt_ruta_archivo = tk.Entry(self.master, width=50)
        txt_ruta_archivo.pack(pady=10)

        btn_cargar_excel = tk.Button(self.master, text="Buscar Archivo", command=self.file_loader.cargar_archivo)
        btn_cargar_excel.pack(pady=10)

        # Configurar arrastrar y soltar para el Entry
        txt_ruta_archivo.drop_target_register(DND_FILES)
        txt_ruta_archivo.dnd_bind('<<Drop>>', self.file_loader.drop)