import tkinter as tk
from tkinter import ttk
import threading
import time

from utils.db_utils import get_all_entries
from intellai_single import SingleModel  # Assuming this is the correct import path
from intellai_hybrid import HybridModel  # Assuming this is the correct import path

class intellai_gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IntellAI Cam Manager")
        self.geometry("1000x600")
        self.create_widgets()

        # Initialize model objects
        self.single_model = SingleModel()  # Make sure these classes are instantiated appropriately.
        self.hybrid_model = HybridModel()

    def create_widgets(self):
        # MODELS FRAME
        control_frame = ttk.LabelFrame(self, text="Model Controls")
        control_frame.pack(side="top", fill="x", padx=10, pady=5)

        single_button = ttk.Button(control_frame, text="Run Single Model", command=self.run_single_model)
        single_button.pack(side="left", padx=5)
        hybrid_button = ttk.Button(control_frame, text="Run Hybrid Model", command=self.run_hybrid_model)
        hybrid_button.pack(side="left", padx=5)

        # ANALYSIS OUTPUT FRAME
        info_frame = ttk.LabelFrame(self, text="Live Analysis Info")
        info_frame.pack(side="top", fill="x", padx=10, pady=5)
        self.info_label = ttk.Label(info_frame, text="Waiting for analysis...")
        self.info_label.pack(padx=5, pady=5)

        # DATABASE VIEWER FRAME
        db_frame = ttk.LabelFrame(self, text="Database Viewer")
        db_frame.pack(side="top", fill="both", expand=True, padx=10, pady=5)

        refresh_button = ttk.Button(db_frame, text="Refresh DB", command=self.load_db_entries)
        refresh_button.pack(anchor="ne", padx=5, pady=2)

        self.db_table = ttk.Treeview(db_frame, columns=("ID", "Age", "Gender", "Race", "Timestamp"), show="headings")
        for col in self.db_table["columns"]:
            self.db_table.heading(col, text=col, command=lambda _col=col: self.sort_by_column(_col, False))
            if col == "ID":
                self.db_table.column(col, width=15, anchor="center")
            else:
                self.db_table.column(col, anchor="center")
        self.db_table.pack(fill="both", expand=True, padx=5, pady=5)

    def sort_by_column(self, col, descending):
        # Grab all items and their values for the given column
        data = [(self.db_table.set(child, col), child) for child in self.db_table.get_children()]

        # Attempt to convert values to appropriate types for sorting
        try:
            data.sort(key=lambda t: float(t[0]), reverse=descending)
        except ValueError:
            data.sort(reverse=descending)

        # Rearrange items in sorted order
        for index, (_, child) in enumerate(data):
            self.db_table.move(child, '', index)

        # Toggle the sort order for next click
        self.db_table.heading(col, command=lambda: self.sort_by_column(col, not descending))

    def load_db_entries(self):
        # Clear existing rows
        for row in self.db_table.get_children():
            self.db_table.delete(row)

        # Fetch and insert rows
        rows = get_all_entries()
        for row in rows:
            self.db_table.insert("", "end", values=row)

        self.update_info(f"Loaded {len(rows)} entries from database.")

    def run_single_model(self):
        # Run the Single Model in a separate thread so the GUI remains responsive.
        threading.Thread(target=self.run_model_thread, args=("single",), daemon=True).start()

    def run_hybrid_model(self):
        # Run the Hybrid Model in a separate thread.
        threading.Thread(target=self.run_model_thread, args=("hybrid",), daemon=True).start()

    def run_model_thread(self, model_type):
        # Indicate the model is running
        self.update_info("Processing... Please wait.")

        try:
            if model_type == "single":
                result = self.single_model.run_model()
            elif model_type == "hybrid":
                result = self.hybrid_model.run_model()
            else:
                result = "Unknown Model Type"
            # Once the model completes, update the live info label with the result.
            self.update_info(f"Analysis Complete: {result}")
        except Exception as e:
            self.update_info(f"Error: {str(e)}")

    def update_info(self, message):
        # Since Tkinter updates must occur in the main thread, use the 'after' method
        self.after(0, lambda: self.info_label.config(text=message))

if __name__ == "__main__":
    app = intellai_gui()
    app.mainloop()
