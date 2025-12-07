"""
Graphical User Interface for DXF Auto.
Built with tkinter and ttk for a native look and feel.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
from typing import Optional

from dxf_analyzer import DXFAnalyzer
from metrics import DXFMetrics
from formatter import ConsoleFormatter


class DXFApp:
    """Main GUI Application class."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("DXF Auto - Manufacturing Analyzer")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Data
        self.current_file: Optional[str] = None
        self.analyzer: Optional[DXFAnalyzer] = None
        self.metrics: Optional[DXFMetrics] = None
        
        # Threading communication
        self.queue = queue.Queue()
        
        # UI Setup
        self._setup_styles()
        self._build_ui()
        
        # Start queue checker
        self.root.after(100, self._check_queue)

    def _setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')  # 'clam' usually looks cleaner than 'default' on cross-platform
        
        # Configure headings and labels
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), foreground="#333")
        style.configure("Subtitle.TLabel", font=("Helvetica", 12, "bold"), foreground="#555")
        style.configure("Metric.TLabel", font=("Helvetica", 10))
        style.configure("Value.TLabel", font=("Helvetica", 10, "bold"), foreground="#0055aa")
        
        # Treeview style
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        style.configure("Treeview", rowheight=25)

    def _build_ui(self):
        """Construct the user interface."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- Header Section ---
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="DXF Manufacturing Analyzer", style="Title.TLabel")
        title_label.pack(side=tk.LEFT)
        
        # --- File Selection Section ---
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=60, state='readonly')
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(file_frame, text="Browse...", command=self._select_file)
        browse_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.analyze_btn = ttk.Button(file_frame, text="Analyze DXF", command=self._start_analysis, state=tk.DISABLED)
        self.analyze_btn.pack(side=tk.LEFT)
        
        # --- Dashboard Section (Metrics) ---
        dashboard_frame = ttk.LabelFrame(main_frame, text="Manufacturing Metrics", padding="15")
        dashboard_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Grid layout for metrics
        # Row 0: Headers
        ttk.Label(dashboard_frame, text="Cutting Length", style="Subtitle.TLabel").grid(row=0, column=0, padx=20, pady=5, sticky="w")
        ttk.Label(dashboard_frame, text="Piercings", style="Subtitle.TLabel").grid(row=0, column=1, padx=20, pady=5, sticky="w")
        ttk.Label(dashboard_frame, text="Material Size", style="Subtitle.TLabel").grid(row=0, column=2, padx=20, pady=5, sticky="w")
        
        # Row 1: Values
        self.length_var = tk.StringVar(value="-")
        self.piercing_var = tk.StringVar(value="-")
        self.material_var = tk.StringVar(value="-")
        
        ttk.Label(dashboard_frame, textvariable=self.length_var, style="Value.TLabel").grid(row=1, column=0, padx=20, pady=5, sticky="w")
        ttk.Label(dashboard_frame, textvariable=self.piercing_var, style="Value.TLabel").grid(row=1, column=1, padx=20, pady=5, sticky="w")
        ttk.Label(dashboard_frame, textvariable=self.material_var, style="Value.TLabel").grid(row=1, column=2, padx=20, pady=5, sticky="w")
        
        # Row 2: Extra info
        self.area_var = tk.StringVar(value="")
        ttk.Label(dashboard_frame, textvariable=self.area_var, style="Metric.TLabel").grid(row=2, column=2, padx=20, pady=0, sticky="w")

        # --- Details Section (Tabs) ---
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Entity Breakdown
        self.entity_tree = self._create_treeview(
            self.notebook, 
            columns=("type", "count", "total_len", "avg_len"),
            headers=("Entity Type", "Count", "Total Length (mm)", "Avg Length (mm)")
        )
        self.notebook.add(self.entity_tree.master, text="Entity Breakdown")
        
        # Tab 2: Layer Distribution
        self.layer_tree = self._create_treeview(
            self.notebook,
            columns=("layer", "count"),
            headers=("Layer Name", "Entity Count")
        )
        self.notebook.add(self.layer_tree.master, text="Layer Distribution")
        
        # Tab 3: Full Report
        report_frame = ttk.Frame(self.notebook)
        self.report_text = tk.Text(report_frame, wrap=tk.WORD, font=("Courier New", 10))
        scrollbar = ttk.Scrollbar(report_frame, orient="vertical", command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scrollbar.set)
        
        self.report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.notebook.add(report_frame, text="Full Report")
        
        # --- Status Bar ---
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=(5, 2))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _create_treeview(self, parent, columns, headers):
        """Helper to create a configured Treeview."""
        frame = ttk.Frame(parent)
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Scrollbar
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure headers
        for col, header in zip(columns, headers):
            tree.heading(col, text=header)
            tree.column(col, width=100)
            
        return tree

    def _select_file(self):
        """Open file dialog."""
        filename = filedialog.askopenfilename(
            title="Select DXF File",
            filetypes=[("DXF Files", "*.dxf"), ("All Files", "*.*")]
        )
        if filename:
            self.current_file = filename
            self.file_path_var.set(filename)
            self.analyze_btn.config(state=tk.NORMAL)
            self.status_var.set("File selected. Ready to analyze.")
            # Auto-analyze for better UX? No, let user click.

    def _start_analysis(self):
        """Start analysis in a separate thread."""
        if not self.current_file:
            return
            
        self.analyze_btn.config(state=tk.DISABLED)
        self.status_var.set("Analyzing...")
        self.root.config(cursor="watch")
        
        # Clear previous results
        self._clear_results()
        
        # Run in thread
        thread = threading.Thread(target=self._perform_analysis)
        thread.daemon = True
        thread.start()

    def _perform_analysis(self):
        """Background analysis task."""
        try:
            analyzer = DXFAnalyzer(self.current_file)
            if not analyzer.load():
                self.queue.put(("error", "Failed to load DXF file."))
                return
                
            metrics = analyzer.analyze()
            if metrics:
                self.queue.put(("success", metrics))
            else:
                self.queue.put(("error", "Analysis failed."))
                
        except Exception as e:
            self.queue.put(("error", str(e)))

    def _check_queue(self):
        """Check for messages from background thread."""
        try:
            while True:
                msg_type, data = self.queue.get_nowait()
                
                if msg_type == "success":
                    self._update_ui(data)
                    self.status_var.set("Analysis complete.")
                elif msg_type == "error":
                    messagebox.showerror("Error", data)
                    self.status_var.set("Analysis failed.")
                
                # Reset UI state
                self.analyze_btn.config(state=tk.NORMAL)
                self.root.config(cursor="")
                
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self._check_queue)

    def _clear_results(self):
        """Clear all result widgets."""
        self.length_var.set("-")
        self.piercing_var.set("-")
        self.material_var.set("-")
        self.area_var.set("")
        
        for item in self.entity_tree.get_children():
            self.entity_tree.delete(item)
        for item in self.layer_tree.get_children():
            self.layer_tree.delete(item)
            
        self.report_text.delete(1.0, tk.END)

    def _update_ui(self, metrics: DXFMetrics):
        """Populate UI with analysis results."""
        self.metrics = metrics
        
        # 1. Dashboard Metrics
        self.length_var.set(f"{metrics.total_cutting_length:.2f} mm")
        self.piercing_var.set(f"{metrics.piercing_count}")
        self.material_var.set(f"{metrics.material_width:.1f} × {metrics.material_height:.1f} mm")
        area_m2 = (metrics.material_width * metrics.material_height) / 1_000_000
        self.area_var.set(f"Area: {area_m2:.4f} m²")
        
        # 2. Entity Tree
        if metrics.entity_breakdown:
            sorted_entities = sorted(
                metrics.entity_breakdown.items(),
                key=lambda x: x[1].count,
                reverse=True
            )
            for etype, emetrics in sorted_entities:
                avg = emetrics.total_length / emetrics.count if emetrics.count else 0
                self.entity_tree.insert("", tk.END, values=(
                    etype,
                    emetrics.count,
                    f"{emetrics.total_length:.2f}",
                    f"{avg:.2f}"
                ))
        
        # 3. Layer Tree
        if metrics.layers:
            sorted_layers = sorted(
                metrics.layers.items(),
                key=lambda x: x[1],
                reverse=True
            )
            for layer, count in sorted_layers:
                self.layer_tree.insert("", tk.END, values=(layer, count))
        
        # 4. Full Report
        # Generate report without color codes for the text widget
        report = ConsoleFormatter.format_metrics(metrics, use_color=False)
        self.report_text.insert(tk.END, report)


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = DXFApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
