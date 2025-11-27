#!/usr/bin/env python3
# main.py
# Programa Tkinter para convertir teletrabajo a "días" de jornada
# Autor: Turidevelop
# Fecha: 2025
import sys, os
import tkinter as tk
from tkinter import ttk, messagebox

def safe_int(value):
    """Convierte a int ignorando espacios; si está vacío devuelve 0; lanza ValueError si no es entero o es negativo."""
    s = value.strip()
    if s == "":
        return 0
    try:
        n = int(s)
    except ValueError:
        raise ValueError("Entrada no es un número entero.")
    if n < 0:
        raise ValueError("Los valores no pueden ser negativos.")
    return n

def calcular():
    try:
        th = safe_int(entry_th.get())   # tele horas
        tm = safe_int(entry_tm.get())   # tele minutos
        jh = safe_int(entry_jh.get())   # jornada horas
        jm = safe_int(entry_jm.get())   # jornada minutos

        # Validaciones simples
        if tm >= 60 or jm >= 60:
            raise ValueError("Los minutos deben estar entre 0 y 59.")
        
        tele_min = th * 60 + tm
        jornada_min = jh * 60 + jm

        if jornada_min == 0:
            raise ValueError("La jornada laboral no puede ser 0 minutos (introduce horas y/o minutos).")

        dias = tele_min / jornada_min  # valor decimal
        dias_4dec = round(dias, 4)

        # Convertir la parte fraccionaria a horas y minutos según la jornada
        dias_ent = int(dias)  # días completos
        rem_minutes = (dias - dias_ent) * jornada_min
        rem_minutes_rounded = int(round(rem_minutes))  # en minutos

        # Normalizar (por si redondeo pasa 60)
        rem_h = rem_minutes_rounded // 60
        rem_m = rem_minutes_rounded % 60

        # Mostrar resultados
        result_decimal_var.set(f"{dias_4dec} días")
        result_breakdown_var.set(f"{dias_ent} días, {rem_h} h, {rem_m} min "
                                  f"(equivalente a {tele_min} min / {jornada_min} min)")

    except ValueError as e:
        messagebox.showerror("Error en entrada", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

def limpiar():
    entry_th.delete(0, tk.END)
    entry_tm.delete(0, tk.END)
    entry_jh.delete(0, tk.END)
    entry_jm.delete(0, tk.END)
    result_decimal_var.set("")
    result_breakdown_var.set("")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Interfaz gráfica ---
root = tk.Tk()
root.title("Convertir teletrabajo a días de jornada")
root.iconphoto(True, tk.PhotoImage(file=resource_path("turidevicon.png")))  # Asegúrate de tener un icono.ico en el mismo directorio
root.resizable(False, False)
padx = 8
pady = 6

frm = ttk.Frame(root, padding=12)
frm.grid(column=0, row=0, sticky="NSEW")

# Teletrabajo
tt_label = ttk.Label(frm, text="Teletrabajo (horas y minutos):", font=("Segoe UI", 10, "bold"))
tt_label.grid(column=0, row=0, columnspan=4, sticky="w", pady=(0,4))

tt_h_label = ttk.Label(frm, text="Horas:")
tt_h_label.grid(column=0, row=1, sticky="e", padx=(0,4))
entry_th = ttk.Entry(frm, width=6)
entry_th.grid(column=1, row=1, sticky="w")

tt_m_label = ttk.Label(frm, text="Minutos:")
tt_m_label.grid(column=2, row=1, sticky="e", padx=(12,4))
entry_tm = ttk.Entry(frm, width=6)
entry_tm.grid(column=3, row=1, sticky="w")

# Jornada laboral
j_label = ttk.Label(frm, text="Jornada laboral (horas y minutos):", font=("Segoe UI", 10, "bold"))
j_label.grid(column=0, row=2, columnspan=4, sticky="w", pady=(12,4))

j_h_label = ttk.Label(frm, text="Horas:")
j_h_label.grid(column=0, row=3, sticky="e", padx=(0,4))
entry_jh = ttk.Entry(frm, width=6)
entry_jh.grid(column=1, row=3, sticky="w")

j_m_label = ttk.Label(frm, text="Minutos:")
j_m_label.grid(column=2, row=3, sticky="e", padx=(12,4))
entry_jm = ttk.Entry(frm, width=6)
entry_jm.grid(column=3, row=3, sticky="w")

# Botones
btn_calcular = ttk.Button(frm, text="Calcular", command=calcular)
btn_calcular.grid(column=0, row=4, columnspan=2, sticky="ew", pady=(12,0), padx=(0,6))
btn_limpiar = ttk.Button(frm, text="Limpiar", command=limpiar)
btn_limpiar.grid(column=2, row=4, columnspan=2, sticky="ew", pady=(12,0), padx=(6,0))

# Resultados
result_decimal_var = tk.StringVar()
result_breakdown_var = tk.StringVar()

res_label = ttk.Label(frm, text="Resultado:", font=("Segoe UI", 10, "bold"))
res_label.grid(column=0, row=5, columnspan=4, sticky="w", pady=(12,4))

res_decimal = ttk.Label(frm, textvariable=result_decimal_var, font=("Segoe UI", 10))
res_decimal.grid(column=0, row=6, columnspan=4, sticky="w")

res_break = ttk.Label(frm, textvariable=result_breakdown_var, wraplength=420)
res_break.grid(column=0, row=7, columnspan=4, sticky="w", pady=(6,0))

# Atajos: enter para calcular
root.bind("<Return>", lambda event: calcular())

# Coloca algunos valores por defecto (opcional)
entry_jh.insert(0, "7")
entry_jm.insert(0, "45")

root.mainloop()
