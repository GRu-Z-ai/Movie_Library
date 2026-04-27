import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime

# Валюты
valuty = [
    "USD", "EUR", "GBP", "JPY", "CNY", "RUB", "CAD", "AUD", "CHF", "TRY", "INR", "BRL"
]

# История
try:
    with open("history.json", "r") as f:
        istoria = json.load(f)
except:
    istoria = []

def poluchit_kurs(ot, v):
    """Получает курс из API"""
    try:
        url = f"https://api.frankfurter.app/latest?from={ot}&to={v}"
        otvet = requests.get(url)
        dannye = otvet.json()
        return dannye["rates"][v]
    except:
        return None

def konvertirovat():
    summ = pole_summy.get().strip()
    
    if not summ:
        messagebox.showerror("Ошибка", "Введите сумму!")
        return
    
    try:
        summa = float(summ)
        if summa <= 0:
            messagebox.showerror("Ошибка", "Сумма > 0!")
            return
    except:
        messagebox.showerror("Ошибка", "Введите число!")
        return
    
    ot = iz_valuty.get()
    v = v_valuty.get()
    
    kurs = poluchit_kurs(ot, v)
    if kurs is None:
        messagebox.showerror("Ошибка", "Нет интернета или ошибка API")
        return
    
    resultat = summa * kurs
    
    metka_result.config(text=f"{summa:.2f} {ot} = {resultat:.2f} {v}")
    
    # Сохраняем
    istoria.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "from": ot,
        "to": v,
        "amount": summa,
        "result": resultat
    })
    
    with open("history.json", "w") as f:
        json.dump(istoria, f, indent=4)
    
    obnovit_istoriyu()

def obnovit_istoriyu(filt=None):
    spisok_ist.delete(0, tk.END)
    
    pokazat = istoria if filt is None else filt
    
    if not pokazat:
        spisok_ist.insert(tk.END, "История пуста")
        return
    
    for i, h in enumerate(pokazat[-8:], 1):
        spisok_ist.insert(tk.END, f"{i}. {h['date']} | {h['amount']} {h['from']} → {h['result']:.2f} {h['to']}")

def filtr():
    ot_f = filtr_ot.get().strip().upper()
    v_f = filtr_v.get().strip().upper()
    
    otbor = []
    for h in istoria:
        if ot_f and ot_f != h['from']:
            continue
        if v_f and v_f != h['to']:
            continue
        otbor.append(h)
    
    obnovit_istoriyu(otbor)

def sbros():
    filtr_ot.delete(0, tk.END)
    filtr_v.delete(0, tk.END)
    obnovit_istoriyu()

def ochistit():
    if messagebox.askyesno("Очистка", "Удалить всю историю?"):
        global istoria
        istoria = []
        with open("history.json", "w") as f:
            json.dump(istoria, f)
        obnovit_istoriyu()

# Окно
okno = tk.Tk()
okno.title("Currency Converter")
okno.geometry("500x550")

tk.Label(okno, text="КОНВЕРТЕР ВАЛЮТ", font=("Arial", 14, "bold")).pack(pady=10)

# Конвертация
frame1 = tk.LabelFrame(okno, text="Конвертация")
frame1.pack(fill="x", padx=10, pady=10)

row1 = tk.Frame(frame1)
row1.pack(pady=10)

tk.Label(row1, text="Из:").pack(side="left")
iz_valuty = ttk.Combobox(row1, values=valuty, width=8)
iz_valuty.set("USD")
iz_valuty.pack(side="left", padx=5)

tk.Label(row1, text="→").pack(side="left", padx=5)

tk.Label(row1, text="В:").pack(side="left")
v_valuty = ttk.Combobox(row1, values=valuty, width=8)
v_valuty.set("EUR")
v_valuty.pack(side="left", padx=5)

row2 = tk.Frame(frame1)
row2.pack(pady=10)

tk.Label(row2, text="Сумма:").pack(side="left")
pole_summy = tk.Entry(row2, width=12)
pole_summy.pack(side="left", padx=5)

tk.Button(frame1, text="Конвертировать", command=konvertirovat, bg="green", fg="white").pack(pady=10)

metka_result = tk.Label(frame1, text="", font=("Arial", 12), fg="blue")
metka_result.pack()

# История
frame2 = tk.LabelFrame(okno, text="История")
frame2.pack(fill="both", expand=True, padx=10, pady=10)

filtr_row = tk.Frame(frame2)
filtr_row.pack(pady=5)

tk.Label(filtr_row, text="Фильтр по валютам:").pack(side="left")
tk.Label(filtr_row, text="Из:").pack(side="left", padx=(10,2))
filtr_ot = tk.Entry(filtr_row, width=6)
filtr_ot.pack(side="left")

tk.Label(filtr_row, text="В:").pack(side="left", padx=2)
filtr_v = tk.Entry(filtr_row, width=6)
filtr_v.pack(side="left")

tk.Button(filtr_row, text="Фильтр", command=filtr).pack(side="left", padx=5)
tk.Button(filtr_row, text="Сброс", command=sbros).pack(side="left")

spisok_ist = tk.Listbox(frame2, height=8)
spisok_ist.pack(fill="both", expand=True, padx=5, pady=5)

tk.Button(okno, text="Очистить историю", command=ochistit, bg="red", fg="white").pack(pady=10)

obnovit_istoriyu()
okno.mainloop()