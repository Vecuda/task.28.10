
import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

DB_CONFIG = {
    "dbname": "alkanes_task1",
    "user": "postgres",
    "password": "1111",
    "host": "localhost",
    "port": 5432,
    "connect_timeout": 5
}


def show_data():
    for item in tree.get_children():
        tree.delete(item)

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT name, formula, carbon_count,
                           hydrogen_count, molar_mass
                    FROM public.alkanes
                    ORDER BY carbon_count ASC
                """)
                rows = cur.fetchall()

        for row in rows:
            tree.insert("", tk.END, values=row)

    except psycopg2.Error as error:
        messagebox.showerror("Ошибка PostgreSQL", str(error))


def clear_table():
    for item in tree.get_children():
        tree.delete(item)


root = tk.Tk()
root.title("Каталог: Алканы")
root.geometry("850x330")

ttk.Label(
    root,
    text="Каталог: Алканы",
    font=("Arial", 16, "bold")
).pack(anchor="w", padx=15, pady=12)

buttons = ttk.Frame(root)
buttons.pack(anchor="w", padx=15, pady=5)

ttk.Button(
    buttons,
    text="Показать",
    command=show_data
).pack(side="left", padx=(0, 8))

ttk.Button(
    buttons,
    text="Очистить таблицу",
    command=clear_table
).pack(side="left")

table_frame = ttk.Frame(root)
table_frame.pack(anchor="nw", padx=15, pady=10, fill="x")

columns = (
    "name", "formula", "carbon_count",
    "hydrogen_count", "molar_mass"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=3
)

headers = (
    "Название", "Формула", "Атомов C",
    "Атомов H", "Масса, г/моль"
)

widths = (180, 130, 120, 120, 160)

for column, header, width in zip(columns, headers, widths):
    tree.heading(column, text=header)
    tree.column(column, width=width, stretch=False)

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="x")
scrollbar.pack(side="left", fill="y")

root.mainloop()
