@echo off

SET PYTHONPATH=./

python automeetingsheet/main.py

SET RESULT=%ERRORLEVEL%

if %RESULT% == 0 (
  start output/generate.pdf
)
