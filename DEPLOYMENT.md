# Deployment Guide - Universal Converter

This document describes how to build and distribute Universal Converter for Windows.

## Overview

Universal Converter is compiled into a standalone executable using PyInstaller and distributed through a professional installer created with NSIS.

## Prerequisites

### Required Software

1. **Python 3.8+**
   - Download: https://python.org/downloads/
   - ✅ Check "Add Python to PATH" during installation

2. **NSIS (Nullsoft Scriptable Install System)**
   - Download: https://nsis.sourceforge.io/Download
   - ✅ Install full version with plugins
   - ✅ Add to system PATH

3. **Git** (optional, for version control)
   - Download: https://git-scm.com/download/win

### Python Dependencies

All dependencies are listed in `requirements.txt` and installed automatically.

## Build Process

### Method 1: Automated Build (Recommended)

Run the complete build script:

```cmd
python build_windows.py
```

This script:
- ✅ Checks all requirements
- ✅ Installs missing dependencies
- ✅ Compiles executable with PyInstaller
- ✅ Creates NSIS installer
- ✅ Shows generated file statistics

### Method 2: Manual Build

#### Step 1: Compile Executable

```cmd
python build_executable.py
```

Or manually with PyInstaller:

```cmd
pyinstaller --onefile --windowed --name=UniversalConverter ^
            --add-data=ui;ui ^
            --add-data=converters;converters ^
            --add-data=utils;utils ^
            --hidden-import=PyQt5.QtCore ^
            --hidden-import=PyQt5.QtGui ^
            --hidden-import=PyQt5.QtWidgets ^
            main.py
```

#### Step 2: Compile Installer

```cmd
build_installer.bat
```

Or manually:

```cmd
makensis /V3 installer.nsi
```

## Generated File Structure

```
project/
├── dist/
│   └── UniversalConverter.exe          # Standalone executable
├── UniversalConverter-1.0.0-Setup.exe  # Final installer
└── build/                              # Temporary files (can delete)
```

## NSIS Installer Features

### Functionality

- ✅ **Modern interface** with welcome, license, components pages
- ✅ **Smart installation** detects previous versions
- ✅ **Multiple components**:
  - Main application (required)
  - Desktop shortcut
  - Start Menu entries
  - File associations
- ✅ **Complete uninstaller** removes all files and registry entries
- ✅ **Windows integration**:
  - Add/Remove Programs
  - File associations
  - Context menus

### Localization

- 🇺🇸 **English** (primary language)
- 🇧🇷 **Portuguese** (secondary)

## Expected File Sizes

| File | Approximate Size |
|------|------------------|
| Executable | 80-120 MB |
| Installer | 85-125 MB |

## Testing and Validation

### Before Distribution

1. **Test the executable**:
   ```cmd
   dist\UniversalConverter.exe
   ```

2. **Test the installer** in different scenarios:
   - ✅ Clean installation
   - ✅ Upgrade from previous version
   - ✅ Complete installation and uninstallation
   - ✅ Different users (admin/standard)

3. **Verify functionality**:
   - ✅ Conversion of different file types
   - ✅ Drag & drop
   - ✅ History
   - ✅ Advanced settings

### Test Environments

- ✅ Windows 10 (x64)
- ✅ Windows 11 (x64)
- ✅ Windows Server 2019/2022
- 🔄 Clean virtual machines
- 🔄 Different user configurations

## Distribution

### Distribution Options

1. **Direct download**
   - Host on website/GitHub Releases
   - Provide SHA256 checksums

2. **Software repositories**
   - Chocolatey (Windows)
   - Winget (Microsoft Store)

3. **Corporate distribution**
   - Deploy via GPO
   - SCCM/Intune

### Digital Signing (Recommended for Production)

To avoid Windows Defender warnings:

```cmd
signtool sign /f certificate.p12 /p password /t http://timestamp.digicert.com UniversalConverter-1.0.0-Setup.exe
```

## Troubleshooting

### Common Errors

**"NSIS not found"**
- Install NSIS and add to PATH
- Restart command prompt

**"PyInstaller failed"**
- Check dependencies: `pip install -r requirements.txt`
- Clear cache: `pyinstaller --clean`

**"Executable won't start"**
- Check system dependencies (Visual C++ Redistributable)
- Test in clean environment

**"Antivirus blocks"**
- Common false positive with PyInstaller
- Submit for analysis to vendors
- Consider digital signing

### Logging and Debug

Executable with logs:
```cmd
UniversalConverter.exe --debug
```

PyInstaller with debug:
```cmd
pyinstaller --debug=all ...
```

## Versioning

### Version Scheme

Format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible changes
- **MINOR**: New compatible features
- **PATCH**: Bug fixes

### Files to Update

- `setup.py` → version
- `installer.nsi` → APP_VERSION
- `main.py` → applicationVersion

## Automation (CI/CD)

### GitHub Actions Example

```yaml
name: Build Windows Installer

on:
  push:
    tags: ['v*']

jobs:
  build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Build
      run: python build_windows.py
    - name: Upload Release
      uses: actions/upload-release-asset@v1
      with:
        asset_path: UniversalConverter-1.0.0-Setup.exe
```

## Release Checklist

- [ ] Code tested and working
- [ ] Version updated in all files
- [ ] Executable builds without errors
- [ ] Installer tested in clean environment
- [ ] Documentation updated
- [ ] Changelog prepared
- [ ] Digital signature applied (if applicable)
- [ ] Upload to distribution platform
- [ ] User notification

## Support

For build process issues:

1. Check this document
2. Review error logs
3. Open repository issue
4. Contact development team

---

**Note**: This process is optimized for Windows distribution. For other platforms, refer to platform-specific scripts.