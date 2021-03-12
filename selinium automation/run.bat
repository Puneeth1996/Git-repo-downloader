set /p searcKey="Please enter Search Term in quotes( Eg. 'Big Data'):"
@REM set str=%searcKey:-=%
python repos.py %searcKey%
pause
