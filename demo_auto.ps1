# 🎯 Script de Démonstration Rapide

# Couleurs pour le terminal
$SUCCESS = @{ ForegroundColor = 'Green' }
$INFO = @{ ForegroundColor = 'Cyan' }
$WARNING = @{ ForegroundColor = 'Yellow' }
$ERROR = @{ ForegroundColor = 'Red' }

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "   Démonstration - Générateur de Tests IA" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Étape 1
Write-Host "[Étape 1/4] Vérification de l'installation..." @INFO
try {
    $null = ut --help 2>&1
    Write-Host "  ✅ Commande 'ut' disponible`n" @SUCCESS
} catch {
    Write-Host "  ❌ Erreur: La commande 'ut' n'est pas installée`n" @ERROR
    exit 1
}

# Étape 2
Write-Host "[Étape 2/4] Nettoyage..." @INFO
if (Test-Path "ut_output/test_*.py") {
    Remove-Item ut_output/test_*.py -Force
    Write-Host "  ✅ Anciens tests supprimés`n" @SUCCESS
} else {
    Write-Host "  ℹ️  Aucun ancien test`n" @INFO
}

# Étape 3
Write-Host "[Étape 3/4] EXEMPLE SIMPLE (converter.py)..." @INFO
Write-Host "  ⏳ Génération..." @WARNING
"y" | ut generate example/converter.py 2>&1 | Out-Null
Write-Host "  ✅ Généré!`n" @SUCCESS
Write-Host "  📊 Exécution des tests:`n" @INFO
python -m pytest ut_output/test_converter.py -v --tb=short
Write-Host "`n"
Read-Host "Appuyez sur Entrée pour continuer"

# Étape 4
Write-Host "[Étape 4/4] EXEMPLE COMPLEXE (calculator.py)..." @INFO
Write-Host "  ⏳ Génération..." @WARNING
"y" | ut generate demo/calculator.py 2>&1 | Out-Null
Write-Host "  ✅ Généré!`n" @SUCCESS
Write-Host "  📊 Exécution des tests:`n" @INFO
python -m pytest ut_output/test_calculator.py -v --tb=short
Write-Host "`n"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Démonstration terminée !" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "`n📁 Fichiers: ut_output/"
Write-Host "📖 Guide: DEMO_GUIDE.md`n"
