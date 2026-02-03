@echo off
REM ========================================
REM Script de Démonstration Automatique
REM ========================================

echo.
echo ============================================
echo    Démonstration - Générateur de Tests IA
echo ============================================
echo.

REM Étape 1 : Vérifier l'installation
echo [Étape 1/4] Vérification de l'installation...
ut --help >nul 2>&1
if %errorlevel% neq 0 (
    echo   ❌ Erreur: La commande 'ut' n'est pas installée
    exit /b 1
)
echo   ✅ Commande 'ut' disponible
echo.

REM Étape 2 : Nettoyer les anciens tests
echo [Étape 2/4] Nettoyage des anciens tests...
if exist ut_output\test_*.py (
    del /Q ut_output\test_*.py >nul 2>&1
    echo   ✅ Anciens tests supprimés
) else (
    echo   ℹ️  Aucun ancien test à supprimer
)
echo.

REM Étape 3 : Générer les tests pour l'exemple simple
echo [Étape 3/4] Génération des tests - Exemple SIMPLE (converter.py)...
echo   ⏳ Génération en cours...
echo y | ut generate example/converter.py >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✅ Tests générés avec succès
    echo.
    echo   📊 Exécution des tests...
    python -m pytest ut_output/test_converter.py -v --tb=short
) else (
    echo   ❌ Erreur lors de la génération
)
echo.
pause

REM Étape 4 : Générer les tests pour l'exemple complexe
echo [Étape 4/4] Génération des tests - Exemple COMPLEXE (calculator.py)...
echo   ⏳ Génération en cours...
echo y | ut generate demo/calculator.py >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✅ Tests générés avec succès
    echo.
    echo   📊 Exécution des tests...
    python -m pytest ut_output/test_calculator.py -v --tb=short
) else (
    echo   ❌ Erreur lors de la génération
)
echo.

echo ============================================
echo    Démonstration terminée !
echo ============================================
echo.
echo 📁 Fichiers générés dans: ut_output/
echo 📖 Guide complet: DEMO_GUIDE.md
echo.
pause
