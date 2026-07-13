@echo off
echo Instalando dependencias necesarias...
pip install pyinstaller waitress

echo.
echo Limpiando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist AduanasApp.spec del AduanasApp.spec

echo.
echo Construyendo el ejecutable AduanasApp.exe...
pyinstaller --name "AduanasApp" ^
            --onefile ^
            --add-data "templates;templates" ^
            --add-data "static;static" ^
            --add-data ".env;." ^
            --hidden-import "waitress" ^
            --hidden-import "flask_sqlalchemy" ^
            --hidden-import "flask_login" ^
            --hidden-import "flask_wtf" ^
            --hidden-import "wtforms" ^
            --hidden-import "sqlite3" ^
            run.py

echo.
echo ==============================================================
echo Construccion completada.
echo El ejecutable se encuentra en la carpeta "dist".
echo ==============================================================
pause
