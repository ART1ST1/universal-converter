#!/usr/bin/env python3
"""
Build script for creating standalone executables using PyInstaller
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not available."""
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])

def get_platform_info():
    """Get platform-specific information."""
    system = platform.system().lower()
    arch = platform.machine().lower()

    if arch in ['x86_64', 'amd64']:
        arch = 'x64'
    elif arch in ['i386', 'i686']:
        arch = 'x86'
    elif arch.startswith('arm'):
        arch = 'arm64' if '64' in arch else 'arm'

    return system, arch

def create_spec_file():
    """Create PyInstaller spec file for better control."""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ui/*.py', 'ui'),
        ('converters/*.py', 'converters'),
        ('utils/*.py', 'utils'),
        ('resources/*', 'resources') if os.path.exists('resources') else [],
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PIL',
        'PIL.Image',
        'PIL.ImageEnhance',
        'pypandoc',
        'docx',
        'openpyxl',
        'py7zr',
        'rarfile',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='UniversalConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icon.ico' if os.path.exists('resources/icon.ico') else None,
)

# Create app bundle for macOS
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='Universal Converter.app',
        icon='resources/icon.icns' if os.path.exists('resources/icon.icns') else None,
        bundle_identifier='com.universalconverter.app',
        info_plist={
            'CFBundleDisplayName': 'Universal Converter',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'LSMinimumSystemVersion': '10.14.0',
            'NSHighResolutionCapable': 'True',
        }
    )
'''

    with open('universal_converter.spec', 'w') as f:
        f.write(spec_content)

def build_executable():
    """Build the executable using PyInstaller."""
    system, arch = get_platform_info()

    print(f"🏗️  Building for {system}-{arch}")
    print("📦 Installing PyInstaller...")
    install_pyinstaller()

    print("📝 Creating spec file...")
    create_spec_file()

    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    print("🔨 Building executable...")
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        'universal_converter.spec'
    ]

    try:
        subprocess.check_call(cmd)

        # Create distribution folder
        dist_name = f"universal-converter-{system}-{arch}"
        if os.path.exists(dist_name):
            shutil.rmtree(dist_name)

        os.makedirs(dist_name, exist_ok=True)

        # Copy executable
        if system == 'windows':
            exe_name = 'UniversalConverter.exe'
            if os.path.exists(f'dist/{exe_name}'):
                shutil.copy2(f'dist/{exe_name}', f'{dist_name}/')
        elif system == 'darwin':
            app_name = 'Universal Converter.app'
            if os.path.exists(f'dist/{app_name}'):
                shutil.copytree(f'dist/{app_name}', f'{dist_name}/{app_name}')
        else:  # Linux
            exe_name = 'UniversalConverter'
            if os.path.exists(f'dist/{exe_name}'):
                shutil.copy2(f'dist/{exe_name}', f'{dist_name}/')
                # Make executable
                os.chmod(f'{dist_name}/{exe_name}', 0o755)

        # Copy documentation
        for doc_file in ['README.md', 'LICENSE']:
            if os.path.exists(doc_file):
                shutil.copy2(doc_file, f'{dist_name}/')

        # Create archive
        if system == 'windows':
            archive_name = f"{dist_name}.zip"
            shutil.make_archive(dist_name, 'zip', dist_name)
        else:
            archive_name = f"{dist_name}.tar.gz"
            shutil.make_archive(dist_name, 'gztar', dist_name)

        print(f"✅ Build completed successfully!")
        print(f"📁 Executable folder: {dist_name}/")
        print(f"📦 Archive created: {archive_name}")

        # Show file sizes
        if system == 'windows':
            exe_path = f"{dist_name}/UniversalConverter.exe"
        elif system == 'darwin':
            exe_path = f"{dist_name}/Universal Converter.app"
        else:
            exe_path = f"{dist_name}/UniversalConverter"

        if os.path.exists(exe_path):
            if os.path.isfile(exe_path):
                size = os.path.getsize(exe_path)
                print(f"📏 Executable size: {size / (1024*1024):.1f} MB")
            else:
                # Calculate app bundle size (macOS)
                total_size = sum(
                    os.path.getsize(os.path.join(dirpath, filename))
                    for dirpath, dirnames, filenames in os.walk(exe_path)
                    for filename in filenames
                )
                print(f"📏 App bundle size: {total_size / (1024*1024):.1f} MB")

        print(f"📏 Archive size: {os.path.getsize(archive_name) / (1024*1024):.1f} MB")

    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with error code {e.returncode}")
        return False

    return True

def main():
    """Main build function."""
    print("🚀 Universal Converter Build Script")
    print("=" * 40)

    # Verify we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found. Please run this script from the project root directory.")
        sys.exit(1)

    # Build executable
    if build_executable():
        print("\n🎉 Build process completed successfully!")
        print("\nNext steps:")
        print("1. Test the executable thoroughly")
        print("2. Distribute the archive file")
        print("3. Consider code signing (for production releases)")
    else:
        print("\n❌ Build process failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()