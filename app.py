from tkinter import *
from tkinter import messagebox
import sqlite3 as sq3
import matplotlib.pyplot as plt


# ************* FUNCIONES VARIAS *************
def searching_schools(update):
    try:
        connection = sq3.connect('mi_db_c23222.db')
        cursor = connection.cursor()
        if update:
            cursor.execute("SELECT _id, localidad, provincia FROM ESCUELAS WHERE nombre = ?", (school.get(),))
            print(school.get())
        else:  # Acá configuro opción para llenar la lista de escuelas cuando abro CRUD
            cursor.execute("SELECT nombre FROM escuelas")

        result = cursor.fetchall()  # RECIBO LISTA DE TUPLAS CON UN ELEMENTO "FANTASMA" (element,)
        print(result)
        retorno = []
        for e in result:
            if update:
                locality.set(e[1])
                province.set(e[2])
                retorno.append(e)
            escuela_id = e[0]
            retorno.append(escuela_id)
        connection.close()
        return retorno
    except Exception as ex:
        print(ex)


# ***************** MENU **********************
#   BBDD
#       Connect
def connect():
    try:
        global connection
        global cursor
        connection = sq3.connect('mi_db_c23222.db')
        cursor = connection.cursor()
        messagebox.showinfo("STATUS", "Conectado correctamente")
    except Exception as ex:
        print(ex)


#   Show List
def get_list():
    try:
        class Table():
            def __init__(self, ubication):
                cols_names = ['legajo', 'Apellido', 'Nombre', 'Promedio', 'Email',
                              'Escuela', 'Localidad', 'Provincia']
                for i in range(number_cols):
                    self.e = Entry(ubication)
                    self.e.config(bg='black', fg='white')
                    self.e.grid(row=0, column=i)
                    self.e.insert(END, cols_names[i])

                for fila in range(number_rows):
                    for col in range(number_cols):
                        self.e = Entry(ubication)
                        self.e.grid(row=fila + 1, column=col)
                        self.e.insert(END, result[fila][col])
                        self.e.config(state='readonly')

        root2 = Tk()
        root2.title("Listado Alumnos")
        main_frame = Frame(root2)
        main_frame.pack(fill='both')
        close_frame = Frame(root2)
        close_frame.config(bg=text_color_button)
        close_frame.pack(fill='both')

        close_button = Button(close_frame, text="CERRAR", command=root2.destroy)
        close_button.config(bg=background_color_button, fg=text_color_button, pady=10, padx=0)
        close_button.pack(fill='both')

        # Obtengo los datos
        connection = sq3.connect('mi_db_c23222.db')
        cursor = connection.cursor()
        query = '''SELECT alumnos.legajo, alumnos.apellido, alumnos.nombre, alumnos.nota, 
        alumnos.email, escuelas.nombre, escuelas.localidad, escuelas.provincia
        FROM alumnos INNER JOIN escuelas
        ON alumnos.id_escuela = escuela._id
        LIMIT 30
        '''
        cursor.execute(query)
        result = cursor.fetchall()

        number_rows = len(result)  # la cantidad de registros para saber cuántas filas [(, , , , , , , , ),(,),(,),(,)]
        number_cols = len(result[0])  # obtengo la cantidad de columnas

        table = Table(main_frame)
        connection.close()
        root2.mainloop()
    except Exception as ex:
        print(ex)


#       Quit
def quit():
    try:
        resp = messagebox.askquestion("Confirme", "¿Realmente te querés ir de esta App?")
        if resp == "yes":
            connection.close()
            root.destroy()
    except Exception as ex:
        print(ex)


#   GRAPHICS
# Students per School
def students_per_school():
    try:
        school_query = (''' SELECT COUNT(alumnos.legajo) AS total, 
                            escuelas.nombre FROM alumnos
                            INNER JOIN escuelas
                            ON alumnos.id_escuela = escuelas._id 
                            GROUP BY escuelas.nombre 
                            ORDER BY total DESC ''')
        cursor.execute(school_query)
        result = cursor.fetchall()  # traera una lista de tuplas [(n,),(n,),(n,),(n,),(n,)]

        total_studens = []
        school_names = []

        for element in result:
            total_studens.append(element[0])
            school_names.append(element[1])

        plt.bar(x=school_names, height=total_studens)
        plt.xticks(rotation=45)
        plt.show()

    except Exception as ex:
        print(ex)


# AVG per School
def avg_per_school():
    try:
        avg_query = ('''SELECT AVG(alumnos.nota) AS promedio, escuelas.nombre
                     FROM alumnos
                     INNER JOIN escuelas
                     ON alumnos.id_escuela = escuelas._id
                     GROUP BY escuelas.nombre
                     ORDER BY promedio''')
        cursor.execute(avg_query)
        data = cursor.fetchall()

        school_names = []
        avg = []

        for element in data:
            avg.append(element[0])
            school_names.append(element[1])

        plt.barh(school_names, avg, height=0.5)

        # Iterar valores de promedio con funcion enumerate para mostrar en barras
        for index, value in enumerate(avg):
            plt.text(value, index, round(float(value), 2))

        plt.show()
    except Exception as ex:
        print(ex)


#   CLEAN
def clean():
    try:
        file_number.set("")
        surname.set("")
        name.set("")
        email.set("")
        qualifications.set(0)
        school.set("Select")
        locality.set("")
        province.set("")
        file_number_input.config(state='normal')
    except Exception as ex:
        print(ex)


#   ABOUT...
#       Licence
def show_licence():
    msg = '''
    CRUD System using Python
    Copyright (C) 2023 - xxxxx xxxx
    Email: xxxx@xxx.xx\n=======================================
    This program is free software: you can redistribute it 
    and/or modify it under the terms of the GNU General Public 
    License as published by the Free Software Foundation, 
    either version 3 of the License, or (at your option) any 
    later version.
    This program is distributed in the hope that it will be 
    useful, but WITHOUT ANY WARRANTY; without even the 
    implied warranty of MERCHANTABILITY or FITNESS FOR A 
    PARTICULAR PURPOSE.  See the GNU General Public License 
    for more details.
    You should have received a copy of the GNU General Public 
    License along with this program.  
    If not, see <https://www.gnu.org/licenses/>.'''
    messagebox.showinfo("LICENCIA", msg)


#       About us...
def show_about_us():
    messagebox.showinfo("About us", "Created by Carolina Riddick \n - Julio 2023")


# ******** CRUD MENU (CREATE-READ-UPDATE-DELETE) **************
#       CREATE
def create():
    try:
        school_id = int(searching_schools(True)[0])
        print(school_id)

        # Llamamos a las variables que controlan los campos de entrada
        data = school_id, file_number.get(), surname.get(), name.get(), qualifications.get(), email.get()
        cursor.execute("INSERT INTO ALUMNOS (id_escuela, legajo, apellido, nombre, nota, email ) VALUES (?,?,?,?,?,?)",
                       data)
        connection.commit()
        messagebox.showinfo("Status", "Registro agregado")
        clean()
    except Exception as ex:
        print(ex)


#       READ
def searching_file_number():
    try:
        query = '''SELECT a.legajo, a.apellido, a.nombre, a.email, a.nota, 
        e.nombre, e.localidad, e.provincia 
        FROM alumnos a INNER JOIN escuelas e ON a.id_escuela=e._id WHERE a.legajo='''
        cursor.execute(query + file_number.get())
        result = cursor.fetchall()  # Me trae lista de tuplas
        if result == []:
            messagebox.showerror("No encontrado", "No existe ese n° de legajo")
        else:  # [(leg1,ap1,n1,c1,e1,l1,p1)]
            for field in result:
                file_number.set(field[0])
                surname.set(field[1])
                name.set(field[2])
                email.set(field[3])
                qualifications.set(field[4])
                school.set(field[5])
                locality.set(field[6])
                province.set(field[7])
                file_number_input.config(state='disabled')
    except Exception as ex:
        print(ex)


#       UPDATE
def update():
    try:
        id_escuela = searching_schools(True)[0]
        update_info = id_escuela, surname.get(), name.get(), qualifications.get(), email.get()  # Tupla
        cursor.execute(
            "UPDATE alumnos SET id_escuela=?, apellido=?, nombre=?, nota=?, email=? WHERE legajo = " + file_number.get(),
            update_info)
        connection.commit()
        messagebox.showinfo("Status", "Registro actualizado")
        clean()
    except Exception as ex:
        print(ex)


#       DELETE
def delete():
    try:
        answer = messagebox.askquestion("Confirme", "¿Realmente querés borrar registro?")
        if answer == "yes":
            cursor.execute("DELETE FROM alumnos WHERE legajo=" + file_number.get())
            connection.commit()
            messagebox.showinfo("Status", "Registro eliminado correctamente")
            clean()
    except Exception as ex:
        print(ex)


'''*********************************
              UI 
********************************* '''

# frame buttons colors
background_framebuttons = "plum"
background_color_button = "black"
text_color_button = background_framebuttons

# frame fields color
bg_color = "cyan"
colored_font = "black"

root = Tk()  # raiz es objeto de la clase TKinter
root.title("GUI - Comisión 23222")

# --------BARRAMENU--------
barramenu = Menu(root)  # Creo un objeto de la clase que se ubica en la raiz
root.config(menu=barramenu)  # Paso argumento como kwargs

# Menú BBDD
bbddmenu = Menu(barramenu, tearoff=0)

# Connect Button
bbddmenu.add_command(label="Connect to DDBB", command=connect)
# Get Button
bbddmenu.add_command(label="List of students", command=get_list)
# Quit Button
bbddmenu.add_command(label="Quit", command=quit)

# Graphics Menu
estadmenu = Menu(barramenu, tearoff=0)
estadmenu.add_command(label="Students per school", command=students_per_school)
estadmenu.add_command(label="Qualifications", command=avg_per_school)

# Clean Menu
limpiarmenu = Menu(barramenu, tearoff=0)
limpiarmenu.add_command(label="Clean fields", command=clean)

# About us Menu
ayudamenu = Menu(barramenu, tearoff=0)
ayudamenu.add_command(label="Licence", command=show_licence)
ayudamenu.add_command(label="About ...", command=show_about_us)

barramenu.add_cascade(label="BBDD", menu=bbddmenu)
barramenu.add_cascade(label="Graphics", menu=estadmenu)
barramenu.add_cascade(label="Clean", menu=limpiarmenu)
barramenu.add_cascade(label="About...", menu=ayudamenu)

# --------FRAME FIELDS --------
frame_fields = Frame(root)
frame_fields.config(bg=bg_color)
frame_fields.pack(fill="both")

# LABEL
'''
"STICKY"
     n
  nw   ne
w         e
  sw   se
     s
'''


def config_label(my_label, number_row):
    label_spaces = {"column": 0, "sticky": "e", "padx": 10, "pady": 10}
    color_labels = {"bg": bg_color, "fg": colored_font}
    my_label.grid(row=number_row, **label_spaces)
    my_label.config(**color_labels)


file_label = Label(frame_fields, text="N° of File")
config_label(file_label, 0)

surname_label = Label(frame_fields, text="Surname")
config_label(surname_label, 1)

name_label = Label(frame_fields, text="Name")
config_label(name_label, 2)

email_label = Label(frame_fields, text="Email")
config_label(email_label, 3)

avg_label = Label(frame_fields, text="AVG")
config_label(avg_label, 4)

school_label = Label(frame_fields, text="School")
config_label(school_label, 5)

locality_label = Label(frame_fields, text="Locality")
config_label(locality_label, 6)

province_label = Label(frame_fields, text="Province")
config_label(province_label, 7)

'''
entero = IntVar()  # Declara variable de tipo entera
flotante = DoubleVar()  # Declara variable de tipo flotante
cadena = StringVar()  # Declara variable de tipo cadena
booleano = BooleanVar()  # Declara variable de tipo booleana
'''

# Create control variables of the entrie fields
file_number = StringVar()
surname = StringVar()
name = StringVar()
email = StringVar()
qualifications = DoubleVar()
school = StringVar()
locality = StringVar()
province = StringVar()


# ENTRY
def config_input(my_input, row_number):
    inputs_space = {'column': 1, 'padx': 10, 'pady': 10, 'ipadx': 50}
    my_input.grid(row=row_number, **inputs_space)


file_number_input = Entry(frame_fields, textvariable=file_number)
surname_input = Entry(frame_fields, textvariable=surname)
name_input = Entry(frame_fields, textvariable=name)
email_input = Entry(frame_fields, textvariable=email)
qualification_input = Entry(frame_fields, textvariable=qualifications)

schools = searching_schools(False)
school.set('Select')
school_options = OptionMenu(frame_fields, school, *schools)
school_options.grid(row=5, column=1, padx=10, pady=10, sticky='w', ipadx=50)

locality_input = Entry(frame_fields, textvariable=locality)
locality_input.config(state='readonly')
province_input = Entry(frame_fields, textvariable=province)
province_input.config(state='readonly')

entries = [file_number_input, surname_input, name_input, email_input, qualification_input, "school_options",
           locality_input, province_input]

for e in range(len(entries)):
    if entries[e] == "school_options":
        continue
    else:
        config_input(entries[e], e)

# --------BUTTONS FRAME -------- CRUD FUNCTIONS
buttons_frame = Frame(root)
buttons_frame.config(bg=background_framebuttons)
buttons_frame.pack(fill='both')


def config_buttons(my_button, columna):
    button_spaces = {'row': 0, 'padx': 5, 'pady': 10, 'ipadx': 12}
    my_button.config(bg=background_color_button, fg=text_color_button)
    my_button.grid(column=columna, **button_spaces)


create_button = Button(buttons_frame, text='Crete', command=create)
config_buttons(create_button, 0)

search_button = Button(buttons_frame, text='Search', command=searching_file_number)
config_buttons(search_button, 1)

update_button = Button(buttons_frame, text='Update', command=update)
config_buttons(update_button, 2)

delete_button = Button(buttons_frame, text='Delete', command=delete)
config_buttons(delete_button, 3)

# --------FRAMECOPY--------
framecopy = Frame(root)
framecopy.config(bg='black')
framecopy.pack(fill='both')

copylabel = Label(framecopy, text="(2023) by Carolina Riddick")
copylabel.config(bg='black', fg='white')
copylabel.grid(row=0, column=0, padx=10, pady=10)

root.mainloop()