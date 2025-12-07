"""Data models for DXF analysis metrics."""
from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class EntityMetrics:
    """Metrics for a specific entity type."""
    count: int = 0
    total_length: float = 0.0
    
    def add(self, length: float):
        """Add an entity with its length."""
        self.count += 1
        self.total_length += length


@dataclass
class DXFMetrics:
    """Complete metrics for DXF analysis."""
    filename: str
    total_entities: int = 0
    total_cutting_length: float = 0.0
    piercing_count: int = 0
    entity_breakdown: Dict[str, EntityMetrics] = field(default_factory=dict)
    bounding_box: Tuple[Tuple[float, float], Tuple[float, float]] = ((0.0, 0.0), (0.0, 0.0))
    material_width: float = 0.0
    material_height: float = 0.0
    layers: Dict[str, int] = field(default_factory=dict)
    
    def add_entity(self, entity_type: str, length: float, layer: str = "0"):
        """Add an entity to the metrics."""
        self.total_entities += 1
        self.total_cutting_length += length
        
        # Track entity type
        if entity_type not in self.entity_breakdown:
            self.entity_breakdown[entity_type] = EntityMetrics()
        self.entity_breakdown[entity_type].add(length)
        
        # Track layer
        if layer not in self.layers:
            self.layers[layer] = 0
        self.layers[layer] += 1
    
    def set_bounding_box(self, min_point: Tuple[float, float], max_point: Tuple[float, float]):
        """Set the bounding box and calculate material dimensions."""
        self.bounding_box = (min_point, max_point)
        self.material_width = max_point[0] - min_point[0]
        self.material_height = max_point[1] - min_point[1]
