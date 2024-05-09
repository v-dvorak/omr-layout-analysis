########## RESOLVE PATH TEMPORARILY COPIED HERE
# # Get the first argument provided to the script
# $firstArgument = $args[0]
#
# # Resolve the absolute path of the first argument
# $resolvedPath = Resolve-Path -Path $firstArgument
#
# # Print the resolved absolute path
# Write-Output "Resolved absolute path: $resolvedPath"

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
python3 -m app download

# FINALLY
# revert to original directory
Pop-Location
