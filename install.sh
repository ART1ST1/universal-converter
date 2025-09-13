#!/bin/bash

# Universal Converter Installation Script for Linux/macOS
# This script installs Universal Converter and its dependencies

set -e

echo "🔧 Universal Converter Installation Script"
echo "=========================================="

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    echo "❌ Unsupported operating system: $OSTYPE"
    exit 1
fi

echo "📋 Detected OS: $OS"

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
    echo "📋 Python version: $PYTHON_VERSION"

    # Check if Python version is >= 3.8
    if [[ $(echo "$PYTHON_VERSION 3.8" | awk '{print ($1 >= $2)}') == 1 ]]; then
        echo "✅ Python version is sufficient"
    else
        echo "❌ Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
        exit 1
    fi
else
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Install system dependencies
echo "📦 Installing system dependencies..."

if [[ "$OS" == "linux" ]]; then
    # Detect Linux distribution
    if command -v apt &> /dev/null; then
        echo "📋 Detected Debian/Ubuntu system"
        sudo apt update
        sudo apt install -y python3-pip python3-venv python3-dev

        # Install optional dependencies
        echo "📦 Installing optional dependencies for enhanced functionality..."
        sudo apt install -y ffmpeg libreoffice pandoc wkhtmltopdf

        # Install PyQt5 system package for better compatibility
        sudo apt install -y python3-pyqt5 python3-pyqt5-dev

    elif command -v dnf &> /dev/null; then
        echo "📋 Detected Fedora system"
        sudo dnf install -y python3-pip python3-virtualenv python3-devel
        sudo dnf install -y ffmpeg libreoffice pandoc wkhtmltopdf
        sudo dnf install -y python3-qt5 python3-qt5-devel

    elif command -v yum &> /dev/null; then
        echo "📋 Detected CentOS/RHEL system"
        sudo yum install -y python3-pip python3-virtualenv python3-devel
        # Note: Some packages might need EPEL repository
        echo "⚠️  Note: You may need to enable EPEL repository for some packages"

    else
        echo "⚠️  Could not detect package manager. Please install dependencies manually:"
        echo "   - python3-pip"
        echo "   - python3-venv"
        echo "   - ffmpeg"
        echo "   - libreoffice"
        echo "   - pandoc"
        echo "   - wkhtmltopdf"
    fi

elif [[ "$OS" == "macos" ]]; then
    echo "📋 Detected macOS system"

    # Check if Homebrew is installed
    if command -v brew &> /dev/null; then
        echo "📦 Installing dependencies via Homebrew..."
        brew install ffmpeg libreoffice pandoc wkhtmltopdf
    else
        echo "⚠️  Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        echo "   Then run this script again."
        exit 1
    fi
fi

echo "✅ System dependencies installed"

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv universal-converter-env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source universal-converter-env/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create desktop shortcut (Linux only)
if [[ "$OS" == "linux" ]]; then
    echo "🔗 Creating desktop shortcut..."

    CURRENT_DIR=$(pwd)
    DESKTOP_FILE="$HOME/.local/share/applications/universal-converter.desktop"

    mkdir -p "$HOME/.local/share/applications"

    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Universal Converter
Comment=Convert files between various formats
Exec=$CURRENT_DIR/universal-converter-env/bin/python $CURRENT_DIR/main.py
Icon=$CURRENT_DIR/resources/icon.png
Terminal=false
Categories=Utility;Office;Graphics;AudioVideo;
Keywords=converter;file;format;image;video;audio;document;
EOF

    chmod +x "$DESKTOP_FILE"
    echo "✅ Desktop shortcut created"
fi

# Create launch script
echo "🚀 Creating launch script..."
cat > "run_universal_converter.sh" << EOF
#!/bin/bash
cd "\$(dirname "\$0")"
source universal-converter-env/bin/activate
python main.py "\$@"
EOF

chmod +x "run_universal_converter.sh"

echo "✅ Installation completed successfully!"
echo ""
echo "🎉 How to run Universal Converter:"
echo "   Method 1: ./run_universal_converter.sh"
echo "   Method 2: source universal-converter-env/bin/activate && python main.py"

if [[ "$OS" == "linux" ]]; then
    echo "   Method 3: Look for 'Universal Converter' in your applications menu"
fi

echo ""
echo "📝 Notes:"
echo "   - The application is installed in: $(pwd)"
echo "   - Virtual environment: $(pwd)/universal-converter-env"
echo "   - To uninstall, simply delete this directory"
echo ""
echo "🆘 If you encounter issues:"
echo "   1. Check that all system dependencies are installed"
echo "   2. Ensure Python 3.8+ is available"
echo "   3. Try running: pip install -r requirements.txt"
echo ""
echo "Happy converting! 🎊"