set /p searcKey="Hit Search Term:"
@REM set str=%searcKey:-=%
python repos.py %searcKey%
pause
