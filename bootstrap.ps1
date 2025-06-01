# scripts/bootstrap.ps1

Write-Host "🚀 Bootstrapping Forecast-Kernel Environment..."

# Step 1: Create virtual environment
uv venv .venv

# Step 2: Activate it
.venv\Scripts\Activate.ps1

# Step 3: Install dependencies
uv pip install -r requirements.txt

# Step 4: Run hello test
python scripts/hello.py

Write-Host "✅ Bootstrap complete."


# Run it with # powershell -ExecutionPolicy Bypass -File scripts/env.ps1