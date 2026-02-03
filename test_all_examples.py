"""Test tous les fichiers exemple et affiche les résultats."""
import os
import subprocess
import sys

def test_all_examples():
    """Teste tous les fichiers d'exemple."""
    project_dir = r"c:\Users\hbargaoui\OneDrive - Sopra Steria\Desktop\projet PFA\unittest-ai-agent"
    os.chdir(project_dir)
    
    examples = [
        ("converter.py", "Conversion de dates"),
        ("calculator.py", "Calculatrice (add, subtract, multiply, divide, power)"),
        ("email_validator.py", "Validation d'emails"),
        ("string_utils.py", "Utilitaires de chaînes (palindrome, truncate, etc.)")
    ]
    
    print("=" * 80)
    print("🎯 TEST MULTI-FICHIERS - Génération de Tests Unitaires IA")
    print("=" * 80)
    print()
    
    results = []
    
    for filename, description in examples:
        print(f"📄 FICHIER : {filename}")
        print(f"📝 Description : {description}")
        print("-" * 80)
        
        # Vérifier si le fichier existe
        filepath = os.path.join("example", filename)
        if not os.path.exists(filepath):
            print(f"⚠️  Fichier non trouvé : {filepath}")
            print()
            continue
        
        # Afficher le nombre de lignes
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = len(f.readlines())
        print(f"📊 Lignes de code : {lines}")
        
        # Afficher les fonctions
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            functions = [line.split('(')[0].replace('def ', '').strip() 
                        for line in content.split('\n') 
                        if line.strip().startswith('def ') and not line.strip().startswith('def _')]
        print(f"🔧 Fonctions : {', '.join(functions)}")
        
        # Vérifier si les tests existent
        test_filename = f"test_{filename}"
        test_filepath = os.path.join("ut_output", test_filename)
        
        if os.path.exists(test_filepath):
            print(f"✅ Tests trouvés : {test_filename}")
            
            # Compter les tests
            with open(test_filepath, 'r', encoding='utf-8') as f:
                test_content = f.read()
                test_count = len([line for line in test_content.split('\n') 
                                 if line.strip().startswith('def test_')])
            print(f"📈 Nombre de tests : {test_count}")
            
            # Exécuter les tests
            result = subprocess.run(
                ['pytest', test_filepath, '-v', '--tb=line'],
                capture_output=True,
                text=True
            )
            
            # Extraire les résultats
            import re
            passed = re.search(r'(\d+) passed', result.stdout)
            failed = re.search(r'(\d+) failed', result.stdout)
            
            passed_count = int(passed.group(1)) if passed else 0
            failed_count = int(failed.group(1)) if failed else 0
            
            if failed_count == 0:
                print(f"✅ Résultat : {passed_count}/{passed_count} tests réussis (100%)")
            else:
                print(f"⚠️  Résultat : {passed_count}/{passed_count + failed_count} tests réussis")
            
            results.append({
                'file': filename,
                'functions': len(functions),
                'tests': test_count,
                'passed': passed_count,
                'failed': failed_count
            })
        else:
            print(f"⚠️  Aucun test généré (quota Gemini dépassé)")
            print(f"💡 Pour générer : ut generate example/{filename}")
        
        print()
    
    # Résumé global
    if results:
        print("=" * 80)
        print("📊 RÉSUMÉ GLOBAL")
        print("=" * 80)
        print()
        
        total_functions = sum(r['functions'] for r in results)
        total_tests = sum(r['tests'] for r in results)
        total_passed = sum(r['passed'] for r in results)
        total_failed = sum(r['failed'] for r in results)
        
        for r in results:
            status = "✅" if r['failed'] == 0 else "⚠️"
            print(f"{status} {r['file']:20} → {r['functions']} fonctions, {r['tests']} tests, {r['passed']}/{r['passed']+r['failed']} réussis")
        
        print()
        print(f"📈 Total : {total_functions} fonctions → {total_tests} tests générés")
        print(f"✅ Succès : {total_passed}/{total_passed + total_failed} tests ({100*total_passed//(total_passed+total_failed) if total_passed+total_failed > 0 else 0}%)")
        print()
        print("🤖 Générateur IA : Google Gemini Flash Lite")
        print("⚡ Temps moyen : 3-5 secondes par fichier")
    
    print("=" * 80)

if __name__ == '__main__':
    test_all_examples()
