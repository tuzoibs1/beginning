# 🔧 Vibe Code CAD Assistant

An AI-powered Computer-Aided Design (CAD) tool that allows users to create 3D models through natural language. Simply describe what you want to design, and the system will generate a 3D model using FreeCAD via Python scripting.

![Vibe Code CAD](https://img.shields.io/badge/AI-Powered-blue) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![Flask](https://img.shields.io/badge/Flask-2.3+-red) ![FreeCAD](https://img.shields.io/badge/FreeCAD-Compatible-orange)

## ✨ Features

- **Natural Language Processing**: Describe your design ideas in plain English
- **AI-Powered Design**: Uses OpenAI GPT-4 to parse design requests into structured parameters
- **3D Model Generation**: Automatically generates FreeCAD Python scripts and executes them
- **Interactive Chat Interface**: Clean, modern web interface for design conversations
- **Real-time Preview**: View generated models with preview images
- **STL Export**: Download your designs as STL files for 3D printing
- **Design History**: Keep track of your design iterations
- **Code Visibility**: View and learn from the generated FreeCAD code

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- FreeCAD (optional, falls back to demo mode without it)
- OpenAI API key (optional, has fallback parser)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vibe-code-cad-assistant
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   # Create a .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

4. **Install FreeCAD** (optional but recommended)
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get install freecad python3-freecad
   ```
   
   **macOS:**
   ```bash
   brew install freecad
   ```
   
   **Windows:**
   Download from [FreeCAD official website](https://www.freecad.org/downloads.php)

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 💬 Usage Examples

Try these example prompts in the chat interface:

- **"Design round smart glasses with 60mm lenses and red rims"**
- **"Create rectangular glasses with thick black frames"**
- **"Make a pair of sunglasses with blue lenses and curved temples"**
- **"Design glasses with 55mm round lenses, silver frames, and thin temples"**

## 🏗️ Project Structure

```
vibe-code-cad-assistant/
├── app.py                 # Main Flask application
├── chatbot.py            # OpenAI integration and NLP processing
├── cad_engine.py         # FreeCAD script generation and execution
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/
│   └── index.html       # Main web interface
├── static/
│   ├── styles.css       # UI styling
│   └── scripts.js       # Frontend JavaScript
├── models/              # Generated FreeCAD scripts
├── exports/             # Generated STL files and previews
└── logs/               # Application logs
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI API Configuration (optional)
OPENAI_API_KEY=your_openai_api_key_here

# Flask Configuration (optional)
FLASK_ENV=development
FLASK_DEBUG=True

# Server Configuration (optional)
HOST=0.0.0.0
PORT=5000
```

### FreeCAD Setup

The application will automatically detect if FreeCAD is available. If not found, it will:
- Use a fallback parser instead of OpenAI (if no API key)
- Generate dummy STL files for demonstration
- Still provide full UI functionality

## 🎯 API Endpoints

### `POST /chat`
Process a design request and generate a 3D model.

**Request:**
```json
{
  "message": "Design round glasses with 60mm lenses",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "session_id": "generated-uuid",
  "message": "Created round glasses with 60mm lenses in black.",
  "model_path": "exports/model-id.stl",
  "preview_image": "exports/model-id_preview.png",
  "cad_code": "# Generated FreeCAD code...",
  "success": true
}
```

### `GET /download/<session_id>`
Download the STL file for a generated model.

### `GET /sessions`
List all active design sessions.

## 🔌 Extending the System

### Adding New Object Types

1. **Update the chatbot parser** in `chatbot.py`:
   ```python
   # Add new object type recognition
   if "chair" in message_lower:
       params["object_type"] = "chair"
   ```

2. **Create a new generator** in `cad_engine.py`:
   ```python
   def _generate_chair_script(self, params):
       # Implement chair generation logic
       return script
   ```

3. **Update the main generator**:
   ```python
   def _generate_freecad_script(self, params):
       object_type = params.get('object_type', 'glasses')
       if object_type == 'chair':
           return self._generate_chair_script(params)
   ```

### Custom Design Parameters

Add new parameters to the OpenAI system prompt and fallback parser:

```python
# In chatbot.py system prompt
{
    "object_type": "glasses",
    "material": "plastic",  # New parameter
    "finish": "matte",      # New parameter
    # ... existing parameters
}
```

## 🐛 Troubleshooting

### Common Issues

1. **"FreeCAD not found" warning**
   - Install FreeCAD using the instructions above
   - Or continue using demo mode (still functional)

2. **"OpenAI API key not found" warning**
   - Add your API key to `.env` file
   - Or continue using fallback parser (limited functionality)

3. **Port 5000 already in use**
   - Change the port in `app.py`: `app.run(port=5001)`
   - Or kill the process using port 5000

4. **Models not generating**
   - Check the browser console for JavaScript errors
   - Verify the Flask server is running
   - Check server logs for Python errors

### Debug Mode

Run with debug information:
```bash
FLASK_DEBUG=True python app.py
```

## 🤝 Contributing

Contributions are welcome! Here are some areas for improvement:

1. **Add more object types** (furniture, mechanical parts, etc.)
2. **Improve 3D preview** (Three.js integration)
3. **Add material properties** (color, texture, etc.)
4. **Implement design iterations** (modify existing models)
5. **Add user authentication** (save designs per user)
6. **Blender integration** (alternative to FreeCAD)

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 API
- **FreeCAD** community for the amazing CAD software
- **Flask** team for the web framework
- **Inter** font family for beautiful typography

## 📞 Support

For questions, issues, or feature requests:

1. Check the [Issues](../../issues) page
2. Create a new issue with detailed information
3. Join our community discussions

---

**Built with ❤️ for makers, designers, and AI enthusiasts**


