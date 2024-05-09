    # PARSE ARGUMENTS
    $ProcessedFiles = @()
    $Files = @()

    # Print out help and exit
    if ("-h" -in $args -or "--help" -in $args) {
        python3 -m app.Predictions -h
        exit 0
    }

    # Extract file names
    foreach ($Arg in $args) {
        if ($Arg -notin ("-o", "--output",
                         "-m", "--model",
                         "-v", "--verbose")) {
            $Files += $Arg
        }
    }

    # Extract model path, output path, and verbose flag
    $OutputIndex = $args.IndexOf("-o") + $args.IndexOf("--output")
    $ModelIndex = $args.IndexOf("-m") + $args.IndexOf("--model")
    $VerboseIndex = $args.IndexOf("-v") + $args.IndexOf("--verbose")

    $OutputPath = ""
    if ($OutputIndex -ge 0) {
        New-Item -ItemType File -Force -Path $args[$OutputIndex + 2] | Out-Null
        $OutputPath = (Resolve-Path $args[$OutputIndex + 2]).Path
    }

    $ModelPath = if ($ModelIndex -ge 0) { (Resolve-Path $args[$ModelIndex + 2]).Path }
    $Verbose = $VerboseIndex -ge 0

    # Resolve path to absolute path (allow the script to load them when in different WD)
    foreach ($File in $Files) {
        $temp = (Resolve-Path $File).Path
        if ($temp -notin ($ModelPath, $OutputPath)) {
            $ProcessedFiles += (Resolve-Path $File).Path
        }
    }

    # Set up args for Python call
    $Arguments = @()

    foreach ($File in $ProcessedFiles) {
        $Arguments += $File
    }

    if ($OutputIndex -ge 0) {
        $Arguments += "-o $OutputPath"
    }
    if ($ModelIndex -ge 0) {
        $Arguments += "-m $ModelPath"
    }
    if ($Verbose) {
        $Arguments += "-v"
    }

    # Write-Host $Arguments

    # INIT SWITCH TO OTHER WD
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
    python3 -m app.Predictions $Arguments

    # FINALLY
    # revert to original directory
    Pop-Location
