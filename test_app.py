#!/usr/bin/env python3
"""
Test script for Vibe Code CAD Assistant
Run this to verify the application is working correctly.
"""

import sys
import os
import requests
import json
import time

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    try:
        from flask import Flask
        from chatbot import ChatBot
        from cad_engine import CADEngine
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_chatbot():
    """Test the chatbot functionality"""
    print("\n🤖 Testing ChatBot...")
    try:
        chatbot = ChatBot()
        result = chatbot.parse_design_request("Design round glasses with 60mm lenses")
        
        if result and 'object_type' in result:
            print(f"✅ ChatBot working - parsed: {result['object_type']}")
            return True
        else:
            print("❌ ChatBot parsing failed")
            return False
    except Exception as e:
        print(f"❌ ChatBot error: {e}")
        return False

def test_cad_engine():
    """Test the CAD engine functionality"""
    print("\n⚙️ Testing CAD Engine...")
    try:
        cad_engine = CADEngine()
        
        # Test with sample parameters
        params = {
            'object_type': 'glasses',
            'lens_diameter': 60,
            'lens_shape': 'round',
            'color': 'black'
        }
        
        result = cad_engine.generate_model(params)
        
        if result and result.get('success'):
            print("✅ CAD Engine working - model generated")
            return True
        else:
            print(f"❌ CAD Engine failed: {result.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ CAD Engine error: {e}")
        return False

def test_directories():
    """Test that required directories exist"""
    print("\n📁 Testing directories...")
    required_dirs = ['models', 'exports', 'logs', 'static', 'templates']
    
    all_exist = True
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ exists")
        else:
            print(f"❌ {dir_name}/ missing")
            all_exist = False
    
    return all_exist

def test_server():
    """Test if the Flask server can start"""
    print("\n🌐 Testing Flask server...")
    try:
        # Import and create app
        from app import app
        
        # Test in test mode
        app.config['TESTING'] = True
        client = app.test_client()
        
        # Test homepage
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Homepage loads successfully")
        else:
            print(f"❌ Homepage failed: {response.status_code}")
            return False
        
        # Test chat endpoint with sample data
        response = client.post('/chat', 
                             json={'message': 'Design round glasses'},
                             content_type='application/json')
        
        if response.status_code == 200:
            data = json.loads(response.data)
            if 'session_id' in data:
                print("✅ Chat endpoint working")
                return True
            else:
                print(f"❌ Chat endpoint response invalid: {data}")
                return False
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Server test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🔧 Vibe Code CAD Assistant - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Directories", test_directories),
        ("ChatBot", test_chatbot),
        ("CAD Engine", test_cad_engine),
        ("Flask Server", test_server)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your CAD Assistant is ready to use.")
        print("\n🚀 To start the application:")
        print("   python app.py")
        print("   Then open http://localhost:5000 in your browser")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        if passed >= total - 1:
            print("💡 The application should still work, but with limited functionality.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)