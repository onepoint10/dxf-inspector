# DXF Auto - Laser CNC Manufacturing Analysis Tool

A professional Python tool for analyzing DXF files to extract metrics needed for laser CNC manufacturing price calculations. This tool provides comprehensive analysis similar to commercial DXF inspection applications.

## Features

### 🎯 Core Capabilities
- **Cutting Length Calculation**: Accurate measurement of total cutting path length across all entity types
- **Piercing Count**: Automatic detection of closed contours requiring laser piercing
- **Material Requirements**: Bounding box analysis to determine required material sheet size
- **Entity Analysis**: Detailed breakdown by entity type (LINE, CIRCLE, ARC, LWPOLYLINE, POLYLINE, SPLINE, ELLIPSE)
- **Layer Distribution**: Entity count by layer for multi-layer designs

### 📊 Manufacturing Metrics
The tool provides all essential data for calculating laser CNC pricing:
- Total cutting length (mm) - for machine time estimation
- Number of piercings - each pierce adds setup time
- Material dimensions - width, height, and area
- Entity complexity - count and distribution
- Layer organization - for multi-stage processing

### 🎨 Professional Output
- Color-coded console output for easy reading
- Structured report format
- Pricing calculation guidance
- Support for both metric and imperial units (via DXF settings)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. **Clone or download this repository**
```bash
cd /Users/onepoint/PycharmProjects/dxf-auto
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

Or install ezdxf directly:
```bash
pip install ezdxf
```

## Usage

### Basic Usage
```bash
# Run the Graphical User Interface (GUI)
python main.py --gui

# Run in Command Line Interface (CLI) mode
python main.py <path_to_dxf_file>
```

### Examples
```bash
# Launch the GUI
python main.py --gui

# Analyze a DXF file in CLI mode
python main.py drawing.dxf

# Analyze with full path
python main.py /path/to/your/file.dxf

# Disable colored output (for logging or older terminals)
python main.py drawing.dxf --no-color

# Show help
python main.py --help

# Show version
python main.py --version
```

## Output Example

```
DXF MANUFACTURING ANALYSIS REPORT
================================================================================

▶ FILE INFORMATION
  Filename: sample_part.dxf

▶ LASER CNC MANUFACTURING METRICS
  Total Cutting Length:  1245.67 mm
  Piercing Count:        12 (closed contours)
  Total Entities:        45

▶ MATERIAL REQUIREMENTS
  Bounding Box:
    Min Point: (0.00, 0.00)
    Max Point: (150.00, 200.00)
  Required Material Size:
    Width:  150.00 mm
    Height: 200.00 mm
    Area:   0.0300 m²

▶ ENTITY BREAKDOWN
  Entity Type          Count      Total Length (mm)    Avg Length (mm)     
  ----------------------------------------------------------------------
  LINE                 25         450.23               18.01               
  CIRCLE               8          402.12               50.27               
  ARC                  10         298.45               29.85               
  LWPOLYLINE           2          94.87                47.44               

▶ LAYER DISTRIBUTION
  Layer Name                     Entity Count   
  ---------------------------------------------
  0                              30             
  CutLayer                       12             
  Engraving                      3              

▶ PRICING CALCULATION FACTORS
  Machine Time Factors:
    • Cutting time: 1245.67 mm ÷ cutting speed (mm/min)
    • Piercing time: 12 piercings × time per pierce (sec)
    • Positioning time: Based on entity distribution

  Material Cost:
    • Sheet size required: 150 × 200 mm
    • Material area: 0.0300 m²

  Complexity Factors:
    • Number of entities: 45
    • Number of layers: 3
```

## Supported Entity Types

The tool accurately calculates lengths for:

| Entity Type | Description | Length Calculation |
|------------|-------------|-------------------|
| LINE | Straight line segment | Euclidean distance |
| CIRCLE | Complete circle | Circumference (2πr) |
| ARC | Circular arc | Arc length (r × θ) |
| LWPOLYLINE | Lightweight polyline | Sum of segments including bulge arcs |
| POLYLINE | Standard polyline | Sum of all vertex-to-vertex segments |
| SPLINE | B-spline curve | Approximation via flattening |
| ELLIPSE | Elliptical arc or full ellipse | Ramanujan's approximation or flattening |
| POINT | Point marker | 0 (no cutting length) |

## Architecture

The project follows professional software engineering practices:

```
dxf-auto/
├── main.py                 # CLI entry point
├── dxf_analyzer.py         # Core DXF analysis engine
├── entity_calculator.py    # Entity-specific length calculations
├── metrics.py              # Data models for analysis results
├── formatter.py            # Console output formatting
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Module Overview

- **main.py**: Command-line interface, argument parsing, file validation
- **dxf_analyzer.py**: Loads DXF files, coordinates analysis, calculates bounding boxes
- **entity_calculator.py**: Implements length calculation algorithms for each entity type
- **metrics.py**: Data classes for storing and organizing analysis results
- **formatter.py**: Formats metrics into professional console output with color support

## Technical Details

### Calculation Methods

1. **Line Length**: Standard 3D Euclidean distance
2. **Circle**: Full circumference using 2πr
3. **Arc**: Arc length formula r × θ (with angle normalization)
4. **Polyline with Bulge**: Converts bulge values to arc geometry
5. **Spline**: Flattening algorithm with 0.01mm tolerance
6. **Ellipse**: Ramanujan's approximation for full ellipse, flattening for partial

### Piercing Detection

Closed contours are detected for:
- CIRCLE entities (always closed)
- Full ELLIPSE entities (2π parameter range)
- LWPOLYLINE with closed flag
- POLYLINE with closed flag

### Bounding Box

Uses ezdxf's optimized bbox module for accurate extent calculation across all entity types.

## Use Cases

### Manufacturing Cost Estimation
- Calculate machine time based on cutting length
- Estimate piercing time from contour count
- Determine material requirements and waste

### Production Planning
- Assess job complexity
- Optimize sheet nesting
- Plan multi-layer processing

### Quality Control
- Verify design dimensions
- Check for missing entities
- Validate layer organization

## Dependencies

- **ezdxf** (≥1.3.0): Professional DXF library for Python
  - Reading DXF files (R12 through R2018+)
  - Entity query and manipulation
  - Geometric calculations
  - Bounding box computation

## Troubleshooting

### "Import ezdxf could not be resolved"
Install the ezdxf library:
```bash
pip install ezdxf
```

### "Not a DXF file or corrupted"
- Ensure the file is a valid DXF format
- Try opening in a CAD application first
- Check file permissions

### "No entities found"
- Verify entities are in modelspace (not paperspace)
- Check that layers are not frozen or off
- Ensure the file contains supported entity types

### Incorrect measurements
- Check drawing units in the DXF file
- Verify scale factors
- Ensure entities are not in blocks (INSERT entities)

## Limitations

- INSERT (block reference) entities are not expanded
- HATCH, TEXT, MTEXT, DIMENSION entities are skipped (not cutting paths)
- LEADER entities are not processed
- Very complex SPLINE entities may have approximation errors

## Future Enhancements

Potential features for future versions:
- [ ] Block reference expansion
- [ ] Export to CSV/JSON
- [ ] Multiple file batch processing
- [ ] Custom unit conversion
- [ ] PDF report generation
- [ ] Integration with pricing databases
- [ ] Web interface
- [ ] CAM file generation hints

## Version History

### v1.0.0 (Current)
- Initial release
- Support for all major entity types
- Comprehensive manufacturing metrics
- Professional console output
- Error handling and validation

## License

This project is provided as-is for educational and commercial use.

## Author

Expert Software Architect & Developer

## Acknowledgments

- Built with [ezdxf](https://ezdxf.readthedocs.io/) - Professional Python DXF library
- Inspired by commercial DXF inspection tools
- Designed for laser CNC manufacturing industry

## Support

For issues, questions, or contributions, please refer to the project repository.

---

**Note**: This tool provides analysis for manufacturing estimation. Always verify measurements with your CAD software and consult with your laser cutting service provider for accurate pricing.
