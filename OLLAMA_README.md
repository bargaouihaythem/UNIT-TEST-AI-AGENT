# 🆓 IA GRATUITE avec Ollama

## ✅ Nouvelles fonctionnalités IA ajoutées

Ton projet supporte maintenant **Ollama** - une IA 100% **gratuite** qui tourne sur ton PC!

### 🎯 Fonctionnalités IA gratuites

1. **💡 Explain Code** - Explique le code uploadé
2. **🐛 Detect Bugs** - Détecte les bugs potentiels
3. **✨ Improve Tests** - Suggère des améliorations pour les tests
4. **🎯 Edge Cases** - Identifie les cas limites manquants

---

## 🚀 Installation Ollama (5 minutes)

### Étape 1 : Télécharger Ollama

**Windows** :
```
https://ollama.com/download
```

Télécharge et installe l'exécutable (comme installer n'importe quel logiciel).

### Étape 2 : Télécharger un modèle IA

Ouvre PowerShell ou CMD et tape :

```powershell
ollama pull llama3
```

Ou pour un modèle plus léger :

```powershell
ollama pull phi
```

### Étape 3 : Lancer Ollama (IMPORTANT)

Avant de lancer ton projet, lance Ollama :

```powershell
ollama serve
```

Laisse cette fenêtre ouverte en arrière-plan.

### Étape 4 : Vérifier que ça fonctionne

```powershell
ollama run llama3
```

Si ça affiche ">>> " avec un curseur qui clignote, c'est bon ! (Tape `/bye` pour sortir)

---

## 🎮 Utilisation dans ton projet

### Démarrer le serveur

```bash
python web_app_demo.py
```

Tu verras :

```
🆓 NOUVELLES FONCTIONNALITÉS IA GRATUITES (Ollama) :
   🤖 Modèle: llama3
   💡 Explain Code - Explique le code
   🐛 Detect Bugs - Détecte les bugs
   ✨ Improve Tests - Améliore les tests
   🎯 Edge Cases - Identifie cas limites
```

### Tester l'API

**1. Vérifier le statut d'Ollama** :

```bash
curl http://127.0.0.1:5000/ai/status
```

**2. Expliquer du code** :

```bash
curl -X POST http://127.0.0.1:5000/ai/explain \
  -H "Content-Type: application/json" \
  -d '{
    "code": "public int add(int a, int b) { return a + b; }",
    "language": "java"
  }'
```

**3. Détecter des bugs** :

```bash
curl -X POST http://127.0.0.1:5000/ai/detect-bugs \
  -H "Content-Type: application/json" \
  -d '{
    "code": "public void process(String input) { input.toLowerCase(); }",
    "language": "java"
  }'
```

---

## 🎨 Intégration Frontend (optionnel)

Tu peux ajouter des boutons dans ton interface web :

```html
<!-- Bouton "Explain Code" -->
<button onclick="explainCode()">💡 Explain Code</button>

<!-- Bouton "Detect Bugs" -->
<button onclick="detectBugs()">🐛 Detect Bugs</button>

<!-- Bouton "Improve Tests" -->
<button onclick="improveTests()">✨ Improve Tests</button>

<script>
async function explainCode() {
    const code = document.getElementById('sourceCode').value;
    
    const response = await fetch('/ai/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code, language: 'java' })
    });
    
    const result = await response.json();
    
    if (result.success) {
        alert(result.explanation);
    } else {
        alert('Erreur: ' + result.error);
    }
}
</script>
```

---

## ⚙️ Configuration avancée

### Changer de modèle

Modifie [ollama_client.py](ollama_client.py) ligne 13 :

```python
def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
```

Modèles disponibles :
- `llama3` (recommandé, 4GB RAM)
- `phi` (léger, 2GB RAM)
- `codellama` (spécialisé code, 7GB RAM)
- `mistral` (performant, 4GB RAM)

Liste complète : https://ollama.com/library

### Installer un autre modèle

```bash
ollama pull codellama
```

---

## 🐛 Dépannage

### Erreur "Ollama non disponible"

**Solution** :
1. Vérifie qu'Ollama est installé : `ollama --version`
2. Lance Ollama : `ollama serve`
3. Redémarre ton projet

### Erreur "model not found"

**Solution** :
```bash
ollama pull llama3
```

### Réponses trop lentes

**Solution** :
- Utilise un modèle plus léger : `ollama pull phi`
- Modifie `ollama_client.py` ligne 13 : `model: str = "phi"`

---

## 📊 Pour ta soutenance

### Points forts à mentionner

✅ **IA gratuite et locale** (pas d'API payante)  
✅ **Pas de quota limité** (utilisation illimitée)  
✅ **Données privées** (rien n'est envoyé sur internet)  
✅ **4 fonctionnalités IA** (Explain, Detect Bugs, Improve, Edge Cases)  
✅ **Extensible** (facile d'ajouter d'autres analyses)

### Démo pour le jury

1. Montre l'upload d'un fichier Java
2. Clique sur **"Explain Code"** → L'IA explique le code
3. Clique sur **"Detect Bugs"** → L'IA trouve des problèmes
4. Clique sur **"Improve Tests"** → L'IA suggère des améliorations
5. Montre que **tout est gratuit** et **local**

---

## 🎯 Avantages vs API payantes

| Critère | Ollama (Gratuit) | Gemini/OpenAI (Payant) |
|---------|------------------|------------------------|
| **Coût** | 0€ | 0.02€ par requête |
| **Quota** | Illimité | Limité |
| **Vitesse** | ~2-5s | ~1-2s |
| **Qualité** | Très bonne | Excellente |
| **Confidentialité** | 100% privé | Données envoyées |

---

## 🚀 Prochaines étapes

1. **Ajoute les boutons dans l'UI** (voir section Frontend)
2. **Teste les 4 fonctionnalités** avec ton code Java
3. **Prépare ta démo** pour la soutenance
4. **Mesure les performances** (temps de réponse)

---

## 📞 Support

- **Ollama** : https://ollama.com
- **Documentation** : https://github.com/ollama/ollama
- **Modèles** : https://ollama.com/library

---

## ✨ Crédit

Projet PFA - Test Unitaire Automatique avec IA  
Version 3.1 - Avec support Ollama gratuit  
Date : Février 2026
