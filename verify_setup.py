#!/usr/bin/env python3
"""
Simple verification script for Vibe Code CAD Assistant
Checks basic structure and imports without external dependencies.
"""

import os
import sys

def check_files():
    """Check that all required files exist"""
    print("📁 Checking project structure...")
    
    required_files = [
        'app.py',
        'chatbot.py', 
        'cad_engine.py',
        'requirements.txt',
        'README.md',
        'templates/index.html',
        'static/styles.css',
        'static/scripts.js'
    ]
    
    required_dirs = [
        'models',
        'exports', 
        'logs',
        'static',
        'templates'
    ]
    
    all_good = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_good = False
    
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ - MISSING")
            all_good = False
    
    return all_good

def check_basic_syntax():
    """Check that Python files have valid syntax"""
    print("\n🐍 Checking Python syntax...")
    
    python_files = ['app.py', 'chatbot.py', 'cad_engine.py']
    all_good = True
    
    for file_path in python_files:
        try:
            with open(file_path, 'r') as f:
                compile(f.read(), file_path, 'exec')
            print(f"✅ {file_path} - syntax OK")
        except SyntaxError as e:
            print(f"❌ {file_path} - syntax error: {e}")
            all_good = False
        except FileNotFoundError:
            print(f"❌ {file_path} - file not found")
            all_good = False
    
    return all_good

def check_html_css():
    """Check that HTML and CSS files exist and have content"""
    print("\n🌐 Checking web files...")
    
    web_files = {
        'templates/index.html': 'html',
        'static/styles.css': 'css',
        'static/scripts.js': 'javascript'
    }
    
    all_good = True
    
    for file_path, file_type in web_files.items():
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                if len(content) > 100:  # Basic content check
                    print(f"✅ {file_path} - {len(content)} chars")
                else:
                    print(f"⚠️  {file_path} - too short ({len(content)} chars)")
        except FileNotFoundError:
            print(f"❌ {file_path} - file not found")
            all_good = False
    
    return all_good

def check_requirements():
    """Check requirements.txt content"""
    print("\n📦 Checking requirements...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
            
        expected_packages = ['Flask', 'openai', 'matplotlib']
        found_packages = []
        
        for req in requirements:
            if req.strip():
                package_name = req.split('==')[0].split('>=')[0].split('<=')[0]
                found_packages.append(package_name)
        
        all_good = True
        for package in expected_packages:
            if any(package.lower() in found.lower() for found in found_packages):
                print(f"✅ {package} listed in requirements")
            else:
                print(f"⚠️  {package} not found in requirements")
                all_good = False
        
        print(f"📋 Total packages: {len(found_packages)}")
        return all_good
        
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False

def main():
    """Run all verification checks"""
    print("🔧 Vibe Code CAD Assistant - Setup Verification")
    print("=" * 55)
    
    checks = [
        ("Project Structure", check_files),
        ("Python Syntax", check_basic_syntax),
        ("Web Files", check_html_css),
        ("Requirements", check_requirements)
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        try:
            if check_func():
                passed += 1
                print(f"✅ {check_name} - PASSED\n")
            else:
                print(f"❌ {check_name} - FAILED\n")
        except Exception as e:
            print(f"💥 {check_name} - ERROR: {e}\n")
    
    print("=" * 55)
    print(f"📊 Verification Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 Perfect! Your Vibe Code CAD Assistant is properly set up!")
        print("\n🚀 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. (Optional) Set up OpenAI API key in .env file")
        print("3. Run the application: python app.py")
        print("4. Open http://localhost:5000 in your browser")
        print("\n💡 The app will work without OpenAI API key using fallback mode.")
    elif passed >= total - 1:
        print("\n✨ Almost perfect! Minor issues detected but app should work.")
        print("💡 Check the failed items above and fix if needed.")
    else:
        print("\n⚠️  Several issues detected. Please fix the failed checks above.")
    
    return passed >= total - 1

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)