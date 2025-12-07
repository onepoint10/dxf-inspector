"""
Example script to create a sample DXF file for testing.
This creates a simple part with various entity types.
"""
import ezdxf

# Create a new DXF document
doc = ezdxf.new('R2010', setup=True)
msp = doc.modelspace()

# Add a layer for cutting
cut_layer = doc.layers.new('CutLayer')
cut_layer.dxf.color = 1
engrave_layer = doc.layers.new('Engraving')
engrave_layer.dxf.color = 3

# Create a rectangular outline (using lines)
msp.add_line((0, 0), (100, 0), dxfattribs={'layer': 'CutLayer'})
msp.add_line((100, 0), (100, 150), dxfattribs={'layer': 'CutLayer'})
msp.add_line((100, 150), (0, 150), dxfattribs={'layer': 'CutLayer'})
msp.add_line((0, 150), (0, 0), dxfattribs={'layer': 'CutLayer'})

# Add some circles (mounting holes)
msp.add_circle((20, 20), radius=5, dxfattribs={'layer': 'CutLayer'})
msp.add_circle((80, 20), radius=5, dxfattribs={'layer': 'CutLayer'})
msp.add_circle((20, 130), radius=5, dxfattribs={'layer': 'CutLayer'})
msp.add_circle((80, 130), radius=5, dxfattribs={'layer': 'CutLayer'})

# Add an arc
msp.add_arc((50, 75), radius=30, start_angle=0, end_angle=180, dxfattribs={'layer': 'CutLayer'})

# Add a polyline (slot)
points = [(40, 100), (60, 100), (60, 110), (40, 110)]
msp.add_lwpolyline(points, close=True, dxfattribs={'layer': 'CutLayer'})

# Add an ellipse for engraving
msp.add_ellipse(
    (50, 40), 
    major_axis=(15, 0, 0), 
    ratio=0.5,
    dxfattribs={'layer': 'Engraving'}
)

# Add text (will be skipped in analysis)
msp.add_text(
    'SAMPLE PART',
    dxfattribs={
        'layer': 'Engraving',
        'height': 5,
        'insert': (30, 60)
    }
)

# Save the file
doc.saveas('sample_part.dxf')
print("Sample DXF file created: sample_part.dxf")
print("\nTo analyze this file, run:")
print("python main.py sample_part.dxf")
