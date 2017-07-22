@echo off
:str
python main.py
if %errorlevel%==0 (
goto end_bat
) else (
echo 等待用户响应 5s后自动重启
ping -n 5 127.0 >null
goto str
)
:end_bat