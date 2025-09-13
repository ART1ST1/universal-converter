# Universal Converter

A powerful Windows desktop application for converting files between various formats. Universal Converter supports documents, images, videos, audio files, spreadsheets, presentations, archives, and code files with a modern, intuitive interface.

## 🚀 Quick Start

### For Users
**Download the latest version:**

📦 [**Download Universal Converter Installer**](https://github.com/Pasblinn/universal-converter/releases/download/v1.0.0/UniversalConverter-Setup.exe)

*Requires Windows 10 or later*

### For Developers
**Get the source code:**

🔧 [**Download Source Code**](https://github.com/Pasblinn/universal-converter/archive/refs/heads/main.zip) or clone:
```bash
git clone https://github.com/Pasblinn/universal-converter.git
```

## ✨ Features

### Supported File Types

| Category | Input Formats | Output Formats |
|----------|---------------|----------------|
| **Documents** | DOCX, PDF, TXT, ODT, RTF, HTML, MD | PDF, DOCX, TXT, RTF, HTML, ODT |
| **Spreadsheets** | XLSX, CSV, ODS | XLSX, CSV, ODS, PDF |
| **Presentations** | PPTX, ODP | PPTX, PDF, ODP |
| **Images** | JPG, PNG, GIF, BMP, TIFF, WEBP, ICO | JPG, PNG, GIF, BMP, TIFF, WEBP, ICO, PDF |
| **Audio** | MP3, WAV, OGG, FLAC, AAC | MP3, WAV, OGG, FLAC, AAC |
| **Video** | MP4, AVI, MKV, MOV, WEBM | MP4, AVI, MKV, MOV, WEBM, MP3, WAV |
| **Archives** | ZIP, RAR, 7Z, TAR.GZ | ZIP, 7Z, TAR.GZ |
| **Code** | PY, JAVA, CPP, JS, HTML, CSS, PHP, GO | PDF, DOCX, HTML, TXT |

### Key Capabilities

- ✅ **Modern Interface** - Clean, intuitive design with drag & drop support
- ✅ **Batch Processing** - Convert multiple files simultaneously
- ✅ **Real-time Progress** - Live status updates and progress tracking
- ✅ **Smart Detection** - Automatic file type recognition
- ✅ **Advanced Settings** - Quality control, compression, and format options
- ✅ **Conversion History** - Track and review past conversions
- ✅ **100% Offline** - No internet connection required, complete privacy
- ✅ **Professional Installer** - Easy installation with desktop shortcuts

## 📖 User Guide

### Installation

1. **Download** the installer from the link above
2. **Run** `UniversalConverter-Setup.exe` as administrator
3. **Follow** the installation wizard
4. **Launch** from desktop shortcut or Start Menu

### Basic Usage

1. **Launch** Universal Converter
2. **Add Files** - Drag & drop files or click "Add Files" button
3. **Select Format** - Choose output format from dropdown
4. **Set Destination** - Choose output folder (optional)
5. **Convert** - Click "Start Conversion" and wait for completion

### Advanced Features

**Batch Conversion**
- Add multiple files of different types
- Convert all to the same output format
- Monitor individual file progress

**Quality Settings**
- Access "Advanced" tab for detailed options
- Adjust image quality, audio bitrate, video compression
- Configure threading and output naming

**History Management**
- View past conversions in History tab
- Open output folders directly
- Clear history when needed

## 🛠️ Technical Requirements

### System Requirements
- **OS**: Windows 10 or later (64-bit recommended)
- **RAM**: 512MB minimum, 2GB recommended
- **Storage**: 150MB for installation + space for conversions
- **CPU**: Any modern x86/x64 processor

### Optional Dependencies
For enhanced functionality, install:
- **FFmpeg** - For advanced audio/video processing
- **LibreOffice** - For enhanced document conversions
- **7-Zip** - For additional archive format support

## 🔧 Developer Information

### Building from Source

**Prerequisites:**
- Python 3.8+
- NSIS (for Windows installer)
- Git

**Build Process:**
```bash
# Clone repository
git clone https://github.com/Pasblinn/universal-converter.git
cd universal-converter

# Install dependencies
pip install -r requirements.txt

# Build executable and installer
python build_windows.py
```

### Project Architecture

```
universal-converter/
├── main.py                    # Application entry point
├── ui/                        # User interface components
│   ├── main_window.py         # Main application window
│   └── advanced_settings.py  # Settings dialog
├── converters/                # Conversion engines
│   ├── image_converter.py     # Image processing
│   ├── document_converter.py  # Document processing
│   ├── audio_converter.py     # Audio processing
│   ├── video_converter.py     # Video processing
│   ├── archive_converter.py   # Archive handling
│   └── code_converter.py      # Code documentation
├── utils/                     # Core utilities
│   ├── file_detector.py       # File type detection
│   ├── conversion_manager.py  # Process orchestration
│   └── history_manager.py     # History tracking
├── installer.nsi             # NSIS installer script
└── build_windows.py          # Automated build system
```

### Technology Stack
- **GUI Framework**: PyQt5
- **Image Processing**: Pillow (PIL)
- **Document Conversion**: pypandoc, python-docx, openpyxl
- **Media Processing**: FFmpeg integration
- **Archive Handling**: py7zr, zipfile, rarfile
- **Installer**: NSIS (Nullsoft Scriptable Install System)

## 📊 Performance Benchmarks

| File Type | Size | Conversion Time* |
|-----------|------|------------------|
| Image (JPG→PNG) | 5MB | 2-3 seconds |
| Document (DOCX→PDF) | 10MB | 5-8 seconds |
| Audio (WAV→MP3) | 50MB | 15-25 seconds |
| Video (MP4→AVI) | 100MB | 60-120 seconds |

*Times measured on Intel i5-8400, 16GB RAM, SSD storage

## 🔒 Privacy & Security

- **100% Local Processing** - All conversions happen on your machine
- **No Data Collection** - Zero telemetry or usage tracking
- **No Internet Required** - Works completely offline
- **Open Source** - Full transparency of code and processes

## 🆘 Troubleshooting

### Common Issues

**Application won't start**
- Install Visual C++ Redistributable
- Run as administrator
- Check antivirus exclusions

**Conversion fails**
- Verify input file isn't corrupted
- Check available disk space
- Try smaller batch sizes

**Missing dependencies**
- Install optional components (FFmpeg, LibreOffice)
- Update Windows to latest version
- Reinstall Universal Converter

### Support

- **Documentation**: Check this README and included help files
- **Issues**: Report bugs via GitHub Issues
- **Updates**: Check GitHub Releases for new versions

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Acknowledgments

- **PyQt5** - Cross-platform GUI toolkit
- **FFmpeg** - Multimedia framework
- **NSIS** - Professional installer system
- **Python Community** - Extensive library ecosystem

---

**Universal Converter** - Making file conversion simple and efficient.