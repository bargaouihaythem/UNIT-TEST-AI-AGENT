"""Test de la génération 100% IA avec Ollama"""
from smart_test_generator import SmartTestGenerator
import os

# Code Java exemple simple
java_code = """
public class Calculator {
    
    public int add(int a, int b) {
        return a + b;
    }
    
    public int subtract(int a, int b) {
        return a - b;
    }
    
    public int divide(int a, int b) {
        if (b == 0) {
            throw new IllegalArgumentException("Cannot divide by zero");
        }
        return a / b;
    }
}
"""

def test_generation_with_ai():
    """Test génération avec IA activée"""
    print("\n" + "="*60)
    print("TEST 1: Génération avec IA Ollama (use_ai=True)")
    print("="*60)
    
    generator = SmartTestGenerator(java_code, "Calculator.java", use_ai=True)
    tests_ai = generator.generate()
    
    # Sauvegarder
    with open("CalculatorTest_AI.java", "w", encoding="utf-8") as f:
        f.write(tests_ai)
    
    print(f"\n✅ Tests générés avec IA ({len(tests_ai)} caractères)")
    print(f"📄 Fichier: CalculatorTest_AI.java")
    print("\n--- APERÇU (100 premiers caractères) ---")
    print(tests_ai[:200])
    print("\n")

def test_generation_without_ai():
    """Test génération avec templates (fallback)"""
    print("\n" + "="*60)
    print("TEST 2: Génération avec templates (use_ai=False)")
    print("="*60)
    
    generator = SmartTestGenerator(java_code, "Calculator.java", use_ai=False)
    tests_template = generator.generate()
    
    # Sauvegarder
    with open("CalculatorTest_Template.java", "w", encoding="utf-8") as f:
        f.write(tests_template)
    
    print(f"\n✅ Tests générés avec templates ({len(tests_template)} caractères)")
    print(f"📄 Fichier: CalculatorTest_Template.java")
    print("\n--- APERÇU (100 premiers caractères) ---")
    print(tests_template[:200])
    print("\n")

def compare_results():
    """Compare les deux approches"""
    print("\n" + "="*60)
    print("COMPARAISON IA vs TEMPLATES")
    print("="*60)
    
    if os.path.exists("CalculatorTest_AI.java") and os.path.exists("CalculatorTest_Template.java"):
        size_ai = os.path.getsize("CalculatorTest_AI.java")
        size_template = os.path.getsize("CalculatorTest_Template.java")
        
        print(f"📊 Taille fichier IA:       {size_ai} octets")
        print(f"📊 Taille fichier Template: {size_template} octets")
        print(f"📊 Différence:              {abs(size_ai - size_template)} octets")
        
        if size_ai > size_template:
            print(f"\n✨ L'IA génère {((size_ai/size_template - 1) * 100):.1f}% plus de contenu")
        else:
            print(f"\n📝 Les templates génèrent {((size_template/size_ai - 1) * 100):.1f}% plus de contenu")
    
    print("\n")

if __name__ == "__main__":
    try:
        # Test 1: Avec IA
        test_generation_with_ai()
        
        # Test 2: Sans IA (templates)
        test_generation_without_ai()
        
        # Comparaison
        compare_results()
        
        print("="*60)
        print("✅ TOUS LES TESTS RÉUSSIS!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
