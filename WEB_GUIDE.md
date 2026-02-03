# 🌐 Interface Web - Guide d'Installation et Utilisation

## 🚀 Installation Rapide

### 1. Installer Flask
```powershell
pip install flask
```

### 2. Lancer le serveur web
```powershell
python web_app.py
```

### 3. Ouvrir dans le navigateur
```
http://127.0.0.1:5000
```

---

## 📱 Utilisation de l'Interface

### **Option 1 : Drag & Drop**
1. Glissez-déposez votre fichier `.py` dans la zone
2. Cliquez sur "Générer les Tests"
3. Attendez 3-5 secondes
4. Consultez les résultats !

### **Option 2 : Upload classique**
1. Cliquez dans la zone d'upload
2. Sélectionnez votre fichier `.py`
3. Cliquez sur "Générer les Tests"
4. Téléchargez le fichier de tests généré

---

## ✨ Fonctionnalités de l'Interface

### 📊 **Dashboard avec statistiques**
- Temps de génération moyen
- Taux de succès
- Nombre de tests générés
- Modèle IA utilisé

### 📈 **Résultats détaillés**
- Nombre total de tests
- Tests réussis / échoués
- Barre de progression visuelle
- Code complet des tests
- Sortie pytest complète

### 💾 **Téléchargement**
- Bouton de téléchargement direct
- Fichier prêt à être intégré
- Format pytest standard

---

## 🎯 **Pour la Démo Jury**

### **Démo CLI + Web (Option complète)**

**Script de présentation :**

1. **Montrer la CLI** (30 sec)
```powershell
ut generate example/converter.py
python -m pytest ut_output/test_converter.py -v
```

2. **Montrer l'Interface Web** (2 min)
```powershell
python web_app.py
```

Puis dans le navigateur :
- Glisser-déposer `example/converter.py`
- Cliquer sur "Générer"
- Montrer les résultats graphiques

3. **Dire au jury** :
> "Le projet offre deux interfaces :
> - **CLI** pour les développeurs et l'intégration CI/CD
> - **Interface Web** pour les non-développeurs et la visualisation"

---

## 🎨 **Avantages de l'Interface Web**

✅ **Intuitive** - Drag & drop simple
✅ **Visuelle** - Statistiques et graphiques
✅ **Accessible** - Pas besoin de connaître la ligne de commande
✅ **Moderne** - Design responsive et élégant
✅ **Complète** - Toutes les infos en un coup d'œil

---

## 🔧 **Architecture**

```
web_app.py              ← Backend Flask
   ↓
templates/index.html    ← Frontend (HTML/CSS/JS)
   ↓
ut generate            ← CLI existante (réutilisée)
   ↓
pytest                 ← Tests exécutés
   ↓
Résultats affichés     ← Interface web
```

---

## 📸 **Captures d'écran (pour le jury)**

L'interface contient :
- 🎨 Design moderne avec dégradé violet
- 📊 4 statistiques clés en haut
- 📤 Zone d'upload drag & drop
- ⚡ Bouton de génération
- 📈 Graphiques de résultats
- 💻 Code source des tests généré
- 🖥️ Sortie pytest complète

---

## 🚨 **Arrêter le serveur**

Dans le terminal :
```
Ctrl + C
```

---

## 💡 **Message pour le Jury**

> "Cette interface web démontre la **polyvalence** du projet :
> - Les développeurs utilisent la CLI
> - Les managers/testeurs utilisent l'interface web
> - Le même moteur IA sous le capot
> - **Double valeur ajoutée** : outil technique ET outil métier"

---

## ⚡ **Commande de démarrage rapide**

```powershell
# Installation
pip install flask

# Lancement
python web_app.py

# Ouvrir le navigateur à http://127.0.0.1:5000
```

**C'est tout ! Interface prête en 30 secondes ! 🎉**
