"""Formatter for displaying DXF analysis results in the console."""
from typing import Dict
from metrics import DXFMetrics, EntityMetrics


class ConsoleFormatter:
    """Format and display DXF analysis results."""
    
    # ANSI color codes for terminal output
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @classmethod
    def format_metrics(cls, metrics: DXFMetrics, use_color: bool = True) -> str:
        """
        Format metrics for console output.
        
        Args:
            metrics: The DXFMetrics to format
            use_color: Whether to use ANSI color codes
            
        Returns:
            Formatted string ready for console output
        """
        if not use_color:
            cls.HEADER = cls.BLUE = cls.CYAN = cls.GREEN = cls.YELLOW = cls.RED = ''
            cls.BOLD = cls.UNDERLINE = cls.END = ''
        
        lines = []
        
        # Header
        lines.append("")
        lines.append(cls._format_header("DXF MANUFACTURING ANALYSIS REPORT"))
        lines.append(cls._format_separator("="))
        
        # File information
        lines.append(cls._format_section("FILE INFORMATION"))
        lines.append(f"  Filename: {cls.CYAN}{metrics.filename}{cls.END}")
        lines.append("")
        
        # Key metrics for laser CNC pricing
        lines.append(cls._format_section("LASER CNC MANUFACTURING METRICS"))
        lines.append(f"  Total Cutting Length:  {cls.GREEN}{cls.BOLD}{metrics.total_cutting_length:.2f} mm{cls.END}")
        lines.append(f"  Piercing Count:        {cls.GREEN}{cls.BOLD}{metrics.piercing_count}{cls.END} (closed contours)")
        lines.append(f"  Total Entities:        {cls.YELLOW}{metrics.total_entities}{cls.END}")
        lines.append("")
        
        # Material requirements
        lines.append(cls._format_section("MATERIAL REQUIREMENTS"))
        lines.append(f"  Bounding Box:")
        lines.append(f"    Min Point: ({metrics.bounding_box[0][0]:.2f}, {metrics.bounding_box[0][1]:.2f})")
        lines.append(f"    Max Point: ({metrics.bounding_box[1][0]:.2f}, {metrics.bounding_box[1][1]:.2f})")
        lines.append(f"  Required Material Size:")
        lines.append(f"    Width:  {cls.CYAN}{metrics.material_width:.2f} mm{cls.END}")
        lines.append(f"    Height: {cls.CYAN}{metrics.material_height:.2f} mm{cls.END}")
        lines.append(f"    Area:   {cls.CYAN}{(metrics.material_width * metrics.material_height / 1000000):.4f} m²{cls.END}")
        lines.append("")
        
        # Entity breakdown
        if metrics.entity_breakdown:
            lines.append(cls._format_section("ENTITY BREAKDOWN"))
            lines.append(f"  {'Entity Type':<20} {'Count':<10} {'Total Length (mm)':<20} {'Avg Length (mm)':<20}")
            lines.append(f"  {'-' * 70}")
            
            # Sort by count (descending)
            sorted_entities = sorted(
                metrics.entity_breakdown.items(),
                key=lambda x: x[1].count,
                reverse=True
            )
            
            for entity_type, entity_metrics in sorted_entities:
                avg_length = entity_metrics.total_length / entity_metrics.count if entity_metrics.count > 0 else 0
                lines.append(
                    f"  {entity_type:<20} "
                    f"{cls.YELLOW}{entity_metrics.count:<10}{cls.END} "
                    f"{entity_metrics.total_length:<20.2f} "
                    f"{avg_length:<20.2f}"
                )
            lines.append("")
        
        # Layer information
        if metrics.layers:
            lines.append(cls._format_section("LAYER DISTRIBUTION"))
            lines.append(f"  {'Layer Name':<30} {'Entity Count':<15}")
            lines.append(f"  {'-' * 45}")
            
            # Sort by entity count (descending)
            sorted_layers = sorted(
                metrics.layers.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            for layer_name, count in sorted_layers:
                lines.append(f"  {layer_name:<30} {cls.YELLOW}{count:<15}{cls.END}")
            lines.append("")
        
        # Cost estimation notes
        lines.append(cls._format_section("PRICING CALCULATION FACTORS"))
        lines.append(f"  {cls.BOLD}Machine Time Factors:{cls.END}")
        lines.append(f"    • Cutting time: {cls.GREEN}{metrics.total_cutting_length:.2f} mm{cls.END} ÷ cutting speed (mm/min)")
        lines.append(f"    • Piercing time: {cls.GREEN}{metrics.piercing_count}{cls.END} piercings × time per pierce (sec)")
        lines.append(f"    • Positioning time: Based on entity distribution")
        lines.append("")
        lines.append(f"  {cls.BOLD}Material Cost:{cls.END}")
        lines.append(f"    • Sheet size required: {cls.CYAN}{metrics.material_width:.0f} × {metrics.material_height:.0f} mm{cls.END}")
        lines.append(f"    • Material area: {cls.CYAN}{(metrics.material_width * metrics.material_height / 1000000):.4f} m²{cls.END}")
        lines.append("")
        lines.append(f"  {cls.BOLD}Complexity Factors:{cls.END}")
        lines.append(f"    • Number of entities: {metrics.total_entities}")
        lines.append(f"    • Number of layers: {len(metrics.layers)}")
        lines.append("")
        
        # Footer
        lines.append(cls._format_separator("="))
        lines.append("")
        
        return "\n".join(lines)
    
    @classmethod
    def _format_header(cls, text: str) -> str:
        """Format a header line."""
        return f"{cls.BOLD}{cls.HEADER}{text}{cls.END}"
    
    @classmethod
    def _format_section(cls, text: str) -> str:
        """Format a section header."""
        return f"{cls.BOLD}{cls.BLUE}▶ {text}{cls.END}"
    
    @classmethod
    def _format_separator(cls, char: str = "-") -> str:
        """Format a separator line."""
        return char * 80
    
    @staticmethod
    def format_error(message: str) -> str:
        """Format an error message."""
        return f"\n❌ ERROR: {message}\n"
    
    @staticmethod
    def format_warning(message: str) -> str:
        """Format a warning message."""
        return f"\n⚠️  WARNING: {message}\n"
    
    @staticmethod
    def format_success(message: str) -> str:
        """Format a success message."""
        return f"\n✅ {message}\n"
