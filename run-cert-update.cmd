@echo off
setlocal
cd /d "%~dp0"
py update_cert_data.py
endlocal
