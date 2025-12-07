#!/usr/bin/env python3
"""
DXF Auto - Laser CNC Manufacturing Analysis Tool

This tool analyzes DXF files and extracts metrics needed for calculating
laser CNC manufacturing prices, including cutting length, piercing count,
and material requirements.

Usage:
    python main.py <dxf_file_path>
    python main.py --help
"""

import sys
import argparse
from pathlib import Path

from dxf_analyzer import DXFAnalyzer
from formatter import ConsoleFormatter


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Analyze DXF files for laser CNC manufacturing pricing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py drawing.dxf
  python main.py /path/to/file.dxf
  python main.py drawing.dxf --no-color

This tool provides comprehensive analysis of DXF files including:
  - Total cutting length (for time estimation)
  - Piercing count (number of closed contours)
  - Material size requirements
  - Entity breakdown by type
  - Layer distribution
        """
    )
    
    parser.add_argument(
        'dxf_file',
        type=str,
        nargs='?',
        help='Path to the DXF file to analyze (optional if using --gui)'
    )
    
    parser.add_argument(
        '--gui',
        action='store_true',
        help='Launch the graphical user interface'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='DXF Auto v1.0.0'
    )
    
    return parser.parse_args()


def validate_file(filepath: str) -> bool:
    """
    Validate that the file exists and is a DXF file.
    
    Args:
        filepath: Path to the file to validate
        
    Returns:
        True if valid, False otherwise
    """
    path = Path(filepath)
    
    if not path.exists():
        print(ConsoleFormatter.format_error(f"File not found: {filepath}"))
        return False
    
    if not path.is_file():
        print(ConsoleFormatter.format_error(f"Path is not a file: {filepath}"))
        return False
    
    if path.suffix.lower() not in ['.dxf']:
        print(ConsoleFormatter.format_warning(
            f"File does not have .dxf extension: {path.suffix}\n"
            "Attempting to process anyway..."
        ))
    
    return True


def main():
    """Main entry point for the application."""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Launch GUI if requested
        if args.gui:
            import gui
            gui.main()
            return 0
            
        # Check if file is provided for CLI mode
        if not args.dxf_file:
            print(ConsoleFormatter.format_error("No DXF file specified."))
            print("Usage: python main.py <dxf_file> OR python main.py --gui")
            return 1
        
        # Validate file
        if not validate_file(args.dxf_file):
            return 1
        
        print(ConsoleFormatter.format_success(
            f"Loading DXF file: {args.dxf_file}"
        ))
        
        # Create analyzer
        analyzer = DXFAnalyzer(args.dxf_file)
        
        # Load DXF file
        if not analyzer.load():
            return 1
        
        print(ConsoleFormatter.format_success("File loaded successfully"))
        print("Analyzing entities...")
        
        # Analyze the file
        metrics = analyzer.analyze()
        
        if metrics is None:
            print(ConsoleFormatter.format_error(
                "Failed to analyze DXF file. Please check the file format."
            ))
            return 1
        
        # Display results
        use_color = not args.no_color
        output = ConsoleFormatter.format_metrics(metrics, use_color=use_color)
        print(output)
        
        # Display document info
        doc_info = analyzer.get_document_info()
        if doc_info:
            print(f"DXF Version: {doc_info.get('dxf_version', 'Unknown')}")
            print(f"File Size: {doc_info.get('file_size_kb', 0):.2f} KB")
            print()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 130
    except Exception as e:
        print(ConsoleFormatter.format_error(f"Unexpected error: {e}"))
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
