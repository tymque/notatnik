import tkinter as tk
from tkinter import ttk, font
from tktooltip import ToolTip
import database
import user
import note


def on_searchbar_focus_in(search_bar):
    if search_bar.get() == "szukaj":
        search_bar.delete(0, tk.END)
        search_bar.configure(foreground="black", font=font)


def on_searchbar_focus_out(search_bar):
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
        if not db.error:
            query_create = db.create_user(un, pw)
            if query_create == "success":
                login_window.destroy()
                main_window()
            elif query_create == "username_taken":
                text = "Konto już istnieje"
                error_label.config(text=text)
        else:
            error_label.config(text="Błąd połączenia")


def login():
    un = login_entry.get()
    pw = pass_entry.get()
    if un == "" or pw == "":
        text = "Wypełnij pola"
        error_label.config(text=text)
    else:
        if not db.error:
            query_login = db.login(un, pw)
            if query_login is None:
                text = "Błędne dane"
                error_label.config(text=text)
            else:
                user.id = query_login[0]
                user.login = query_login[1]
                login_window.destroy()
                main_window()
        else:
            error_label.config(text="Błąd połączenia")


def get_notes(query, listbox):
    listbox.configure(state="normal")
    listbox.delete(0, tk.END)
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


def get_note_data(listbox, delete_button, save_button, text_box, date, search_bar):
    selected_note = listbox.curselection()
    if search_bar.get() == "szukaj":
        query = db.select_all_notes(user.id)
    else:
        query = db.search(user.id, search_bar.get())
    row = query[selected_note[0]]
    note.id = row[0]
    note.content = row[2]
    note.date = str(row[3].strftime("%d.%m.%Y, %H:%M"))
    delete_button.config(state=tk.NORMAL)
    save_button.config(state=tk.NORMAL)
    display_data(text_box, date)


def display_data(text_box, date):
    clear_data(text_box, date)
    text_box.insert(tk.END, note.content)
    date.config(text=note.date)


def clear_data(text_box, date):
    text_box.delete("1.0", tk.END)
    date.config(text="")


def delete_note(text_box, date, listbox, delete_button, save_button, search_bar):
    db.delete_note(note.id)
    clear_data(text_box, date)
    get_notes(db.select_all_notes(user.id), listbox)
    delete_button.config(state=tk.DISABLED)
    save_button.config(state=tk.DISABLED)
    search_bar.delete(0, tk.END)
    search_bar.event_generate("<FocusOut>")


def create_note(listbox, text_box, date, search_bar):
    db.create_note(user.id, "Nowa notatka")
    get_notes(db.select_all_notes(user.id), listbox)
    listbox.select_set(0)
    listbox.event_generate("<<ListboxSelect>>")
    display_data(text_box, date)
    search_bar.delete(0, tk.END)
    search_bar.event_generate("<FocusOut>")


def edit_note(text_box, listbox, date, search_bar):
    new_content = text_box.get("1.0", tk.END).strip()
    db.edit_note(note.id, new_content)
    get_notes(db.select_all_notes(user.id), listbox)
    listbox.select_set(0)
    listbox.event_generate("<<ListboxSelect>>")
    display_data(text_box, date)
    search_bar.delete(0, tk.END)
    search_bar.event_generate("<FocusOut>")


def search(search_bar, delete_button, save_button, listbox, text_box, date):
    phrase = search_bar.get()
    if phrase != "szukaj":
        query = db.search(user.id, phrase)
        get_notes(query, listbox)
    else:
        query = db.select_all_notes(user.id)
        get_notes(query, listbox)
    delete_button.config(state=tk.DISABLED)
    save_button.config(state=tk.DISABLED)
    clear_data(text_box, date)


def main_window(tkfont=font):
    root = tk.Tk()
    root.title("Notatnik")
    root.iconbitmap("notepad_icon.ico")
    root.geometry("645x550")
    root.resizable(False, False)
    root.defaultFont = tkfont.nametofont("TkDefaultFont")
    root.defaultFont.configure(family="Helvetica", size=11)

    save_icon = tk.PhotoImage(file=r"./icons/save.png")
    delete_icon = tk.PhotoImage(file=r"./icons/delete.png")
    create_icon = tk.PhotoImage(file=r"./icons/new.png")

    date = ttk.Label(root)
    delete_button = ttk.Button(root, image=delete_icon,
                               command=lambda: delete_note(text_box, date, listbox, delete_button, save_button,
                                                           search_bar))
    save_button = ttk.Button(root, image=save_icon, command=lambda: edit_note(text_box, listbox, date, search_bar))
    create_button = ttk.Button(root, image=create_icon,
                               command=lambda: create_note(listbox, text_box, date, search_bar))
    search_bar = ttk.Entry(root, width=30, font=font_placeholder)
    text_box = tk.Text(root, width=40, height=25, font=("Helvetica", 13), wrap="word", relief="solid")
    listbox = tk.Listbox(root, width=30, height=27, font=font, exportselection=False)

    search_bar.insert(0, "szukaj")
    search_bar.configure(foreground="gray")
    search_bar.bind("<FocusIn>", lambda x: on_searchbar_focus_in(search_bar))
    search_bar.bind("<FocusOut>", lambda x: on_searchbar_focus_out(search_bar))
    search_bar.bind("<KeyRelease>", lambda x: search(search_bar, delete_button, save_button, listbox, text_box, date))

    listbox.bind("<<ListboxSelect>>", lambda x: get_note_data(listbox, delete_button, save_button, text_box, date, search_bar))

    ToolTip(save_button, msg="Zapisz", delay=0.75)
    ToolTip(delete_button, msg="Usuń", delay=0.75)
    ToolTip(create_button, msg="Nowy", delay=0.75)

    delete_button.config(state=tk.DISABLED)
    save_button.config(state=tk.DISABLED)

    date.grid(column=0, row=0, pady=0, padx=10, sticky=tk.W)
    delete_button.grid(column=1, row=0, columnspan=3, pady=0, padx=70, sticky=tk.E)
    save_button.grid(column=2, row=0, columnspan=2, pady=0, padx=40, sticky=tk.E)
    create_button.grid(column=3, row=0, pady=0, padx=10, sticky=tk.E)
    search_bar.grid(column=4, row=0, pady=0, padx=5, sticky=tk.W)
    text_box.grid(column=0, row=1, columnspan=4, pady=5, padx=10)
    listbox.grid(column=4, row=1, pady=5, padx=5, sticky=tk.N)

    get_notes(db.select_all_notes(user.id), listbox)
    root.mainloop()


db = database.Database()
user = user.User
note = note.Note()

font = ("Helvetica", 11)
font_header = ("Helvetica", 14, "bold")
font_placeholder = ("Helvetica", 11, "italic")

login_window = tk.Tk()
login_window.title("Notatnik - logowanie")
login_window.iconbitmap("notepad_icon.ico")
login_window.geometry("400x200")
login_window.resizable(False, False)


label = ttk.Label(login_window, text="Zaloguj się", font=font_header)
login_label = ttk.Label(login_window, text="Login:", font=font)
login_entry = ttk.Entry(login_window, font=font)
pass_label = ttk.Label(login_window, text="Hasło:", font=font)
pass_entry = ttk.Entry(login_window, show="*", font=font)
login_button = ttk.Button(login_window, text="Zaloguj", command=login)
register_button = ttk.Button(login_window, text="Zarejestruj", command=register)
error_label = ttk.Label(login_window, font=font, foreground="red")

login_window.bind("<Return>", lambda x: login())

label.grid(column=0, row=0, columnspan=2, pady=10, padx=150)
login_label.grid(column=0, row=1, pady=5, padx=5, sticky=tk.E)
login_entry.grid(column=1, row=1, pady=5, padx=5, sticky=tk.W)
pass_label.grid(column=0, row=2, pady=5, padx=5, sticky=tk.E)
pass_entry.grid(column=1, row=2, pady=5, padx=5, sticky=tk.W)
login_button.grid(column=1, row=3, pady=5, padx=5)
register_button.grid(column=0, row=3, columnspan=2, pady=5, padx=91, sticky=tk.W)
error_label.grid(column=1, row=4, pady=5, padx=15, sticky=tk.W)


login_window.mainloop()
