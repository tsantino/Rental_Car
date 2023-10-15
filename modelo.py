from peewee import *
import re
from datetime import timedelta, date
from datetime import datetime
from tkinter.messagebox import *
from tkinter import messagebox
import calendar
from tkcalendar import Calendar
from tkcalendar import DateEntry
import datetime
from observador import Sujeto

message1 = False
message2 = False

# ****************************************************************
# Creacion de base de datos con peewee
# ******************************************************************
db = SqliteDatabase("mi_base.db")


class BaseModel(Model):
    class Meta:
        database = db


class Alquiler(BaseModel):
    nombre = CharField()
    direccion = CharField()
    telefono = CharField()
    mail = CharField()
    vehiculo = CharField()
    inicio = CharField()
    fin = CharField()


db.connect()
db.create_tables([Alquiler])


################################################################
# MODELO-TODAS LAS FUNCIONES DEL PROGRAMA
################################################################


class Abmc(Sujeto):
    def __init__(
        self,
    ):

        pass

    # ********************************************************************
    # Decoradores
    # ********************************************************************
    def decorador_crud(function):
        def wrapper(*args, **kwargs):
            print("Se ha ejecutado la funcion %s" % function.__name__)
            fecha_hora_actual = datetime.datetime.now()
            archivo = open("logger.txt", "a")
            archivo.write(
                "%s se ha ejecutado la funcion: %s\n"
                % (fecha_hora_actual, function.__name__)
            )
            return function(*args, **kwargs)

        return wrapper

    # ********************************************************************
    # Funcion actualizar treeview
    # ********************************************************************

    def actualizar_treeview(self, mitreview):

        records = mitreview.get_children()
        for element in records:
            mitreview.delete(element)

        for fila in Alquiler().select():

            mitreview.insert(
                "",
                "end",
                text=fila.id,
                values=(
                    fila.nombre,
                    fila.vehiculo,
                    fila.inicio,
                    fila.fin,
                ),
            )

    # ****************************************************************
    # Funciones del calendario
    # ****************************************************************

    def daterange(self, date1, date2):
        for n in range(int((date2 - date1).days) + 1):
            yield date1 + timedelta(n)

    def obtengo_fechas(self, inicio, fin):
        global lista_reservaauto
        lista_reservaauto = []

        x, z, y = inicio[2], inicio[1], inicio[0]
        start_dt = date(int("20" + x), int(z), int(y))

        f, j, q = fin[2], fin[1], fin[0]
        end_dt = date(int("20" + f), int(j), int(q))

        for dt in self.daterange(start_dt, end_dt):
            lista_reservaauto.append(dt.strftime("%Y,%m,%d"))

        return lista_reservaauto, start_dt, end_dt

    # ****************************************************************
    # Funcion del Boton Disponibilidad
    # ****************************************************************

    def f_disponibilidad(self, y, cal):

        count = 0
        cal.calevent_remove("all")
        fechas_no_dispo = []

        if y != "Total":

            total = []

            for fila in Alquiler().select().where(Alquiler.vehiculo == y):

                a = fila.inicio.split("/")
                b = fila.fin.split("/")

                total, start_dt, end_dt = self.obtengo_fechas(a, b)

                fechas_no_dispo += total

                for dt in self.daterange(start_dt, end_dt):
                    a, b, c = dt.strftime("%Y,%m,%d").split(",")
                    day = datetime.date(int(a), int(b), int(c))
                    cal.calevent_create(day, y, tags="")
                    cal.tag_config("", background="red")

            return fechas_no_dispo
        else:

            lista_autos = ["Volkswagen", "Fiat", "Chevrolet", "Renault"]
            a, b, c, d = set(), set(), set(), set()
            lista = [a, b, c, d]
            for x in lista_autos:

                lista[count] = set(self.f_disponibilidad(x, cal))
                count += 1

            for x in lista:

                if len(x) != 0:

                    f = lista[0].intersection(lista[1], lista[2], lista[3])

            if len(f) != 0:

                messagebox.showinfo(
                    message="No hay ningun vehiculo disponible en las fechas mostradas en el calendario",
                    title="Advertencia",
                )

            cal.calevent_remove("all")
            for z in f:
                j, k, l = z.split(",")
                day = datetime.date(int(j), int(k), int(l))
                cal.calevent_create(day, y, tags="")
                cal.tag_config("", background="red")

    # ****************************************************************
    # Funcion del boton reservar
    # ****************************************************************
    @decorador_crud
    def f_boton_reservar(self, tree, e_mail, cal, *args):
        control1 = False

        fechas, sndreturn, trcreturn = self.obtengo_fechas(
            args[5].get().split("/"), args[6].get().split("/")
        )
        variab_auto = args[4].get()
        fechas_dispo = self.f_disponibilidad(variab_auto, cal)

        for p in fechas:
            if p in fechas_dispo:

                messagebox.showinfo(
                    message="El vehiculo seleccionado no esta disponible en esta fecha",
                    title="Advertencia",
                )
                return
            else:

                message1 = True

        # *****************************valido campo de email****************************

        patron = "^[a-z0-9]+[._-]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

        if re.match(patron, e_mail.get()):
            control1 = True
            alquiler_autos = Alquiler()

            alquiler_autos.nombre = args[0].get()
            alquiler_autos.direccion = args[1].get()
            alquiler_autos.telefono = args[2].get()
            alquiler_autos.mail = args[3].get()
            alquiler_autos.vehiculo = args[4].get()
            alquiler_autos.inicio = args[5].get()
            alquiler_autos.fin = args[6].get()
            alquiler_autos.save()

            self.actualizar_treeview(tree)

        if message1 == True & control1 == True:
            self.notificar(args[0].get(), args[4].get())
            messagebox.showinfo(
                message="Vehiculo reservado con exito",
                title="Advertencia",
            )
            control1 = False
            message1 = False

        else:

            messagebox.showinfo(
                message="Error en campo de mail, ingrese un mail correcto con el formato xx@xx.com",
                title="Advertencia",
            )

    # ************************************************************************
    # Funcion borrar datos de base de datos
    # ************************************************************************
    @decorador_crud
    def borrar(self, tree):

        item_seleccionado = tree.focus()
        valor_id = tree.item(item_seleccionado)
        borrar = Alquiler().get(Alquiler.id == valor_id["text"])
        borrar.delete_instance()
        self.actualizar_treeview(tree)

    # ****************************************************************
    # Funcion del boton Modificar
    # ****************************************************************
    @decorador_crud
    def modificar(self, tree, *args):
        item_seleccionado = tree.focus()
        valor_id = tree.item(item_seleccionado)
        actualizar = Alquiler.update(
            nombre=args[0].get(),
            direccion=args[1].get(),
            telefono=args[2].get(),
            mail=args[3].get(),
            vehiculo=args[4].get(),
            inicio=args[5].get(),
            fin=args[6].get(),
        ).where(Alquiler.id == valor_id["text"])
        actualizar.execute()

        self.actualizar_treeview(tree)
