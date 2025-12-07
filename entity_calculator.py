"""Entity calculator for computing lengths of various DXF entity types."""
import math
from typing import Optional
import ezdxf
from ezdxf.entities import (
    DXFGraphic, Line, Circle, Arc, LWPolyline, 
    Polyline, Spline, Ellipse, Point
)


class EntityCalculator:
    """Calculate lengths and properties of DXF entities."""
    
    @staticmethod
    def calculate_line_length(entity: Line) -> float:
        """Calculate length of a LINE entity."""
        start = entity.dxf.start
        end = entity.dxf.end
        return math.sqrt(
            (end[0] - start[0])**2 + 
            (end[1] - start[1])**2 + 
            (end[2] - start[2])**2
        )
    
    @staticmethod
    def calculate_circle_length(entity: Circle) -> float:
        """Calculate circumference of a CIRCLE entity."""
        radius = entity.dxf.radius
        return 2 * math.pi * radius
    
    @staticmethod
    def calculate_arc_length(entity: Arc) -> float:
        """Calculate length of an ARC entity."""
        radius = entity.dxf.radius
        start_angle = math.radians(entity.dxf.start_angle)
        end_angle = math.radians(entity.dxf.end_angle)
        
        # Handle angle wrapping
        angle_diff = end_angle - start_angle
        if angle_diff < 0:
            angle_diff += 2 * math.pi
        
        return radius * angle_diff
    
    @staticmethod
    def calculate_lwpolyline_length(entity: LWPolyline) -> float:
        """Calculate length of a lightweight POLYLINE entity."""
        total_length = 0.0
        points = list(entity.get_points('xyb'))  # x, y, bulge
        
        for i in range(len(points) - 1):
            x1, y1, bulge1 = points[i]
            x2, y2, bulge2 = points[i + 1]
            
            if abs(bulge1) < 1e-10:
                # Straight segment
                total_length += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            else:
                # Arc segment
                chord_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                if chord_length > 1e-10:
                    # Calculate arc length from bulge
                    angle = 4 * math.atan(abs(bulge1))
                    radius = chord_length / (2 * math.sin(angle / 2))
                    arc_length = radius * angle
                    total_length += arc_length
        
        # Handle closed polylines
        if entity.closed and len(points) > 1:
            x1, y1, bulge1 = points[-1]
            x2, y2, bulge2 = points[0]
            
            if abs(bulge1) < 1e-10:
                total_length += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            else:
                chord_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                if chord_length > 1e-10:
                    angle = 4 * math.atan(abs(bulge1))
                    radius = chord_length / (2 * math.sin(angle / 2))
                    arc_length = radius * angle
                    total_length += arc_length
        
        return total_length
    
    @staticmethod
    def calculate_polyline_length(entity: Polyline) -> float:
        """Calculate length of a POLYLINE entity."""
        total_length = 0.0
        vertices = list(entity.vertices)
        
        for i in range(len(vertices) - 1):
            v1 = vertices[i].dxf.location
            v2 = vertices[i + 1].dxf.location
            total_length += math.sqrt(
                (v2[0] - v1[0])**2 + 
                (v2[1] - v1[1])**2 + 
                (v2[2] - v1[2])**2
            )
        
        # Handle closed polylines
        if entity.is_closed and len(vertices) > 1:
            v1 = vertices[-1].dxf.location
            v2 = vertices[0].dxf.location
            total_length += math.sqrt(
                (v2[0] - v1[0])**2 + 
                (v2[1] - v1[1])**2 + 
                (v2[2] - v1[2])**2
            )
        
        return total_length
    
    @staticmethod
    def calculate_spline_length(entity: Spline) -> float:
        """Calculate approximate length of a SPLINE entity using flattening."""
        try:
            # Flatten the spline to a polyline approximation
            points = list(entity.flattening(0.01))  # 0.01 is the distance tolerance
            
            total_length = 0.0
            for i in range(len(points) - 1):
                p1 = points[i]
                p2 = points[i + 1]
                total_length += math.sqrt(
                    (p2[0] - p1[0])**2 + 
                    (p2[1] - p1[1])**2 + 
                    (p2[2] - p1[2])**2
                )
            
            return total_length
        except Exception:
            # If flattening fails, return 0
            return 0.0
    
    @staticmethod
    def calculate_ellipse_length(entity: Ellipse) -> float:
        """Calculate approximate length of an ELLIPSE entity."""
        try:
            # Get ellipse parameters
            center = entity.dxf.center
            major_axis = entity.dxf.major_axis
            ratio = entity.dxf.ratio  # minor_axis / major_axis
            start_param = entity.dxf.start_param
            end_param = entity.dxf.end_param
            
            # Calculate semi-major and semi-minor axes
            a = math.sqrt(major_axis[0]**2 + major_axis[1]**2 + major_axis[2]**2)
            b = a * ratio
            
            # For a full ellipse, use Ramanujan's approximation
            if abs(end_param - start_param) >= 2 * math.pi - 0.001:
                # Full ellipse
                h = ((a - b)**2) / ((a + b)**2)
                circumference = math.pi * (a + b) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))
                return circumference
            else:
                # Partial ellipse - use flattening
                points = list(entity.flattening(0.01))
                total_length = 0.0
                for i in range(len(points) - 1):
                    p1 = points[i]
                    p2 = points[i + 1]
                    total_length += math.sqrt(
                        (p2[0] - p1[0])**2 + 
                        (p2[1] - p1[1])**2 + 
                        (p2[2] - p1[2])**2
                    )
                return total_length
        except Exception:
            return 0.0
    
    @classmethod
    def calculate_entity_length(cls, entity: DXFGraphic) -> Optional[float]:
        """
        Calculate the length of any supported DXF entity.
        
        Args:
            entity: The DXF entity to measure
            
        Returns:
            The length of the entity, or None if the entity type is not supported
        """
        entity_type = entity.dxftype()
        
        try:
            if entity_type == 'LINE':
                return cls.calculate_line_length(entity)
            elif entity_type == 'CIRCLE':
                return cls.calculate_circle_length(entity)
            elif entity_type == 'ARC':
                return cls.calculate_arc_length(entity)
            elif entity_type == 'LWPOLYLINE':
                return cls.calculate_lwpolyline_length(entity)
            elif entity_type == 'POLYLINE':
                return cls.calculate_polyline_length(entity)
            elif entity_type == 'SPLINE':
                return cls.calculate_spline_length(entity)
            elif entity_type == 'ELLIPSE':
                return cls.calculate_ellipse_length(entity)
            elif entity_type == 'POINT':
                return 0.0  # Points have no length
            else:
                return None
        except Exception as e:
            print(f"Warning: Error calculating length for {entity_type}: {e}")
            return None
    
    @staticmethod
    def is_closed_entity(entity: DXFGraphic) -> bool:
        """Determine if an entity represents a closed contour (for piercing count)."""
        entity_type = entity.dxftype()
        
        if entity_type == 'CIRCLE':
            return True
        elif entity_type == 'ELLIPSE':
            # Check if it's a full ellipse
            start_param = entity.dxf.start_param
            end_param = entity.dxf.end_param
            return abs(end_param - start_param) >= 2 * math.pi - 0.001
        elif entity_type == 'LWPOLYLINE':
            return entity.closed
        elif entity_type == 'POLYLINE':
            return entity.is_closed
        
        return False
