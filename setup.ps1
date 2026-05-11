# EvolveAI Setup Script (PowerShell)
# Kullanım: .\setup.ps1
# PowerShell'de && çalışmadığı için her komut ayrı satırda.

Write-Host "=== EvolveAI Setup ===" -ForegroundColor Cyan
Write-Host ""

# 1. Conda kontrolü
Write-Host "Step 1: Conda check" -ForegroundColor Yellow
$condaVersion = conda --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Conda not found. Anaconda/Miniconda yükle." -ForegroundColor Red
    exit 1
}
Write-Host "OK: $condaVersion" -ForegroundColor Green

# 2. Environment oluştur
Write-Host ""
Write-Host "Step 2: Creating conda environment 'evolveai'" -ForegroundColor Yellow
conda env list | Select-String "evolveai"
if ($LASTEXITCODE -eq 0) {
    Write-Host "WARNING: 'evolveai' ortamı zaten var. Silmek için: conda env remove -n evolveai" -ForegroundColor Yellow
} else {
    conda env create -f environment.yml
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Environment creation failed." -ForegroundColor Red
        exit 1
    }
}

# 3. Activate ve PyTorch CUDA test
Write-Host ""
Write-Host "Step 3: Activating environment and testing PyTorch CUDA" -ForegroundColor Yellow
conda activate evolveai
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU only\"}')"

# 4. Config sanity check
Write-Host ""
Write-Host "Step 4: Config sanity check" -ForegroundColor Yellow
python config.py

# 5. Smoke tests
Write-Host ""
Write-Host "Step 5: Smoke tests" -ForegroundColor Yellow
pytest tests/test_smoke.py -v

# 6. Klasörleri oluştur
Write-Host ""
Write-Host "Step 6: Output directories" -ForegroundColor Yellow
$dirs = @("checkpoints", "replays", "logs", "logs/tensorboard")
foreach ($d in $dirs) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Path $d | Out-Null
        Write-Host "Created: $d" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Cyan
Write-Host "Next: python train.py --stage qlearning" -ForegroundColor Green
Write-Host "Or:   python -m app.main_app" -ForegroundColor Green
