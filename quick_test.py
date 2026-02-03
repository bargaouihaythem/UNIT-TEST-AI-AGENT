"""Test rapide de la génération avec IA"""

print("🚀 Test rapide de génération")

# Code simple
code = """
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
}
"""

print("\n1️⃣ Import du générateur...")
from smart_test_generator import SmartTestGenerator

print("2️⃣ Création du générateur AVEC IA...")
gen = SmartTestGenerator(code, "Calculator.java", use_ai=True)

print("3️⃣ Génération des tests...")
result = gen.generate()

print("\n✅ RÉSULTAT:")
print("="*60)
print(result[:800])
print("="*60)
print(f"\n📊 Taille: {len(result)} caractères")
print("✨ Test terminé!")
