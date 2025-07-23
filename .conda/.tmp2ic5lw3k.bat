@ECHO OFF
@SET PYTHONIOENCODING=utf-8
@SET PYTHONUTF8=1
@FOR /F "tokens=2 delims=:." %%A in ('chcp') do for %%B in (%%A) do set "_CONDA_OLD_CHCP=%%B"
@chcp 65001 > NUL
@CALL "C:\Users\hp\anaconda3\condabin\conda.bat" activate "c:\Users\hp\COURSE\SISTECH\PP_MachineLearningOperations_TalithaRahmadewatiW\FINAL PROJECT\.conda"
@IF %ERRORLEVEL% NEQ 0 EXIT /b %ERRORLEVEL%
@"c:\Users\hp\COURSE\SISTECH\PP_MachineLearningOperations_TalithaRahmadewatiW\FINAL PROJECT\.conda\python.exe" -Wi -m compileall -q -l -i C:\Users\hp\AppData\Local\Temp\tmp9v6x25fo -j 0
@IF %ERRORLEVEL% NEQ 0 EXIT /b %ERRORLEVEL%
@chcp %_CONDA_OLD_CHCP%>NUL
