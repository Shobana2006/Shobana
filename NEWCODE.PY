import tkinter as tk
from tkinter import ttk, messagebox
import json
import csv
import os
from PIL import Image, ImageTk 

# ------------------- Login Window --
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("STOCK MANAGEMENT-ELECTRONIC MART")
        self.root.geometry("500x350")
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Login frame
        login_frame = tk.Frame(self.root, width=400, height=250, bg="white", bd=3)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Load and resize the background image to fit the frame
        image = Image.open("bg.png")
        image = image.resize((400, 250))  # Resize to frame size
        self.frame_bg = ImageTk.PhotoImage(image)

        # Add image inside the frame
        bg_label = tk.Label(login_frame, image=self.frame_bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Place widgets on top of image using another frame
        input_frame = tk.Frame(login_frame, bg="#ffffff", bd=0)
        input_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(input_frame, text="Username", bg="white").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(input_frame, textvariable=self.username_var).grid(row=0, column=1, padx=10)

        tk.Label(input_frame, text="Password", bg="white").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(input_frame, textvariable=self.password_var, show="*").grid(row=1, column=1, padx=10)

        tk.Button(input_frame, text="Login", command=self.check_login).grid(row=2, columnspan=2, pady=10)

    def check_login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if username == "admin" and password == "admin123":
            self.root.destroy()
            main_app_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


'''class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("600x400")

        self.bg_image = tk.PhotoImage(file="bg.png")
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        login_frame = tk.Frame(self.root, bg="white", bd=2, relief="ridge")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(login_frame, text="Username", bg="white").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(login_frame, text="Password", bg="white").grid(row=1, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_entry = tk.Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(login_frame, text="Login", command=self.check_login).grid(row=2, column=0, columnspan=2, pady=10)

def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "admin123":
            self.root.destroy()
            main_app_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")'''

# ------------------- Inventory App -------------------
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("900x600")

        self.name_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.stock_in_var = tk.IntVar()
        self.stock_out_var = tk.IntVar()
        self.balance_var = tk.IntVar()
        self.issue_qty_var = tk.IntVar()
        self.inventory = []

        self.create_widgets()
        self.load_inventory()

    def create_widgets(self):
        form_frame = tk.LabelFrame(self.root, text="Item Details", bg="lightyellow")
        form_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="Item Name:", bg="lightyellow").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.name_var).grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Category:", bg="lightyellow").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, state="readonly")
        self.category_combo['values'] = ("Mobile", "Laptop", "Accessory", "Tablet", "Refrigerator", "Air Conditioner", "Washing Machine", "Television", "Others")
        self.category_combo.set("Others")
        self.category_combo.grid(row=0, column=3, padx=5)

        tk.Label(form_frame, text="Stock In:", bg="lightyellow").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.stock_in_var).grid(row=1, column=1, padx=5)

        tk.Label(form_frame, text="Issue Quantity:", bg="lightyellow").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.issue_qty_var).grid(row=1, column=3, padx=5)

        tk.Label(form_frame, text="Balance:", bg="lightyellow").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.balance_var, state='readonly').grid(row=2, column=1, padx=5)

        button_frame = tk.Frame(self.root, bg="lightblue")
        button_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(button_frame, text="Add Item", command=self.add_item).pack(side="left", padx=5)
        tk.Button(button_frame, text="Update Item", command=self.update_item).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete Item", command=self.delete_item).pack(side="left", padx=5)
        tk.Button(button_frame, text="Issue Stock", command=self.issue_stock).pack(side="left", padx=5)
        tk.Button(button_frame, text="View All", command=self.view_all_items).pack(side="left", padx=5)
        tk.Button(button_frame, text="Clear", command=self.clear_fields).pack(side="left", padx=5)
        tk.Button(button_frame, text="Save", command=self.save_inventory).pack(side="left", padx=5)
        tk.Button(button_frame, text="Load", command=self.load_inventory).pack(side="left", padx=5)
        tk.Button(button_frame, text="Export CSV", command=self.export_csv).pack(side="left", padx=5)

        self.tree = ttk.Treeview(self.root, columns=("name", "category", "stock_in", "stock_out", "balance"), show="headings")
        self.tree.heading("name", text="Item Name")
        self.tree.heading("category", text="Category")
        self.tree.heading("stock_in", text="Stock In")
        self.tree.heading("stock_out", text="Issued")
        self.tree.heading("balance", text="Balance")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

    def get_item_data(self):
        name = self.name_var.get().strip()
        category = self.category_var.get().strip()
        stock_in = self.stock_in_var.get()
        stock_out = self.stock_out_var.get()
        balance = stock_in - stock_out
        self.balance_var.set(balance)
        return {"name": name, "category": category, "stock_in": stock_in, "stock_out": stock_out, "balance": balance}

    def add_item(self):
        data = self.get_item_data()
        if data["name"] == "":
            messagebox.showwarning("Input Error", "Item Name is required.")
            return
        for item in self.inventory:
            if item["name"] == data["name"] and item["category"] == data["category"]:
                messagebox.showwarning("Duplicate Entry", "Item already exists.")
                return
        self.inventory.append(data)
        self.tree.insert("", "end", values=(data["name"], data["category"], data["stock_in"], data["stock_out"], data["balance"]))
        self.clear_fields()

    def update_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Item", "Please select an item to update.")
            return
        index = self.tree.index(selected[0])
        data = self.get_item_data()
        self.inventory[index] = data
        self.tree.item(selected[0], values=(data["name"], data["category"], data["stock_in"], data["stock_out"], data["balance"]))
        self.clear_fields()

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Item", "Please select an item to delete.")
            return
        index = self.tree.index(selected[0])
        del self.inventory[index]
        self.tree.delete(selected[0])
        self.clear_fields()

    def issue_stock(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Item", "Please select an item to issue.")
            return
        index = self.tree.index(selected[0])
        issued_qty = self.issue_qty_var.get()
        item = self.inventory[index]
        if issued_qty <= 0 or issued_qty > (item["stock_in"] - item["stock_out"]):
            messagebox.showerror("Invalid Quantity", "Issue quantity must be >0 and <= balance.")
            return
        item["stock_out"] += issued_qty
        item["balance"] = item["stock_in"] - item["stock_out"]
        self.balance_var.set(item["balance"])
        self.tree.item(selected[0], values=(item["name"], item["category"], item["stock_in"], item["stock_out"], item["balance"]))
        self.clear_fields()

    def view_all_items(self):
        self.tree.delete(*self.tree.get_children())
        for item in self.inventory:
            self.tree.insert("", "end", values=(item["name"], item["category"], item["stock_in"], item["stock_out"], item["balance"]))

    def save_inventory(self):
        try:
            with open("inventory_data.json", "w") as f:
                json.dump(self.inventory, f, indent=4)
            messagebox.showinfo("Saved", "Inventory saved to inventory_data.json")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save inventory: {e}")

    def load_inventory(self):
        if not os.path.exists("inventory_data.json"):
            return
        try:
            with open("inventory_data.json", "r") as f:
                self.inventory = json.load(f)
            self.view_all_items()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load inventory: {e}")

    def export_csv(self):
        if not self.inventory:
            messagebox.showwarning("No Data", "No inventory data to export.")
            return
        try:
            with open("inventory_export.csv", "w", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["name", "category", "stock_in", "stock_out", "balance"])
                writer.writeheader()
                writer.writerows(self.inventory)
            messagebox.showinfo("Exported", "Inventory exported to inventory_export.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV: {e}")

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.name_var.set(values[0])
            self.category_var.set(values[1])
            self.stock_in_var.set(int(values[2]))
            self.stock_out_var.set(int(values[3]))
            self.balance_var.set(int(values[4]))

    def clear_fields(self):
        self.name_var.set("")
        self.category_var.set("Others")
        self.stock_in_var.set(0)
        self.stock_out_var.set(0)
        self.balance_var.set(0)
        self.issue_qty_var.set(0)

# ------------------- App Launcher -------------------
def main_app_window():
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()
    app = LoginWindow(login_root)
    login_root.mainloop()
