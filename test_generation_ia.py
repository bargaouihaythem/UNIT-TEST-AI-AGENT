"""Test de génération avec et sans IA"""
from smart_test_generator import SmartTestGenerator

# Code simple à tester
code = """
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
    
    public int divide(int a, int b) {
        if (b == 0) {
            throw new IllegalArgumentException("Cannot divide by zero");
        }
        return a / b;
    }
}
"""

print("=" * 80)
print("TEST 1: Génération SANS IA (templates seulement)")
print("=" * 80)
try:
    gen1 = SmartTestGenerator(code, "Calculator.java", use_ai=False)
    test1 = gen1.generate()
    print(f"✅ Succès! Taille: {len(test1)} caractères")
    with open("Calculator_SANS_IA_Test.java", "w") as f:
        f.write(test1)
    print("📁 Sauvegardé: Calculator_SANS_IA_Test.java")
except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n" + "=" * 80)
print("TEST 2: Génération AVEC IA Ollama")
print("=" * 80)
try:
    gen2 = SmartTestGenerator(code, "Calculator.java", use_ai=True)
    test2 = gen2.generate()
    print(f"✅ Succès! Taille: {len(test2)} caractères")
    with open("Calculator_AVEC_IA_Test.java", "w") as f:
        f.write(test2)
    print("📁 Sauvegardé: Calculator_AVEC_IA_Test.java")
    
    # Afficher la différence
    if len(test2) > len(test1):
        diff = len(test2) - len(test1)
        print(f"\n🤖 L'IA a ajouté {diff} caractères de suggestions!")
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("🎉 Tests terminés!")
print("=" * 80)
