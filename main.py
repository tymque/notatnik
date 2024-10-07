import tkinter as tk
from tkinter import ttk, font
from tktooltip import ToolTip
import database
import user


def on_focus_in(event):
    if search_bar.get() == "szukaj":
        search_bar.delete(0, tk.END)
        search_bar.configure(foreground="black", font=font)


def on_focus_out(event):
    if search_bar.get() == "":
        search_bar.insert(0, "szukaj")
        search_bar.configure(foreground="gray", font=font_placeholder)


def register():
    un = login_entry.get()
    pw = pass_entry.get()
    if un == "" or pw == "":
        text = "Wypełnij pola"
        error_label.config(text=text)
    else:
        query_create = Base.create_user(un, pw)
        if query_create == "success":
            login_window.destroy()
            root.deiconify()
            get_notes(Base.select_all_notes(user.id))
        elif query_create == "username_taken":
            text = "Konto już istnieje"
            error_label.config(text=text)


def login():
    un = login_entry.get()
    pw = pass_entry.get()
    if un == "" or pw == "":
        text = "Wypełnij pola"
        error_label.config(text=text)
    else:
        query_login = Base.login(un, pw)
        if query_login is None:
            text = "Błędne dane"
            error_label.config(text=text)
        else:
            user.id = query_login[0]
            user.login = query_login[1]
            print("Zalogowano pomyślnie " + str(user.id))
            login_window.destroy()
            root.deiconify()
            get_notes(Base.select_all_notes(user.id))


def get_notes(query):
    listbox.delete(0, 10)
    if len(query) == 0:
        listbox.insert("end", "Brak notatek")
        listbox.configure(state="disabled")
    else:
        for row in query:
            date = str(row[3].strftime("%d.%m.%Y"))
            if len(row[2]) > 20:
                listbox.insert("end", row[2][0:20] + "... " + date)
            else:
                listbox.insert("end", row[2] + " " + date)
            listbox.configure(state="normal")


def display_note(event):
    text_box.delete(1.0, tk.END)
    selected_note = listbox.curselection()
    query = Base.select_all_notes(user.id)
    row = query[selected_note[0]]
    text_box.insert(tk.END, row[2])
    date = str(row[3].strftime("%d.%m.%Y, %H:%M"))
    info.config(text=date)


def search():
    phrase = search_bar.get()
    if phrase != "szukaj":
        query = Base.search(user.id, phrase)
        get_notes(query)
    else:
        query = Base.select_all_notes(user.id)
        get_notes(query)


Base = database.Database()
user = user.User

root = tk.Tk()
root.title("Notatnik")
root.iconbitmap("notepad_icon.ico")
root.geometry("655x700")
root.resizable(False, False)
root.defaultFont = font.nametofont("TkDefaultFont")
root.defaultFont.configure(family="Helvetica", size=11)

search_icon = tk.PhotoImage(file=r"./icons/search.png")
save_icon = tk.PhotoImage(file=r"./icons/save.png")
delete_icon = tk.PhotoImage(file=r"./icons/delete.png")
create_icon = tk.PhotoImage(file=r"./icons/new.png")

font = ("Helvetica", 11)
font_header = ("Helvetica", 14, "bold")
font_placeholder = ("Helvetica", 11, "italic")

info = ttk.Label(root)
delete_button = ttk.Button(root, image=delete_icon)
save_button = ttk.Button(root, image=save_icon)
create_button = ttk.Button(root, image=create_icon)
search_bar = ttk.Entry(root, width=25, font=font_placeholder)
search_button = ttk.Button(image=search_icon, command=search)
text_box = tk.Text(root, width=40, font=("Helvetica", 13), wrap="word", relief="groove")
listbox = tk.Listbox(root, width=30, font=font)

search_bar.insert(0, "szukaj")
search_bar.configure(foreground="gray")
search_bar.bind("<FocusIn>", on_focus_in)
search_bar.bind("<FocusOut>", on_focus_out)

listbox.bind("<<ListboxSelect>>", display_note)

ToolTip(save_button, msg="Zapisz", delay=0.75)
ToolTip(delete_button, msg="Usuń", delay=0.75)
ToolTip(create_button, msg="Nowy", delay=0.75)

info.grid(column=0, row=0, pady=0, padx=10, sticky=tk.S)
delete_button.grid(column=1, row=0, columnspan=3, pady=0, padx=70, sticky=tk.E)
save_button.grid(column=2, row=0, columnspan=2, pady=0, padx=40, sticky=tk.E)
create_button.grid(column=3, row=0, pady=0, padx=10, sticky=tk.E)
search_bar.grid(column=4, row=0, pady=0, padx=5, sticky=tk.W)
search_button.grid(column=5, row=0, pady=0, padx=5, sticky=tk.E)
text_box.grid(column=0, row=1, columnspan=4, pady=5, padx=10)
listbox.grid(column=4, row=1, columnspan=2, pady=5, padx=5, sticky=tk.N)

login_window = tk.Toplevel()
login_window.title("Notatnik - logowanie")
login_window.iconbitmap("notepad_icon.ico")
login_window.geometry("400x200")
login_window.protocol('WM_DELETE_WINDOW', root.quit)
login_window.resizable(False, False)


label = ttk.Label(login_window, text="Zaloguj się", font=font_header)
login_label = ttk.Label(login_window, text="Login:", font=font)
login_entry = ttk.Entry(login_window, font=font)
pass_label = ttk.Label(login_window, text="Hasło:", font=font)
pass_entry = ttk.Entry(login_window, font=font)
login_button = ttk.Button(login_window, text="Zaloguj", command=login)
register_button = ttk.Button(login_window, text="Zarejestruj", command=register)
error_label = ttk.Label(login_window, font=font, foreground="red")

label.grid(column=0, row=0, columnspan=2, pady=10, padx=150)
login_label.grid(column=0, row=1, pady=5, padx=5, sticky=tk.E)
login_entry.grid(column=1, row=1, pady=5, padx=5, sticky=tk.W)
pass_label.grid(column=0, row=2, pady=5, padx=5, sticky=tk.E)
pass_entry.grid(column=1, row=2, pady=5, padx=5, sticky=tk.W)
login_button.grid(column=1, row=3, pady=5, padx=5)
register_button.grid(column=0, row=3, columnspan=2, pady=5, padx=91, sticky=tk.W)
error_label.grid(column=1, row=4, pady=5, padx=15, sticky=tk.W)

root.withdraw()
login_window.mainloop()
root.mainloop()
