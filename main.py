import tkinter as tk
from tkinter import ttk, font


root = tk.Tk()
root.title("Notatnik")
root.iconbitmap("notepad_icon.ico")
root.geometry("575x700")
root.resizable(False, False)
root.defaultFont = font.nametofont("TkDefaultFont")
root.defaultFont.configure(family="Helvetica", size=11)


info = ttk.Label(root, text="24.09.2024, 19:15 | 123")
saveButton = ttk.Button(root, text="Zapisz")
textBox = tk.Text(root, width=40, font=("Helvetica", 12))
listBox = tk.Listbox(root)
for x in range(20):
    listBox.insert("end", x+1)

info.grid(column=0, row=0, pady=0, padx=15, sticky=tk.S)
saveButton.grid(column=2, row=0, pady=0, padx=15, sticky=tk.E)
textBox.grid(column=0, row=1, columnspan=3, pady=5, padx=15)
listBox.grid(column=3, row=1, pady=5, padx=5, sticky=tk.N)


login_window = tk.Tk()
login_window.title("Notatnik - logowanie")
login_window.iconbitmap("notepad_icon.ico")
login_window.geometry("400x200")
login_window.resizable(False, False)

font = ("Helvetica", 11)
font_header = ("Helvetica", 14, "bold")

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
login_window.mainloop()
