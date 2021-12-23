import tkinter as tk
import mysql.connector
from tabulate import tabulate

mydb = mysql.connector.connect(host="localhost",
                                           user="pullrequestor",
                                           password="password",
                                           database="pullrequests")

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM requestsdata")

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        table = tk.Frame(self)
        table.pack(side="top", fill="both", expand=True)
        data = mycursor.fetchall()

        self.widgets = {}

        self.widgets["URL"] = {
            "url": tk.Label(table, text="URL"),
            "id_number": tk.Label(table, text="id_number"),
            "number": tk.Label(table, text="number"),
            "state": tk.Label(table, text="state"),
            "user": tk.Label(table, text="user"),
            "title": tk.Label(table, text="title"),
            "created_at": tk.Label(table, text="created_at")
        }

        self.widgets["URL"]["url"].grid(row=1, column=0, sticky="nsew")
        self.widgets["URL"]["id_number"].grid(row=1, column=1, sticky="nsew")
        self.widgets["URL"]["number"].grid(row=1, column=2, sticky="nsew")
        self.widgets["URL"]["state"].grid(row=1, column=2, sticky="nsew")
        self.widgets["URL"]["user"].grid(row=1, column=4, sticky="nsew")
        self.widgets["URL"]["title"].grid(row=1, column=5, sticky="nsew")
        self.widgets["URL"]["created_at"].grid(row=1, column=6, sticky="nsew")

        row = 1
        for url, id_number, number, state, user, title, created_at in (data):
            row += 1
            self.widgets[url] = {
                "url": tk.Label(table, text=url),
                "id_number": tk.Label(table, text=id_number),
                "number": tk.Label(table, text=number),
                "state": tk.Label(table, text=state),
                "user": tk.Label(table, text=user),
                "title": tk.Label(table, text=title),
                "created_at": tk.Label(table, text=created_at)
            }

            self.widgets[url]["url"].grid(row=row, column=0, sticky="nsew")
            self.widgets[url]["id_number"].grid(row=row, column=1, sticky="nsew")
            self.widgets[url]["number"].grid(row=row, column=2, sticky="nsew")
            self.widgets[url]["state"].grid(row=row, column=2, sticky="nsew")
            self.widgets[url]["user"].grid(row=row, column=4, sticky="nsew")
            self.widgets[url]["title"].grid(row=row, column=5, sticky="nsew")
            self.widgets[url]["created_at"].grid(row=row, column=6, sticky="nsew")

        table.grid_columnconfigure(1, weight=1)
        table.grid_columnconfigure(2, weight=1)
        # invisible row after last row gets all extra space
        table.grid_rowconfigure(row+1, weight=1)

    def upload_cor(self):
        for rowid in sorted(self.widgets.keys()):
            entry_widget = self.widgets[rowid]["num_seconds_correction"]
            new_value = entry_widget.get()
            print("%s: %s" % (rowid, new_value))

class RunGrid:
    def run_me(self):
        root = tk.Tk(className='new pull request')
        Example(root).pack(fill="both", expand=True)
        root.mainloop()
