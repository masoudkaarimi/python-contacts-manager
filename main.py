import tkinter as tk
from tkinter import ttk, messagebox

from db import ContactDatabase


class ContactManager:
    def __init__(self, root):
        self.root = root
        self.db = ContactDatabase()
        self.root.title("Contact Manager")
        style = ttk.Style()

        # Styles
        self.font_style = ("Helvetica", 10)
        self.label_width = 6

        style.configure(
            'TButton',
            background='gray',
            foreground='black',
            font=('Arial', 11),
            borderwidth=0,
            relief='flat',
            anchor='center',
            padding=5,
            width=15,
            wraplength=150,
        )
        style.map('TButton', background=[('active', '#3949ab')])

        style.configure(
            'TEntry',
            background='gray',
            foreground='black',
            font=('Arial', 12),
            borderwidth=2,
            relief='groove',
            padding=8,
            width=20,
            insertcolor='black',
        )
        style.map('TEntry', background=[('active', 'gray')], foreground=[('active', '#3949ab')])

        style.configure(
            'TLabel',
            foreground='black',
            font=('Arial', 12),
            width=0,
        )

        # Setting the initial window size and position
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.window_width = 845
        self.window_height = 665
        self.x = (self.screen_width - self.window_width) // 2
        self.y = (self.screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{self.x}+{self.y}")
        self.root.resizable(False, False)
        self.root['padx'] = 20
        self.root['pady'] = 20
        # self.root.columnconfigure(1, weight=1)
        # self.root.rowconfigure(0, weight=1)

        # input_frame = ttk.Frame(root)
        # input_frame.grid(padx=(5, 0), pady=(40, 5), sticky="we")
        # label_frame = ttk.Frame(root)
        # label_frame.grid(padx=0, pady=(40, 5), sticky="e")

        # Define Title
        self.title_label = ttk.Label(self.root, width=0, wraplength=0, text="Contact Manager", font=("Arial", 20, "bold"), foreground='#3f51b5')
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 0))

        # Define Labels and Input Fields
        self.id_label = ttk.Label(self.root, text="ID", width=self.label_width, font=self.font_style)
        self.id_label.grid(row=1, column=0, padx=0, pady=(40, 5), sticky="e")
        self.id_entry = ttk.Entry(self.root)
        self.id_entry.grid(row=1, column=1, padx=(5, 0), pady=(40, 5), sticky="we")
        self.id_entry.configure(state="readonly")

        self.name_label = ttk.Label(self.root, text="Name", width=self.label_width, font=self.font_style)
        self.name_label.grid(row=2, column=0, padx=0, pady=5, sticky="e")
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.grid(row=2, column=1, padx=(5, 0), pady=5, sticky="we")

        self.phone_label = ttk.Label(self.root, text="Phone", width=self.label_width, font=self.font_style)
        self.phone_label.grid(row=3, column=0, padx=0, pady=5, sticky="e")
        self.phone_entry = ttk.Entry(self.root)
        self.phone_entry.grid(row=3, column=1, padx=(5, 0), pady=5, sticky="we")

        self.email_label = ttk.Label(self.root, text="Email", width=self.label_width, font=self.font_style)
        self.email_label.grid(row=4, column=0, padx=0, pady=5, sticky="e")
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.grid(row=4, column=1, padx=(5, 0), pady=5, sticky="we")

        # Define Buttons
        self.add_button = ttk.Button(self.root, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=1, column=2, padx=(5, 20), pady=(40, 5), sticky="w")

        self.update_button = ttk.Button(self.root, text="Update Contact", command=self.update_contact)
        self.update_button.grid(row=2, column=2, padx=(5, 20), pady=5, sticky="w")

        self.remove_button = ttk.Button(self.root, text="Remove Contact", command=self.remove_contact)
        self.remove_button.grid(row=3, column=2, padx=(5, 20), pady=5, sticky="w")

        self.clear_button = ttk.Button(self.root, text="Clear", command=self.clear_inputs)
        self.clear_button.grid(row=4, column=2, padx=(5, 20), pady=5, sticky="w")

        # Search Bar
        self.search_label = ttk.Label(self.root, text="Search", width=self.label_width, font=self.font_style)
        self.search_label.grid(row=5, column=0, padx=0, pady=5, sticky="we")
        self.search_entry = ttk.Entry(self.root)
        self.search_entry.grid(row=6, column=0, columnspan=3, padx=(0, 0), pady=5, sticky="we")
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_contacts())

        # Define Treeview (Table)
        self.tree = ttk.Treeview(self.root, columns=('ID', 'Name', 'Phone', 'Email'), show="headings")
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Phone', text='Phone')
        self.tree.heading('Email', text='Email')
        self.tree.bind("<<TreeviewSelect>>", self.update_input_fields)
        self.tree.grid(row=7, column=0, columnspan=3, padx=0, pady=20, sticky='nsew')

        # Define Exit Button
        self.exit_button = ttk.Button(self.root, text="Exit", command=self.root.quit, style='ExitButton.TButton')
        self.exit_button.grid(row=8, column=2, padx=(0, 0), pady=(0, 0), sticky="e")

        # Load contacts into Treeview
        self.load_contacts()

    def load_contacts(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        contacts = self.db.read_records()
        for contact in contacts:
            self.tree.insert("", "end", values=contact)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if name and phone and email:
            self.db.create_record(name, phone, email)
            self.load_contacts()
            self.clear_inputs()
            messagebox.showinfo("Success", "Contact added successfully!")
        else:
            messagebox.showerror("Error", "All fields must be filled!")

    def update_contact(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "Select a contact to update!")
            return

        contact_id = self.tree.item(selected_item[0])['values'][0]
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if not all([name, phone, email]):
            messagebox.showerror("Error", "All fields must be filled!")
            return

        self.db.update_record(contact_id, name, phone, email)
        self.load_contacts()
        self.clear_inputs()
        messagebox.showinfo("Success", "Contact updated successfully!")

    def remove_contact(self):
        selected_item = self.tree.selection()

        if selected_item:
            item_values = self.tree.item(selected_item[0])['values']
            contact_id = item_values[0]
            self.db.delete_record(contact_id)
            self.tree.delete(selected_item[0])
            messagebox.showinfo("Success", "Contact removed successfully!")
        else:
            messagebox.showerror("Error", "Select a contact to remove!")

    def clear_inputs(self):
        # Clear all input fields
        self.id_entry.configure(state="normal")
        self.id_entry.delete(0, tk.END)
        self.id_entry.configure(state="readonly")
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    def search_contacts(self):
        search_query = self.search_entry.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)

        contacts = self.db.read_records()
        for contact in contacts:
            if search_query in contact[1].lower() or search_query in contact[2] or search_query in contact[3].lower():
                self.tree.insert("", "end", values=contact)

    def update_input_fields(self, event):
        selected_item = self.tree.selection()

        if selected_item:
            item = self.tree.item(selected_item[0])
            values = item['values']
            self.id_entry.configure(state="normal")
            self.id_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.phone_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')

            if len(values) >= 3:
                self.id_entry.insert(0, values[0])
                self.name_entry.insert(0, values[1])
                self.phone_entry.insert(0, values[2])
                self.email_entry.insert(0, values[3])
                self.id_entry.configure(state="readonly")


if __name__ == "__main__":
    main_root = tk.Tk()
    app = ContactManager(main_root)
    main_root.mainloop()
