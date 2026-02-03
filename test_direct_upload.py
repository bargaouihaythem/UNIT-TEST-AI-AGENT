"""Test direct de l'upload via Python requests."""
import requests

# Lire le fichier TestSimple.java
with open('TestSimple.java', 'rb') as f:
    files = {'file': ('TestSimple.java', f, 'text/plain')}
    
    print("📤 Envoi de TestSimple.java au serveur...")
    response = requests.post('http://127.0.0.1:5000/upload', files=files)
    
    print(f"\n📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Upload réussi !")
            print(f"📝 Tests générés: {len(data.get('test_content', ''))} chars")
            print(f"📊 Stats: {data.get('stats')}")
        else:
            print(f"❌ Erreur: {data.get('error')}")
    else:
        print(f"❌ Erreur HTTP: {response.text}")
