# PowerShell script to set up and run the weather portal

# Define project directory (optional, assumes script is run from project root)
# $ProjectDir = $PSScriptRoot

Write-Host "Setting up Python virtual environment..."

# Check if .venv exists, create if not
if (-not (Test-Path .venv -PathType Container)) {
    Write-Host "Creating virtual environment '.venv'..."
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment. Please ensure Python is installed and accessible."
        exit 1
    }
}

Write-Host "Activating virtual environment..."
# PowerShell specific activation
. .\.venv\Scripts\Activate.ps1

# Check if the VIRTUAL_ENV environment variable is set.
if (-not $env:VIRTUAL_ENV) {
    Write-Error "Failed to activate virtual environment. VIRTUAL_ENV not set."
    exit 1
}
# Optional: Check if it points to the correct path
$ExpectedVenvPath = (Resolve-Path ".\\.venv").Path
if ($env:VIRTUAL_ENV -ne $ExpectedVenvPath) {
    Write-Warning "VIRTUAL_ENV ('$($env:VIRTUAL_ENV)') does not match expected path ('$ExpectedVenvPath'). This might be okay if nested."
} else {
    Write-Host "Virtual environment activated: $env:VIRTUAL_ENV"
}

Write-Host "Installing dependencies from requirements.txt..."
$PipExe = Join-Path $env:VIRTUAL_ENV "Scripts\\pip.exe"
Write-Host "Using pip at: $PipExe"
& $PipExe install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install dependencies using '$PipExe'. Please check requirements.txt and network connection."
    exit 1
}

Write-Host "Starting Weather Portal with Waitress on http://localhost:8080 ..."
Write-Host "Press CTRL+C to stop the server."

# Run Waitress server
# The --call argument tells waitress to find the 'app' object within the 'serve_protected' module
$WaitressServeExe = Join-Path $env:VIRTUAL_ENV "Scripts\\waitress-serve.exe"
Write-Host "Using waitress-serve at: $WaitressServeExe"
& $WaitressServeExe --host=127.0.0.1 --port=8080 serve_protected:app

# Deactivate virtual environment when server stops (Ctrl+C)
# Note: This part might not execute if Ctrl+C terminates the script abruptly.
# For robust deactivation, users might need to manually run 'deactivate' in their terminal.
Write-Host "Server stopped. Deactivating virtual environment (if possible in script context)."
# Attempt to deactivate - this command might not be available or work as expected when script exits
if (Get-Command deactivate -ErrorAction SilentlyContinue) {
    deactivate
}

Write-Host "Setup complete. If the server is running, access it at http://localhost:8080"
