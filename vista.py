from xml.etree.ElementTree import TreeBuilder
from tkinter import *
from tkinter import ttk
import calendar
from tkcalendar import Calendar
from tkcalendar import DateEntry
import re
from tkinter import messagebox
import datetime
from modelo import Abmc
from modelo import Alquiler, BaseModel, SqliteDatabase
from modelo import message2

lista_autos = ["Volkswagen", "Fiat", "Chevrolet", "Renault"]


######################################################################################
##VISTA Y CONTROLADOR
#####################################################################################
# **************************************Conexion a base de datos***********************


# *****************************************************************************************
# Inicializacion Tkinter
# *******************************************************************************************
class Mivista:
    def __init__(self, window):

        self.root = window
        self.mi_abmc = Abmc()
        self.root.title("Alquiler de Autos - Reservas")
        self.root.geometry("1200x800")

        # ************************************************************************************
        # variables tkinter
        # ***************************************************************************************

        (
            self.var_fecha_inicio,
            self.var_fecha_fin,
            self.var_vehiculo,
            self.var_nombre,
            self.var_direccion,
            self.var_telefono,
            self.var_mail,
            self.variable_autos,
        ) = (
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
        )
        # ****************************************************************
        # entrada fecha inicio y fin, tipo de auto a reservar
        # ****************************************************************

        self.fecha_inicio = DateEntry(
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="dd/mm/yy",
        )
        self.fecha_inicio.place(x=10, y=20, width=100, height=25)

        self.fecha_fin = DateEntry(
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="dd/mm/yy",
        )
        self.fecha_fin.place(x=120, y=20, width=100, height=25)

        self.variable_autos.set("Volkswagen")  # default value

        self.w = OptionMenu(
            self.root,
            self.variable_autos,
            "Volkswagen",
            "Fiat",
            "Chevrolet",
            "Renault",
            "Total",
        )
        self.w.place(x=235, y=17, height=30)

        # ****************************************************************
        # datos del cliente
        # ****************************************************************

        self.label_nombre = Label(self.root, text="Nombre:")
        self.label_nombre.place(x=10, y=500)

        self.label_telefono = Label(self.root, text="Telefono:")
        self.label_telefono.place(x=10, y=535)

        self.label_direccion = Label(self.root, text="Direccion:")
        self.label_direccion.place(x=10, y=570)

        self.label_mail = Label(self.root, text="Mail:")
        self.label_mail.place(x=10, y=605)

        self.e_nombre = Entry(self.root, textvariable=self.var_nombre)
        self.e_nombre.place(x=120, y=500, width=710, height=25)

        self.e_direccion = Entry(self.root, textvariable=self.var_direccion)
        self.e_direccion.place(x=120, y=535, width=710, height=25)

        self.e_telefono = Entry(self.root, textvariable=self.var_telefono)
        self.e_telefono.place(x=120, y=570, width=710, height=25)

        self.e_mail = Entry(self.root, textvariable=self.var_mail)
        self.e_mail.place(x=120, y=605, width=710, height=25)

        # ****************************************************************
        # calendario
        # ****************************************************************
        self.today = datetime.date.today()
        self.cal = Calendar(
            self.root,
            selectmode="day",
            year=self.today.year,
            month=self.today.month,
            day=self.today.day,
        )

        self.cal.place(x=920, y=55)

        # ****************************************************************
        # lista de reservas
        # ****************************************************************
        self.f = Frame(self.root, height=425, width=890, bg="yellow")
        self.f.place(x=10, y=55, width=890, height=425)
        treeScroll = ttk.Scrollbar(self.f)

        self.tree = ttk.Treeview(self.f, show="tree headings")
        self.tree["columns"] = ("col1", "col2", "col3", "col4")
        treeScroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=treeScroll.set)
        treeScroll.pack(side=RIGHT, fill=BOTH)
        self.tree.pack()
        self.tree.heading("#0", text="ID")

        # self.tree.heading("col1", text="ID")
        self.tree.heading("col1", text="Nombre")
        self.tree.heading("col2", text="Vehiculo")
        self.tree.heading("col3", text="Desde")
        self.tree.heading("col4", text="Hasta")

        self.tree.column("#0", width=10, minwidth=10, anchor=W)
        self.tree.column("col1", width=10, minwidth=10, anchor=W)
        self.tree.column("col2", width=20, minwidth=10, anchor=W)
        self.tree.column("col3", width=10, minwidth=10, anchor=W)
        self.tree.column("col4", width=10, minwidth=10, anchor=W)
        # self.tree.column("col5", width=80, minwidth=80, anchor=W)

        self.tree.place(x=0, y=0, width=873, height=425)
        self.mi_abmc.actualizar_treeview(self.tree)

        # ****************************************************************
        # boton reservar
        # ****************************************************************

        self.boton_reservar = Button(
            self.root,
            text="Reservar",
            command=lambda: self.mi_abmc.f_boton_reservar(
                self.tree,
                self.e_mail,
                self.cal,
                self.e_nombre,
                self.e_direccion,
                self.e_telefono,
                self.e_mail,
                self.variable_autos,
                self.fecha_inicio,
                self.fecha_fin,
            ),
        )

        self.boton_reservar.place(x=150, y=660, width=100, height=25)

        # ****************************************************************
        # Boton Baja de reserva
        # ****************************************************************

        self.boton_baja = Button(
            self.root, text="Baja", command=lambda: self.mi_abmc.borrar(self.tree)
        )
        self.boton_baja.place(x=275, y=660, width=100, height=25)

        # ****************************************************************
        # boton baja de modificar
        # ****************************************************************

        self.boton_modificar = Button(
            self.root,
            text="Modificar",
            command=lambda: self.mi_abmc.modificar(
                self.tree,
                self.e_nombre,
                self.e_direccion,
                self.e_telefono,
                self.e_mail,
                self.variable_autos,
                self.fecha_inicio,
                self.fecha_fin,
            ),
        )
        self.boton_modificar.place(x=400, y=660, width=100, height=25)

        # ****************************************************************
        # boton baja de salir
        # ****************************************************************

        self.boton_salir = Button(self.root, text="Salir")  # command=f_boton_salir)
        self.boton_salir.place(x=500, y=750, width=100, height=25)

        # ****************************************************************
        # boton disponibilidad
        # ****************************************************************

        self.boton_disponibilidad = Button(
            self.root,
            text="Disponibilidad",
            command=lambda: self.mi_abmc.f_disponibilidad(
                self.variable_autos.get(), self.cal
            ),
        )
        self.boton_disponibilidad.place(x=350, y=19, width=100, height=25)
