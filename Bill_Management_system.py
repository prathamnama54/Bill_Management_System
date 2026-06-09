from tkinter import *
from tkinter import messagebox
import tempfile
import os
import subprocess  # Needed for Mac printing

root = Tk()
root.title('Billing Management System')
root.geometry('1280x720')
bg_color = '#2D9290'

# =====================variables===================
Pizza = IntVar()
Burger = IntVar()
Patties = IntVar()
ColdCoffee = IntVar()
Total = IntVar()

cp = StringVar()
cb = StringVar()
cr = StringVar()
cc = StringVar()
total_cost = StringVar()

# ===========Function===============
def total():
    if Pizza.get() == 0 and Burger.get() == 0 and Patties.get() == 0 and ColdCoffee.get() == 0:
        messagebox.showerror('Error', 'Please select number of quantity')
    else:
        p, b, pa, cc_val = Pizza.get(), Burger.get(), Patties.get(), ColdCoffee.get()

        t = float(p * 149 + b * 79 + pa * 35 + cc_val * 49)
        Total.set(p + b + pa + cc_val)
        total_cost.set(f'₹ {round(t, 2)}')

        cp.set(f'₹ {p * 149}')
        cb.set(f'₹ {b * 79}')
        cr.set(f'₹ {pa * 35}')
        cc.set(f'₹ {cc_val * 49}')

def receipt():
    textarea.delete(1.0, END)
    textarea.insert(END, ' Items\t\tQty\tCost\n')
    textarea.insert(END, '='*35 + '\n')

    if Pizza.get() > 0:
        textarea.insert(END, f'Pizza\t\t{Pizza.get()}\t{cp.get()}\n')
    if Burger.get() > 0:
        textarea.insert(END, f'Burger\t\t{Burger.get()}\t{cb.get()}\n')
    if Patties.get() > 0:
        textarea.insert(END, f'Patties\t\t{Patties.get()}\t{cr.get()}\n')
    if ColdCoffee.get() > 0:
        textarea.insert(END, f'Coffee\t\t{ColdCoffee.get()}\t{cc.get()}\n')

    textarea.insert(END, f"\n" + "="*35)
    textarea.insert(END, f'\nTotal Items:\t{Total.get()}')
    textarea.insert(END, f'\nTotal Price:\t\t{total_cost.get()}')
    textarea.insert(END, f"\n" + "="*35)

def print_receipt():
    content = textarea.get('1.0', 'end-1c')
    if not content.strip():
        messagebox.showerror('Error', 'No receipt to print!')
        return
    
    # Using a safer way to create a temp file
    fd, path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(content)
        
        # macOS specific print command
        subprocess.run(['lpr', path]) 
        messagebox.showinfo('Success', 'Receipt sent to printer!')
    finally:
        # Keep the file or delete it after printing
        pass

def reset():
    textarea.delete(1.0, END)
    for var in [Pizza, Burger, Patties, ColdCoffee, Total]: var.set(0)
    for var in [cp, cb, cr, cc, total_cost]: var.set('')

def exit_app():
    if messagebox.askyesno('Exit', 'Do you really want to exit?'):
        root.destroy()

# ================= UI Elements =================
title = Label(root, pady=5, text="Billing Management System", bd=12, bg=bg_color, fg='white', font=('times new roman', 35, 'bold'), relief=GROOVE)
title.pack(fill=X)

F1 = LabelFrame(root, text='Product Details', font=('times new roman', 18, 'bold'), fg='gold', bg=bg_color, bd=15, relief=RIDGE)
F1.place(x=5, y=90, width=800, height=500)

# Labels
headers = ["Items", "Quantity", "Cost"]
for i, h in enumerate(headers):
    Label(F1, text=h, font=('Helvetica', 20, 'bold', 'underline'), fg='black', bg=bg_color).grid(row=0, column=i, padx=20, pady=15)

# Product Rows (Condensed for brevity)
products = [('Pizza', Pizza, cp), ('Burger', Burger, cb), ('Patties', Patties, cr), ('Cold Coffee', ColdCoffee, cc), ('Total', Total, total_cost)]
for i, (name, var_qty, var_cost) in enumerate(products, 1):
    Label(F1, text=name, font=('times new roman', 20, 'bold'), fg='lawngreen', bg=bg_color).grid(row=i, column=0, padx=20, pady=15)
    Entry(F1, font='arial 15 bold', bd=7, textvariable=var_qty, width=12).grid(row=i, column=1, padx=20)
    Entry(F1, font='arial 15 bold', bd=7, textvariable=var_cost, width=12).grid(row=i, column=2, padx=20)

# Bill Area
F2 = Frame(root, relief=GROOVE, bd=10)
F2.place(x=820, y=90, width=430, height=500)
Label(F2, text='Receipt', font='arial 15 bold', bd=7, relief=GROOVE).pack(fill=X)
textarea = Text(F2, font='arial 15')
textarea.pack(fill=BOTH, expand=True)

# Buttons
F3 = Frame(root, bg=bg_color, bd=15, relief=RIDGE)
F3.place(x=5, y=590, width=1270, height=120)

btns = [('Total', total), ('Receipt', receipt), ('Print', print_receipt), ('Reset', reset), ('Exit', exit_app)]
for i, (txt, cmd) in enumerate(btns):
    Button(F3, text=txt, font='arial 20 bold', fg='red', width=9, command=cmd).grid(row=0, column=i, padx=12, pady=15)

root.mainloop()