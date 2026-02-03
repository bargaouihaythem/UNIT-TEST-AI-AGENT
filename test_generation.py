"""Script de test pour démontrer la génération avec et sans IA"""
import os
import time

# Code Java simple pour tester
JAVA_CODE = """
public class Calculator {
    
    public int add(int a, int b) {
        return a + b;
    }
    
    public int subtract(int a, int b) {
        return a - b;
    }
    
    public long multiply(long a, long b) {
        return a * b;
    }
}
"""

def test_without_ai():
    """Test génération SANS IA"""
    print("\n" + "="*60)
    print("TEST 1: Génération SANS IA (rapide)")
    print("="*60)
    
    from smart_test_generator import SmartTestGenerator
    
    start = time.time()
    generator = SmartTestGenerator(JAVA_CODE, "Calculator.java", use_ai=False)
    tests = generator.generate()
    elapsed = time.time() - start
    
    print(f"\n✅ Tests générés en {elapsed:.2f}s")
    print(f"📄 Taille: {len(tests)} caractères")
    print(f"\n--- EXTRAIT DES TESTS GÉNÉRÉS ---")
    print(tests[:500] + "...\n")
    
    # Sauvegarder
    output_path = "test_output_without_ai.java"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(tests)
    print(f"✅ Sauvegardé: {output_path}")
    
    return tests

def test_with_ai():
    """Test génération AVEC IA"""
    print("\n" + "="*60)
    print("TEST 2: Génération AVEC IA (amélioration intelligente)")
    print("="*60)
    
    from smart_test_generator import SmartTestGenerator
    
    start = time.time()
    generator = SmartTestGenerator(JAVA_CODE, "Calculator.java", use_ai=True)
    tests = generator.generate()
    elapsed = time.time() - start
    
    print(f"\n✅ Tests générés et améliorés par IA en {elapsed:.2f}s")
    print(f"📄 Taille: {len(tests)} caractères")
    
    # Chercher le bloc de suggestions IA
    if "SUGGESTIONS IA" in tests:
        print(f"\n🤖 L'IA a ajouté des suggestions!")
        # Extraire le bloc IA
        start_idx = tests.find("SUGGESTIONS IA")
        end_idx = tests.find("*/", start_idx) + 2
        ai_block = tests[start_idx:end_idx]
        print("\n--- SUGGESTIONS IA ---")
        print(ai_block[:800] + "...\n")
    else:
        print(f"\n--- EXTRAIT DES TESTS GÉNÉRÉS ---")
        print(tests[:500] + "...\n")
    
    # Sauvegarder
    output_path = "test_output_with_ai.java"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(tests)
    print(f"✅ Sauvegardé: {output_path}")
    
    return tests

def compare_results(tests_no_ai, tests_with_ai):
    """Comparer les deux résultats"""
    print("\n" + "="*60)
    print("COMPARAISON")
    print("="*60)
    
    print(f"\nSans IA: {len(tests_no_ai)} caractères")
    print(f"Avec IA: {len(tests_with_ai)} caractères")
    print(f"Différence: +{len(tests_with_ai) - len(tests_no_ai)} caractères")
    
    has_ai_suggestions = "SUGGESTIONS IA" in tests_with_ai
    print(f"\n🤖 Suggestions IA ajoutées: {'✅ OUI' if has_ai_suggestions else '❌ NON'}")
    
    if has_ai_suggestions:
        print("\n✨ La version IA contient des suggestions intelligentes pour:")
        print("   - Edge cases spécifiques")
        print("   - Améliorations des tests")
        print("   - Cas limites à tester")

if __name__ == "__main__":
    print("\n🧪 TEST DE GÉNÉRATION DE TESTS UNITAIRES")
    print("=" * 60)
    
    try:
        # Test 1: Sans IA
        tests_no_ai = test_without_ai()
        
        # Test 2: Avec IA
        tests_with_ai = test_with_ai()
        
        # Comparaison
        compare_results(tests_no_ai, tests_with_ai)
        
        print("\n" + "="*60)
        print("✅ TOUS LES TESTS RÉUSSIS!")
        print("="*60)
        print("\nFichiers générés:")
        print("  - test_output_without_ai.java (génération classique)")
        print("  - test_output_with_ai.java (génération améliorée par IA)")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
