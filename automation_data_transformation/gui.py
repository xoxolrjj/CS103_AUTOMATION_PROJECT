
import customtkinter as ctk
from data_operations import DataOperations


class DataTransformationApp:
    def __init__(self, root):
        self.root = root
        self.data_ops = DataOperations()
        self.setup_root()
        self.setup_header()
        self.setup_button_frame()
        self.setup_footer()

    def setup_root(self):
        """Configure the main window."""
        self.root.title("Data Transformation Toolkit")
        self.root.geometry("850x700")
        self.root.configure(bg="#f0f4f8")  # Light subtle background color
        self.root.resizable(False, False)

    def setup_header(self): 
        """Set up the header section."""
        header_frame = ctk.CTkFrame(self.root, fg_color="#ffffff", corner_radius=15)
        header_frame.pack(pady=10, padx=10, fill="x")

        # Title Label
        title_label = ctk.CTkLabel(
            header_frame,
            text="DATA TRANSFORMATION TOOLKIT",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#007ACC"
        )
        title_label.pack(pady=15)

        # Separator
        separator = ctk.CTkFrame(header_frame, height=2, fg_color="#E0E0E0")
        separator.pack(fill="x", pady=10)

    def setup_button_frame(self):
        """Create a frame for the buttons."""
        button_frame = ctk.CTkFrame(self.root, fg_color="#ffffff", corner_radius=15)
        button_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Instruction Label
        instruction_label = ctk.CTkLabel(
            button_frame,
            text="Choose an operation to get started:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        instruction_label.grid(row=0, column=0, columnspan=2, pady=15)

        # Buttons
        self.create_button(button_frame, "Upload Your File", self.data_ops.upload_file, row=1, column=0, color="#4CAF50")
        self.create_button(button_frame, "Data Deduplication", self.data_ops.data_deduplication, row=2, column=0)
        self.create_button(button_frame, "Data Cleansing", self.data_ops.data_cleansing, row=3, column=0)
        self.create_button(button_frame, "Format Revisioning", self.data_ops.format_revisioning, row=4, column=0)
        self.create_button(button_frame, "Merging / Joining", self.data_ops.data_merging,row=5, column=0)
        self.create_button(button_frame, "Data Derivation", self.data_ops.data_derivation, row=2, column=1)
        self.create_button(button_frame, "Data Aggregation", self.data_ops.data_aggregation, row=3, column=1)
        self.create_button(button_frame, "Descriptive Statistics", self.data_ops.descriptive_statistics, row=4, column=1)
        self.create_button(button_frame, "Data Visualization", self.data_ops.data_visualization, row=5, column=1)

        self.create_button(button_frame, "Preview Dataset", self.data_ops.preview_dataset, row=1, column=1, color="#FF9800")
        self.create_button(button_frame, "Save Data", self.data_ops.save_data, row=6, column=1, color="#FF5722")

    def create_button(self, frame, text, command, row, column, color="#007ACC"):
        """Helper to create styled buttons and place them in a grid layout."""
        button = ctk.CTkButton(
            frame,
            text=text,
            command=command,
            width=300,
            height=50,
            corner_radius=8,
            fg_color=color,
            hover_color="#005EA6",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        button.grid(row=row, column=column, pady=10, padx=10, sticky="nsew")

        # Ensure buttons expand nicely
        frame.grid_rowconfigure(row, weight=1)
        frame.grid_columnconfigure(column, weight=1)

    def setup_footer(self):
        """Set up the footer section."""
        footer_frame = ctk.CTkFrame(self.root, fg_color="#f0f4f8")
        footer_frame.pack(fill="x", pady=10)

        footer_label = ctk.CTkLabel(
            footer_frame,
            text="",
            font=ctk.CTkFont(size=12, weight="normal"),
            text_color="#6C757D"
        )
        footer_label.pack(pady=10)
