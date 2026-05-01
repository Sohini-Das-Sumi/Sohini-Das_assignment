Write-Host "🧪 Testing Trinethra API..." -ForegroundColor Green

# Health
try {
    $health = iwr "http://localhost:5000/health" -Method GET
    Write-Host "✅ Health: $($health.Content)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health failed: $_" -ForegroundColor Red
}

# API
try {
    $body = @{transcript="John is excellent!"} | ConvertTo-Json
    $api = iwr "http://localhost:5000/api/analyze_single" -Method POST -ContentType "application/json" -Body $body
    Write-Host "✅ API: Score = $($api.Content | ConvertFrom-Json | select -exp score.value)" -ForegroundColor Green
} catch {
    Write-Host "❌ API failed: $_" -ForegroundColor Red
}