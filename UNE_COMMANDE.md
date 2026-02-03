# 🎯 UNE SEULE COMMANDE POUR LA DÉMO

## ⚡ LA COMMANDE ESSENTIELLE

Pour générer ET exécuter les tests en une seule fois :

```powershell
ut generate example/converter.py; python -m pytest ut_output/test_converter.py -v
```

**C'est tout ! Cette commande fait :**
1. ✅ Génère 14 tests automatiquement
2. ✅ Les exécute et montre le résultat

---

## 🎬 SCRIPT COMPLET AUTO (si vous préférez)

Si vous voulez TOUT automatiser (nettoyage + génération + exécution) :

```powershell
Remove-Item ut_output/test_*.py -ErrorAction SilentlyContinue; ut generate example/converter.py; python -m pytest ut_output/test_converter.py -v
```

---

## 💡 CE QU'IL FAUT DIRE PENDANT

### Avant d'exécuter (10 secondes)
> "Je vais maintenant générer automatiquement les tests pour cette fonction de conversion de dates."

### Pendant l'exécution (quelques secondes)
> "L'IA analyse le code..."

### Après les résultats (30 secondes)
> "Voilà : **14 tests générés et validés** en quelques secondes. Regardons la qualité..."

Puis ouvrir le fichier :
```powershell
code ut_output/test_converter.py
```

---

## 📊 RÉSULTAT ATTENDU

```
✅ Tests generated successfully
================== 14 passed in 0.10s ===================
```

---

## 🎯 C'EST TOUT !

**Une seule commande suffit pour impressionner le jury !** 🚀
