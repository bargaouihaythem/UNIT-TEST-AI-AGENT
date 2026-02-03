"""Test rapide de génération IA"""

# Code très simple
CODE = """
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
}
"""

print("🚀 Test de génération avec IA Ollama")
print("="*50)

from smart_test_generator import SmartTestGenerator

generator = SmartTestGenerator(CODE, "Calculator.java", use_ai=True)
print("✅ Generator créé")

tests = generator.generate()
print("\n📝 Tests générés:")
print("="*50)
print(tests)
print("="*50)
print(f"\n✅ Total: {len(tests)} caractères")
