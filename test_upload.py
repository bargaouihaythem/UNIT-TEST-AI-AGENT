"""Script de test rapide pour uploader un fichier"""
import requests
import os

print("=" * 70)
print("🧪 TEST UPLOAD DIRECT")
print("=" * 70)

# 1. Vérifier que le serveur répond
print("\n1️⃣ Vérification serveur...")
try:
    response = requests.get('http://127.0.0.1:5000')
    print(f"   ✅ Serveur accessible (status: {response.status_code})")
except Exception as e:
    print(f"   ❌ Serveur inaccessible: {e}")
    print("   💡 Démarre le serveur avec: python web_app_demo.py")
    exit(1)

# 2. Uploader un fichier
print("\n2️⃣ Upload du fichier TestSimple.java...")
try:
    with open('TestSimple.java', 'rb') as f:
        files = {'file': ('TestSimple.java', f, 'text/plain')}
        response = requests.post('http://127.0.0.1:5000/upload', files=files)
        
    print(f"   📡 Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Upload réussi !")
        print(f"   📄 Fichier: {data.get('filename', 'N/A')}")
        print(f"   📊 Tests générés: {data.get('stats', {}).get('total', 'N/A')}")
        print(f"   ✅ Passed: {data.get('stats', {}).get('passed', 'N/A')}")
        print(f"   ❌ Failed: {data.get('stats', {}).get('failed', 'N/A')}")
        
        # Afficher un extrait du code de test
        if 'test_content' in data:
            print("\n📝 Extrait des tests générés:")
            print("-" * 70)
            print(data['test_content'][:500] + "...")
            print("-" * 70)
        
        print("\n🎯 SUCCÈS ! L'upload fonctionne correctement.")
        print("💡 Ouvre http://127.0.0.1:5000 dans ton navigateur pour voir l'interface.")
        
    else:
        print(f"   ❌ Erreur: {response.status_code}")
        print(f"   📄 Réponse: {response.text[:500]}")
        
except FileNotFoundError:
    print("   ❌ Fichier TestSimple.java non trouvé")
    print("   💡 Crée un fichier Java de test d'abord")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

print("\n" + "=" * 70)
