# INIT
# store CWD
$currentDirectory = Get-Location
# load location of this script
$module_directory = $PSScriptRoot
$module_directory = Split-Path -Path $module_directory -Parent
# Change the working directory to the script directory temporarily
Push-Location $scriptDirectory

# ACT
# set working directory to this script location
Set-Location $module_directory
# set the PYTHONPATH environment variable to include the module directory
$env:PYTHONPATH = $module_directory
# run script
python3 -m app build

# FINALLY
# revert to original directory
Pop-Location
