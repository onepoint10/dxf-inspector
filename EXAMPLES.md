# Examples and Use Cases

## Sample Analysis Outputs

### Example 1: Simple Bracket
```bash
$ python main.py bracket.dxf
```

**Analysis Results:**
- Total Cutting Length: 450.50 mm
- Piercing Count: 8 (4 mounting holes + 4 corners)
- Material Size: 150 × 100 mm
- Estimated Time: ~15 minutes

**Use Case:** Standard sheet metal bracket with mounting holes

---

### Example 2: Gear Component (Included Sample)
```bash
$ python main.py complex_gear.dxf
```

**Analysis Results:**
- Total Cutting Length: 965.39 mm
- Piercing Count: 19 (multiple circular features)
- Material Size: 100 × 100 mm
- Estimated Time: ~30 minutes

**Use Case:** Mechanical gear with decorative elements

---

## Pricing Calculation Example

Let's calculate the cost for a typical laser cutting job:

### Given Parameters:
- Cutting Length: 1000 mm
- Piercing Count: 10
- Material: 3mm Steel, 200×200mm sheet
- Machine Speed: 2000 mm/min (2m/min)
- Pierce Time: 2 seconds each
- Material Cost: $5 per 200×200mm sheet
- Machine Rate: $60/hour

### Calculation:

1. **Cutting Time:**
   - 1000 mm ÷ 2000 mm/min = 0.5 minutes

2. **Piercing Time:**
   - 10 piercings × 2 sec = 20 seconds = 0.33 minutes

3. **Total Machine Time:**
   - 0.5 + 0.33 + 2 min setup = **2.83 minutes** (~$3)

4. **Material Cost:**
   - 1 sheet required = **$5**

5. **Total Estimated Cost:**
   - Machine: $3
   - Material: $5
   - **Total: $8** (before markup)

---

## Command Line Examples

### Basic Analysis
```bash
# Analyze a local file
python main.py drawing.dxf

# Analyze with full path
python main.py /Users/username/Documents/part.dxf
```

### Output Control
```bash
# Disable colors (for logging)
python main.py drawing.dxf --no-color

# Redirect output to file
python main.py drawing.dxf > analysis_report.txt

# Save without colors
python main.py drawing.dxf --no-color > report.txt
```

### Batch Processing (Shell Script)
```bash
#!/bin/bash
# Analyze all DXF files in a directory

for file in *.dxf; do
    echo "Analyzing $file..."
    python main.py "$file" --no-color > "${file%.dxf}_analysis.txt"
done
```

---

## Integration Examples

### Python Script Integration
```python
from dxf_analyzer import DXFAnalyzer
from formatter import ConsoleFormatter

# Analyze a file programmatically
analyzer = DXFAnalyzer('part.dxf')
if analyzer.load():
    metrics = analyzer.analyze()
    if metrics:
        print(f"Cutting length: {metrics.total_cutting_length:.2f} mm")
        print(f"Piercings: {metrics.piercing_count}")
        print(f"Material: {metrics.material_width:.1f} × {metrics.material_height:.1f} mm")
```

### Automated Quoting System
```python
from dxf_analyzer import DXFAnalyzer

def estimate_price(dxf_file, material_type='steel', thickness=3):
    """Generate a price quote from a DXF file."""
    analyzer = DXFAnalyzer(dxf_file)
    
    if not analyzer.load():
        return None
    
    metrics = analyzer.analyze()
    if not metrics:
        return None
    
    # Calculate costs
    cutting_time = metrics.total_cutting_length / 2000  # minutes
    piercing_time = metrics.piercing_count * 2 / 60     # minutes
    total_time = cutting_time + piercing_time + 2       # +2 min setup
    
    machine_cost = total_time * (60 / 60)  # $60/hour
    material_cost = calculate_material_cost(
        metrics.material_width,
        metrics.material_height,
        material_type,
        thickness
    )
    
    return {
        'cutting_length': metrics.total_cutting_length,
        'time_minutes': total_time,
        'machine_cost': machine_cost,
        'material_cost': material_cost,
        'total_cost': machine_cost + material_cost
    }
```

---

## Common Scenarios

### Scenario 1: Prototype Part
- **Quantity:** 1 piece
- **Urgency:** High
- **Analysis Focus:** Material size, complexity
- **Typical Markup:** 2-3x

### Scenario 2: Production Run
- **Quantity:** 100+ pieces
- **Urgency:** Normal
- **Analysis Focus:** Cutting length optimization, nesting
- **Typical Markup:** 1.2-1.5x

### Scenario 3: Complex Assembly
- **Quantity:** Multiple parts
- **Urgency:** Varies
- **Analysis Focus:** Total cutting time, material utilization
- **Typical Markup:** Varies by part

---

## Tips for Best Results

### 1. File Preparation
- Ensure all cutting paths are on appropriate layers
- Remove construction lines and annotations
- Verify units (mm vs inches)
- Check for duplicate entities

### 2. Optimization
- Nest multiple parts to save material
- Group similar thickness materials
- Consider grain direction for anisotropic materials

### 3. Accuracy
- Use the tool for estimation only
- Verify critical dimensions in CAD software
- Account for kerf width in tight tolerances
- Consider post-processing time (deburring, finishing)

---

## Creating Test Files

You can create test DXF files using the included scripts:

```bash
# Simple part
python create_sample.py

# Complex gear
python create_complex_sample.py
```

Or create your own using any CAD software (AutoCAD, QCAD, LibreCAD, etc.)

---

## Troubleshooting Examples

### Issue: "No entities found"
```bash
# Check if entities are in modelspace
python -c "
import ezdxf
doc = ezdxf.readfile('file.dxf')
print(f'Modelspace entities: {len(list(doc.modelspace()))}')
print(f'Paperspace entities: {len(list(doc.paperspace()))}')
"
```

### Issue: Wrong measurements
```bash
# Check drawing units
python -c "
import ezdxf
doc = ezdxf.readfile('file.dxf')
print(f'Units: {doc.header.get(\"$INSUNITS\", \"Unknown\")}')
print(f'Measurement: {doc.header.get(\"$MEASUREMENT\", \"Unknown\")}')
"
```

---

## Advanced Usage

### Custom Analysis
Extend the tool for specific needs:

```python
from dxf_analyzer import DXFAnalyzer
from entity_calculator import EntityCalculator

class CustomAnalyzer(DXFAnalyzer):
    def analyze_by_layer(self, layer_name):
        """Analyze only entities on a specific layer."""
        msp = self.doc.modelspace()
        entities = msp.query(f'*[layer=="{layer_name}"]')
        
        total_length = 0
        for entity in entities:
            length = self.calculator.calculate_entity_length(entity)
            if length:
                total_length += length
        
        return total_length
```

---

## Performance Tips

For large files:
1. Use `--no-color` to reduce processing overhead
2. Disable unnecessary layers before export
3. Simplify complex splines (reduce control points)
4. Remove unused blocks and definitions

---

## Support and Documentation

- Full Documentation: See README.md
- Quick Start: See QUICKSTART.md
- Library Documentation: https://ezdxf.readthedocs.io/
- Report Issues: Contact your administrator
