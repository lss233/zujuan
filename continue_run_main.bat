@echo off
:str
python main.py
if %errorlevel%==0 (
goto end_bat
) else (
echo �ȴ��û���Ӧ 5s���Զ�����
ping -n 5 127.0 >null
goto str
)
:end_bat