from MainFrame import MainFrame
from tkinterdnd2 import TkinterDnD

def main():
    root = TkinterDnD.Tk()
    root.state('zoomed')  # Maximizar la ventana
    MainFrame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
