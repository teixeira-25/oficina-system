import tkinter as tk
from interface_nova import InterfaceOficina


def main():
    root = tk.Tk()
    app = InterfaceOficina(root)
    root.mainloop()


if __name__ == "__main__":
    main()
