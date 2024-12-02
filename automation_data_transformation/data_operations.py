import seaborn as sns
import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from tkinter import messagebox
from tkinter import filedialog, messagebox, simpledialog, ttk
from utils import single_select_from_dropdown
from utils import multi_select_from_dropdown
from utils import show_stats_table
from utils import save_to_file_dialog
from utils import select_from_dropdown
 
class DataOperations:
    def __init__(self):
        self.data = None
        self.root = tk.Tk()

    def upload_file(self):
        """Handles file upload and loading of CSV data."""
        self.file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if self.file_path:
            try:
                self.data = pd.read_csv(self.file_path)
                messagebox.showinfo("Success", "File Uploaded Successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
        else:
            messagebox.showerror("Error", "No File Selected!")
        pass


    def data_deduplication(self, subset_columnss=None):
        """
        Enhanced Data Deduplication with preview, logging, and column information.

        :param subset_columns: List of column names to check for duplicates . 
                            If None, all columns are used.
        """
        if self.data is not None:
            try:
                # Determine the subset of columns for deduplication
                columns_used = subset_columnss if subset_columnss else self.data.columns.tolist()

                # Preview duplicate rows
                duplicate_rows = self.data[self.data.duplicated(subset=columns_used)]
                if not duplicate_rows.empty:
                    # Formatting the preview to show each duplicate row with column names and values
                    preview_message = "Preview of Duplicate Rows (with column details):\n"
                    for index, row in duplicate_rows.iterrows():
                        row_details = {col: row[col] for col in columns_used}
                        preview_message += f"\nRow {index + 1}: {row_details}"

                    # Show the preview in a message box
                    messagebox.showinfo(
                        "Preview Duplicates",
                        f"Columns Used for Deduplication: {', '.join(columns_used)}\n\n{preview_message}"
                    )

                # Perform deduplication
                original_count = len(self.data)
                self.data = self.data.drop_duplicates(subset=columns_used)
                deduplicated_count = len(self.data)

                # Log details
                messagebox.showinfo(
                    "Deduplication Results",
                    f"Columns Used for Deduplication: {', '.join(columns_used)}\n"
                    f"Duplicates Removed: {original_count - deduplicated_count}\n"
                    f"Remaining Rows: {deduplicated_count}"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Data Deduplication Failed: {str(e)}")
        else:
            messagebox.showerror("Error", "No Data Loaded!")

        pass

    def data_cleansing(self):
        """Enhanced Data Cleansing with custom strategies, validation, and logging."""
        if self.data is not None:
            try:
                # Initial missing values
                initial_missing = self.data.isnull().sum().sum()

                # Step 1: Standardize null values
                self.data.replace(
                    to_replace=[r'^\s*$', 'nan', 'Nan', 'NAn', 'NaN'],  # Customize as needed
                    value=np.nan,
                    regex=True,
                    inplace=True
                )
                standardized_missing = self.data.isnull().sum().sum()

                # Step 2: Drop completely empty columns (if enabled)
                empty_columns = self.data.columns[self.data.isnull().all()]
                if not empty_columns.empty:
                    drop_confirm = messagebox.askyesno(
                        "Drop Empty Columns",
                        f"Found empty columns: {list(empty_columns)}\n\n"
                        "Do you want to drop them?"
                    )
                    if drop_confirm:
                        self.data = self.data.dropna(axis=1, how='all')

                after_drop_columns_missing = self.data.isnull().sum().sum()

                # Step 3: Handle missing values for numeric columns
                numeric_cols = self.data.select_dtypes(include=['float64', 'int64']).columns
                for col in numeric_cols:
                    if self.data[col].isnull().sum() > 0:
                        fill_value = self.data[col].mean()  # Default to mean
                        self.data[col].fillna(fill_value, inplace=True)

                after_numeric_fill_missing = self.data.isnull().sum().sum()

                # Step 4: Handle missing values for categorical columns
                categorical_cols = self.data.select_dtypes(include=['object']).columns
                for col in categorical_cols:
                    if self.data[col].isnull().sum() > 0:
                        # Ask user for handling strategy
                        handling_choice = messagebox.askyesno(
                            "Handle Missing Categorical Values",
                            f"Column '{col}' has {self.data[col].isnull().sum()} missing values.\n\n"
                            "Choose Yes to fill with the most frequent value (mode).\n"
                            "Choose No to fill with 'Unknown'."
                        )
                        if handling_choice:  # Fill with mode
                            mode_value = self.data[col].mode()[0]  # Get the most frequent value
                            self.data[col].fillna(mode_value, inplace=True)
                        else:  # Fill with "Unknown"
                            self.data[col].fillna('Unknown', inplace=True)

                after_categorical_fill_missing = self.data.isnull().sum().sum()

                # Log each step
                cleansing_log = (
                    f"Initial Missing Values: {initial_missing}\n"
                    f"After Standardization: {standardized_missing}\n"
                    f"After Dropping Empty Columns: {after_drop_columns_missing}\n"
                    f"After Filling Numeric Columns: {after_numeric_fill_missing}\n"
                    f"After Filling Categorical Columns: {after_categorical_fill_missing}\n"
                )

                # Show log
                messagebox.showinfo("Data Cleansing Summary", cleansing_log)
            except Exception as e:
                messagebox.showerror("Error", f"Data Cleansing Failed: {str(e)}")
        else:
            messagebox.showerror("Error", "No Data Loaded!")
        pass

    def format_revisioning(self):
        """Automatic Format Revisioning: Detect and convert numeric columns to int or float."""
        if self.data is not None:
            try:
                # Step 1: Identify numeric columns
                numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
                if numeric_cols.empty:
                    messagebox.showinfo("No Numeric Columns", "No numeric columns to revise.")
                    return

                # Step 2: Process each numeric column
                revised_columns = []
                for col in numeric_cols:
                    try:
                        # Check if all values are whole numbers
                        if self.data[col].dropna().apply(lambda x: float(x).is_integer()).all():
                            # Convert to int if all values are integers
                            self.data[col] = self.data[col].astype(int)
                            revised_columns.append((col, 'int'))
                        else:
                            # Ensure column is float
                            self.data[col] = self.data[col].astype(float)
                            revised_columns.append((col, 'float'))
                    except Exception as col_error:
                        messagebox.showwarning(
                            "Conversion Warning",
                            f"Failed to revise column '{col}': {str(col_error)}"
                        )

                # Notify success
                if revised_columns:
                    summary = "\n".join([f"{col}: {dtype}" for col, dtype in revised_columns])
                    messagebox.showinfo(
                        "Format Revisioning Completed",
                        f"Revised columns:\n{summary}"
                    )
                else:
                    messagebox.showinfo("Format Revisioning", "No columns revised.")
            except Exception as e:
                messagebox.showerror("Error", f"Format Revisioning Failed: {str(e)}")
        else:
            messagebox.showerror("Error", "No Data Loaded!")
        pass

    def data_merging(self):
    
        if self.data is not None:
            try:
                # Load the second file for merging
                file_to_merge = filedialog.askopenfilename(
                    title="Select File to Merge",
                    filetypes=[("CSV Files", "*.csv")]
                )
                if not file_to_merge:
                    messagebox.showerror("Error", "No File Selected for Merging!")
                    return

                other_data = pd.read_csv(file_to_merge)

                # Dropdown for merging options
                merge_options = ["Inner Merge", "Outer Merge", "Left Merge", "Right Merge","Concatenate (Side by Side)"]
                merge_choice = select_from_dropdown(
                    "Merge Options",
                    "Choose the type of merging operation:",
                    merge_options
                )
                if not merge_choice:
                    return  # User clicked Back
                
                if merge_choice == "Concatenate (Side by Side)":
                    # Perform concatenation
                    self.data = pd.concat([self.data, other_data], axis=1)
                    messagebox.showinfo(
                        "Data Merging",
                        "Data concatenated successfully side by side!"
                    )            
                else:
                    # Select Inner or Outer merge
                    join_type = None
                    if merge_choice == "Inner Merge":
                        join_type = "inner"
                    elif merge_choice == "Outer Merge":
                        join_type = "outer"
                    elif merge_choice == "Right Merge":
                        join_type = "right"
                    elif merge_choice == "Left Merge":
                        join_type = "left"
                     # Perform the merge
                    merged_data = pd.merge(self.data, other_data, how=join_type)
                    self.data = merged_data

                    messagebox.showinfo(
                        "Data Merging",
                        f"Data merged successfully with {join_type.title()} join!"
                    )

            except Exception as e:
                messagebox.showerror("Error", f"Data Merging Failed: {str(e)}")
        else:
            messagebox.showerror("Error", "No Data Loaded!")
        pass

    def data_derivation(self):
        """Performs data derivation or custom aggregation based on user selection."""
        if self.data is not None:
            try:
                # Step 1: Select numeric columns for derivation
                numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
                if numeric_cols.empty:
                    messagebox.showerror("Error", "No numeric columns available for derivation.")
                    return

                # Step 2: Select derivation type
                derivation_type = select_from_dropdown(
                    "Select Derivation Type",
                    "Choose the type of derivation to perform:",
                    ["Binary Operation (Two Columns)", "Custom Aggregation (Single Column)"]
                )
                if not derivation_type:
                    return  # User clicked Back

                # If Binary Operation
                if derivation_type == "Binary Operation (Two Columns)":
                    column1 = select_from_dropdown(
                        "Select First Numeric Column",
                        "Choose the first numeric column for derivation:",
                        numeric_cols
                    )
                    if not column1:
                        return  # User clicked Back

                    column2 = select_from_dropdown(
                        "Select Second Numeric Column",
                        "Choose the second numeric column for derivation:",
                        numeric_cols
                    )
                    if not column2:
                        return  # User clicked Back

                    if column1 == column2:
                        messagebox.showerror("Error", "The two selected columns must be different.")
                        return

                    # Step 3: Define the operation for derivation
                    operations = ['+', '-', '*', '/', '%']  # Binary operations
                    derivation_operation = select_from_dropdown(
                        f"Define Operation for {column1} and {column2}",
                        "Choose a binary operation to apply:",
                        operations
                    )
                    if not derivation_operation:
                        return  # User clicked Back

                    # Perform the derivation
                    derived_column_name = f"Derived_{column1}_{derivation_operation}_{column2}"
                    try:
                        self.data[derived_column_name] = eval(
                            f"self.data[column1] {derivation_operation} self.data[column2]"
                        )
                        messagebox.showinfo(
                            "Data Derivation",
                            f"A new derived column '{derived_column_name}' has been added."
                        )
                    except ZeroDivisionError:
                        messagebox.showerror("Error", "Division by zero occurred during derivation.")
                    except Exception as e:
                        messagebox.showerror("Error", f"Invalid operation: {str(e)}")

                # If Custom Aggregation
                elif derivation_type == "Custom Aggregation (Single Column)":
                    column = select_from_dropdown(
                        "Select Numeric Column",
                        "Choose a numeric column to aggregate:",
                        numeric_cols
                    )
                    if not column:
                        return  # User clicked Back

                    # Step 4: Define custom aggregation
                    aggregation_type = select_from_dropdown(
                        f"Custom Aggregation for {column}",
                        "Choose a custom aggregation to apply:",
                        ["Sum and Divide by 2", "Operation with a Number", "Mean", "Count"]
                    )
                    if not aggregation_type:
                        return  # User clicked Back

                    try:
                        # Perform the chosen aggregation
                        if aggregation_type == "Sum and Divide by 2":
                            derived_column_name = f"Derived_{column}_SumDiv2"
                            self.data[derived_column_name] = self.data[column].sum() / 2

                        elif aggregation_type == "Operation with a Number":
                            # Select operation
                            operations = ['+', '-', '*', '/']  # Basic math operations
                            operation = select_from_dropdown(
                                "Select Operation",
                                f"Choose an operation to apply to {column}:",
                                operations
                            )
                            if not operation:
                                return  # User clicked Back

                            # Enter a number
                            number = simpledialog.askfloat(
                                "Input Number",
                                f"Enter the number to {operation} with {column}:"
                            )
                            if number is None:
                                return  # User clicked Back

                            # Apply operation
                            derived_column_name = f"Derived_{column}_{operation}{number}"
                            self.data[derived_column_name] = eval(f"self.data[column] {operation} number")

                        elif aggregation_type == "Mean":
                            derived_column_name = f"Derived_{column}_Mean"
                            self.data[derived_column_name] = self.data[column].mean()

                        elif aggregation_type == "Count":
                            derived_column_name = f"Derived_{column}_Count"
                            self.data[derived_column_name] = self.data[column].count()

                        # Notify user of success
                        messagebox.showinfo(
                            "Data Derivation",
                            f"A new derived column '{derived_column_name}' has been added."
                        )
                    except ZeroDivisionError:
                        messagebox.showerror("Error", "Division by zero occurred during derivation.")
                    except Exception as e:
                        messagebox.showerror("Error", f"Invalid operation: {str(e)}")

            except Exception as e:
                messagebox.showerror("Error", f"Data Derivation Failed: {str(e)}")
        else:
            messagebox.showerror("Error", "No Data Loaded!")
        pass

    def data_aggregation(self):
        """Automates data aggregation: extracting columns or grouping with aggregation metrics."""
        if self.data is not None:
            try:
                # Step 1: Choose operation type: extract column or group by
                operation_type = single_select_from_dropdown(
                    "Select Operation",
                    "Would you like to extract specific columns or perform a group-by operation?",
                    ["Extract Column", "Group By"]
                )
                if not operation_type:
                    messagebox.showwarning("Data Aggregation", "No operation selected.")
                    return

                # Option 1: Extract specific columns
                if operation_type == "Extract Column":
                    selected_columns = multi_select_from_dropdown(
                        "Select Columns to Extract",
                        "Choose one or more columns to extract:",
                        self.data.columns.tolist()
                    )
                    if not selected_columns:
                        messagebox.showwarning("Data Aggregation", "No columns selected.")
                        return

                    # Extract selected columns and save as a new dataset
                    extracted_data = self.data[selected_columns]
                    save_path = save_to_file_dialog("Save Extracted Data", "extracted_data.csv")
                    if save_path:
                        extracted_data.to_csv(save_path, index=False)
                        messagebox.showinfo("Data Extraction", "Columns extracted and saved successfully!")

                # Option 2: Group by and aggregate
                elif operation_type == "Group By":
                    # Step 2: Select columns for grouping
                    grouping_columns = multi_select_from_dropdown(
                        "Select Grouping Columns",
                        "Choose one or more columns to group by:",
                        self.data.columns.tolist()
                    )
                    if not grouping_columns:
                        messagebox.showwarning("Data Aggregation", "No grouping columns selected.")
                        return

                    # Step 3: Select numeric columns for aggregation
                    numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns.tolist()
                    if not numeric_cols:
                        messagebox.showerror("Error", "No numeric columns available for aggregation.")
                        return

                    selected_numeric_cols = multi_select_from_dropdown(
                        "Select Numeric Columns",
                        "Choose one or more numeric columns to aggregate:",
                        numeric_cols
                    )
                    if not selected_numeric_cols:
                        messagebox.showwarning("Data Aggregation", "No numeric columns selected.")
                        return

                    # Step 4: Select aggregation metrics for each numeric column
                    aggregation_selections = {}
                    for col in selected_numeric_cols:
                        metrics = multi_select_from_dropdown(
                            f"Select Aggregation Metrics for {col}",
                            f"Choose one or more metrics for {col}:",
                            ['mean', 'sum', 'count', 'max', 'min', 'median', 'std']
                        )
                        if metrics:
                            aggregation_selections[col] = metrics

                    if not aggregation_selections:
                        messagebox.showerror("Error", "No aggregation metrics selected.")
                        return

                    # Step 5: Perform aggregation
                    aggregated_data = self.data.groupby(grouping_columns).agg(aggregation_selections)

                    # Resetting column names to a cleaner format
                    aggregated_data.columns = ['_'.join(col).strip() for col in aggregated_data.columns.values]
                    aggregated_data = aggregated_data.reset_index()

                    # Save aggregated data
                    save_path = save_to_file_dialog("Save Aggregated Data", "aggregated_data.csv")
                    if save_path:
                        aggregated_data.to_csv(save_path, index=False)
                        messagebox.showinfo("Data Aggregation", "Data aggregated and saved successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Data Aggregation Failed: {str(e)}")
        else:
            messagebox.showerror("Error", "No Data Loaded!")
        pass
    

    def descriptive_statistics(self):
        """Enhanced Descriptive Statistics displayed in a table."""
        if self.data is not None:
            try:
                # Generate basic statistics
                stats = self.data.describe()

                # Calculate additional metrics
                skewness = self.data.skew(numeric_only=True)
                kurtosis = self.data.kurtosis(numeric_only=True)

                # Combine skewness and kurtosis with descriptive stats
                stats.loc['skewness'] = skewness
                stats.loc['kurtosis'] = kurtosis

                # Display the statistics in a table
                show_stats_table(stats)
            except Exception as e:
                messagebox.showerror("Error", f"Statistics Generation Failed: {str(e)}")
        else:
            messagebox.showerror("Error", "No Data Loaded!")
        pass   

    def data_visualization(self):
        """Allows the user to choose visualization type and columns using dropdowns."""
        if self.data is not None:
            try:
                # Step 1: Select Visualization Type
                vis_types = ["bar", "scatter", "histogram"]
                vis_type = select_from_dropdown(
                    "Select Visualization Type",
                    "Choose a visualization type:",
                    vis_types
                )
                if not vis_type:
                    return  # User clicked Back

                # Step 2: Select X-axis Column
                x_axis_column = select_from_dropdown(
                    "Select X-axis Column",
                    "Choose a column for the X-axis:",
                    self.data.columns
                )
                if not x_axis_column:
                    return  # User clicked Back

                # Step 3: Select Y-axis Column (optional for certain visualizations)
                y_axis_column = None
                if vis_type in ["bar", "scatter"]:
                    y_axis_column = select_from_dropdown(
                        "Select Y-axis Column",
                        "Choose a column for the Y-axis:",
                        self.data.columns
                    )
                    if not y_axis_column:
                        return  # User clicked Back

                # Step 4: Generate the Visualization
                plt.figure(figsize=(8, 6))
                if vis_type == "bar":
                    sns.barplot(x=self.data[x_axis_column], y=self.data[y_axis_column])
                elif vis_type == "scatter":
                    sns.scatterplot(x=self.data[x_axis_column], y=self.data[y_axis_column])
                elif vis_type == "histogram":
                    sns.histplot(self.data[x_axis_column])
                else:
                    messagebox.showerror("Error", "Invalid Visualization Type!")
                    return

                plt.title(f"{vis_type.capitalize()} Visualization")
                plt.show()

            except Exception as e:
                messagebox.showerror("Error", f"Data Visualization Failed: {str(e)}")
        else:
            messagebox.showerror("Error", "No Data Loaded!")
        pass

    def preview_dataset(self):
        """Preview the loaded dataset in a scrollable table."""
        if self.data is not None:
            preview_window = tk.Toplevel(self.root)
            preview_window.title("Dataset Preview")
            preview_window.geometry("850x500")
            preview_window.resizable(True, True)

            # Create a Frame to hold the Treeview and scrollbars
            frame = tk.Frame(preview_window)
            frame.pack(fill=tk.BOTH, expand=True)

            # Create a Treeview widget for displaying the dataset
            tree = ttk.Treeview(frame, columns=list(self.data.columns), show="headings")
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Add column headers
            for column in self.data.columns:
                tree.heading(column, text=column)
                tree.column(column, width=100, anchor="center")

            # Add rows to the Treeview
            for index, row in self.data.iterrows():
                tree.insert("", "end", values=row.tolist())

            # Add a vertical scrollbar
            v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.configure(yscrollcommand=v_scrollbar.set)

            # Add a horizontal scrollbar
            h_scrollbar = ttk.Scrollbar(preview_window, orient="horizontal", command=tree.xview)
            h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
            tree.configure(xscrollcommand=h_scrollbar.set)

        else:
            messagebox.showerror("Error", "No data loaded to preview!")
        pass

    def save_data(self):
        if self.data is not None:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv")]
            )
            if save_path:
                try:
                    self.data.to_csv(save_path, index=False)
                    messagebox.showinfo("Success", "Data Saved Successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {str(e)}")
        else:
            messagebox.showerror("Error", "No Data Loaded!")
        pass