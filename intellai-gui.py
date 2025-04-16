import tkinter as tk
from tkinter import ttk
import threading
import time

from intellai_single import SingleModel  # Assuming this is the correct import path
from intellai_hybrid import HybridModel  # Assuming this is the correct import path

class FaceAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Face Analysis Control Center")
        self.geometry("1000x600")
        self.create_widgets()

        # Model instances
        self.single_model = SingleModel()  # Make sure these classes are instantiated appropriately.
        self.hybrid_model = HybridModel()

    def create_widgets(self):
        # Frame for model controls
        control_frame = ttk.LabelFrame(self, text="Model Controls")
        control_frame.pack(side="top", fill="x", padx=10, pady=5)

        # Buttons for running models
        single_button = ttk.Button(control_frame, text="Run Single Model", command=self.run_single_model)
        single_button.pack(side="left", padx=5)
        hybrid_button = ttk.Button(control_frame, text="Run Hybrid Model", command=self.run_hybrid_model)
        hybrid_button.pack(side="left", padx=5)

        # Frame for live analysis output
        info_frame = ttk.LabelFrame(self, text="Live Analysis Info")
        info_frame.pack(side="top", fill="x", padx=10, pady=5)
        self.info_label = ttk.Label(info_frame, text="Waiting for analysis...")
        self.info_label.pack(padx=5, pady=5)

        # Frame for database browsing (for now, it's just a placeholder table)
        db_frame = ttk.LabelFrame(self, text="Database Viewer")
        db_frame.pack(side="top", fill="both", expand=True, padx=10, pady=5)
        self.db_table = ttk.Treeview(db_frame, columns=("ID", "Age", "Gender", "Timestamp"), show="headings")
        for col in self.db_table["columns"]:
            self.db_table.heading(col, text=col)
        self.db_table.pack(fill="both", expand=True, padx=5, pady=5)

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
    app = FaceAnalysisApp()
    app.mainloop()
