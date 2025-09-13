@echo off
REM Script para compilar o instalador NSIS do Universal Converter

echo Universal Converter - Build Installer
echo =====================================

REM Verificar se o NSIS está instalado
where makensis >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: NSIS não encontrado!
    echo Por favor, instale o NSIS de: https://nsis.sourceforge.io/Download
    echo Certifique-se de que makensis.exe está no PATH do sistema
    pause
    exit /b 1
)

echo ✓ NSIS encontrado

REM Verificar se o executável foi compilado
if not exist "dist\UniversalConverter.exe" (
    echo ERRO: Executável não encontrado!
    echo Execute primeiro: python build_executable.py
    pause
    exit /b 1
)

echo ✓ Executável encontrado

REM Criar diretório resources se não existir
if not exist "resources" mkdir resources

REM Verificar se os recursos existem (criar placeholders se necessário)
if not exist "resources\icon.ico" (
    echo Aviso: Ícone não encontrado em resources\icon.ico
    echo Usando ícone padrão...
)

if not exist "resources\header.bmp" (
    echo Aviso: Header image não encontrada em resources\header.bmp
)

if not exist "resources\welcome.bmp" (
    echo Aviso: Welcome image não encontrada em resources\welcome.bmp
)

echo.
echo Compilando instalador NSIS...
makensis /V3 installer.nsi

if %errorlevel% equ 0 (
    echo.
    echo ✓ Instalador compilado com sucesso!
    echo Arquivo criado: UniversalConverter-1.0.0-Setup.exe
    echo.
    echo Tamanho do arquivo:
    for %%I in (UniversalConverter-1.0.0-Setup.exe) do echo %%~zI bytes
    echo.
    echo O instalador está pronto para distribuição!
) else (
    echo.
    echo ✗ Erro ao compilar o instalador
    echo Verifique os erros acima
)

pause