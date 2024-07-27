import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import datetime
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.use('TkAgg')

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("500x600")  # Adjust window size

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # Description
        self.description_label = tk.Label(self.root, text="Description:")
        self.description_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.description_entry = tk.Entry(self.root, width=40)
        self.description_entry.grid(row=0, column=1, padx=10, pady=10)

        # Amount
        self.amount_label = tk.Label(self.root, text="Amount ($):")
        self.amount_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.amount_entry = tk.Entry(self.root, width=40)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        # Log Button
        self.log_button = tk.Button(self.root, text="Log Expense", command=self.log_expense, width=20)
        self.log_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # View Button
        self.view_button = tk.Button(self.root, text="View Expenses", command=self.view_expenses, width=20)
        self.view_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Upload Button
        self.upload_button = tk.Button(self.root, text="Upload Expense File", command=self.upload_file, width=20)
        self.upload_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.visualize_button = tk.Button(self.root, text="Visualize Expenses", command=self.visualize_expenses, width=20)
        self.visualize_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Search Label and Entry
        self.search_label = tk.Label(self.root, text="Search Expenses:")
        self.search_label.grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)
        self.search_entry = tk.Entry(self.root, width=40)
        self.search_entry.grid(row=6, column=1, padx=10, pady=10)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_expenses, width=20)
        self.search_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        # Status Label
        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Update Button
        self.update_button = tk.Button(self.root, text="Update Expense", command=self.select_expense_for_update, width=20)
        self.update_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

        # Delete Button
        self.delete_button = tk.Button(self.root, text="Delete Expense", command=self.select_expense_for_delete, width=20)
        self.delete_button.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

        # Update/Delete Search Label and Entry
        self.update_search_label = tk.Label(self.root, text="Search to Update/Delete:")
        self.update_search_label.grid(row=13, column=0, padx=10, pady=10, sticky=tk.W)
        self.update_search_entry = tk.Entry(self.root, width=40)
        self.update_search_entry.grid(row=13, column=1, padx=10, pady=10)

    def log_expense(self):
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        if description and amount:
            with open("expenses.txt", "a") as file:
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{date} | {description} | ${amount}\n")
            self.description_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.status_label.config(text="Expense logged successfully!")
        else:
            messagebox.showerror("Input Error", "Please enter both description and amount.")

    def view_expenses(self):
        try:
            with open("expenses.txt", "r") as file:
                expenses = file.readlines()
                if expenses:
                    expenses_str = "\n".join([e.strip() for e in expenses])
                    messagebox.showinfo("Logged Expenses", expenses_str)
                else:
                    messagebox.showinfo("Logged Expenses", "No expenses logged yet.")
        except FileNotFoundError:
            messagebox.showinfo("Logged Expenses", "No expenses logged yet.")

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    for line in file:
                        parts = line.strip().split('|')
                        if len(parts) == 3:
                            description = parts[1].strip()
                            amount = parts[2].replace('$', '').strip()
                            self._expense_from_file(description, amount)
                self.display_expenses_window()
            except Exception as e:
                messagebox.showerror("File Upload Error", str(e))

    def _expense_from_file(self, description, amount):
        if description and amount:
            with open("expenses.txt", "a") as file:
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{date} | {description} | ${amount}\n")

    def display_expenses_window(self):
        top = tk.Toplevel(self.root)
        top.title("Edit Expenses")

        expenses_list = tk.Listbox(top, width=80, height=20)
        expenses_list.pack(padx=10, pady=10)

        # Populate listbox with current expenses
        try:
            with open("expenses.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    expenses_list.insert(tk.END, line.strip())
        except FileNotFoundError:
            messagebox.showinfo("Edit Expenses", "No expenses to display.")

        def edit_expense():
            selected_index = expenses_list.curselection()
            if selected_index:
                selected_line = expenses_list.get(selected_index).strip()
                parts = selected_line.split('|')
                if len(parts) == 3:
                    description = parts[1].strip()
                    amount = parts[2].replace('$', '').strip()
                    new_description = simpledialog.askstring("Edit Expense", "Enter new description:", initialvalue=description)
                    new_amount = simpledialog.askstring("Edit Expense", "Enter new amount ($):", initialvalue=amount)
                    if new_description and new_amount:
                        updated_lines = []
                        with open("expenses.txt", "r") as file:
                            lines = file.readlines()
                            for line in lines:
                                if selected_line in line:
                                    updated_line = f"{parts[0]} | {new_description} | ${new_amount}\n"
                                    updated_lines.append(updated_line)
                                else:
                                    updated_lines.append(line)
                        with open("expenses.txt", "w") as file:
                            file.writelines(updated_lines)
                        top.destroy()
                        messagebox.showinfo("Edit Expense", "Expense updated successfully.")
                    else:
                        messagebox.showerror("Input Error", "Please enter a description and amount.")
                else:
                    messagebox.showerror("Selection Error", "Invalid selection.")
            else:
                messagebox.showerror("Selection Error", "No expense selected.")

        # Edit button
        edit_button = tk.Button(top, text="Edit Selected Expense", command=edit_expense)
        edit_button.pack(pady=10)

    def search_expenses(self):
        search_term = self.search_entry.get().lower()
        if search_term:
            try:
                with open("expenses.txt", "r") as file:
                    lines = file.readlines()

                filtered_expenses = [line.strip() for line in lines if search_term in line.lower()]
                if filtered_expenses:
                    self.show_expenses_for_search(filtered_expenses)
                else:
                    messagebox.showinfo("Search Results", "No expenses found matching the search term.")
            except FileNotFoundError:
                messagebox.showinfo("Search Results", "No expenses logged yet.")
        else:
            messagebox.showerror("Input Error", "Please enter a search term.")

    def show_expenses_for_search(self, expenses):
        top = tk.Toplevel(self.root)
        top.title("Search Results")

        expenses_list = tk.Listbox(top, width=80, height=20)
        expenses_list.pack(padx=10, pady=10)

        for expense in expenses:
            expenses_list.insert(tk.END, expense)

        # Optionally, add functionality for editing or deleting directly from search results
        # For example:
        # edit_button = tk.Button(top, text="Edit Selected Expense", command=self.edit_expense)
        # edit_button.pack(pady=10)

    def select_expense_for_update(self):
        search_term = self.update_search_entry.get().lower()
        if search_term:
            try:
                with open("expenses.txt", "r") as file:
                    lines = file.readlines()

                filtered_expenses = [line.strip() for line in lines if search_term in line.lower()]
                if filtered_expenses:
                    self.show_expenses_for_update(filtered_expenses)
                else:
                    messagebox.showinfo("Update Expense", "No expenses found matching the search term.")
            except FileNotFoundError:
                messagebox.showinfo("Update Expense", "No expenses logged yet.")
        else:
            messagebox.showerror("Input Error", "Please enter a search term.")

    def select_expense_for_delete(self):
        search_term = self.update_search_entry.get().lower()
        if search_term:
            try:
                with open("expenses.txt", "r") as file:
                    lines = file.readlines()

                filtered_expenses = [line.strip() for line in lines if search_term in line.lower()]
                if filtered_expenses:
                    self.show_expenses_for_delete(filtered_expenses)
                else:
                    messagebox.showinfo("Delete Expense", "No expenses found matching the search term.")
            except FileNotFoundError:
                messagebox.showinfo("Delete Expense", "No expenses logged yet.")
        else:
            messagebox.showerror("Input Error", "Please enter a search term.")

    def show_expenses_for_update(self, expenses):
        top = tk.Toplevel(self.root)
        top.title("Select Expense to Update")

        expenses_list = tk.Listbox(top, width=80, height=20)
        expenses_list.pack(padx=10, pady=10)

        for expense in expenses:
            expenses_list.insert(tk.END, expense)

        def update_expense():
            selected_index = expenses_list.curselection()
            if selected_index:
                selected_line = expenses_list.get(selected_index).strip()
                parts = selected_line.split('|')
                if len(parts) == 3:
                    date_str, description, amount = parts
                    new_description = simpledialog.askstring("Update Expense", "Enter new description:", initialvalue=description.strip())
                    new_amount = simpledialog.askstring("Update Expense", "Enter new amount ($):", initialvalue=amount.strip().replace('$', ''))
                    if new_description and new_amount:
                        updated_lines = []
                        with open("expenses.txt", "r") as file:
                            lines = file.readlines()
                            for line in lines:
                                if selected_line in line:
                                    updated_line = f"{date_str} | {new_description} | ${new_amount}\n"
                                    updated_lines.append(updated_line)
                                else:
                                    updated_lines.append(line)
                        with open("expenses.txt", "w") as file:
                            file.writelines(updated_lines)
                        top.destroy()
                        messagebox.showinfo("Update Expense", "Expense updated successfully.")
                    else:
                        messagebox.showerror("Input Error", "Please enter a description and amount.")
                else:
                    messagebox.showerror("Selection Error", "Invalid selection.")
            else:
                messagebox.showerror("Selection Error", "No expense selected.")

        # Update button
        update_button = tk.Button(top, text="Update Selected Expense", command=update_expense)
        update_button.pack(pady=10)

    def show_expenses_for_delete(self, expenses):
        top = tk.Toplevel(self.root)
        top.title("Select Expense to Delete")

        expenses_list = tk.Listbox(top, width=80, height=20)
        expenses_list.pack(padx=10, pady=10)

        for expense in expenses:
            expenses_list.insert(tk.END, expense)

        def delete_expense():
            selected_index = expenses_list.curselection()
            if selected_index:
                selected_line = expenses_list.get(selected_index).strip()
                updated_lines = []
                with open("expenses.txt", "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        if selected_line not in line:
                            updated_lines.append(line)
                with open("expenses.txt", "w") as file:
                    file.writelines(updated_lines)
                top.destroy()
                messagebox.showinfo("Delete Expense", "Expense deleted successfully.")
            else:
                messagebox.showerror("Selection Error", "No expense selected.")

        # Delete button
        delete_button = tk.Button(top, text="Delete Selected Expense", command=delete_expense)
        delete_button.pack(pady=10)


    def visualize_expenses(self):
        try:
            expenses = {}
            with open("expenses.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        description = parts[1].strip()
                        amount = float(parts[2].replace('$', '').strip())
                        if description in expenses:
                            expenses[description] += amount
                        else:
                            expenses[description] = amount

            if expenses:
                labels = list(expenses.keys())
                sizes = list(expenses.values())
                plt.figure(figsize=(10, 6))
                plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
                plt.title('Expense Distribution')
                plt.show()
            else:
                messagebox.showinfo("Visualization", "No expenses to visualize.")
        except FileNotFoundError:
            messagebox.showinfo("Visualization", "No expenses logged yet.")
        except Exception as e:
            messagebox.showerror("Visualization Error", str(e))



if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
