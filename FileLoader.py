from tkinter import filedialog

class FileLoader:
    def __init__(self, callback):
        self.callback = callback

    def cargar_archivo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx;*.xls")])
        if file_path:
            self.callback(file_path)

    def drop(self, event):
        file_path = event.data
        self.callback(file_path)