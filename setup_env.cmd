@echo off
rem pushd %~dp0..

py -3 -c "import sys; assert sys.version_info >= (3, 7), 'Python version must be 3.7 or newer!'"

if %ERRORLEVEL% equ 9009 (
    echo ERROR: Python Launcher py.exe not installed. Install the latest Python 3 version.
    goto :END
)
if %ERRORLEVEL% neq 0 (
    goto :END
)

if not exist .env (
    echo Creating and activating Python virtual environment...
    py -3 -m venv .env || goto :END
    call .env\scripts\activate.bat || goto :END
    echo Installing dependencies, with additional pip install args [%*]...
    echo.
    python -m pip install %* --upgrade pip || goto :END
    if exist requirements.txt pip install %* --upgrade -r requirements.txt || goto :END
    python --version
) else (
    call .env\scripts\activate.bat || goto :END
    python --version
)

:END
popd
echo on
exit /b %ERRORLEVEL%
