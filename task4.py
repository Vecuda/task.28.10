import tkinter as tk
from tkinter import ttk
import psycopg2

DB_NAME = "alkynes_task4"
DB_USER = "postgres"
DB_PASS = "1111"
DB_HOST = "localhost"
DB_PORT = "5432"
COLUMNS = ['name', 'formula', 'carbon_count', 'hydrogen_count', 'molar_mass']
RU_COLS = ['Название', 'Формула', 'Атомов C', 'Атомов H', 'Масса, г/моль']

def load_data():
    for item in tree.get_children(): tree.delete(item)
    with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT name, formula, carbon_count, hydrogen_count, molar_mass FROM public.alkynes ORDER BY carbon_count ASC")
            for row in cur.fetchall(): tree.insert("", tk.END, values=tuple(row))

def clear_table():
    for item in tree.get_children(): tree.delete(item)

root = tk.Tk()
root.title("Алкины — Task 4")
root.geometry("1000x650")
tk.Label(root, text="Каталог: Алкины", font=("Arial", 20)).pack(pady=10)
btn_frame = tk.Frame(root); btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Показать", width=20, command=load_data).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Очистить таблицу", width=20, command=clear_table).pack(side=tk.LEFT, padx=5)

table_frame = tk.Frame(root)
table_frame.pack(padx=10, pady=10, anchor="n", fill="x", expand=False)
tree = ttk.Treeview(table_frame, columns=tuple(COLUMNS), show="headings", height=3)
for c, ru in zip(COLUMNS, RU_COLS):
    tree.heading(c, text=ru)
    tree.column(c, width=170, anchor="center")
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")
root.mainloop()
