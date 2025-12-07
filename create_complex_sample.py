"""
Create a more complex sample DXF for demonstration.
This creates a gear-like part with multiple features.
"""
import ezdxf
import math

# Create a new DXF document
doc = ezdxf.new('R2010', setup=True)
msp = doc.modelspace()

# Add layers
cut_layer = doc.layers.new('Outer')
cut_layer.dxf.color = 1
holes_layer = doc.layers.new('Holes')
holes_layer.dxf.color = 3
engrave_layer = doc.layers.new('Engraving')
engrave_layer.dxf.color = 5

# Create outer circle
outer_radius = 50
msp.add_circle((0, 0), radius=outer_radius, dxfattribs={'layer': 'Outer'})

# Create center hole
center_hole_radius = 10
msp.add_circle((0, 0), radius=center_hole_radius, dxfattribs={'layer': 'Holes'})

# Create gear teeth (small circles around perimeter)
num_teeth = 12
tooth_radius = 5
for i in range(num_teeth):
    angle = (2 * math.pi * i) / num_teeth
    x = (outer_radius - tooth_radius) * math.cos(angle)
    y = (outer_radius - tooth_radius) * math.sin(angle)
    msp.add_circle((x, y), radius=tooth_radius, dxfattribs={'layer': 'Holes'})

# Create mounting holes
mounting_hole_radius = 4
mounting_circle_radius = 30
num_mounting_holes = 4
for i in range(num_mounting_holes):
    angle = (2 * math.pi * i) / num_mounting_holes + math.pi/4
    x = mounting_circle_radius * math.cos(angle)
    y = mounting_circle_radius * math.sin(angle)
    msp.add_circle((x, y), radius=mounting_hole_radius, dxfattribs={'layer': 'Holes'})

# Create keyway slot (polyline)
keyway_width = 3
keyway_depth = 5
keyway_points = [
    (-keyway_width/2, center_hole_radius),
    (keyway_width/2, center_hole_radius),
    (keyway_width/2, center_hole_radius + keyway_depth),
    (-keyway_width/2, center_hole_radius + keyway_depth)
]
msp.add_lwpolyline(keyway_points, close=True, dxfattribs={'layer': 'Outer'})

# Add decorative splines for engraving
control_points = [(-15, 0), (-10, 5), (0, 7), (10, 5), (15, 0)]
msp.add_spline(control_points, dxfattribs={'layer': 'Engraving'})
control_points2 = [(-15, -2), (-10, -7), (0, -9), (10, -7), (15, -2)]
msp.add_spline(control_points2, dxfattribs={'layer': 'Engraving'})

# Add arcs for decorative elements
msp.add_arc((0, 20), radius=8, start_angle=45, end_angle=135, dxfattribs={'layer': 'Engraving'})
msp.add_arc((0, -20), radius=8, start_angle=225, end_angle=315, dxfattribs={'layer': 'Engraving'})

# Save the file
doc.saveas('complex_gear.dxf')
print("Complex gear DXF file created: complex_gear.dxf")
print(f"\nThis file contains:")
print(f"  - 1 outer circle (radius {outer_radius}mm)")
print(f"  - {num_teeth} gear teeth")
print(f"  - {num_mounting_holes} mounting holes")
print(f"  - 1 center hole and keyway slot")
print(f"  - Decorative engraving elements")
print("\nTo analyze this file, run:")
print("python main.py complex_gear.dxf")
