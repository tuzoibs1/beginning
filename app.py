from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import os
import json
from datetime import datetime
import uuid

from chatbot import ChatBot
from cad_engine import CADEngine

app = Flask(__name__)
CORS(app)

# Initialize components
chatbot = ChatBot()
cad_engine = CADEngine()

# Store active sessions
sessions = {}

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and generate CAD models"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Initialize session if new
        if session_id not in sessions:
            sessions[session_id] = {
                'history': [],
                'current_model': None,
                'created_at': datetime.now().isoformat()
            }
        
        session = sessions[session_id]
        
        # Process message with chatbot
        design_params = chatbot.parse_design_request(user_message, session['history'])
        
        # Generate CAD code and model
        cad_result = cad_engine.generate_model(design_params)
        
        # Update session
        session['history'].append({
            'user_message': user_message,
            'design_params': design_params,
            'timestamp': datetime.now().isoformat()
        })
        session['current_model'] = cad_result
        
        # Prepare response
        response = {
            'session_id': session_id,
            'message': cad_result.get('description', 'Model generated successfully'),
            'model_path': cad_result.get('model_path'),
            'preview_image': cad_result.get('preview_image'),
            'cad_code': cad_result.get('cad_code'),
            'success': cad_result.get('success', True)
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<session_id>')
def download_model(session_id):
    """Download the generated STL file"""
    try:
        if session_id not in sessions:
            return jsonify({'error': 'Session not found'}), 404
        
        session = sessions[session_id]
        if not session.get('current_model') or not session['current_model'].get('model_path'):
            return jsonify({'error': 'No model available for download'}), 404
        
        model_path = session['current_model']['model_path']
        if not os.path.exists(model_path):
            return jsonify({'error': 'Model file not found'}), 404
        
        return send_file(model_path, as_attachment=True, download_name=f'model_{session_id}.stl')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sessions')
def list_sessions():
    """List all active sessions"""
    return jsonify({
        'sessions': {
            sid: {
                'created_at': session['created_at'],
                'message_count': len(session['history']),
                'has_model': bool(session.get('current_model'))
            }
            for sid, session in sessions.items()
        }
    })

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('models', exist_ok=True)
    os.makedirs('exports', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)