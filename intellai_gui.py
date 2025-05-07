import tkinter as tk
from tkinter import ttk
import threading

from utils.db_utils import filter_entries, reset_db
from intellai_single import SingleModel
from intellai_hybrid import HybridModel

class intellai_gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IntellAI Cam Manager")
        self.geometry("1000x900")
        self.create_widgets()

        self.terminate_flag = False

        # Initialize model objects
        self.single_model = SingleModel()
        self.hybrid_model = HybridModel()

        self.current_thread = None

    def create_widgets(self):
        # FRAME: Models
        control_frame = ttk.LabelFrame(self, text="Model Controls")
        control_frame.pack(side="top", fill="x", padx=10, pady=5)

        single_button = ttk.Button(control_frame, text="Run Single Model", command=self.run_single_model)
        single_button.pack(side="left", padx=5)
        hybrid_button = ttk.Button(control_frame, text="Run Hybrid Model", command=self.run_hybrid_model)
        hybrid_button.pack(side="left", padx=5)
        stop_button = ttk.Button(control_frame, text="Stop Model", command=self.terminate_model)
        stop_button.pack(side="left", padx=5)

        # FRAME: Analysis Section (holds current + previous side-by-side)
        analysis_section_frame = ttk.Frame(self)
        analysis_section_frame.pack(fill="x", padx=10, pady=5)

        # INNER FRAME: Current Analysis Info
        current_frame = ttk.LabelFrame(analysis_section_frame, text="Current Analysis Info")
        current_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.analysis_info_label = ttk.Label(current_frame, text="Waiting for analysis...")
        self.analysis_info_label.pack(padx=5, pady=5, fill="both", expand=True)
        self.analysis_info_label.configure(anchor="center", justify="left")

        # INNER FRAME: Previous Analysis Info
        previous_frame = ttk.LabelFrame(analysis_section_frame, text="Previous Analysis Info")
        previous_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))
        self.previous_analysis_label = ttk.Label(previous_frame, text="No previous analysis.")
        self.previous_analysis_label.pack(padx=5, pady=5, fill="both", expand=True)
        self.previous_analysis_label.configure(anchor="center", justify="left")

        # FRAME: Manager Info
        manager_info_frame = ttk.LabelFrame(self, text="Manager Info")
        manager_info_frame.pack(side="top", fill="x", padx=10, pady=5)
        self.manager_info_label = ttk.Label(manager_info_frame, text="Waiting for query...")
        self.manager_info_label.pack(padx=5, pady=5, fill="x")
        self.manager_info_label.configure(anchor="center", justify="center")

        # # FRAME: Database Viewer
        db_frame = ttk.LabelFrame(self, text="Database Viewer")
        db_frame.pack(side="top", fill="both", expand=True, padx=10, pady=5)

        # INNER FRAME: Database Filters
        filter_frame = ttk.Frame(db_frame)
        filter_frame.pack(anchor="w", fill="x", padx=5, pady=(0, 10))

        # DB Gender filter
        ttk.Label(filter_frame, text="Gender:").pack(side="left")
        self.gender_var = tk.StringVar(value="All")
        gender_filter = ttk.Combobox(filter_frame, textvariable=self.gender_var, values=["All", "Man", "Woman"], state="readonly", width=10)
        gender_filter.pack(side="left", padx=(0, 10))

        # DB Age filter
        ttk.Label(filter_frame, text="Min Age:").pack(side="left")
        self.min_age_var = tk.StringVar()
        min_age_entry = ttk.Entry(filter_frame, textvariable=self.min_age_var, width=5)
        min_age_entry.pack(side="left", padx=(0, 5))

        ttk.Label(filter_frame, text="Max Age:").pack(side="left")
        self.max_age_var = tk.StringVar()
        max_age_entry = ttk.Entry(filter_frame, textvariable=self.max_age_var, width=5)
        max_age_entry.pack(side="left", padx=(0, 10))

        # DB Race filter
        ttk.Label(filter_frame, text="Race:").pack(side="left")
        self.race_var = tk.StringVar(value="All")
        race_filter = ttk.Combobox(filter_frame, textvariable=self.race_var, values=["All", "white", "black", "asian", "latino hispanic", "middle eastern", "indian"], state="readonly", width=18)
        race_filter.pack(side="left", padx=(0, 10))

        # Apply DB filter button
        ttk.Button(filter_frame, text="Apply Filter", command=self.load_db_entries).pack(side="left")

        # Reset DB button
        ttk.Button(filter_frame, text="Reset DB", command=self.reset_db).pack(side="right")

        # Refresh DB button
        ttk.Button(filter_frame, text="Refresh DB", command=self.load_db_entries).pack(side="right")

        # Show database table
        self.db_table = ttk.Treeview(db_frame, columns=("ID", "Age", "Gender", "Race", "Timestamp"), show="headings")
        for col in self.db_table["columns"]:
            self.db_table.heading(col, text=col, command=lambda _col=col: self.sort_by_column(_col, False))
            if col == "ID":
                self.db_table.column(col, width=15, anchor="center")
            else:
                self.db_table.column(col, anchor="center")
        self.db_table.pack(fill="both", expand=True, padx=5, pady=5)

    # DEF: Sorts database viewer by column
    def sort_by_column(self, col, descending):
        data = [(self.db_table.set(child, col), child) for child in self.db_table.get_children()]

        try:
            data.sort(key=lambda t: float(t[0]), reverse=descending)
        except ValueError:
            data.sort(reverse=descending)

        for index, (_, child) in enumerate(data):
            self.db_table.move(child, '', index)

        self.db_table.heading(col, command=lambda: self.sort_by_column(col, not descending))

    # DEF: Resets the database
    # Uses db_utils function to delete the database file and reload entries
    def reset_db(self):
        reset_db()
        self.load_db_entries()
        self.update_manager_info("Database reset.")

    # DEF: Loads database entries into the table
    # Uses db_utils functions, gets all entries or filtered entries
    def load_db_entries(self):
        for row in self.db_table.get_children():
            self.db_table.delete(row)

        gender = self.gender_var.get()
        race = self.race_var.get()
        min_age = self.min_age_var.get()
        max_age = self.max_age_var.get()

        try:
            min_age_val = int(min_age) if min_age else None
        except ValueError:
            min_age_val = None

        try:
            max_age_val = int(max_age) if max_age else None
        except ValueError:
            max_age_val = None

        rows = filter_entries(
            gender=gender,
            race=race,
            min_age=min_age_val,
            max_age=max_age_val
        )

        for row in rows:
            self.db_table.insert("", "end", values=row)

        if min_age_val is None:
            min_age = "None"
        if max_age_val is None:
            max_age = "None"

        self.update_manager_info(f"""
            Showing {len(rows)} entries 
            \nFilter: [Gender = {gender}]  [Race = {race}]  [Min Age = {min_age}]  [Max Age = {max_age}]
        """)

    # DEF: Specifies Single Model to the threading function
    def run_single_model(self):
        self.update_previous_analysis()

        # Terminate existing model thread
        self.terminate_model()

        threading.Thread(target=self.run_model_thread, args=("single",), daemon=True).start()

    # DEF: Specifies Hybrid Model to the threading function
    def run_hybrid_model(self):
        self.update_previous_analysis()

        # Terminate existing model thread
        self.terminate_model()

        threading.Thread(target=self.run_model_thread, args=("hybrid",), daemon=True).start()


    def terminate_model(self):
        print("called gui terminate")
        print("Terminating model thread...")
        self.single_model.terminate()
        self.hybrid_model.terminate()
        print("Model thread terminated.")

    # DEF: Runs specified analysis model in a separate thread
    def run_model_thread(self, model_type):
        # Indicate the model is running
        self.update_analysis_info("Processing... Please wait.")

        try:
            if model_type == "single":
                result = self.single_model.run_model(update_callback=self.update_analysis_info)
            elif model_type == "hybrid":
                result = self.hybrid_model.run_model(update_callback=self.update_analysis_info)
            else:
                self.update_analysis_info("Unknown Model Type")
                result = "Unknown Model Type"
        except Exception as e:
            self.update_analysis_info(f"Error: {str(e)}")

    # DEF: Updates analysis info label
    def update_analysis_info(self, message):
        self.after(0, lambda: self.analysis_info_label.config(text=message))
    
    # DEF: Updates manager info label
    def update_manager_info(self, message):
        self.after(0, lambda: self.manager_info_label.config(text=message))

    def update_previous_analysis(self):
        current_analysis = self.analysis_info_label.cget("text")
        self.after(0, lambda: self.previous_analysis_label.config(text=current_analysis))

if __name__ == "__main__":
    app = intellai_gui()
    app.mainloop()
