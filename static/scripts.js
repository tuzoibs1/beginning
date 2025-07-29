// Chat Application JavaScript
class CADChatApp {
    constructor() {
        this.sessionId = null;
        this.currentModel = null;
        this.isLoading = false;
        
        this.initializeElements();
        this.bindEvents();
        this.updateStatus('Ready');
    }
    
    initializeElements() {
        // Chat elements
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.clearChatBtn = document.getElementById('clearChat');
        
        // Preview elements
        this.previewContainer = document.getElementById('previewContainer');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.modelInfo = document.getElementById('modelInfo');
        this.codeSection = document.getElementById('codeSection');
        this.toggleCodeBtn = document.getElementById('toggleCode');
        this.codeContainer = document.getElementById('codeContainer');
        this.cadCode = document.getElementById('cadCode');
        
        // Status and loading
        this.statusText = document.querySelector('.status-text');
        this.loadingOverlay = document.getElementById('loadingOverlay');
    }
    
    bindEvents() {
        // Send message events
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Clear chat
        this.clearChatBtn.addEventListener('click', () => this.clearChat());
        
        // Download model
        this.downloadBtn.addEventListener('click', () => this.downloadModel());
        
        // Toggle code display
        this.toggleCodeBtn.addEventListener('click', () => this.toggleCode());
        
        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => this.autoResizeTextarea());
    }
    
    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }
    
    updateStatus(status, type = 'ready') {
        this.statusText.textContent = status;
        
        const indicator = document.querySelector('.status-indicator');
        indicator.className = 'status-indicator';
        
        switch(type) {
            case 'loading':
                indicator.style.background = '#f59e0b';
                break;
            case 'success':
                indicator.style.background = '#10b981';
                break;
            case 'error':
                indicator.style.background = '#ef4444';
                break;
            default:
                indicator.style.background = '#10b981';
        }
    }
    
    showLoading(show = true) {
        this.isLoading = show;
        this.loadingOverlay.style.display = show ? 'flex' : 'none';
        this.sendButton.disabled = show;
        this.messageInput.disabled = show;
        
        if (show) {
            this.updateStatus('Generating model...', 'loading');
        }
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isLoading) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.autoResizeTextarea();
        
        this.showLoading(true);
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Update session ID
            this.sessionId = data.session_id;
            
            // Add assistant response
            this.addMessage(data.message, 'assistant');
            
            // Update model preview
            if (data.success && data.model_path) {
                this.updateModelPreview(data);
                this.updateStatus('Model generated successfully', 'success');
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage(`Sorry, there was an error: ${error.message}`, 'assistant', true);
            this.updateStatus('Error occurred', 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    addMessage(content, sender, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const avatar = sender === 'user' ? '👤' : '🤖';
        const bgClass = isError ? 'error' : '';
        
        messageDiv.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content ${bgClass}">
                <p>${this.formatMessage(content)}</p>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    formatMessage(message) {
        // Simple formatting for messages
        return message
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    updateModelPreview(data) {
        this.currentModel = data;
        
        // Clear preview container
        this.previewContainer.innerHTML = '';
        
        // Show preview image if available
        if (data.preview_image) {
            const img = document.createElement('img');
            img.src = `/static/exports/${data.preview_image.split('/').pop()}`;
            img.className = 'preview-image';
            img.alt = 'Generated 3D Model Preview';
            img.onerror = () => {
                this.showPreviewPlaceholder('Preview not available');
            };
            this.previewContainer.appendChild(img);
        } else {
            this.showPreviewPlaceholder('Model generated successfully');
        }
        
        // Update model info
        this.updateModelInfo(data.design_params);
        
        // Update CAD code
        if (data.cad_code) {
            this.updateCADCode(data.cad_code);
        }
        
        // Enable download button
        this.downloadBtn.disabled = false;
    }
    
    showPreviewPlaceholder(message) {
        this.previewContainer.innerHTML = `
            <div class="preview-placeholder">
                <div class="preview-icon">✅</div>
                <p>${message}</p>
                <small>Download the STL file to view in your 3D software</small>
            </div>
        `;
    }
    
    updateModelInfo(designParams) {
        if (!designParams) return;
        
        // Show model info section
        this.modelInfo.style.display = 'block';
        
        // Update info fields
        document.getElementById('objectType').textContent = 
            designParams.object_type || 'Unknown';
        
        document.getElementById('dimensions').textContent = 
            `${designParams.lens_diameter || 50}mm lens, ${designParams.frame_width || 140}mm frame`;
        
        document.getElementById('shape').textContent = 
            designParams.lens_shape || 'Round';
        
        document.getElementById('color').textContent = 
            designParams.color || 'Black';
    }
    
    updateCADCode(code) {
        if (!code) return;
        
        // Show code section
        this.codeSection.style.display = 'block';
        
        // Update code content
        this.cadCode.textContent = code;
        
        // Syntax highlighting (basic)
        this.highlightCode();
    }
    
    highlightCode() {
        // Simple syntax highlighting for Python
        let code = this.cadCode.textContent;
        
        // Keywords
        code = code.replace(/\b(import|def|class|if|else|elif|for|while|try|except|return|True|False|None)\b/g, 
            '<span style="color: #c678dd;">$1</span>');
        
        // Strings
        code = code.replace(/"([^"]*)"/g, '<span style="color: #98c379;">"$1"</span>');
        code = code.replace(/'([^']*)'/g, '<span style="color: #98c379;">\\'$1\\'</span>');
        
        // Comments
        code = code.replace(/#.*/g, '<span style="color: #5c6370;">$&</span>');
        
        // Numbers
        code = code.replace(/\b\d+\.?\d*\b/g, '<span style="color: #d19a66;">$&</span>');
        
        this.cadCode.innerHTML = code;
    }
    
    toggleCode() {
        const isVisible = this.codeContainer.style.display !== 'none';
        this.codeContainer.style.display = isVisible ? 'none' : 'block';
        this.toggleCodeBtn.textContent = isVisible ? 'Show Code' : 'Hide Code';
    }
    
    async downloadModel() {
        if (!this.sessionId || !this.currentModel) {
            alert('No model available for download');
            return;
        }
        
        try {
            const response = await fetch(`/download/${this.sessionId}`);
            
            if (!response.ok) {
                throw new Error('Download failed');
            }
            
            // Create download link
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `cad_model_${this.sessionId}.stl`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            this.updateStatus('Model downloaded successfully', 'success');
            
        } catch (error) {
            console.error('Download error:', error);
            alert('Failed to download model: ' + error.message);
            this.updateStatus('Download failed', 'error');
        }
    }
    
    clearChat() {
        // Clear messages except the initial assistant message
        const messages = this.chatMessages.querySelectorAll('.message');
        for (let i = 1; i < messages.length; i++) {
            messages[i].remove();
        }
        
        // Reset session
        this.sessionId = null;
        this.currentModel = null;
        
        // Reset preview
        this.previewContainer.innerHTML = `
            <div class="preview-placeholder">
                <div class="preview-icon">🎯</div>
                <p>Your 3D model will appear here</p>
                <small>Start by describing a design in the chat</small>
            </div>
        `;
        
        // Hide info sections
        this.modelInfo.style.display = 'none';
        this.codeSection.style.display = 'none';
        
        // Disable download
        this.downloadBtn.disabled = true;
        
        // Reset status
        this.updateStatus('Ready');
    }
    
    // Utility methods
    formatTimestamp(timestamp) {
        return new Date(timestamp).toLocaleTimeString();
    }
    
    showNotification(message, type = 'info') {
        // Simple notification system
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 1001;
            animation: slideIn 0.3s ease;
        `;
        
        switch(type) {
            case 'success':
                notification.style.background = '#10b981';
                break;
            case 'error':
                notification.style.background = '#ef4444';
                break;
            default:
                notification.style.background = '#3b82f6';
        }
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .message-content.error {
        background: #fee2e2 !important;
        color: #dc2626 !important;
        border: 1px solid #fecaca;
    }
`;
document.head.appendChild(style);

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.cadApp = new CADChatApp();
    
    // Add some helpful keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter to send message
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            window.cadApp.sendMessage();
        }
        
        // Escape to clear loading
        if (e.key === 'Escape' && window.cadApp.isLoading) {
            window.cadApp.showLoading(false);
        }
    });
});

// Export for potential external use
window.CADChatApp = CADChatApp;