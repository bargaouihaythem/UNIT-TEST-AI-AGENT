"""Script de test pour vérifier Ollama et les nouvelles fonctionnalités IA."""
import sys
import requests
import json

def test_ollama_installation():
    """Teste si Ollama est installé et fonctionne."""
    print("=" * 70)
    print("🧪 TEST 1: Installation Ollama")
    print("=" * 70)
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print("✅ Ollama est installé et lancé")
            print(f"📦 Modèles disponibles: {len(models)}")
            for model in models:
                print(f"   - {model['name']}")
            return True
        else:
            print("❌ Ollama répond mais avec une erreur")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Ollama n'est pas lancé")
        print("💡 Solution: Lance 'ollama serve' dans un terminal")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_ollama_client():
    """Teste le client Ollama Python."""
    print("\n" + "=" * 70)
    print("🧪 TEST 2: Client Python Ollama")
    print("=" * 70)
    
    try:
        from ollama_client import OllamaClient
        
        client = OllamaClient()
        
        if not client.available:
            print("❌ Client créé mais Ollama non disponible")
            return False
        
        print(f"✅ Client Ollama créé")
        print(f"🤖 Modèle: {client.model}")
        print(f"🌐 URL: {client.base_url}")
        
        return True
    except ImportError:
        print("❌ Module ollama_client non trouvé")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_explain_code():
    """Teste la fonctionnalité 'Explain Code'."""
    print("\n" + "=" * 70)
    print("🧪 TEST 3: Explain Code")
    print("=" * 70)
    
    try:
        from ollama_client import OllamaClient
        
        client = OllamaClient()
        
        if not client.available:
            print("⚠️  Sauté (Ollama non disponible)")
            return False
        
        code = """
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
}
"""
        
        print("📝 Code à expliquer:")
        print(code)
        print("\n🤖 Génération de l'explication...")
        
        explanation = client.explain_code(code, "java")
        
        if explanation and len(explanation) > 50:
            print("✅ Explication générée:")
            print(explanation[:200] + "...")
            return True
        else:
            print("❌ Explication vide ou trop courte")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_detect_bugs():
    """Teste la fonctionnalité 'Detect Bugs'."""
    print("\n" + "=" * 70)
    print("🧪 TEST 4: Detect Bugs")
    print("=" * 70)
    
    try:
        from ollama_client import OllamaClient
        
        client = OllamaClient()
        
        if not client.available:
            print("⚠️  Sauté (Ollama non disponible)")
            return False
        
        code = """
public void processUser(User user) {
    String name = user.getName().toLowerCase();
    System.out.println(name);
}
"""
        
        print("📝 Code à analyser (avec bug potentiel):")
        print(code)
        print("\n🤖 Détection de bugs...")
        
        bugs = client.detect_bugs(code, "java")
        
        if bugs and len(bugs) > 30:
            print("✅ Bugs détectés:")
            print(bugs[:200] + "...")
            return True
        else:
            print("❌ Aucun bug détecté ou réponse vide")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_api_endpoints():
    """Teste les endpoints API du serveur Flask."""
    print("\n" + "=" * 70)
    print("🧪 TEST 5: API Endpoints")
    print("=" * 70)
    
    print("⚠️  Lance d'abord 'python web_app_demo.py' dans un autre terminal")
    input("Appuie sur ENTER quand le serveur est lancé...")
    
    try:
        # Test /ai/status
        print("\n📡 Test: /ai/status")
        response = requests.get("http://127.0.0.1:5000/ai/status", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test /ai/explain
        print("\n📡 Test: /ai/explain")
        response = requests.post(
            "http://127.0.0.1:5000/ai/explain",
            json={
                "code": "public int add(int a, int b) { return a + b; }",
                "language": "java"
            },
            timeout=60
        )
        print(f"   Status: {response.status_code}")
        result = response.json()
        if result.get('success'):
            print(f"   ✅ Explication: {result['explanation'][:100]}...")
        else:
            print(f"   ❌ Erreur: {result.get('error')}")
        
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Serveur Flask non lancé")
        print("💡 Lance: python web_app_demo.py")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def main():
    """Lance tous les tests."""
    print("\n" + "🧪" * 35)
    print("TESTS OLLAMA - Fonctionnalités IA Gratuites")
    print("🧪" * 35 + "\n")
    
    results = {
        "Ollama Installation": test_ollama_installation(),
        "Client Python": test_ollama_client(),
        "Explain Code": test_explain_code(),
        "Detect Bugs": test_detect_bugs(),
        "API Endpoints": test_api_endpoints()
    }
    
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    print("\n" + "=" * 70)
    print(f"🎯 Score: {passed}/{total} tests réussis")
    
    if passed == total:
        print("✅ Tous les tests passent! Ton projet est prêt! 🚀")
    elif passed >= 3:
        print("⚠️  Quelques tests échouent, mais c'est OK pour la démo")
    else:
        print("❌ Plusieurs tests échouent. Vérifie l'installation Ollama")
        print("\n💡 SOLUTIONS:")
        print("   1. Installe Ollama: https://ollama.com/download")
        print("   2. Télécharge un modèle: ollama pull llama3")
        print("   3. Lance Ollama: ollama serve")
        print("   4. Relance ces tests: python test_ollama.py")
    
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
