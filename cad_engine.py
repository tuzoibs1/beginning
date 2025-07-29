import os
import sys
import uuid
import subprocess
import tempfile
from typing import Dict, Any
import json

class CADEngine:
    def __init__(self):
        """Initialize the CAD Engine"""
        self.models_dir = "models"
        self.exports_dir = "exports"
        
        # Ensure directories exist
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.exports_dir, exist_ok=True)
        
        # Check if FreeCAD is available
        self.freecad_available = self._check_freecad()
        
    def _check_freecad(self) -> bool:
        """Check if FreeCAD is available in the system"""
        try:
            # Try to import FreeCAD
            result = subprocess.run(['python3', '-c', 'import FreeCAD'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def generate_model(self, design_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a 3D model based on design parameters
        
        Args:
            design_params: Dictionary containing design specifications
            
        Returns:
            Dictionary containing model generation results
        """
        try:
            # Generate unique ID for this model
            model_id = str(uuid.uuid4())
            
            # Generate FreeCAD script
            cad_script = self._generate_freecad_script(design_params)
            
            # Save script
            script_path = os.path.join(self.models_dir, f"{model_id}.py")
            with open(script_path, 'w') as f:
                f.write(cad_script)
            
            # Execute script and generate model
            if self.freecad_available:
                model_path, preview_image = self._execute_freecad_script(script_path, model_id)
            else:
                # Fallback: create dummy files for demonstration
                model_path, preview_image = self._create_dummy_model(model_id)
            
            # Generate description
            from chatbot import ChatBot
            chatbot = ChatBot()
            description = chatbot.generate_response_message(design_params)
            
            return {
                'success': True,
                'model_id': model_id,
                'model_path': model_path,
                'preview_image': preview_image,
                'cad_code': cad_script,
                'description': description,
                'design_params': design_params
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'description': f"Failed to generate model: {str(e)}"
            }
    
    def _generate_freecad_script(self, params: Dict[str, Any]) -> str:
        """Generate FreeCAD Python script based on design parameters"""
        
        object_type = params.get('object_type', 'glasses')
        
        if object_type == 'glasses':
            return self._generate_glasses_script(params)
        else:
            # Default to glasses for now
            return self._generate_glasses_script(params)
    
    def _generate_glasses_script(self, params: Dict[str, Any]) -> str:
        """Generate FreeCAD script for glasses"""
        
        # Extract parameters with defaults
        lens_diameter = params.get('lens_diameter', 50)
        lens_shape = params.get('lens_shape', 'round')
        frame_width = params.get('frame_width', 140)
        bridge_width = params.get('bridge_width', 18)
        temple_length = params.get('temple_length', 140)
        rim_thickness = params.get('rim_thickness', 2)
        
        script = f'''
import FreeCAD as App
import Part
import Draft

# Create new document
doc = App.newDocument("Glasses")

# Parameters
lens_diameter = {lens_diameter}
lens_shape = "{lens_shape}"
frame_width = {frame_width}
bridge_width = {bridge_width}
temple_length = {temple_length}
rim_thickness = {rim_thickness}

def create_lens(x_offset=0):
    """Create a lens shape"""
    if lens_shape == "round":
        # Create circular lens
        lens = Part.makeCylinder(lens_diameter/2, rim_thickness, 
                               App.Vector(x_offset, 0, 0), 
                               App.Vector(0, 0, 1))
        # Create inner hole (lens opening)
        inner_hole = Part.makeCylinder(lens_diameter/2 - rim_thickness, rim_thickness + 1,
                                     App.Vector(x_offset, 0, -0.5),
                                     App.Vector(0, 0, 1))
        lens = lens.cut(inner_hole)
    else:
        # Create rectangular lens
        lens_width = lens_diameter * 0.8
        lens_height = lens_diameter * 0.6
        
        # Outer rectangle
        outer = Part.makeBox(lens_width, lens_height, rim_thickness,
                           App.Vector(x_offset - lens_width/2, -lens_height/2, 0))
        # Inner rectangle (lens opening)
        inner = Part.makeBox(lens_width - 2*rim_thickness, 
                           lens_height - 2*rim_thickness, 
                           rim_thickness + 1,
                           App.Vector(x_offset - (lens_width - 2*rim_thickness)/2, 
                                    -(lens_height - 2*rim_thickness)/2, -0.5))
        lens = outer.cut(inner)
    
    return lens

def create_bridge():
    """Create bridge connecting the lenses"""
    bridge_height = rim_thickness
    bridge = Part.makeBox(bridge_width, bridge_height, rim_thickness,
                         App.Vector(-bridge_width/2, -bridge_height/2, 0))
    return bridge

def create_temple(side="left"):
    """Create temple arm"""
    temple_thickness = rim_thickness
    temple_height = rim_thickness * 2
    
    if side == "left":
        start_x = -frame_width/2 - lens_diameter/2
    else:
        start_x = frame_width/2 + lens_diameter/2
    
    # Main temple arm
    temple = Part.makeBox(temple_length, temple_height, temple_thickness,
                         App.Vector(start_x, 0, 0))
    
    # Curved end for ear
    if temple_length > 100:
        curve_radius = 20
        curve_center = App.Vector(start_x + temple_length - curve_radius, 
                                temple_height, temple_thickness/2)
        curve = Part.makeTorus(curve_radius, temple_thickness/2, curve_center)
        temple = temple.fuse(curve)
    
    return temple

# Create components
left_lens = create_lens(-frame_width/2)
right_lens = create_lens(frame_width/2)
bridge = create_bridge()
left_temple = create_temple("left")
right_temple = create_temple("right")

# Combine all parts
glasses = left_lens.fuse(right_lens)
glasses = glasses.fuse(bridge)
glasses = glasses.fuse(left_temple)
glasses = glasses.fuse(right_temple)

# Create FreeCAD object
glasses_obj = doc.addObject("Part::Feature", "Glasses")
glasses_obj.Shape = glasses

# Recompute document
doc.recompute()

# Export to STL
import Mesh
mesh = Mesh.Mesh()
mesh.addFacets(glasses.tessellate(0.1))
mesh.write("{{model_path}}")

print("Glasses model created successfully!")
'''
        
        return script
    
    def _execute_freecad_script(self, script_path: str, model_id: str) -> tuple:
        """Execute FreeCAD script and generate STL file"""
        
        model_path = os.path.join(self.exports_dir, f"{model_id}.stl")
        preview_path = os.path.join(self.exports_dir, f"{model_id}_preview.png")
        
        # Update script with actual model path
        with open(script_path, 'r') as f:
            script_content = f.read()
        
        script_content = script_content.replace('{{model_path}}', model_path)
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        try:
            # Execute FreeCAD script
            result = subprocess.run(['python3', script_path], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(model_path):
                # Generate preview image (simplified)
                self._generate_preview_image(model_path, preview_path)
                return model_path, preview_path
            else:
                raise Exception(f"FreeCAD execution failed: {result.stderr}")
                
        except Exception as e:
            print(f"Error executing FreeCAD script: {e}")
            # Fallback to dummy model
            return self._create_dummy_model(model_id)
    
    def _create_dummy_model(self, model_id: str) -> tuple:
        """Create dummy files for demonstration when FreeCAD is not available"""
        
        model_path = os.path.join(self.exports_dir, f"{model_id}.stl")
        preview_path = os.path.join(self.exports_dir, f"{model_id}_preview.png")
        
        # Create dummy STL file
        dummy_stl_content = '''solid Glasses
  facet normal 0.0 0.0 1.0
    outer loop
      vertex 0.0 0.0 0.0
      vertex 1.0 0.0 0.0
      vertex 1.0 1.0 0.0
    endloop
  endfacet
  facet normal 0.0 0.0 1.0
    outer loop
      vertex 0.0 0.0 0.0
      vertex 1.0 1.0 0.0
      vertex 0.0 1.0 0.0
    endloop
  endfacet
endsolid Glasses'''
        
        with open(model_path, 'w') as f:
            f.write(dummy_stl_content)
        
        # Create dummy preview image (1x1 pixel PNG)
        dummy_png = b'\\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\rIHDR\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x01\\x08\\x06\\x00\\x00\\x00\\x1f\\x15\\xc4\\x89\\x00\\x00\\x00\\nIDATx\\x9cc\\x00\\x01\\x00\\x00\\x05\\x00\\x01\\r\\n-\\xdb\\x00\\x00\\x00\\x00IEND\\xaeB`\\x82'
        
        with open(preview_path, 'wb') as f:
            f.write(dummy_png)
        
        return model_path, preview_path
    
    def _generate_preview_image(self, model_path: str, preview_path: str):
        """Generate preview image from STL file"""
        # This would typically use a 3D rendering library
        # For now, create a placeholder
        try:
            # Try using matplotlib for simple visualization
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D
            
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, projection='3d')
            
            # Simple wireframe representation
            ax.text(0.5, 0.5, 0.5, 'Glasses Model\\nPreview', 
                   horizontalalignment='center', fontsize=12)
            
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title('3D Model Preview')
            
            plt.savefig(preview_path, dpi=100, bbox_inches='tight')
            plt.close()
            
        except ImportError:
            # Fallback: create text-based preview
            self._create_dummy_model(preview_path.split('/')[-1].replace('_preview.png', ''))
    
    def list_models(self) -> Dict[str, Any]:
        """List all generated models"""
        models = []
        
        for filename in os.listdir(self.exports_dir):
            if filename.endswith('.stl'):
                model_id = filename.replace('.stl', '')
                model_path = os.path.join(self.exports_dir, filename)
                preview_path = os.path.join(self.exports_dir, f"{model_id}_preview.png")
                
                models.append({
                    'model_id': model_id,
                    'model_path': model_path,
                    'preview_path': preview_path if os.path.exists(preview_path) else None,
                    'created_at': os.path.getctime(model_path)
                })
        
        return {'models': models}