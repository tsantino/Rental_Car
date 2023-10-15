import vista
from tkinter import Tk
import observador


class Controller:
    def __init__(self, root):
        self.root_controller = root
        self.objeto_vista = vista.Mivista(self.root_controller)
        self.el_observador = observador.ConcreteObserverA(self.objeto_vista.mi_abmc)


if __name__ == "__main__":
    root_tk = Tk()
    Controller(root_tk)
    root_tk.mainloop()
