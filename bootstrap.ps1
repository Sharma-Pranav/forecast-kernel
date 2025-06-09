# ./bootstrap.ps1

Write-Host "🚀 Bootstrapping Forecast-Kernel Environment..."

# Step 1: Create virtual environment if missing
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Creating .venv using uv..."
    uv venv --python=3.10 .venv
} else {
    Write-Host "📦 .venv already exists, skipping..."
}

# Step 2: Activate environment
Write-Host "🔄 Activating .venv..."
. .venv\Scripts\Activate.ps1

# Step 3: Install dependencies
Write-Host "📦 Installing dependencies from requirements.txt..."
uv pip install -r requirements.txt

# Step 4: Install package in editable mode
Write-Host "🔧 Installing forecastkernel in editable mode..."
pip install -e .

# Step 5: Run hello test
Write-Host "🧪 Running hello test..."
python -m forecastkernel.scripts.hello

# Step 6: Run Phase 1 forecast
Write-Host "📊 Running Phase 1 forecast baseline..."
python -m forecastkernel.scripts.baseline_sf `
  --data data/raw/univariate_example.csv `
  --horizon 14 `
  --tag demo `
  --phase 1

# Step 7: Validate CI runtime
Write-Host "🛡️ Running CI runtime test..."
python -m forecastkernel.tests.test_ci_runtime `
  --run_dir data/outputs/baseline/demo `
  --data data/raw/univariate_example.csv

# Step 8: Run hash audit
Write-Host "🔐 Validating file hashes..."
python -m forecastkernel.utils.ci_utils `
  --audit_log data/outputs/baseline/demo/audit_log.json `
  --output_dir data/outputs/baseline/demo

# Step 9: Generate visual delta comparison
Write-Host "🖼️ Generating visual delta audit..."
python -m forecastkernel.scripts.visual_delta_audit `
  --output_path data/outputs/baseline/demo

Write-Host "✅ Bootstrap complete."
