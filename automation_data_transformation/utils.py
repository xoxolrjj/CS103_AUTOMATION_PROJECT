import tkinter as tk
from tkinter import Label, Toplevel, simpledialog
from tkinter import ttk
from tkinter import filedialog

def select_from_dropdown(title, message, options):
    """Helper to let the user select an option from a dropdown menu."""
    selected_value = None
    top = tk.Toplevel()
    top.title(title)

    tk.Label(top, text=message, font=("Arial", 12)).pack(pady=10)

    # Dropdown for options
    selected_option = tk.StringVar(top)
    selected_option.set("Select an option")  # Default value

    dropdown = tk.OptionMenu(top, selected_option, *options)
    dropdown.pack(pady=10)

    # Confirm button to finalize selection
    def confirm_selection():
        nonlocal selected_value
        selected_value = selected_option.get()
        top.destroy()

    tk.Button(top, text="Confirm", width=15, command=confirm_selection).pack(pady=5)
    top.wait_window()
    return selected_value

def single_select_from_dropdown( title, message, options):
    """Creates a single-selection dropdown dialog and returns the selected item."""
    import tkinter as tk
    from tkinter import simpledialog

    class SingleSelectDialog(simpledialog.Dialog):
        def __init__(self, parent, title, message, options):
            self.options = options
            self.selected_item = None
            super().__init__(parent, title)

        def body(self, master):
            tk.Label(master, text=message).grid(row=0, column=0, columnspan=2, sticky='w')
            self.var = tk.StringVar(value=options[0])
            self.dropdown = tk.OptionMenu(master, self.var, *options)
            self.dropdown.grid(row=1, column=0, columnspan=2)
            return self.dropdown

        def apply(self):
            self.selected_item = self.var.get()

    dialog = SingleSelectDialog(None, title, message, options)
    return dialog.selected_item

def multi_select_from_dropdown( title, message, options):

    class MultiSelectDialog(simpledialog.Dialog):
        def __init__(self, parent, title, message, options):
            self.options = options
            self.selected_items = []
            super().__init__(parent, title)

        def body(self, master):
            tk.Label(master, text=message).grid(row=0, column=0, columnspan=2, sticky='w')
            self.listbox = tk.Listbox(master, selectmode=tk.MULTIPLE, height=10, exportselection=0)
            for option in self.options:
                self.listbox.insert(tk.END, option)
            self.listbox.grid(row=1, column=0, columnspan=2)
            return self.listbox

        def apply(self):
            selections = self.listbox.curselection()
            self.selected_items = [self.options[i] for i in selections]

    dialog = MultiSelectDialog(None, title, message, options)
    return dialog.selected_items


def show_stats_table( stats):
        """Displays combined descriptive statistics, skewness, and kurtosis in a table."""
        # Create a new window
        window = Toplevel()
        window.title("Descriptive Statistics")

        # Add a label for the window
        Label(window, text="Descriptive Statistics", font=("Arial", 14, "bold")).pack(pady=10)

        # Create a Treeview widget
        tree = ttk.Treeview(window, columns=['Statistic'] + list(stats.columns), show="headings", height=15)
        tree.pack(fill="both", expand=True)

        # Define headings for the Treeview
        tree.heading('Statistic', text='Statistic')
        tree.column('Statistic', anchor="center", width=150)
        for col in stats.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)

        # Insert data into the Treeview
        for index, row in stats.iterrows():
            tree.insert("", "end", values=[index] + list(row.values))

        # Add vertical and horizontal scrollbars
        v_scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(window, orient="horizontal", command=tree.xview)
        tree.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Allow the window to resize
        window.geometry("800x400")
        window.mainloop()

#aggregation own save file
def save_to_file_dialog( title, default_filename):
    """Creates a save file dialog and returns the selected file path."""
    return filedialog.asksaveasfilename(title=title, defaultextension=".csv", initialfile=default_filename)

