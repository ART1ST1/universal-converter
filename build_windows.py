#!/usr/bin/env python3
"""
Build script específico para Windows - compila executável e instalador NSIS
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Verifica se todos os requisitos estão instalados."""
    print("🔍 Verificando requisitos...")

    # Verificar Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        return False

    print("✅ Python OK")

    # Verificar PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller OK")
    except ImportError:
        print("📦 Instalando PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        print("✅ PyInstaller instalado")

    # Verificar NSIS
    try:
        result = subprocess.run(['makensis', '/VERSION'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ NSIS OK - {result.stdout.strip()}")
        else:
            print("❌ NSIS não encontrado ou com erro")
            print("💡 Baixe e instale o NSIS de: https://nsis.sourceforge.io/Download")
            return False
    except FileNotFoundError:
        print("❌ NSIS não encontrado no PATH")
        print("💡 Baixe e instale o NSIS de: https://nsis.sourceforge.io/Download")
        print("💡 Certifique-se de adicionar ao PATH do sistema")
        return False

    return True

def create_resources():
    """Cria recursos necessários para o instalador."""
    print("🎨 Criando recursos...")

    resources_dir = Path("resources")
    resources_dir.mkdir(exist_ok=True)

    # Criar ícone simples (placeholder se não existir)
    icon_path = resources_dir / "icon.ico"
    if not icon_path.exists():
        print("💡 Criando ícone placeholder...")
        # Este seria um ícone real em produção
        with open(icon_path, 'w') as f:
            f.write("# Placeholder para ícone")

    print("✅ Recursos preparados")

def build_executable():
    """Compila o executável usando PyInstaller."""
    print("🔨 Compilando executável...")

    # Limpar builds anteriores
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Removido diretório {dir_name}")

    # Comando PyInstaller
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name=UniversalConverter',
        '--add-data=ui;ui',
        '--add-data=converters;converters',
        '--add-data=utils;utils',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=PIL',
        '--hidden-import=PIL.Image',
        'main.py'
    ]

    # Adicionar ícone se existir
    icon_path = Path("resources/icon.ico")
    if icon_path.exists():
        cmd.extend(['--icon=resources/icon.ico'])

    print("🔄 Executando PyInstaller...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Executável compilado com sucesso!")

        # Mostrar tamanho do arquivo
        exe_path = Path("dist/UniversalConverter.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📏 Tamanho: {size_mb:.1f} MB")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao compilar executável:")
        print(e.stderr)
        return False

def build_installer():
    """Compila o instalador NSIS."""
    print("📦 Compilando instalador NSIS...")

    # Verificar se o executável existe
    exe_path = Path("dist/UniversalConverter.exe")
    if not exe_path.exists():
        print("❌ Executável não encontrado! Execute build_executable() primeiro.")
        return False

    # Compilar com NSIS
    cmd = ['makensis', '/V3', 'installer.nsi']

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Instalador compilado com sucesso!")

        # Mostrar informações do instalador
        installer_path = Path("UniversalConverter-1.0.0-Setup.exe")
        if installer_path.exists():
            size_mb = installer_path.stat().st_size / (1024 * 1024)
            print(f"📏 Tamanho do instalador: {size_mb:.1f} MB")
            print(f"📁 Localização: {installer_path.absolute()}")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao compilar instalador:")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    """Função principal de build."""
    print("🚀 Universal Converter - Build para Windows")
    print("=" * 50)

    # Verificar se estamos no diretório correto
    if not Path("main.py").exists():
        print("❌ main.py não encontrado!")
        print("💡 Execute este script no diretório raiz do projeto")
        sys.exit(1)

    # Verificar requisitos
    if not check_requirements():
        print("\n❌ Requisitos não atendidos. Instalação cancelada.")
        input("Pressione Enter para sair...")
        sys.exit(1)

    print()

    # Criar recursos
    create_resources()
    print()

    # Compilar executável
    if not build_executable():
        print("\n❌ Falha ao compilar executável!")
        input("Pressione Enter para sair...")
        sys.exit(1)

    print()

    # Compilar instalador
    if not build_installer():
        print("\n❌ Falha ao compilar instalador!")
        input("Pressione Enter para sair...")
        sys.exit(1)

    print()
    print("🎉 Build completo!")
    print("=" * 30)
    print("✅ Executável: dist/UniversalConverter.exe")
    print("✅ Instalador: UniversalConverter-1.0.0-Setup.exe")
    print()
    print("📋 Próximos passos:")
    print("1. Teste o executável em diferentes versões do Windows")
    print("2. Teste o instalador em máquinas limpas")
    print("3. Considere assinar digitalmente o instalador para produção")
    print("4. Distribua o instalador!")
    print()
    input("Pressione Enter para sair...")

if __name__ == '__main__':
    main()