# Start of the installation script for the srt-translator Python application

Write-Host "Starting installation..." -ForegroundColor Green

# Check if conda is installed
if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    Write-Host "Conda is not installed. Please install Anaconda or Miniconda first." -ForegroundColor Red
    exit 1
}

# Define the environment name
$envName = "srt-translator"

# Check if the environment already exists
$envList = conda env list | Select-String $envName
if ($envList) {
    Write-Host "The environment '$envName' already exists." -ForegroundColor Yellow
} else {
    # Create the conda environment with Python 3.11
    conda create --yes --name $envName python=3.11
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error creating the environment." -ForegroundColor Red
        exit 1
    }
}

# Activate the environment
conda activate $envName
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error activating the environment." -ForegroundColor Red
    exit 1
}

# Install Python dependencies from requirements.txt
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error installing dependencies." -ForegroundColor Red
    exit 1
}

Write-Host "Installation completed successfully." -ForegroundColor Green
Write-Host "Put your srt files into batch/todo and execute the run PowerShell script. Enter your DeepL API key on first launch. Have fun!" -ForegroundColor Yellow