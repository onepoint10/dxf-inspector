"""Core DXF analyzer for processing DXF files and extracting metrics."""
import sys
from pathlib import Path
from typing import Optional
import ezdxf
from ezdxf import bbox

from metrics import DXFMetrics
from entity_calculator import EntityCalculator


class DXFAnalyzer:
    """Analyze DXF files and extract manufacturing metrics."""
    
    def __init__(self, filepath: str):
        """
        Initialize the DXF analyzer.
        
        Args:
            filepath: Path to the DXF file to analyze
        """
        self.filepath = Path(filepath)
        self.doc: Optional[ezdxf.document.Drawing] = None
        self.metrics: Optional[DXFMetrics] = None
        self.calculator = EntityCalculator()
    
    def load(self) -> bool:
        """
        Load the DXF file.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            self.doc = ezdxf.readfile(str(self.filepath))
            return True
        except IOError:
            print(f"Error: Could not read file '{self.filepath}'")
            print("Please check that the file exists and is accessible.")
            return False
        except ezdxf.DXFStructureError:
            print(f"Error: '{self.filepath}' is not a valid DXF file or is corrupted.")
            return False
        except Exception as e:
            print(f"Error: Unexpected error loading file: {e}")
            return False
    
    def analyze(self) -> Optional[DXFMetrics]:
        """
        Analyze the loaded DXF file and extract metrics.
        
        Returns:
            DXFMetrics object containing analysis results, or None if analysis fails
        """
        if self.doc is None:
            print("Error: No DXF file loaded. Call load() first.")
            return None
        
        try:
            # Initialize metrics
            self.metrics = DXFMetrics(filename=self.filepath.name)
            
            # Get modelspace
            msp = self.doc.modelspace()
            
            # Analyze each entity
            for entity in msp:
                self._analyze_entity(entity)
            
            # Calculate bounding box
            self._calculate_bounding_box(msp)
            
            return self.metrics
            
        except Exception as e:
            print(f"Error during analysis: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _analyze_entity(self, entity):
        """Analyze a single entity and update metrics."""
        entity_type = entity.dxftype()
        
        # Skip unsupported entity types
        if entity_type in ['DIMENSION', 'TEXT', 'MTEXT', 'INSERT', 'HATCH', 'LEADER']:
            return
        
        # Calculate entity length
        length = self.calculator.calculate_entity_length(entity)
        
        if length is not None and length > 0:
            # Get layer name
            layer = entity.dxf.get('layer', '0')
            
            # Add to metrics
            self.metrics.add_entity(entity_type, length, layer)
            
            # Check if entity is closed (for piercing count)
            if self.calculator.is_closed_entity(entity):
                self.metrics.piercing_count += 1
    
    def _calculate_bounding_box(self, msp):
        """Calculate the bounding box of all entities in modelspace."""
        try:
            # Use ezdxf's bbox module for accurate bounding box calculation
            extents = bbox.extents(msp, fast=True)
            
            if extents.has_data:
                min_point = (extents.extmin.x, extents.extmin.y)
                max_point = (extents.extmax.x, extents.extmax.y)
                self.metrics.set_bounding_box(min_point, max_point)
            else:
                # No valid bounding box
                self.metrics.set_bounding_box((0.0, 0.0), (0.0, 0.0))
                
        except Exception as e:
            print(f"Warning: Could not calculate bounding box: {e}")
            self.metrics.set_bounding_box((0.0, 0.0), (0.0, 0.0))
    
    def get_document_info(self) -> dict:
        """
        Get general information about the DXF document.
        
        Returns:
            Dictionary with document information
        """
        if self.doc is None:
            return {}
        
        info = {
            'dxf_version': self.doc.dxfversion,
            'filename': self.filepath.name,
            'file_size_kb': self.filepath.stat().st_size / 1024 if self.filepath.exists() else 0,
        }
        
        # Add header variables if available
        try:
            info['units'] = self.doc.header.get('$INSUNITS', 0)
            info['measurement'] = self.doc.header.get('$MEASUREMENT', 0)  # 0=English, 1=Metric
        except:
            pass
        
        return info
