# Run script for the srt-translator Python application

# Check if conda is installed
if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    Write-Host "Conda is not installed. Please install Anaconda or Miniconda first." -ForegroundColor Red
    exit 1
}

# Define the environment name
$envName = "srt-translator"

# Check if the environment exists
$envList = conda env list | Select-String $envName
if (-not $envList) {
    Write-Host "The environment '$envName' does not exist. Please run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Activate the conda environment
conda activate $envName

# Run the Python application
python srt-translator.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error running srt-translator.py." -ForegroundColor Red
}

# Wait for user input before closing
Write-Host -NoNewLine 'Press any key to continue...' -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')