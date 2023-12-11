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
        self.custom_font = ("Perfect DOS VGA 437", 12)
        self.junk_listbox = tk.Listbox(
            self.root, width=50, height=15, font=self.custom_font
        )
        self.backpack_items = []
        self.backpack_item_ids = {}
        
        self.MAX_WEIGHT = 45  # Peso maximo na mochila

        self.create_widgets()

    def attempt_add(self):
        selected_items = self.tree.selection()
        if selected_items:  # Checa se selecionou
            selected_item_id = selected_items[0]

            if "disabled" in self.tree.item(
                selected_item_id, "tags"
            ):  # Checa se o item ta desabilitado
                messagebox.showwarning(
                    "Warning", "This item is already in the backpack"
                )
                return

            selected_item_values = self.tree.item(
                selected_item_id, "values"
            )  # pega os valores do item (nome, valor e peso)

            name = selected_item_values[0]
            value = int(selected_item_values[1])  # de string pra int
            weight = float(selected_item_values[2])  # de string pra float
            selected_item = Junk(name, value, weight)
            self.add_to_backpack(selected_item)
        else:
            messagebox.showwarning("Warning", "No item selected")

    def add_to_backpack(self, item):
        if self.total_weight + item.weight <= self.MAX_WEIGHT:
            self.total_weight += item.weight
            self.total_backpack += item.value
            self.backpack_contents.insert(tk.END, str(item))
            self.backpack_items.append(item)
        
            self.update_weight_label()
            self.update_value_label()

            # Disabilita o item na lista
            selected_id = self.tree.selection()[0]
            current_tags = tuple(self.tree.item(selected_id, 'tags'))
            new_tags = current_tags + ('disabled',)
            self.tree.item(selected_id, tags=new_tags)

            self.backpack_item_ids[item] = selected_id
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
                current_tags = tuple(self.tree.item(treeview_id, 'tags'))
                if "highlight" in current_tags:
                    current_tags = ("highlight",)
                else:
                    current_tags = ""
                self.tree.item(treeview_id, tags=current_tags)  # Tira a tag de 'disabled'

        except IndexError:
            messagebox.showwarning("Warning", "No item selected to remove")

    def update_weight_label(self):
        self.weight_label.config(
            text=f"Total Weight: {self.total_weight}Kg / {self.MAX_WEIGHT}Kg"
        )

    def update_value_label(self):
        self.value_label.config(text=f"Total Value in Backpack: ${self.total_backpack}")

    def calculate_total_value(self, items):
        return sum(item.value for item in items)

    def create_widgets(self):
        top_frame = ttk.Frame(self.root)
        top_frame.pack(side="top", padx=10, pady=10, expand=True)

        self.tree = ttk.Treeview(
            top_frame, columns=("Name", "Value", "Weight"), show="headings"
        )
        self.tree.heading("Name", text="Name")
        self.tree.heading("Value", text="Value")
        self.tree.heading("Weight", text="Weight")
        self.tree.column("Name", width=200)
        self.tree.column("Value", width=50, anchor="center")
        self.tree.column("Weight", width=70, anchor="center")
        self.tree.tag_configure("highlight", background="lightblue")
        self.tree.tag_configure("disabled", foreground="gray")

        for item in self.junk_items:
            self.tree.insert("", tk.END, values=(item.name, item.value, item.weight))

        scrollbar = ttk.Scrollbar(top_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left")
        scrollbar.pack(side="right", fill="y")

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        add_button = tk.Button(
            button_frame, text="Add to Backpack", command=self.attempt_add
        )
        add_button.pack(side="left", fill="both", expand=True, pady=5, padx=5)

        remove_button = tk.Button(
            button_frame, text="Remove from Backpack", command=self.remove_item
        )
        remove_button.pack(side="left", fill="both", expand=True, pady=5, padx=5)

        knapsack_button = tk.Button(
            button_frame, text="Ask the computer", command=self.highlight_items
        )
        knapsack_button.pack(side="left", fill="both", expand=True, pady=5, padx=5)

        self.total_weight = 0
        self.weight_label = tk.Label(
            self.root,
            text=f"Current Weight: {self.total_weight}Kg / {self.MAX_WEIGHT}Kg",
        )
        self.weight_label.pack(pady=5)

        self.total_backpack = 0
        self.value_label = tk.Label(
            self.root, text=f"Current Value: ${self.total_backpack}"
        )
        self.value_label.pack(pady=5)

        # total_value_label = tk.Label(self.root, text=f"Total Value of Items: ${self.calculate_total_value(self.junk_items)}")
        # total_value_label.pack(pady=5)

        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(side="bottom", padx=10, pady=10, expand=True)

        self.backpack_contents = tk.Listbox(
            bottom_frame, width=50, height=10, font=self.custom_font
        )
        scrollbar_2 = ttk.Scrollbar(
            bottom_frame, orient="vertical", command=self.backpack_contents.yview
        )

        self.backpack_contents.configure(yscrollcommand=scrollbar_2.set)
        self.backpack_contents.pack(side="left")
        scrollbar_2.pack(side="right", fill="y")

    def knapsack(self):
        n = len(self.junk_items)
        dp = [[0] * (self.MAX_WEIGHT + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            item = self.junk_items[i - 1]
            value = item.get_value()
            weight = item.get_weight()
            for w in range(1, self.MAX_WEIGHT + 1):
                if weight > w:
                    dp[i][w] = dp[i - 1][w]
                else:
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)

        selected_items = []
        w = self.MAX_WEIGHT
        print("weight before " + str(w))
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                item = self.junk_items[i - 1]
                value = item.get_value()
                weight = item.get_weight()
                selected_items.append(self.junk_items[i - 1].name)
                w -= weight
        print("weight after " + str(w))
        return selected_items[::-1]
    
    def highlight_items(self):
        item_list = self.knapsack()
        print(item_list)
        tree_list = self.tree.get_children()

        for item in item_list:
            for item_id in tree_list:
                item_values = self.tree.item(item_id)['values']

                if item_values and item_values[0] == item:
                    current_tags = tuple(self.tree.item(item_id, 'tags'))
                    new_tags = current_tags + ('highlight',)
                    self.tree.item(item_id, tags=new_tags)
                    break
        