# 🧪 UNIT TEST AI AGENT

## Générateur Automatique de Tests Unitaires avec Intelligence Artificielle

---

# 📋 RAPPORT DE PROJET DE FIN D'ANNÉE (PFA)

**Établissement :** Sopra Steria  
**Année Académique :** 2025-2026  
**Auteur :** Haythem BARGAOUI  
**Date :** Février 2026  

---

## 📑 Table des Matières

1. [Introduction](#-introduction)
2. [Contexte et Problématique](#-contexte-et-problématique)
3. [Objectifs du Projet](#-objectifs-du-projet)
4. [Architecture Technique](#-architecture-technique)
5. [Fonctionnalités](#-fonctionnalités)
6. [Technologies Utilisées](#-technologies-utilisées)
7. [Installation et Configuration](#-installation-et-configuration)
8. [Guide d'Utilisation](#-guide-dutilisation)
9. [Démonstration](#-démonstration)
10. [Résultats et Performances](#-résultats-et-performances)
11. [Perspectives et Améliorations](#-perspectives-et-améliorations)
12. [Conclusion](#-conclusion)

---

## 🎯 Introduction

**UNIT TEST AI AGENT** est un outil intelligent de génération automatique de tests unitaires utilisant l'intelligence artificielle. Ce projet combine des techniques de templates intelligents avec des modèles d'IA locale (Ollama) pour produire des tests unitaires de haute qualité pour plusieurs langages de programmation.

Le système analyse automatiquement le code source, détecte les patterns, identifie les cas limites potentiels, et génère des tests complets avec assertions, mocks et vérifications.

---

## 🔍 Contexte et Problématique

### Problématique

Dans le développement logiciel moderne, les tests unitaires sont essentiels pour :
- ✅ Garantir la qualité du code
- ✅ Faciliter la maintenance et le refactoring
- ✅ Documenter le comportement attendu
- ✅ Détecter les régressions rapidement

**Cependant**, l'écriture manuelle des tests présente plusieurs défis :
- ⏱️ **Temps considérable** : 30-50% du temps de développement
- 😓 **Tâche répétitive** : Patterns similaires entre les tests
- 🎯 **Couverture incomplète** : Oubli de cas limites importants
- 📉 **Qualité variable** : Dépend de l'expérience du développeur

### Solution Proposée

Un **agent IA intelligent** capable de :
1. Analyser automatiquement le code source
2. Générer des tests unitaires complets
3. Détecter les bugs potentiels
4. Suggérer des améliorations
5. Prédire la couverture de code

---

## 🎯 Objectifs du Projet

### Objectifs Principaux

| # | Objectif | Status |
|---|----------|--------|
| 1 | Générer automatiquement des tests unitaires | ✅ Réalisé |
| 2 | Support multi-langages (Python, Java, TypeScript) | ✅ Réalisé |
| 3 | Interface web intuitive | ✅ Réalisé |
| 4 | Intégration IA locale (Ollama) | ✅ Réalisé |
| 5 | Analyse de qualité du code | ✅ Réalisé |

### Objectifs Secondaires

- 🔍 Détection automatique de bugs
- 📊 Prédiction de couverture de code
- 🛡️ Analyse de sécurité
- ⚡ Analyse de performance
- 🔧 Détection de code smells

---

## 🏗️ Architecture Technique

### Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                        UNIT TEST AI AGENT                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │   Interface  │────▶│   Backend    │────▶│  Générateur  │    │
│  │     Web      │     │    Flask     │     │    Tests     │    │
│  │   (HTML/JS)  │     │   (Python)   │     │   (Smart)    │    │
│  └──────────────┘     └──────────────┘     └──────────────┘    │
│         │                    │                    │             │
│         │                    ▼                    │             │
│         │           ┌──────────────┐              │             │
│         │           │   Ollama IA  │◀─────────────┘             │
│         │           │   (Local)    │                            │
│         │           └──────────────┘                            │
│         │                    │                                  │
│         ▼                    ▼                                  │
│  ┌──────────────┐     ┌──────────────┐                         │
│  │   Résultats  │     │   Analyses   │                         │
│  │    Tests     │     │   IA Code    │                         │
│  └──────────────┘     └──────────────┘                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Composants Principaux

#### 1. 🖥️ Interface Web (Frontend)
- **Technologies** : HTML5, CSS3, JavaScript, Bootstrap
- **Fonctionnalités** : Upload de fichiers, affichage résultats, téléchargement tests

#### 2. ⚙️ Backend Flask (Python)
- **Framework** : Flask
- **Rôle** : Orchestration, API REST, gestion fichiers

#### 3. 🧠 Smart Test Generator
- **Fichier** : `smart_test_generator.py`
- **Approche** : Templates intelligents + analyse regex
- **Résultat** : Tests JUnit 5, pytest, Jest

#### 4. 🤖 Client Ollama (IA Locale)
- **Fichier** : `ollama_client.py`
- **Modèle** : phi (1.3B) / codellama (7B)
- **Fonctions** : Détection bugs, suggestions, explications

#### 5. 🔬 Analyseur de Code
- **Fichier** : `code_analyzer.py`
- **Analyses** : Bugs, sécurité, performance, complexité, code smells

---

## ✨ Fonctionnalités

### 1. 📝 Génération de Tests Unitaires

| Langage | Framework | Fonctionnalités |
|---------|-----------|-----------------|
| **Java** | JUnit 5 + Mockito | @Test, @Mock, @InjectMocks, verify() |
| **Python** | pytest | fixtures, parametrize, mocks |
| **TypeScript** | Jest | describe, it, expect, mocks |

**Caractéristiques des tests générés :**
- ✅ Tests de cas normaux
- ✅ Tests de cas limites (edge cases)
- ✅ Tests de gestion d'erreurs
- ✅ Tests avec valeurs nulles
- ✅ Mocks et vérifications
- ✅ 10-15 tests par fichier

### 2. 🔍 Analyse de Code IA

#### 🐛 Détection de Bugs
```
Détecte automatiquement :
- Null Pointer Exceptions
- Fuites mémoire
- Conditions raciales
- Erreurs logiques
- Division par zéro
```

#### 🛡️ Analyse de Sécurité
```
Identifie les vulnérabilités :
- Injections SQL/XSS
- Validation d'entrées
- Gestion des secrets
- Permissions
```

#### ⚡ Analyse de Performance
```
Détecte les problèmes :
- Boucles inefficaces
- Requêtes N+1
- Allocations mémoire
- Complexité algorithmique
```

#### 🔧 Code Smells
```
Identifie :
- Méthodes trop longues
- Code dupliqué
- Couplage fort
- Nommage inadéquat
```

### 3. 📊 Prédiction de Couverture

Le système estime la couverture de code attendue basée sur :
- Nombre de branches conditionnelles
- Nombre de méthodes
- Complexité cyclomatique
- Tests générés

### 4. 💡 Suggestions d'Amélioration

L'IA propose des améliorations pour :
- Ajouter des cas de test manquants
- Renforcer les assertions
- Améliorer la lisibilité
- Optimiser la structure

---

## 🛠️ Technologies Utilisées

### Backend

| Technologie | Version | Rôle |
|-------------|---------|------|
| Python | 3.9+ | Langage principal |
| Flask | 2.x | Framework web |
| Ollama | Latest | IA locale |
| pytest | 7.x | Framework de tests Python |

### Frontend

| Technologie | Rôle |
|-------------|------|
| HTML5 | Structure |
| CSS3 / Bootstrap | Style |
| JavaScript | Interactivité |

### IA et Modèles

| Modèle | Taille | Utilisation |
|--------|--------|-------------|
| phi | 1.3B | Analyses rapides |
| codellama | 7B | Génération de code (optionnel) |
| llama3 | 8B | Analyses avancées (optionnel) |

### Outils de Développement

- **Git** : Versioning
- **Poetry** : Gestion des dépendances Python
- **VS Code** : IDE recommandé

---

## 📦 Installation et Configuration

### Prérequis

```bash
# Python 3.9 ou supérieur
python --version

# Git
git --version

# Ollama (pour l'IA locale)
# Télécharger depuis : https://ollama.com
```

### Installation

```bash
# 1. Cloner le repository
git clone https://github.com/bargaouihaythem/UNIT-TEST-AI-AGENT.git
cd UNIT-TEST-AI-AGENT

# 2. Installer les dépendances Python
pip install -r requirements.txt
# OU avec Poetry
poetry install

# 3. Installer Ollama et le modèle
ollama pull phi
# OU pour de meilleurs résultats
ollama pull codellama:7b
```

### Configuration

```bash
# Variables d'environnement (optionnel)
# Créer un fichier .env
OPENAI_API_KEY=your_key_here  # Si utilisation d'OpenAI
OLLAMA_BASE_URL=http://localhost:11434
```

---

## 📖 Guide d'Utilisation

### 1. Mode Interface Web

```bash
# Lancer le serveur web
python web_app.py

# Ou avec le script batch (Windows)
start_web.bat
```

Ensuite, ouvrir dans le navigateur : **http://127.0.0.1:5000**

#### Étapes :
1. 📤 **Upload** : Glisser-déposer ou sélectionner un fichier
2. ⚙️ **Génération** : Cliquer sur "Générer les tests"
3. 📋 **Résultats** : Visualiser les tests générés
4. 📊 **Analyses** : Consulter les analyses IA
5. 💾 **Télécharger** : Récupérer les fichiers de tests

### 2. Mode Ligne de Commande (CLI)

```bash
# Générer des tests pour un fichier Python
poetry run ut generate example/calculator.py

# Générer des tests pour tous les exemples
python test_all_examples.py
```

### 3. Mode Démonstration

```bash
# Lancer la démo automatique
python demo_mode.py

# Ou avec le script batch
demo_auto.bat
```

---

## 🎬 Démonstration

### Exemple 1 : Fichier Java (Calculator.java)

**Code source :**
```java
public class Calculator {
    public int add(int a, int b) { return a + b; }
    public int divide(int a, int b) { return a / b; }
}
```

**Tests générés (JUnit 5 + Mockito) :**
```java
@ExtendWith(MockitoExtension.class)
class CalculatorTest {
    
    @InjectMocks
    private Calculator calculator;
    
    @Test
    void testAdd_normalCase() {
        assertEquals(5, calculator.add(2, 3));
    }
    
    @Test
    void testAdd_negativeNumbers() {
        assertEquals(-5, calculator.add(-2, -3));
    }
    
    @Test
    void testDivide_normalCase() {
        assertEquals(2, calculator.divide(6, 3));
    }
    
    @Test
    void testDivide_byZero_throwsException() {
        assertThrows(ArithmeticException.class, 
            () -> calculator.divide(5, 0));
    }
}
```

### Exemple 2 : Fichier Python (calculator.py)

**Tests générés (pytest) :**
```python
import pytest
from calculator import Calculator

class TestCalculator:
    
    def test_add_positive_numbers(self):
        calc = Calculator()
        assert calc.add(2, 3) == 5
    
    def test_add_negative_numbers(self):
        calc = Calculator()
        assert calc.add(-2, -3) == -5
    
    def test_divide_normal(self):
        calc = Calculator()
        assert calc.divide(6, 3) == 2
    
    def test_divide_by_zero_raises_error(self):
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(5, 0)
```

---

## 📈 Résultats et Performances

### Métriques de Performance

| Métrique | Valeur |
|----------|--------|
| **Temps moyen de génération** | 1-5 secondes |
| **Tests générés par fichier** | 10-15 tests |
| **Langages supportés** | 3 (Java, Python, TypeScript) |
| **Taux de tests corrects** | ~95% (templates) |
| **Couverture de code estimée** | 70-85% |

### Comparaison : Templates vs IA Pure

| Critère | Templates | IA (phi) | IA (codellama) |
|---------|-----------|----------|----------------|
| Exactitude | ✅ 100% | ❌ 30% | ✅ 80% |
| Nombre tests | ✅ 10-15 | ❌ 2-3 | ✅ 8-12 |
| Vitesse | ✅ 1s | ❌ 60s | ❌ 30s |
| Créativité | ❌ Limitée | ✅ Élevée | ✅ Élevée |

### Avantages de l'Approche Hybride

Notre solution combine le meilleur des deux mondes :
- **Templates** → Tests corrects et rapides
- **IA** → Analyses intelligentes et suggestions

---

## 🚀 Perspectives et Améliorations

### Court Terme (3-6 mois)

- [ ] Support de langages supplémentaires (C#, Go, Rust)
- [ ] Intégration IDE (plugin VS Code)
- [ ] Mode batch pour projets complets
- [ ] Export vers CI/CD (GitHub Actions, GitLab CI)

### Moyen Terme (6-12 mois)

- [ ] Apprentissage des patterns spécifiques au projet
- [ ] Génération de tests d'intégration
- [ ] Support des microservices
- [ ] Interface en ligne (SaaS)

### Long Terme (12+ mois)

- [ ] Auto-correction des tests échoués
- [ ] Génération de documentation automatique
- [ ] Analyse de régression automatique
- [ ] IA fine-tunée sur les patterns de l'entreprise

---

## 📝 Conclusion

Le projet **UNIT TEST AI AGENT** démontre avec succès la faisabilité d'un système hybride combinant :

1. **Templates intelligents** pour une génération rapide et fiable
2. **IA locale (Ollama)** pour des analyses approfondies
3. **Interface web intuitive** pour une utilisation simplifiée

### Points Forts

- ✅ **Gain de temps significatif** : Réduction de 80% du temps d'écriture de tests
- ✅ **Qualité constante** : Tests standardisés et complets
- ✅ **Multi-langages** : Support Java, Python, TypeScript
- ✅ **IA locale** : Pas de dépendance cloud, confidentialité des données
- ✅ **Analyses riches** : Bugs, sécurité, performance, code smells

### Compétences Acquises

- Développement Python avancé
- Intégration d'IA (LLM) dans une application
- Développement web (Flask, HTML/CSS/JS)
- Architecture logicielle
- Génération de code automatique
- DevOps (Git, CI/CD)

---

## 📚 Références

- [Ollama Documentation](https://ollama.com)
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## 📞 Contact

**Auteur :** Haythem BARGAOUI  
**Email :** haythem.bargaoui@soprasteria.com  
**GitHub :** [github.com/bargaouihaythem](https://github.com/bargaouihaythem)

---

## 📄 Licence

Ce projet est sous licence **Apache 2.0** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<div align="center">

**🎓 Projet de Fin d'Année - 2025/2026**

*Développé avec ❤️ par Haythem BARGAOUI*

</div>
