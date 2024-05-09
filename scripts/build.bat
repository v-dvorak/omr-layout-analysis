@echo off
REM INIT
REM Store current working directory
set "currentDirectory=%cd%"
REM Get the directory of this script
for %%I in (%0) do set "scriptDirectory=%%~dpI"
REM Get the parent directory of the module directory
for %%I in ("%scriptDirectory%..") do set "scriptDirectory=%%~fI"

REM ACT
REM Set the working directory to the script location
cd /d "%scriptDirectory%"

REM Set the PYTHONPATH environment variable to include the module directory
set "PYTHONPATH=%scriptDirectory%"

REM Run the script
python3 -m app build

REM FINALLY
REM Revert to original directory
cd /d "%currentDirectory%"
