import tkinter as tk
from tkinter import ttk, font
from tktooltip import ToolTip


def on_focus_in(event):
    if searchBar.get() == "szukaj":
        searchBar.delete(0, tk.END)
        searchBar.configure(foreground="black", font=font)


def on_focus_out(event):
    if searchBar.get() == "":
        searchBar.insert(0, "szukaj")
        searchBar.configure(foreground="gray", font=font_placeholder)


root = tk.Tk()
root.title("Notatnik")
root.iconbitmap("notepad_icon.ico")
root.geometry("655x700")
root.resizable(False, False)
root.defaultFont = font.nametofont("TkDefaultFont")
root.defaultFont.configure(family="Helvetica", size=11)

searchIcon = tk.PhotoImage(file=r"./icons/search.png")
saveIcon = tk.PhotoImage(file=r"./icons/save.png")
deleteIcon = tk.PhotoImage(file=r"./icons/delete.png")
createIcon = tk.PhotoImage(file=r"./icons/new.png")

font = ("Helvetica", 11)
font_header = ("Helvetica", 14, "bold")
font_placeholder = ("Helvetica", 11, "italic")

info = ttk.Label(root, text="24.09.2024, 19:15")
deleteButton = ttk.Button(root, image=deleteIcon)
saveButton = ttk.Button(root, image=saveIcon)
createButton = ttk.Button(root, image=createIcon)
searchBar = ttk.Entry(root, width=25, font=font_placeholder)
searchButton = ttk.Button(image=searchIcon)
textBox = tk.Text(root, width=40, font=("Helvetica", 13))
listBox = tk.Listbox(root, width=30, font=font)
for x in range(20):
    listBox.insert("end", x + 1)

searchBar.insert(0, "szukaj")
searchBar.configure(foreground="gray")
searchBar.bind("<FocusIn>", on_focus_in)
searchBar.bind("<FocusOut>", on_focus_out)

ToolTip(saveButton, msg="Zapisz", delay=0.75)
ToolTip(deleteButton, msg="Usuń", delay=0.75)
ToolTip(createButton, msg="Nowy", delay=0.75)

info.grid(column=0, row=0, pady=0, padx=10, sticky=tk.S)
deleteButton.grid(column=1, row=0, columnspan=3, pady=0, padx=70, sticky=tk.E)
saveButton.grid(column=2, row=0, columnspan=2, pady=0, padx=40, sticky=tk.E)
createButton.grid(column=3, row=0, pady=0, padx=10, sticky=tk.E)
searchBar.grid(column=4, row=0, pady=0, padx=5, sticky=tk.W)
searchButton.grid(column=5, row=0, pady=0, padx=5, sticky=tk.E)
textBox.grid(column=0, row=1, columnspan=4, pady=5, padx=10)
listBox.grid(column=4, row=1, columnspan=2, pady=5, padx=5, sticky=tk.N)

login_window = tk.Tk()
login_window.title("Notatnik - logowanie")
login_window.iconbitmap("notepad_icon.ico")
login_window.geometry("400x200")
login_window.resizable(False, False)


label = ttk.Label(login_window, text="Zaloguj się", font=font_header)
login_label = ttk.Label(login_window, text="Login:", font=font)
login_entry = ttk.Entry(login_window, font=font)
pass_label = ttk.Label(login_window, text="Hasło:", font=font)
pass_entry = ttk.Entry(login_window, font=font)
login_button = ttk.Button(login_window, text="Zaloguj")
register_button = ttk.Button(login_window, text="Zarejestruj")
error_label = ttk.Label(login_window, text="Błędne dane", font=font, foreground="red")

label.grid(column=0, row=0, columnspan=2, pady=10, padx=150)
login_label.grid(column=0, row=1, pady=5, padx=5, sticky=tk.E)
login_entry.grid(column=1, row=1, pady=5, padx=5, sticky=tk.W)
pass_label.grid(column=0, row=2, pady=5, padx=5, sticky=tk.E)
pass_entry.grid(column=1, row=2, pady=5, padx=5, sticky=tk.W)
login_button.grid(column=1, row=3, pady=5, padx=5)
register_button.grid(column=0, row=3, columnspan=2, pady=5, padx=91, sticky=tk.W)
error_label.grid(column=1, row=4, pady=5, padx=15, sticky=tk.W)

root.mainloop()
