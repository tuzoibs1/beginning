import openai
import json
import os
from typing import Dict, List, Any

class ChatBot:
    def __init__(self):
        """Initialize the ChatBot with OpenAI API"""
        # Get API key from environment variable
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not found in environment variables")
        
        openai.api_key = self.api_key
        
        # System prompt for design parsing
        self.system_prompt = """
You are a CAD design assistant that converts natural language descriptions into structured design parameters.

Your job is to parse user requests for 3D models and extract:
1. Object type (glasses, frame, lens, etc.)
2. Dimensions (width, height, depth, thickness, etc.)
3. Shape properties (round, rectangular, curved, etc.)
4. Material properties (color, finish, etc.)
5. Special features or modifications

Always respond with a JSON object containing these parameters. If information is missing, use reasonable defaults for the object type.

Example input: "Design round smart glasses with 60mm lenses and red rims"
Example output:
{
    "object_type": "glasses",
    "lens_diameter": 60,
    "lens_shape": "round",
    "rim_color": "red",
    "frame_width": 140,
    "temple_length": 140,
    "bridge_width": 18,
    "modifications": ["smart_features"]
}
"""

    def parse_design_request(self, user_message: str, history: List[Dict] = None) -> Dict[str, Any]:
        """
        Parse user message into structured design parameters
        
        Args:
            user_message: The user's natural language request
            history: Previous conversation history for context
            
        Returns:
            Dictionary containing structured design parameters
        """
        try:
            # Build context from history
            context = ""
            if history:
                context = "Previous requests in this session:\n"
                for item in history[-3:]:  # Last 3 items for context
                    context += f"- {item['user_message']}\n"
                context += "\nCurrent request:\n"
            
            # Prepare messages for OpenAI
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"{context}{user_message}"}
            ]
            
            # Call OpenAI API
            if self.api_key:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.3,
                    max_tokens=500
                )
                
                # Parse response
                content = response.choices[0].message.content
                design_params = json.loads(content)
                
            else:
                # Fallback parsing when no API key
                design_params = self._fallback_parse(user_message)
            
            # Add metadata
            design_params['original_request'] = user_message
            design_params['parsed_at'] = json.dumps({"timestamp": "now"})
            
            return design_params
            
        except Exception as e:
            print(f"Error parsing design request: {e}")
            return self._fallback_parse(user_message)
    
    def _fallback_parse(self, user_message: str) -> Dict[str, Any]:
        """
        Fallback parser when OpenAI API is not available
        Uses simple keyword matching
        """
        message_lower = user_message.lower()
        
        # Default glasses parameters
        params = {
            "object_type": "glasses",
            "frame_width": 140,
            "lens_diameter": 50,
            "lens_shape": "round",
            "temple_length": 140,
            "bridge_width": 18,
            "rim_thickness": 2,
            "color": "black",
            "modifications": []
        }
        
        # Simple keyword extraction
        if "rectangular" in message_lower or "square" in message_lower:
            params["lens_shape"] = "rectangular"
        
        if "round" in message_lower or "circular" in message_lower:
            params["lens_shape"] = "round"
        
        # Extract dimensions (basic regex would be better)
        import re
        numbers = re.findall(r'(\d+)\s*mm', message_lower)
        if numbers:
            # First number likely to be lens size
            params["lens_diameter"] = int(numbers[0])
            if len(numbers) > 1:
                params["frame_width"] = int(numbers[1])
        
        # Extract colors
        colors = ["red", "blue", "green", "black", "white", "silver", "gold"]
        for color in colors:
            if color in message_lower:
                params["color"] = color
                break
        
        # Check for modifications
        if "smart" in message_lower:
            params["modifications"].append("smart_features")
        if "thick" in message_lower:
            params["rim_thickness"] = 4
        if "thin" in message_lower:
            params["rim_thickness"] = 1
        
        params['original_request'] = user_message
        params['parsed_with'] = 'fallback'
        
        return params

    def generate_response_message(self, design_params: Dict[str, Any]) -> str:
        """Generate a friendly response message describing what was created"""
        obj_type = design_params.get('object_type', 'object')
        
        if obj_type == 'glasses':
            lens_shape = design_params.get('lens_shape', 'round')
            lens_size = design_params.get('lens_diameter', 50)
            color = design_params.get('color', 'black')
            
            message = f"Created {lens_shape} {obj_type} with {lens_size}mm lenses in {color}."
            
            if design_params.get('modifications'):
                modifications = ', '.join(design_params['modifications'])
                message += f" Added features: {modifications}."
                
            return message
        
        return f"Created a {obj_type} based on your specifications."