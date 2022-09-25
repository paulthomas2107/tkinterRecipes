import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random

bg_colour = "#3d6466"


def clear_widgets(frame_in):
    for widget in frame_in.winfo_children():
        widget.destroy()


def fetch_db():
    connection = sqlite3.connect("data/recipes.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table';")
    all_tables = cursor.fetchall()

    # Get random recipe
    index = random.randint(0, len(all_tables) - 1)

    # Get ingredients
    table_name = all_tables[index][1]
    cursor.execute("SELECT * FROM " + table_name + ";")
    table_records = cursor.fetchall()

    connection.close()
    return table_name, table_records


def pre_process(table_name, table_records):
    title = table_name[:-6]
    title = "".join([char if char.islower() else " " + char for char in title])

    ingredients = []

    # Ingredients
    for i in table_records:
        name = i[1]
        qty = i[2]
        unit = i[3]
        ingredients.append(qty + " " + unit + " " + name)

    return title, ingredients


def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)
    # frame1 widgets
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo.png")
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_colour)
    logo_widget.image = logo_img
    logo_widget.pack()

    # Label widget
    tk.Label(frame1,
             text="Ready for your random recipe ?",
             bg=bg_colour,
             fg="white",
             font=("TkMenuFont", 14)
             ).pack()

    # Button Widget
    tk.Button(
        frame1,
        text="SHUFFLE",
        font=("TkHeadingFont", 20),
        bg="#28393a",
        fg="black",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="white",
        command=lambda: load_frame2()
    ).pack(pady=20)


def load_frame2():
    clear_widgets(frame1)
    frame2.tkraise()
    table_name, table_records = fetch_db()
    title, ingredients = pre_process(table_name, table_records)

    # frame2 widget
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo_bottom.png")
    logo_widget = tk.Label(frame2, image=logo_img, bg=bg_colour)
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)

    # Label widget
    tk.Label(frame2,
             text=title,
             bg=bg_colour,
             fg="white",
             font=("TkHeadingFont", 20)
             ).pack(pady=25)

    for i in ingredients:
        tk.Label(frame2,
                 text=i,
                 bg="#28393a",
                 fg="white",
                 font=("TkMenuFont", 12)
                 ).pack(fill="both")

    # Button Widget
    tk.Button(
        frame2,
        text="BACK",
        font=("TkHeadingFont", 18),
        bg="#28393a",
        fg="black",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="white",
        command=lambda: load_frame1()
    ).pack(pady=20)


# initialize app
root = tk.Tk()
root.title("Recipe Picker")
root.eval("tk::PlaceWindow . center")

# Create frame widget
frame1 = tk.Frame(root, width=500, height=600, bg=bg_colour)
frame2 = tk.Frame(root, bg=bg_colour)

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nesw")

# Start app
load_frame1()
root.mainloop()
