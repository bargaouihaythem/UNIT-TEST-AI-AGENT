# 🚀 Guide Installation Rapide - IA Gratuite Ollama

## ⏱️ Installation en 5 minutes

### 📥 Étape 1: Télécharger Ollama (2 min)

**Windows**:
1. Va sur: https://ollama.com/download
2. Clique sur "Download for Windows"
3. Lance l'installateur `OllamaSetup.exe`
4. Suis les instructions (Next → Next → Install)

### 🤖 Étape 2: Télécharger un modèle IA (2 min)

Ouvre **PowerShell** ou **CMD** et tape:

```powershell
ollama pull llama3
```

Ou pour un modèle plus léger (si tu as peu de RAM):

```powershell
ollama pull phi
```

**Temps d'attente**: 2-5 minutes (télécharge ~4GB)

### ▶️ Étape 3: Lancer Ollama (10 sec)

Dans PowerShell/CMD:

```powershell
ollama serve
```

Tu dois voir:
```
Ollama is running
```

**IMPORTANT**: Laisse cette fenêtre ouverte! Ollama tourne en arrière-plan.

### ✅ Étape 4: Vérifier l'installation (30 sec)

Dans un **NOUVEAU** PowerShell/CMD:

```powershell
cd "c:\Users\hbargaoui\OneDrive - Sopra Steria\Desktop\projet PFA\unittest-ai-agent"
python test_ollama.py
```

Tu dois voir:
```
✅ Ollama est installé et lancé
✅ Client Ollama créé
✅ Explication générée
✅ Bugs détectés
```

---

## 🎮 Lancer ton projet avec IA

### Méthode simple

1. **Terminal 1** (Ollama):
```powershell
ollama serve
```

2. **Terminal 2** (Ton projet):
```powershell
cd "c:\Users\hbargaoui\OneDrive - Sopra Steria\Desktop\projet PFA\unittest-ai-agent"
python web_app_demo.py
```

Tu verras:
```
🆓 NOUVELLES FONCTIONNALITÉS IA GRATUITES (Ollama) :
   🤖 Modèle: llama3
   💡 Explain Code - Explique le code
   🐛 Detect Bugs - Détecte les bugs
   ✨ Improve Tests - Améliore les tests
   🎯 Edge Cases - Identifie cas limites
```

3. **Navigateur**:
```
http://127.0.0.1:5000
```

---

## 🧪 Tester les nouvelles fonctionnalités

### Via l'API

**1. Vérifier le statut**:
```bash
curl http://127.0.0.1:5000/ai/status
```

Réponse attendue:
```json
{
  "available": true,
  "model": "llama3",
  "message": "✅ Ollama prêt"
}
```

**2. Expliquer du code**:
```bash
curl -X POST http://127.0.0.1:5000/ai/explain ^
  -H "Content-Type: application/json" ^
  -d "{\"code\": \"public int add(int a, int b) { return a + b; }\", \"language\": \"java\"}"
```

**3. Détecter des bugs**:
```bash
curl -X POST http://127.0.0.1:5000/ai/detect-bugs ^
  -H "Content-Type: application/json" ^
  -d "{\"code\": \"public void process(String s) { s.toLowerCase(); }\", \"language\": \"java\"}"
```

---

## 🐛 Problèmes fréquents

### ❌ "Ollama n'est pas lancé"

**Solution**:
```powershell
ollama serve
```

### ❌ "model not found"

**Solution**:
```powershell
ollama pull llama3
```

### ❌ "port 11434 already in use"

**Solution**: Ollama est déjà lancé! C'est bon!

### ❌ Réponses très lentes

**Solution**: Utilise un modèle plus léger
```powershell
ollama pull phi
```

Puis modifie `ollama_client.py` ligne 13:
```python
def __init__(self, base_url: str = "http://localhost:11434", model: str = "phi"):
```

---

## 📊 Pour ta présentation PFA

### Points à mentionner

✅ **IA 100% gratuite** (Ollama local)  
✅ **Pas de quota** (utilisation illimitée)  
✅ **Données privées** (tout reste sur ton PC)  
✅ **4 nouvelles fonctionnalités IA**:
   - Explain Code
   - Detect Bugs
   - Improve Tests  
   - Edge Cases

### Démo en direct

1. Montre le serveur qui démarre avec Ollama activé
2. Upload un fichier Java
3. Clique sur **"Explain Code"** → Montre l'explication
4. Clique sur **"Detect Bugs"** → Montre les bugs trouvés
5. Explique que **c'est gratuit et local**

---

## 🎯 Comparaison avec API payantes

| Critère | Ollama | Gemini/OpenAI |
|---------|--------|---------------|
| **Coût** | 0€ | ~0.02€/requête |
| **Quota** | Illimité | Limité |
| **Vitesse** | 2-5s | 1-2s |
| **Qualité** | Très bonne | Excellente |
| **Confidentialité** | 100% | Données envoyées |
| **Installation** | 5 min | API key |

---

## 📞 Liens utiles

- **Site Ollama**: https://ollama.com
- **Documentation**: https://github.com/ollama/ollama
- **Modèles**: https://ollama.com/library
- **Support**: https://discord.gg/ollama

---

## ✨ Résumé

```bash
# 1. Installe Ollama
https://ollama.com/download

# 2. Télécharge un modèle
ollama pull llama3

# 3. Lance Ollama
ollama serve

# 4. Lance ton projet
python web_app_demo.py

# 5. Teste
python test_ollama.py
```

**Temps total**: 5-10 minutes  
**Résultat**: Projet avec IA gratuite et illimitée! 🚀
