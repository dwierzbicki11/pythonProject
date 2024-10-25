import os.path
import tempfile
import tkinter as tk
from tkinter import font
from tkinter.font import families
from tkinter.ttk import *

import mysql.connector
from PIL import ImageFont, Image, ImageDraw
from fontTools.afmLib import preferredAttributeOrder

# Połączenie z bazą danych
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gastro"
)



root = tk.Tk()
root.geometry("500x500")
sql = db.cursor()

def ala():
    pass

ilosc=0


def addToKoszyk(nazwa, cena):
    sql.execute("INSERT INTO zamowienie (nazwa, cena) VALUES (%s, %s)", (nazwa, cena))

def Koszyk():
    sql.execute("SELECT * FROM zamowienie")
    

def main():


    def order_food(dish_name,price):
        global ilosc, koszyk
        order_win = tk.Toplevel(root)
        order_win.geometry("500x500")
        order_win.title("Zamawianie")


        frame = tk.Frame(order_win)
        frame.pack()

        label = tk.Label(frame, text="Nazwa potrawy: ",font=("Comic Sans MS",15))
        label.pack(side=tk.LEFT)

        nazwa = tk.Label(frame, text=f'{dish_name}: {price}', font=("Comic Sans MS",15))
        nazwa.pack(side=tk.LEFT)

        frame2= tk.Frame(order_win)
        frame2.pack(anchor='w')

        ilosc_label = tk.Label(frame2, text=f"{ilosc}")
        minus = tk.Button(frame2, text="-", command=lambda: iloscPotrawy('-'))
        plus = tk.Button(frame2, text="+", command=lambda: iloscPotrawy('+'))

        frame3 = tk.Frame(order_win)
        submit = tk.Button(frame3, text="Zamów", command=lambda: addToKoszyk(dish_name,price)).pack(side=tk.LEFT)
        frame3.pack(anchor='w')

        order_win.destroy()

        def iloscPotrawy(znak):
            global ilosc
            if znak == '-':
                ilosc -= 1
            elif znak == '+':
                ilosc += 1
            if ilosc < 0:
                minus.config(state="disabled")
                ilosc=0
            else:
                minus.config(state="normal")

            ilosc_label.config(text=f"{ilosc}")

        label2 = tk.Label(frame2, text="Ilość: ",font=("Comic Sans MS",15))
        label2.pack(side=tk.LEFT)
        minus.pack(side=tk.LEFT)
        ilosc_label.pack(side=tk.LEFT)
        plus.pack(side=tk.LEFT)

        frame3 = tk.Frame(order_win)
        frame3.pack(anchor='w')




    header = Frame(root,
                   width=500,
                   height=100).pack(anchor="n")
    headerLabel = Label(header,
                   text="Zamów jedzenie",
                   background="#0000ff",
                   foreground="#ffffff",
                   width="300",
                  anchor="center",
                   font=("Comic Sans MS", 20))
    headerLabel.pack(side = tk.TOP)
    koszyk = Button(header, text="Koszyk", command=Koszyk()).pack(side=tk.LEFT)

    # Utworzenie Canvas i Scrollbar
    canvas = tk.Canvas(root)
    scroll_y = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    # Ustawienia Scrollable Frame
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Dodanie Canvas do Frame
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Ustawienia Scrollbar
    canvas.configure(yscrollcommand=scroll_y.set)

    # Umieszczanie Canvas i Scrollbar w głównym oknie
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)


    sql.execute("SELECT * FROM dania")

    # Dodawanie wierszy do Scrollable Frame
    for row in sql.fetchall():
        dish_name = row[1]
        price = f'{row[2]} zł'

        # Utworzenie ramki dla dania i przycisku
        item_frame = Frame(scrollable_frame)
        item_frame.pack(fill=tk.X, padx=5, pady=5)

        # Dodanie Label z nazwą dania i ceną
        label = Label(item_frame, text=f"{dish_name} {price}", anchor='w', width=30,font=(font_name, 15))
        label.pack(side=tk.LEFT)

        # Dodanie przycisku "Zamów"
        order_button = Button(item_frame, text="Zamów", command=lambda name=dish_name, pr=price: order_food(name,pr))
        order_button.pack(side=tk.RIGHT)

    root.mainloop()

if db.is_connected():
    print("Connected to MySQL database")
    main()
else:
    print("Failed to connect to MySQL")