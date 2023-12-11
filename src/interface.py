import tkinter as tk
from tkinter import messagebox
from junk.get_junk import junk_list
from tkinter import ttk
from junk.junk import Junk

class InterfaceGrafica:

    junk_items = junk_list()
    def __init__(self, root):
        self.root = root
        self.root.title("Harmless Company")
        self.total_weight = 0
        self.backpack_contents = tk.Listbox(self.root, width=50, height=10, font=('Perfect DOS VGA 437', 10))
        self.junk_listbox = tk.Listbox(self.root, width=50, height=15, font=('Perfect DOS VGA 437', 10))
        self.backpack_items = []
        self.backpack_item_ids = {}

        self.MAX_WEIGHT = 45  # Peso maximo na mochila
        self.MAX_SLOTS = 4  # Slots maximo
        self.used_slots = 0  # Numero de slots atual

        self.create_widgets()

    def attempt_add(self):
        selected_items = self.tree.selection()
        if selected_items:  # Checa se selecionou
            selected_item_id = selected_items[0]

            if 'disabled' in self.tree.item(selected_item_id, 'tags'): # Checa se o item ta desabilitado
                messagebox.showwarning("Warning", "This item is already in the backpack")
                return

            selected_item_values = self.tree.item(selected_item_id, 'values') # pega os valores do item (nome, valor e peso)

            name = selected_item_values[0]
            value = int(selected_item_values[1])  # de string pra int
            weight = float(selected_item_values[2])  # de string pra float
            selected_item = Junk(name, value, weight)
            self.add_to_backpack(selected_item)
        else:
            messagebox.showwarning("Warning", "No item selected")


    def add_to_backpack(self, item):
        slots_needed = self.MAX_SLOTS - self.used_slots if item.weight > 20 else 1  # Itens pesados pegam os slots restantes

        if self.total_weight + item.weight <= self.MAX_WEIGHT and \
            self.used_slots + slots_needed <= self.MAX_SLOTS:
            
            self.total_weight += item.weight
            self.total_backpack += item.value
            self.backpack_contents.insert(tk.END, str(item))
            self.backpack_items.append(item)
            self.used_slots += slots_needed # Update nos slots
            self.update_weight_label()
            self.update_value_label()
            
            # Disabilita o item na lista
            selected_id = self.tree.selection()[0] 
            self.tree.item(selected_id, tags='disabled')
            self.backpack_item_ids[item] = selected_id
            self.tree.tag_configure('disabled', foreground='gray') 
        else:
            messagebox.showwarning("Warning", "Backpack is full or item is too heavy!")
        
    def remove_item(self):
        try:
            selected_index = self.backpack_contents.curselection()[0]
            item = self.backpack_items.pop(selected_index)
            self.backpack_contents.delete(selected_index)
            self.total_weight -= item.weight
            self.total_backpack -= item.value
            self.update_weight_label()
            self.update_value_label()

            # Reabilita o item na lista (view)
            treeview_id = self.backpack_item_ids.pop(item, None)
            if treeview_id:
                self.tree.item(treeview_id, tags='')  # Tira a tag de 'disabled'

        except IndexError:
            messagebox.showwarning("Warning", "No item selected to remove")


    def update_weight_label(self):
        self.weight_label.config(text=f"Total Weight: {self.total_weight}Kg / {self.MAX_WEIGHT}Kg")

    def update_value_label(self):
        self.value_label.config(text=f"Total Value in Backpack: ${self.total_backpack}")

    def calculate_total_value(self, items):
        return sum(item.value for item in items)

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=('Name', 'Value', 'Weight'), show='headings')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Value', text='Value')
        self.tree.heading('Weight', text='Weight')
        self.tree.column('Name', width=200)
        self.tree.column('Value', width=50, anchor='center')
        self.tree.column('Weight', width=70, anchor='center')

        for item in self.junk_items:
            self.tree.insert('', tk.END, values=(item.name, item.value, item.weight))

        self.tree.pack(pady=10)

        add_button = tk.Button(self.root, text="Add to Backpack", command=self.attempt_add)
        add_button.pack(pady=5)

        remove_button = tk.Button(self.root, text="Remove from Backpack", command=self.remove_item)
        remove_button.pack(pady=5)

        self.total_weight = 0
        self.weight_label = tk.Label(self.root, text=f"Total Weight: {self.total_weight}Kg / {self.MAX_WEIGHT}Kg")
        self.weight_label.pack(pady=5)

        self.total_backpack = 0
        self.value_label = tk.Label(self.root, text=f"Total Value in Backpack: ${self.total_backpack}")
        self.value_label.pack(pady=5)

        total_value_label = tk.Label(self.root, text=f"Total Value of All Items: ${self.calculate_total_value(self.junk_items)}")
        total_value_label.pack(pady=5)

        self.backpack_contents.pack(pady=10)