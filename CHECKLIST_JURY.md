# 📊 Présentation Jury - Checklist

## ✅ Avant la présentation

### Configuration
- [ ] Terminal PowerShell ouvert dans `unittest-ai-agent/`
- [ ] Connexion Internet active
- [ ] Clé API Gemini configurée dans `.env`
- [ ] VS Code ouvert avec les fichiers importants

### Fichiers à avoir en onglets VS Code
- [ ] `DEMO_GUIDE.md` (guide complet)
- [ ] `example/converter.py` (exemple simple)
- [ ] `demo/calculator.py` (exemple complexe)
- [ ] `ut_output/test_converter.py` (résultat généré)

### Test rapide
```powershell
# Vérifier que tout fonctionne
ut --help
python -m pytest --version
```

---

## 🎬 Déroulement de la démo (10 minutes)

### 1. Introduction (1 min)
**À dire :**
- "Je présente un générateur de tests unitaires par IA"
- "Problème : écrire des tests prend du temps"
- "Solution : automatisation avec Gemini"

### 2. Démo Simple (3 min)

**Montrer le fichier source :**
```powershell
code example/converter.py
```

**Générer les tests :**
```powershell
ut generate example/converter.py
```

**Montrer le résultat :**
- Ouvrir `ut_output/test_converter.py`
- Souligner : 14 tests, pattern AAA, cas limites

**Exécuter :**
```powershell
python -m pytest ut_output/test_converter.py -v
```

**Résultat : 14 passed ✅**

### 3. Démo Complexe (4 min)

**Montrer le fichier source :**
```powershell
code demo/calculator.py
```

**Points à souligner :**
- 4 fonctions
- Exceptions (ValueError, TypeError)
- Logique mathématique

**Générer les tests :**
```powershell
ut generate demo/calculator.py
```

**Montrer le résultat :**
- 35 tests générés
- Tests d'exceptions avec pytest.raises
- Validation de types

**Exécuter :**
```powershell
python -m pytest ut_output/test_calculator.py -v
```

### 4. Architecture (2 min)

**Montrer les fichiers clés :**

1. **Configuration** `.env`
```
GEMINI_API_KEY=...
```

2. **Client LLM** `src/ut/llm_client.py`
```python
model = genai.GenerativeModel('gemini-flash-lite-latest')
```

3. **Prompt** `src/ut/prompts/generate_unittest_standalone.txt`

**À dire :**
- "Utilise Google Gemini avec prompt optimisé"
- "Architecture modulaire et extensible"
- "Peut supporter d'autres modèles IA"

---

## 💡 Messages clés à faire passer

1. **Gain de temps massif** : 80-90% de temps économisé
2. **Qualité professionnelle** : Respect des best practices
3. **Couverture complète** : Happy path + edge cases + erreurs
4. **IA compréhensive** : Comprend la logique métier

---

## 🎯 Réponses aux questions probables

### "Pourquoi ne pas utiliser des outils classiques ?"
> "Les outils classiques mesurent la couverture ou génèrent des données aléatoires, mais ne comprennent pas la logique. L'IA analyse le contexte et génère des tests pertinents."

### "Comment vous assurez la qualité ?"
> "Prompt engineering optimisé + validation pytest automatique + possibilité de review manuelle"

### "Quelles limitations ?"
> "Nécessite Internet, quota API limité en gratuit, tests très complexes peuvent nécessiter ajustements"

### "Quelles améliorations possibles ?"
> "Support d'autres langages, intégration CI/CD, interface web, support de plusieurs modèles IA"

---

## 📈 Statistiques à citer

| Métrique | Valeur |
|----------|--------|
| Temps génération | 3-5 sec |
| Tests exemple simple | 14 tests |
| Tests exemple complexe | 35 tests |
| Taux de succès | 100% |
| Gain de temps | 80-90% |

---

## 🚨 Plan B (si problème technique)

### Si l'API échoue
- Montrer les tests déjà générés
- Expliquer l'architecture
- Montrer le code du prompt

### Si pytest échoue
```powershell
# Réinstaller
pip install --force-reinstall pytest
```

### Si la démo est trop courte
- Ouvrir un fichier de test généré et analyser en détail
- Montrer la structure du projet
- Parler des cas d'usage réels

---

## ⏱️ Timing précis

| Minute | Action |
|--------|--------|
| 0:00 | Intro + contexte |
| 1:00 | Démo simple - montrer code |
| 1:30 | Démo simple - générer |
| 2:00 | Démo simple - exécuter |
| 3:00 | Démo complexe - montrer code |
| 4:00 | Démo complexe - générer |
| 5:00 | Démo complexe - exécuter |
| 7:00 | Architecture - montrer config |
| 8:00 | Architecture - expliquer |
| 9:00 | Conclusion |
| 10:00+ | Questions |

---

## 📝 Script exact à dire

### Début
> "Bonjour, je vous présente aujourd'hui un générateur automatique de tests unitaires utilisant l'intelligence artificielle."

### Problématique
> "Le problème que je résous : écrire des tests unitaires complets est chronophage. Pour une fonction simple, il faut 30 minutes à 1 heure pour couvrir tous les cas."

### Solution
> "Ma solution utilise Google Gemini pour analyser le code et générer automatiquement des tests suivant les meilleures pratiques."

### Démo
> "Je vais vous montrer deux exemples : un simple et un complexe."

[FAIRE LA DÉMO]

### Conclusion
> "Ce projet montre comment l'IA peut concrètement améliorer la productivité des développeurs. Merci, je suis prêt à répondre à vos questions."

---

## ✅ Post-démonstration

- [ ] Répondre aux questions calmement
- [ ] Noter les suggestions d'amélioration
- [ ] Montrer des détails si demandé
- [ ] Rester confiant et souriant

**Bonne chance ! 🍀**
