"""
🔬 Code Analyzer IA - Analyse dynamique RÉELLE pour chaque fichier
Détecte les bugs, vulnérabilités, complexité et code smells
"""
import re
from typing import Dict, List, Any, Optional

# Import Ollama pour IA
try:
    from ollama_client import OllamaClient
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


class CodeAnalyzer:
    """Analyseur de code intelligent avec détection dynamique"""
    
    def __init__(self, source_code: str, filename: str, use_ai: bool = False):
        self.code = source_code
        self.filename = filename
        self.extension = filename.split('.')[-1].lower()
        self.lines = source_code.split('\n')
        self.use_ai = use_ai and OLLAMA_AVAILABLE
        self.ollama = OllamaClient(model="phi") if self.use_ai else None
        self.is_interface = self._detect_interface()
    
    def _detect_interface(self) -> bool:
        """Détecte si le fichier est une interface Java"""
        if self.extension == 'java':
            return bool(re.search(r'\binterface\s+\w+', self.code))
        return False
    
    def analyze_all(self, tests_generated: int = 1) -> Dict[str, Any]:
        """Lance toutes les analyses et retourne un résultat complet
        
        Args:
            tests_generated: Nombre de tests générés pour calculer la coverage honnêtement
        """
        # Si c'est une interface, retourner un message spécial
        if self.is_interface:
            return self._interface_analysis()
        
        return {
            'bug_analysis': self.analyze_bugs(),
            'test_complexity': self.analyze_complexity(),
            'security_analysis': self.analyze_security(),
            'coverage_prediction': self.predict_coverage(tests_generated),
            'performance_analysis': self.analyze_performance(),
            'code_smells': self.detect_code_smells(),
            'functions_count': self.count_functions(),
            'classes_count': self.count_classes(),
            'tests_generated': tests_generated
        }
    
    def _interface_analysis(self) -> Dict[str, Any]:
        """Analyse spéciale pour les interfaces Java"""
        interface_name = re.search(r'interface\s+(\w+)', self.code)
        name = interface_name.group(1) if interface_name else self.filename
        
        return {
            'is_interface': True,
            'interface_name': name,
            'bug_analysis': {
                'score': 100,
                'issues': [],
                'strengths': [f'⚠️ Interface Java détectée : {name}', '📋 Les interfaces définissent des contrats, pas de logique'],
                'suggestions': [f'Uploader l\'implémentation : {name}Impl.java']
            },
            'test_complexity': {
                'score': 0,
                'cyclomatic': 0,
                'maintainability': 100,
                'duplication': 0,
                'level': 'N/A - Interface'
            },
            'security_analysis': {
                'score': 100,
                'risk_level': 'N/A',
                'vulnerabilities': [],
                'secure_points': ['Interface sans logique exécutable'],
                'recommendations': ['Analyser l\'implémentation pour la sécurité']
            },
            'coverage_prediction': {
                'score': 0,
                'estimated_coverage': 0,
                'uncovered_lines': 0,
                'missing_tests': 0,
                'strengths': ['⚠️ Interface non testable directement']
            },
            'performance_analysis': {
                'score': 100,
                'level': 'N/A',
                'bottlenecks': [],
                'complexity': 'N/A',
                'strengths': ['Interface sans exécution']
            },
            'code_smells': {
                'score': 100,
                'level': 'N/A',
                'smells': [],
                'lines_per_function': 0,
                'strengths': ['Interface bien définie']
            },
            'functions_count': len(re.findall(r'\w+\s+\w+\s*\([^)]*\)\s*;', self.code)),
            'classes_count': 0
        }
    
    # ========================================
    # 🔍 SMART BUG DETECTOR
    # ========================================
    def analyze_bugs(self) -> Dict[str, Any]:
        """Détecte les bugs potentiels dans le code"""
        issues = []
        strengths = []
        
        if self.extension == 'java':
            issues.extend(self._detect_java_bugs())
            strengths.extend(self._java_strengths())
        elif self.extension == 'py':
            issues.extend(self._detect_python_bugs())
            strengths.extend(self._python_strengths())
        elif self.extension in ['ts', 'js']:
            issues.extend(self._detect_javascript_bugs())
            strengths.extend(self._javascript_strengths())
        
        # Calculer le score (100 - pénalités)
        penalty = len([i for i in issues if i.get('severity') == 'critical']) * 15
        penalty += len([i for i in issues if i.get('severity') == 'warning']) * 5
        score = max(50, 100 - penalty)
        
        return {
            'score': score,
            'issues': issues,
            'strengths': strengths if strengths else ['✅ Code structure correcte'],
            'suggestions': self._generate_bug_suggestions(issues)
        }
    
    def _detect_java_bugs(self) -> List[Dict]:
        """Détecte les bugs spécifiques Java"""
        bugs = []
        
        for i, line in enumerate(self.lines, 1):
            # NullPointerException potentiel
            if re.search(r'\.\w+\(', line) and 'null' in line.lower():
                bugs.append({
                    'type': 'NullPointerException Risk',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Ajouter une vérification null avant l\'appel',
                    'severity': 'warning'
                })
            
            # Resource leak - pas de try-with-resources
            if re.search(r'new\s+(FileInputStream|BufferedReader|Connection|Statement)', line):
                if 'try' not in self.code[max(0, self.code.find(line)-100):self.code.find(line)]:
                    bugs.append({
                        'type': 'Resource Leak',
                        'line': i,
                        'code': line.strip()[:60],
                        'suggestion': 'Utiliser try-with-resources pour fermer automatiquement',
                        'severity': 'critical'
                    })
            
            # Catch Exception générique
            if re.search(r'catch\s*\(\s*Exception\s+', line):
                bugs.append({
                    'type': 'Generic Exception Catch',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Attraper des exceptions spécifiques',
                    'severity': 'warning'
                })
            
            # String comparison avec ==
            if re.search(r'==\s*"[^"]*"', line) or re.search(r'"[^"]*"\s*==', line):
                bugs.append({
                    'type': 'String Comparison avec ==',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Utiliser .equals() pour comparer les Strings',
                    'severity': 'critical'
                })
            
            # Division par zéro potentielle (exclure annotations, commentaires, strings)
            # Ne pas détecter sur les lignes avec @, //, /*, ou entre guillemets
            if (re.search(r'[^/]\s*/\s*[a-zA-Z_]\w*', line) and 
                'if' not in line.lower() and
                not line.strip().startswith('@') and
                not line.strip().startswith('//') and
                not line.strip().startswith('/*') and
                not line.strip().startswith('*') and
                '"' not in line.split('/')[0] if '/' in line else True):
                # Vérifier que c'est vraiment une division arithmétique
                if re.search(r'[\w\)\]]\s*/\s*[\w\(]', line):
                    bugs.append({
                        'type': 'Division par zéro possible',
                        'line': i,
                        'code': line.strip()[:60],
                        'suggestion': 'Vérifier que le diviseur n\'est pas zéro',
                        'severity': 'warning'
                    })
        
        return bugs
    
    def _detect_python_bugs(self) -> List[Dict]:
        """Détecte les bugs spécifiques Python"""
        bugs = []
        
        for i, line in enumerate(self.lines, 1):
            # Mutable default argument
            if re.search(r'def\s+\w+\([^)]*=\s*(\[\]|\{\})', line):
                bugs.append({
                    'type': 'Mutable Default Argument',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Utiliser None comme défaut et initialiser dans la fonction',
                    'severity': 'critical'
                })
            
            # Bare except
            if re.search(r'^\s*except\s*:', line):
                bugs.append({
                    'type': 'Bare Except',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Spécifier le type d\'exception à attraper',
                    'severity': 'warning'
                })
            
            # eval() usage
            if 'eval(' in line:
                bugs.append({
                    'type': 'Usage dangereux de eval()',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Éviter eval(), utiliser ast.literal_eval() si nécessaire',
                    'severity': 'critical'
                })
            
            # Variable non utilisée (simple check)
            if re.search(r'^\s*\w+\s*=', line) and line.strip().split('=')[0].strip().startswith('_'):
                pass  # Variables avec _ sont OK
            
        return bugs
    
    def _detect_typescript_bugs(self) -> List[Dict]:
        """Détecte les bugs spécifiques TypeScript"""
        bugs = []
        
        for i, line in enumerate(self.lines, 1):
            # Usage de any
            if ': any' in line or 'as any' in line:
                bugs.append({
                    'type': 'Type any utilisé',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Définir un type spécifique au lieu de any',
                    'severity': 'warning'
                })
            
            # == au lieu de ===
            if re.search(r'[^=!]==[^=]', line) and '===' not in line:
                bugs.append({
                    'type': 'Comparaison loose ==',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Utiliser === pour comparaison stricte',
                    'severity': 'warning'
                })
            
            # console.log en production
            if 'console.log' in line:
                bugs.append({
                    'type': 'console.log en production',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Supprimer les console.log en production',
                    'severity': 'warning'
                })
        
        return bugs
    
    def _detect_javascript_bugs(self) -> List[Dict]:
        """Détecte les bugs spécifiques JavaScript/TypeScript - AMÉLIORÉ"""
        bugs = []
        
        for i, line in enumerate(self.lines, 1):
            # == au lieu de === (comparaison non stricte)
            if re.search(r'[^=!]==[^=]', line) and '===' not in line:
                bugs.append({
                    'type': 'Comparaison loose ==',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Utiliser === pour comparaison stricte',
                    'severity': 'warning'
                })
            
            # console.log en production
            if 'console.log' in line and not line.strip().startswith('//'):
                bugs.append({
                    'type': 'console.log en production',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Supprimer les console.log en production',
                    'severity': 'info'
                })
            
            # Variable non déclarée (usage de var au lieu de let/const)
            if re.search(r'\bvar\s+\w+', line):
                bugs.append({
                    'type': 'Usage de var (scope global)',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Utiliser let ou const au lieu de var',
                    'severity': 'warning'
                })
            
            # Callback hell potentiel (fonctions imbriquées)
            if line.count('function') > 1 or (line.count('=>') > 1 and 'function' in line):
                bugs.append({
                    'type': 'Callback hell potentiel',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Utiliser async/await ou Promises',
                    'severity': 'warning'
                })
            
            # eval() dangereux
            if 'eval(' in line:
                bugs.append({
                    'type': 'Usage dangereux de eval()',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Éviter eval() pour des raisons de sécurité',
                    'severity': 'critical'
                })
            
            # innerHTML (XSS potentiel)
            if 'innerHTML' in line and '=' in line:
                bugs.append({
                    'type': 'innerHTML potentiellement vulnérable',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Utiliser textContent ou sanitizer',
                    'severity': 'warning'
                })
            
            # setTimeout/setInterval avec string (eval implicite)
            if re.search(r'(setTimeout|setInterval)\s*\(\s*["\']', line):
                bugs.append({
                    'type': 'setTimeout avec string',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Passer une fonction, pas une string',
                    'severity': 'warning'
                })
            
            # Magic numbers
            if re.search(r'[^\d]\d{3,}[^\d]', line) and 'const' not in line and 'HEIGHT' not in line.upper():
                bugs.append({
                    'type': 'Magic number détecté',
                    'line': i,
                    'code': line.strip()[:60],
                    'suggestion': 'Extraire dans une constante nommée',
                    'severity': 'info'
                })
            
            # Fonction trop longue (détection simple)
            if 'function' in line and '{' in line:
                # Compter les lignes jusqu'à la fin de la fonction
                brace_count = 1
                func_lines = 1
                for j in range(i, min(i + 100, len(self.lines))):
                    if j < len(self.lines):
                        brace_count += self.lines[j].count('{') - self.lines[j].count('}')
                        func_lines += 1
                        if brace_count <= 0:
                            break
                if func_lines > 50:
                    bugs.append({
                        'type': 'Fonction trop longue',
                        'line': i,
                        'code': line.strip()[:60],
                        'suggestion': f'Fonction de {func_lines} lignes - découper en sous-fonctions',
                        'severity': 'warning'
                    })
            
            # Accès DOM sans vérification null
            if re.search(r'(getElementById|querySelector|getElementsBy)\([^)]+\)\.', line):
                if 'if' not in self.code[max(0, self.code.find(line)-100):self.code.find(line)]:
                    bugs.append({
                        'type': 'Accès DOM sans vérification null',
                        'line': i,
                        'code': line.strip()[:60],
                        'suggestion': 'Vérifier que l\'\u00e9lément existe avant accès',
                        'severity': 'warning'
                    })
        
        return bugs
    
    def _javascript_strengths(self) -> List[str]:
        """Points forts pour JavaScript/TypeScript"""
        strengths = []
        if 'use strict' in self.code or "'use strict'" in self.code:
            strengths.append('✅ Mode strict activé')
        if 'const ' in self.code:
            strengths.append('✅ Utilisation de const pour l\'immutabilité')
        if 'async' in self.code and 'await' in self.code:
            strengths.append('✅ Async/await pour code asynchrone propre')
        if 'try' in self.code and 'catch' in self.code:
            strengths.append('✅ Gestion des erreurs présente')
        if '===' in self.code:
            strengths.append('✅ Comparaisons strictes utilisées')
        if 'prototype' not in self.code and 'class ' in self.code:
            strengths.append('✅ Classes ES6 modernes')
        return strengths if strengths else ['✅ Code JavaScript standard']
    
    def _java_strengths(self) -> List[str]:
        """Points forts pour Java"""
        strengths = []
        if '@Override' in self.code:
            strengths.append('✅ Utilisation correcte de @Override')
        if 'private' in self.code:
            strengths.append('✅ Encapsulation avec membres privés')
        if 'final' in self.code:
            strengths.append('✅ Utilisation de final pour l\'immutabilité')
        if 'try' in self.code and ('catch' in self.code or 'finally' in self.code):
            strengths.append('✅ Gestion des exceptions présente')
        return strengths if strengths else ['✅ Code Java standard respecté']
    
    def _python_strengths(self) -> List[str]:
        """Points forts pour Python"""
        strengths = []
        if 'def ' in self.code:
            strengths.append('✅ Fonctions bien définies')
        if '"""' in self.code or "'''" in self.code:
            strengths.append('✅ Docstrings présents')
        if 'typing' in self.code or ': ' in self.code:
            strengths.append('✅ Type hints utilisés')
        return strengths if strengths else ['✅ Code Python lisible']
    
    def _typescript_strengths(self) -> List[str]:
        """Points forts pour TypeScript"""
        strengths = []
        if 'interface' in self.code:
            strengths.append('✅ Interfaces TypeScript définies')
        if 'private' in self.code or 'readonly' in self.code:
            strengths.append('✅ Encapsulation TypeScript')
        if 'async' in self.code and 'await' in self.code:
            strengths.append('✅ Gestion asynchrone correcte')
        return strengths if strengths else ['✅ Code TypeScript typé']
    
    def _generate_bug_suggestions(self, issues: List[Dict]) -> List[str]:
        """Génère des suggestions basées sur les bugs détectés"""
        suggestions = []
        issue_types = [i['type'] for i in issues]
        
        if any('Null' in t for t in issue_types):
            suggestions.append('🔧 Ajouter des vérifications null systématiques')
        if any('Resource' in t for t in issue_types):
            suggestions.append('🔧 Utiliser try-with-resources ou context managers')
        if any('Exception' in t for t in issue_types):
            suggestions.append('🔧 Améliorer la gestion des exceptions')
        
        return suggestions if suggestions else ['✅ Continuer les bonnes pratiques']
    
    # ========================================
    # 📊 COMPLEXITY ANALYZER
    # ========================================
    def analyze_complexity(self) -> Dict[str, Any]:
        """Analyse la complexité du code"""
        cyclomatic = self._calculate_cyclomatic_complexity()
        loc = len([l for l in self.lines if l.strip() and not l.strip().startswith(('//', '#', '/*', '*'))])
        functions = self.count_functions()
        
        # Calculer maintenabilité
        maintainability = max(50, 100 - (cyclomatic * 3) - (loc / 10))
        
        # Score global
        score = int((maintainability + (100 - cyclomatic * 5)) / 2)
        score = max(50, min(100, score))
        
        return {
            'score': score,
            'cyclomatic': round(cyclomatic, 1),
            'maintainability': int(maintainability),
            'duplication': self._estimate_duplication(),
            'loc': loc,
            'functions': functions,
            'level': 'Simple' if cyclomatic < 5 else ('Moyen' if cyclomatic < 10 else 'Complexe')
        }
    
    def _calculate_cyclomatic_complexity(self) -> float:
        """Calcule la complexité cyclomatique"""
        complexity = 1  # Base
        
        # Compter les structures de contrôle
        patterns = [
            r'\bif\b', r'\belif\b', r'\belse\s+if\b',
            r'\bfor\b', r'\bwhile\b',
            r'\bcase\b', r'\bcatch\b',
            r'\band\b', r'\bor\b', r'\b\&\&\b', r'\b\|\|\b',
            r'\?'  # Ternaire
        ]
        
        for pattern in patterns:
            complexity += len(re.findall(pattern, self.code))
        
        # Normaliser par le nombre de fonctions
        functions = max(1, self.count_functions())
        return complexity / functions
    
    def _estimate_duplication(self) -> int:
        """Estime le pourcentage de duplication"""
        lines_set = set()
        duplicates = 0
        
        for line in self.lines:
            clean = line.strip()
            if len(clean) > 10:  # Ignorer les lignes courtes
                if clean in lines_set:
                    duplicates += 1
                else:
                    lines_set.add(clean)
        
        total = len([l for l in self.lines if len(l.strip()) > 10])
        return int((duplicates / max(1, total)) * 100)
    
    # ========================================
    # 🔒 SECURITY ANALYZER
    # ========================================
    def analyze_security(self) -> Dict[str, Any]:
        """Analyse les vulnérabilités de sécurité"""
        vulnerabilities = []
        secure_points = []
        
        if self.extension == 'java':
            vulnerabilities.extend(self._detect_java_security())
        elif self.extension == 'py':
            vulnerabilities.extend(self._detect_python_security())
        elif self.extension == 'ts':
            vulnerabilities.extend(self._detect_typescript_security())
        
        # Points sécurisés
        secure_points = self._detect_security_strengths()
        
        # Calculer le score
        critical = len([v for v in vulnerabilities if v.get('severity') == 'critical'])
        warnings = len([v for v in vulnerabilities if v.get('severity') == 'warning'])
        score = max(40, 100 - (critical * 20) - (warnings * 5))
        
        # Niveau de risque
        risk_level = 'Low' if score >= 80 else ('Medium' if score >= 60 else 'High')
        
        return {
            'score': score,
            'risk_level': risk_level,
            'vulnerabilities': vulnerabilities,
            'secure_points': secure_points,
            'recommendations': self._generate_security_recommendations(vulnerabilities)
        }
    
    def _detect_java_security(self) -> List[Dict]:
        """Détecte les vulnérabilités Java"""
        vulns = []
        
        for i, line in enumerate(self.lines, 1):
            # SQL Injection
            if re.search(r'(executeQuery|executeUpdate|execute)\s*\(\s*["\'].*\+', line):
                vulns.append({
                    'type': 'SQL Injection',
                    'line': i,
                    'code': line.strip()[:50],
                    'severity': 'critical',
                    'fix': 'Utiliser PreparedStatement avec paramètres'
                })
            
            # Hardcoded password
            if re.search(r'(password|pwd|secret|key)\s*=\s*["\'][^"\']+["\']', line, re.I):
                vulns.append({
                    'type': 'Mot de passe hardcodé',
                    'line': i,
                    'code': line.strip()[:50],
                    'severity': 'critical',
                    'fix': 'Utiliser des variables d\'environnement'
                })
            
            # XSS potentiel
            if 'innerHTML' in line or 'document.write' in line:
                vulns.append({
                    'type': 'XSS Potentiel',
                    'line': i,
                    'code': line.strip()[:50],
                    'severity': 'warning',
                    'fix': 'Encoder les sorties HTML'
                })
        
        return vulns
    
    def _detect_python_security(self) -> List[Dict]:
        """Détecte les vulnérabilités Python"""
        vulns = []
        
        for i, line in enumerate(self.lines, 1):
            # eval/exec dangereux
            if 'eval(' in line or 'exec(' in line:
                vulns.append({
                    'type': 'Exécution de code arbitraire',
                    'line': i,
                    'code': line.strip()[:50],
                    'severity': 'critical',
                    'fix': 'Éviter eval/exec, utiliser des alternatives sûres'
                })
            
            # pickle non sécurisé
            if 'pickle.load' in line:
                vulns.append({
                    'type': 'Désérialisation non sécurisée',
                    'line': i,
                    'code': line.strip()[:50],
                    'severity': 'critical',
                    'fix': 'Utiliser json ou des formats sûrs'
                })
            
            # Shell injection
            if re.search(r'(os\.system|subprocess\.\w+)\s*\([^)]*\+', line):
                vulns.append({
                    'type': 'Injection Shell',
                    'line': i,
                    'code': line.strip()[:50],
                    'severity': 'critical',
                    'fix': 'Utiliser subprocess avec liste d\'arguments'
                })
        
        return vulns
    
    def _detect_typescript_security(self) -> List[Dict]:
        """Détecte les vulnérabilités TypeScript"""
        vulns = []
        
        for i, line in enumerate(self.lines, 1):
            # innerHTML XSS
            if 'innerHTML' in line:
                vulns.append({
                    'type': 'XSS via innerHTML',
                    'line': i,
                    'code': line.strip()[:50],
                    'severity': 'critical',
                    'fix': 'Utiliser textContent ou sanitizer'
                })
            
            # localStorage sensible
            if re.search(r'localStorage\.(setItem|getItem)\s*\([^)]*token', line, re.I):
                vulns.append({
                    'type': 'Token stocké dans localStorage',
                    'line': i,
                    'code': line.strip()[:50],
                    'severity': 'warning',
                    'fix': 'Utiliser httpOnly cookies pour les tokens'
                })
        
        return vulns
    
    def _detect_security_strengths(self) -> List[str]:
        """Détecte les bonnes pratiques de sécurité"""
        strengths = []
        
        if 'PreparedStatement' in self.code or 'parameterized' in self.code.lower():
            strengths.append('✅ Requêtes paramétrées utilisées')
        # Exclure HashMap du check de hachage
        if ('bcrypt' in self.code.lower() or 'passwordencoder' in self.code.lower() or 
            ('hash' in self.code.lower() and 'hashmap' not in self.code.lower() and 'hashcode' not in self.code.lower())):
            strengths.append('✅ Hachage des mots de passe')
        if 'https' in self.code.lower():
            strengths.append('✅ Connexions HTTPS')
        if 'validate' in self.code.lower() or 'sanitize' in self.code.lower():
            strengths.append('✅ Validation des entrées')
        
        return strengths if strengths else ['✅ Pas de vulnérabilité critique détectée']
    
    def _generate_security_recommendations(self, vulns: List[Dict]) -> List[str]:
        """Génère des recommandations de sécurité"""
        recs = []
        
        if any('SQL' in v.get('type', '') for v in vulns):
            recs.append('🔒 Implémenter des requêtes préparées')
        if any('XSS' in v.get('type', '') for v in vulns):
            recs.append('🔒 Encoder toutes les sorties HTML')
        if any('password' in v.get('type', '').lower() for v in vulns):
            recs.append('🔒 Utiliser un gestionnaire de secrets')
        
        return recs if recs else ['✅ Continuer les bonnes pratiques de sécurité']
    
    # ========================================
    # 📈 COVERAGE PREDICTOR - VERSION HONNÊTE
    # ========================================
    def predict_coverage(self, tests_generated: int = 1) -> Dict[str, Any]:
        """Prédit la couverture de code - VERSION HONNÊTE ET RÉALISTE
        
        Formule réaliste:
        - 1 test = ~5-10% coverage (teste juste 'pas de crash')
        - 1 test par fonction = ~60% coverage (chemins principaux)
        - 2-3 tests par fonction = ~80% coverage (edge cases)
        - 4+ tests par fonction = ~90% coverage (complet)
        """
        functions = self.count_functions()
        branches = self._count_branches()
        total_lines = len([l for l in self.lines if l.strip()])
        
        # Analyser la testabilité réelle du code
        testability_factors = self._analyze_testability()
        
        # ========== CALCUL HONNÊTE ==========
        # Base: combien de fonctions sont réellement testées?
        if functions == 0:
            coverage_ratio = 0.1 if tests_generated > 0 else 0
        else:
            # Ratio tests/fonctions
            tests_per_function = tests_generated / functions
            
            if tests_per_function < 0.2:
                # Très peu de tests = coverage minimale
                coverage_ratio = 0.05 + (tests_per_function * 0.2)
            elif tests_per_function < 0.5:
                # Quelques tests = coverage faible
                coverage_ratio = 0.15 + (tests_per_function * 0.3)
            elif tests_per_function < 1:
                # Tests partiels
                coverage_ratio = 0.30 + (tests_per_function * 0.35)
            elif tests_per_function < 2:
                # 1-2 tests par fonction = couverture correcte
                coverage_ratio = 0.50 + ((tests_per_function - 1) * 0.20)
            else:
                # Tests complets
                coverage_ratio = min(0.90, 0.70 + (tests_per_function - 2) * 0.10)
        
        # Pénalités pour code difficile à tester
        if testability_factors['has_dom']:
            coverage_ratio *= 0.7  # DOM = -30%
        if testability_factors['has_external_deps']:
            coverage_ratio *= 0.85  # Deps externes = -15%
        if testability_factors['has_side_effects']:
            coverage_ratio *= 0.90  # Effets de bord = -10%
        if testability_factors['has_ui_events']:
            coverage_ratio *= 0.80  # Events UI = -20%
        
        # Bonus pour code pur
        if testability_factors['has_pure_functions']:
            coverage_ratio = min(0.95, coverage_ratio * 1.1)
        
        estimated = int(coverage_ratio * 100)
        estimated = max(3, min(95, estimated))  # Entre 3% et 95%
        
        # Lignes non couvertes estimées
        uncovered = int(total_lines * (100 - estimated) / 100)
        
        # Tests manquants pour atteindre 80% coverage
        target_coverage = 80
        if estimated < target_coverage:
            # Pour 80% coverage, il faut ~2 tests par fonction
            tests_needed = int(functions * 2)
            missing_tests = max(0, tests_needed - tests_generated)
        else:
            missing_tests = 0
        
        # Avertissements HONNÊTES
        warnings = []
        if tests_generated == 1 and functions > 1:
            warnings.append(f'⚠️ 1 test pour {functions} fonctions = coverage très faible (~{estimated}%)')
        if testability_factors['has_dom']:
            warnings.append('⚠️ Code DOM nécessite des mocks (jsdom, @testing-library)')
        if testability_factors['has_external_deps']:
            warnings.append('⚠️ Dépendances externes à mocker')
        if testability_factors['has_ui_events']:
            warnings.append('⚠️ Événements UI nécessitent simulation (userEvent)')
        if coverage_ratio < 0.20:
            warnings.append('🚨 Coverage critique: tests trop superficiels')
        
        return {
            'score': estimated,
            'estimated_coverage': estimated,
            'uncovered_lines': uncovered,
            'missing_tests': missing_tests,
            'tests_generated': tests_generated,
            'functions_count': functions,
            'branches': branches,
            'testability': testability_factors,
            'warnings': warnings,
            'strengths': self._coverage_strengths(tests_generated, functions),
            'honest_verdict': self._get_coverage_verdict(estimated, tests_generated, functions)
        }
    
    def _analyze_testability(self) -> Dict[str, Any]:
        """Analyse la testabilité réelle du code"""
        code_lower = self.code.lower()
        
        # Détection DOM
        has_dom = any(pattern in self.code for pattern in [
            'document.', 'getElementById', 'querySelector', 'innerHTML',
            'addEventListener', 'createElement', 'appendChild', 'jquery',
            'jQuery', '$(', '.html(', '.css(', '.attr('
        ])
        
        # Détection dépendances externes
        has_external_deps = any(pattern in self.code for pattern in [
            'fetch(', 'axios', 'http.', 'XMLHttpRequest', 'require(',
            'import ', 'from ', 'socket', 'websocket', 'database',
            'localStorage', 'sessionStorage'
        ])
        
        # Détection événements UI
        has_ui_events = any(pattern in code_lower for pattern in [
            'onclick', 'onchange', 'onsubmit', 'keydown', 'keyup',
            'mousedown', 'mouseup', 'scroll', 'resize', 'attachEvent'
        ])
        
        # Détection effets de bord
        has_side_effects = any(pattern in self.code for pattern in [
            'console.', 'print(', 'window.', 'global.',
            'setTimeout', 'setInterval', 'Date.now', 'Math.random'
        ])
        
        # Fonctions pures (sans dépendances)
        pure_functions = 0
        for line in self.lines:
            if 'function' in line or 'def ' in line:
                # Simple heuristique: fonction sans this, document, window
                if 'this.' not in line and 'document.' not in line and 'window.' not in line:
                    pure_functions += 1
        
        # Compter fonctions non testables directement
        untestable = 0
        if has_dom:
            untestable += self.code.count('attachEvent') + self.code.count('addEventListener')
        
        return {
            'has_dom': has_dom,
            'has_external_deps': has_external_deps,
            'has_ui_events': has_ui_events,
            'has_side_effects': has_side_effects,
            'has_pure_functions': pure_functions > 0,
            'pure_function_count': pure_functions,
            'untestable_count': untestable
        }
    
    def _count_branches(self) -> int:
        """Compte les branches dans le code"""
        patterns = [r'\bif\b', r'\belif\b', r'\belse\b', r'\bcase\b', r'\bfor\b', r'\bwhile\b']
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, self.code))
        return count
    
    def _coverage_strengths(self, tests_generated: int = 1, functions: int = 0) -> List[str]:
        """Points forts pour la couverture - VERSION HONNÊTE"""
        strengths = []
        
        if functions > 0:
            ratio = tests_generated / functions
            if ratio >= 1:
                strengths.append('✅ Au moins 1 test par fonction')
            if ratio >= 2:
                strengths.append('✅ Tests multiples par fonction (edge cases)')
        
        if self.count_functions() > 0 and self.count_functions() < 10:
            strengths.append('✅ Nombre de fonctions raisonnable, testable')
        if self._count_branches() < 15:
            strengths.append('✅ Complexité faible, facile à couvrir')
        
        return strengths if strengths else ['⚠️ Peu de points forts - améliorer les tests']
    
    def _get_coverage_verdict(self, coverage: int, tests: int, functions: int) -> str:
        """Verdict honnête sur la couverture"""
        if coverage < 15:
            return f"🚨 CRITIQUE: {tests} test(s) pour {functions} fonctions = couverture quasi nulle"
        elif coverage < 30:
            return f"⚠️ FAIBLE: Tests superficiels, seulement les chemins principaux testés"
        elif coverage < 60:
            return f"📊 PARTIEL: Couverture de base, mais manque edge cases et branches"
        elif coverage < 80:
            return f"✅ CORRECT: Bonne couverture des chemins principaux"
        else:
            return f"🎯 EXCELLENT: Couverture complète incluant edge cases"
    
    def _get_smell_verdict(self, score: int, smells: List[Dict]) -> str:
        """Verdict honnête sur les code smells"""
        high_count = len([s for s in smells if s.get('severity') == 'high'])
        
        if score >= 85:
            return "✅ Code propre, bien structuré"
        elif score >= 70:
            return "📊 Qualité acceptable avec quelques améliorations possibles"
        elif score >= 55:
            if high_count > 0:
                return f"⚠️ {high_count} problème(s) majeur(s) à corriger en priorité"
            return "⚠️ Plusieurs code smells détectés, refactoring recommandé"
        else:
            return f"🚨 Qualité insuffisante: {len(smells)} problèmes détectés dont {high_count} critiques"
    
    # ========================================
    # ⚡ PERFORMANCE ANALYZER
    # ========================================
    def analyze_performance(self) -> Dict[str, Any]:
        """Analyse les performances du code"""
        bottlenecks = []
        
        for i, line in enumerate(self.lines, 1):
            # Boucles imbriquées
            if re.search(r'for.*for|while.*while', self.code[max(0,i*50-200):i*50]):
                bottlenecks.append({
                    'type': 'Boucles imbriquées',
                    'line': i,
                    'impact': 'O(n²)',
                    'suggestion': 'Optimiser avec des structures de données adaptées'
                })
            
            # Concaténation de strings dans une boucle (Java)
            if self.extension == 'java' and '+=' in line and 'String' in line:
                bottlenecks.append({
                    'type': 'Concaténation String dans boucle',
                    'line': i,
                    'impact': 'O(n²)',
                    'suggestion': 'Utiliser StringBuilder'
                })
        
        # Score basé sur les bottlenecks
        score = max(60, 100 - len(bottlenecks) * 10)
        
        # Déterminer la complexité dominante
        complexity = 'O(n)' if bottlenecks else 'O(1)'
        if any('O(n²)' in b.get('impact', '') for b in bottlenecks):
            complexity = 'O(n²)'
        
        return {
            'score': score,
            'level': 'Excellent' if score >= 85 else ('Bon' if score >= 70 else 'À optimiser'),
            'bottlenecks': bottlenecks,
            'complexity': complexity,
            'strengths': self._performance_strengths()
        }
    
    def _performance_strengths(self) -> List[str]:
        """Points forts performance"""
        strengths = []
        if 'StringBuilder' in self.code or 'StringBuffer' in self.code:
            strengths.append('✅ Utilisation de StringBuilder')
        if 'HashMap' in self.code or 'dict' in self.code:
            strengths.append('✅ Structures de données efficaces')
        return strengths if strengths else ['✅ Pas de bottleneck majeur détecté']
    
    # ========================================
    # 👃 CODE SMELL DETECTOR - VERSION HONNÊTE
    # ========================================
    def detect_code_smells(self) -> Dict[str, Any]:
        """Détecte les code smells - VERSION COMPLÈTE ET HONNÊTE"""
        smells = []
        penalties = 0  # Pénalités cumulées
        
        # Long method (> 30 lignes)
        functions = self._get_function_lengths()
        long_methods = 0
        for name, length in functions.items():
            if length > 50:
                smells.append({
                    'type': 'Very Long Method',
                    'location': name,
                    'detail': f'{length} lignes (max recommandé: 30)',
                    'suggestion': 'Diviser en méthodes plus petites',
                    'severity': 'high'
                })
                penalties += 8
                long_methods += 1
            elif length > 30:
                smells.append({
                    'type': 'Long Method',
                    'location': name,
                    'detail': f'{length} lignes',
                    'suggestion': 'Diviser en méthodes plus petites',
                    'severity': 'medium'
                })
                penalties += 4
                long_methods += 1
        
        # God class (> 300 lignes)
        if len(self.lines) > 500:
            smells.append({
                'type': 'God Class',
                'location': self.filename,
                'detail': f'{len(self.lines)} lignes (critique)',
                'suggestion': 'Diviser en modules plus petits',
                'severity': 'high'
            })
            penalties += 10
        elif len(self.lines) > 300:
            smells.append({
                'type': 'Large File',
                'location': self.filename,
                'detail': f'{len(self.lines)} lignes',
                'suggestion': 'Envisager de diviser ce fichier',
                'severity': 'medium'
            })
            penalties += 5
        
        # Magic numbers
        magic_numbers = re.findall(r'[^0-9\.](\d{2,})[^0-9\.]', self.code)
        if len(magic_numbers) > 5:
            smells.append({
                'type': 'Magic Numbers',
                'location': 'Multiple',
                'detail': f'{len(magic_numbers)} nombres magiques',
                'suggestion': 'Utiliser des constantes nommées',
                'severity': 'medium'
            })
            penalties += 3
        elif len(magic_numbers) > 3:
            penalties += 2
        
        # ========== NOUVEAUX CODE SMELLS POUR JS ==========
        
        # 🔥 Pattern "_that = this" - ancien et mauvaise pratique
        that_pattern = len(re.findall(r'_that\s*=\s*this|that\s*=\s*this|self\s*=\s*this', self.code))
        if that_pattern > 0:
            smells.append({
                'type': 'Outdated "that = this" Pattern',
                'location': self.filename,
                'detail': f'{that_pattern} occurrences de _that/that/self = this',
                'suggestion': 'Utiliser arrow functions () => {} ou .bind(this)',
                'severity': 'medium'
            })
            penalties += that_pattern * 2
        
        # 🔥 Duplication de code (même bloc répété)
        # Chercher des patterns dupliqués (lignes similaires)
        duplicate_patterns = self._detect_code_duplication()
        if duplicate_patterns > 3:
            smells.append({
                'type': 'Code Duplication',
                'location': self.filename,
                'detail': f'{duplicate_patterns} blocs de code similaires',
                'suggestion': 'Extraire en fonctions réutilisables',
                'severity': 'high'
            })
            penalties += min(10, duplicate_patterns * 2)
        
        # 🔥 Dépendances globales (scheduler, moment, $)
        global_deps = []
        if 'scheduler.' in self.code and 'scheduler' not in self.code[:200]:
            global_deps.append('scheduler')
        if 'moment(' in self.code and 'moment' not in self.code[:200]:
            global_deps.append('moment')
        if re.search(r'\$\(', self.code) and 'jquery' not in self.code[:300].lower():
            global_deps.append('jQuery')
        
        if len(global_deps) >= 2:
            smells.append({
                'type': 'Implicit Global Dependencies',
                'location': self.filename,
                'detail': f'Dépendances globales: {", ".join(global_deps)}',
                'suggestion': 'Injecter les dépendances explicitement',
                'severity': 'medium'
            })
            penalties += len(global_deps) * 2
        
        # 🔥 Fonctions avec trop de responsabilités (beaucoup de if/for/while)
        complex_functions = self._detect_complex_functions()
        if complex_functions:
            for func_name, complexity in complex_functions[:3]:
                smells.append({
                    'type': 'Function Too Complex',
                    'location': func_name,
                    'detail': f'Complexité cyclomatique ≈ {complexity}',
                    'suggestion': 'Diviser en fonctions plus simples',
                    'severity': 'high' if complexity > 15 else 'medium'
                })
                penalties += 3 if complexity > 15 else 2
        
        # Callbacks inline (fonction anonyme dans paramètre)
        inline_callbacks = len(re.findall(r'\(\s*function\s*\([^)]*\)\s*{', self.code))
        if inline_callbacks > 5:
            smells.append({
                'type': 'Callback Hell',
                'location': 'Multiple',
                'detail': f'{inline_callbacks} callbacks inline',
                'suggestion': 'Extraire en fonctions nommées ou utiliser async/await',
                'severity': 'high'
            })
            penalties += min(10, inline_callbacks)
        elif inline_callbacks > 2:
            smells.append({
                'type': 'Inline Callbacks',
                'location': 'Multiple', 
                'detail': f'{inline_callbacks} callbacks',
                'suggestion': 'Préférer les fonctions nommées',
                'severity': 'low'
            })
            penalties += 2
        
        # Couplage jQuery fort
        jquery_calls = len(re.findall(r'\$\([^)]+\)', self.code))
        if jquery_calls > 20:
            smells.append({
                'type': 'Tight jQuery Coupling',
                'location': self.filename,
                'detail': f'{jquery_calls} appels jQuery',
                'suggestion': 'Extraire la logique DOM dans des helpers',
                'severity': 'medium'
            })
            penalties += 5
        
        # Mélange UI/Logique métier (events + calculs dans même fonction)
        has_event_handlers = len(re.findall(r'on[A-Z]\w+|addEventListener|attachEvent|\.click\(|\.on\(', self.code))
        has_business_logic = len(re.findall(r'if.*return|for.*{|while.*{|switch.*{', self.code))
        if has_event_handlers > 5 and has_business_logic > 10:
            smells.append({
                'type': 'Mixed Concerns',
                'location': self.filename,
                'detail': 'UI events + logique métier mélangés',
                'suggestion': 'Séparer la logique métier des handlers UI',
                'severity': 'high'
            })
            penalties += 8
        
        # Variables globales implicites
        global_vars = len(re.findall(r'^\s*var\s+\w+\s*=', self.code, re.MULTILINE))
        if global_vars > 10:
            smells.append({
                'type': 'Too Many Global Variables',
                'location': self.filename,
                'detail': f'{global_vars} variables avec var',
                'suggestion': 'Utiliser const/let et encapsuler dans modules',
                'severity': 'medium'
            })
            penalties += 4
        
        # 🔥 Usage de "var" au lieu de const/let (JavaScript moderne)
        if self.extension == 'js':
            var_usage = len(re.findall(r'\bvar\s+\w+', self.code))
            const_let_usage = len(re.findall(r'\b(const|let)\s+\w+', self.code))
            if var_usage > 0 and const_let_usage == 0:
                smells.append({
                    'type': 'Outdated "var" Usage',
                    'location': self.filename,
                    'detail': f'{var_usage} déclarations avec var (0 const/let)',
                    'suggestion': 'Utiliser const pour les constantes, let pour les variables',
                    'severity': 'medium'
                })
                penalties += min(6, var_usage)
            elif var_usage > 5:
                smells.append({
                    'type': 'Mixed var/const/let',
                    'location': self.filename,
                    'detail': f'{var_usage} var vs {const_let_usage} const/let',
                    'suggestion': 'Migrer tous les var vers const/let',
                    'severity': 'low'
                })
                penalties += 2
        
        # Deep nesting (plus de 4 niveaux)
        deep_nesting = len(re.findall(r'{[^{}]*{[^{}]*{[^{}]*{[^{}]*{', self.code))
        if deep_nesting > 0:
            smells.append({
                'type': 'Deep Nesting',
                'location': self.filename,
                'detail': f'{deep_nesting} blocs profondément imbriqués',
                'suggestion': 'Extraire en fonctions, utiliser early return',
                'severity': 'medium'
            })
            penalties += 4
        
        # Calcul du score HONNÊTE
        base_score = 100
        score = max(45, base_score - penalties)
        
        # Ajustements selon sévérité
        high_severity = len([s for s in smells if s.get('severity') == 'high'])
        if high_severity >= 3:
            score = min(score, 65)  # Plafonné si 3+ problèmes graves
        elif high_severity >= 2:
            score = min(score, 75)  # Plafonné si 2 problèmes graves
        
        # Si beaucoup de smells détectés, plafonner davantage
        if len(smells) >= 5:
            score = min(score, 70)
        
        # Lignes par fonction
        avg_lines = sum(functions.values()) / max(1, len(functions)) if functions else len(self.lines)
        
        return {
            'score': score,
            'level': 'Excellent' if score >= 85 else ('Bon' if score >= 70 else ('Acceptable' if score >= 55 else 'À améliorer')),
            'smells': smells,
            'smells_count': len(smells),
            'high_severity_count': high_severity,
            'lines_per_function': int(avg_lines),
            'penalties': penalties,
            'strengths': self._smell_strengths(),
            'honest_verdict': self._get_smell_verdict(score, smells)
        }
    
    def _get_function_lengths(self) -> Dict[str, int]:
        """Retourne la longueur de chaque fonction - SUPPORTE JavaScript"""
        functions = {}
        
        if self.extension == 'java':
            pattern = r'(public|private|protected)?\s*(static)?\s*\w+\s+(\w+)\s*\([^)]*\)\s*{'
        elif self.extension == 'py':
            pattern = r'def\s+(\w+)\s*\('
        elif self.extension == 'ts':
            pattern = r'(async\s+)?(\w+)\s*\([^)]*\)\s*[:{]'
        elif self.extension == 'js':
            # JavaScript: plusieurs patterns possibles
            patterns = [
                r'function\s+(\w+)\s*\([^)]*\)\s*{',           # function name() {}
                r'(\w+)\s*[:=]\s*function\s*\([^)]*\)\s*{',    # name: function() {} ou name = function() {}
                r'(\w+)\s*[:=]\s*\([^)]*\)\s*=>\s*[{]',        # name = () => {}
            ]
            
            for pattern in patterns:
                matches = list(re.finditer(pattern, self.code))
                for i, match in enumerate(matches):
                    name = match.group(1)
                    if name and not name.startswith('_'):  # Ignorer les fonctions privées
                        start = self.code[:match.start()].count('\n')
                        # Trouver la fin de la fonction (accolade fermante correspondante)
                        func_start = match.end()
                        brace_count = 1
                        pos = func_start
                        while pos < len(self.code) and brace_count > 0:
                            if self.code[pos] == '{':
                                brace_count += 1
                            elif self.code[pos] == '}':
                                brace_count -= 1
                            pos += 1
                        end_line = self.code[:pos].count('\n')
                        func_length = end_line - start
                        if func_length > 0:
                            functions[name] = func_length
            return functions
        else:
            return functions
        
        matches = list(re.finditer(pattern, self.code))
        
        for i, match in enumerate(matches):
            name = match.group(3) if self.extension == 'java' else (match.group(1) if self.extension == 'py' else match.group(2))
            start = self.code[:match.start()].count('\n')
            end = matches[i+1].start() if i+1 < len(matches) else len(self.code)
            end_line = self.code[:end].count('\n')
            functions[name or f'func_{i}'] = end_line - start
        
        return functions
    
    def _smell_strengths(self) -> List[str]:
        """Points forts qualité"""
        strengths = []
        if len(self.lines) < 200:
            strengths.append('✅ Fichier de taille raisonnable')
        if self.count_functions() > 0 and len(self.lines) / self.count_functions() < 20:
            strengths.append('✅ Fonctions courtes et focalisées')
        # Bonnes pratiques
        if 'const ' in self.code and 'var ' not in self.code:
            strengths.append('✅ Utilisation de const (pas de var)')
        if '=>' in self.code:
            strengths.append('✅ Arrow functions modernes')
        return strengths if strengths else ['⚠️ Peu de points forts détectés']
    
    def _detect_code_duplication(self) -> int:
        """Détecte les blocs de code dupliqués"""
        # Chercher des patterns de code similaires
        duplicate_count = 0
        
        # Pattern: mêmes appels de fonction répétés
        function_calls = re.findall(r'\.\w+\([^)]*\)', self.code)
        call_counts = {}
        for call in function_calls:
            # Ignorer les appels courants
            if call not in ['.log(', '.push(', '.pop(', '.length']:
                call_counts[call] = call_counts.get(call, 0) + 1
        
        # Compter les appels très répétitifs (>4 fois)
        for call, count in call_counts.items():
            if count > 4:
                duplicate_count += 1
        
        # Pattern: blocs if similaires
        if_blocks = re.findall(r'if\s*\([^)]+\)\s*{[^}]{10,50}}', self.code)
        if len(if_blocks) != len(set(if_blocks)):
            duplicate_count += 2
        
        # Pattern: assignations similaires répétées
        assignments = re.findall(r'\w+\.\w+\s*=\s*[^;]+;', self.code)
        assignment_patterns = {}
        for assign in assignments:
            # Extraire le pattern (ex: .innerHTML = ...)
            pattern = re.sub(r'\w+\.', '.', assign)
            assignment_patterns[pattern] = assignment_patterns.get(pattern, 0) + 1
        
        for pattern, count in assignment_patterns.items():
            if count > 5:
                duplicate_count += 1
        
        return duplicate_count
    
    def _detect_complex_functions(self) -> List[tuple]:
        """Détecte les fonctions avec trop de complexité"""
        complex_functions = []
        
        # Chercher les fonctions et analyser leur corps
        if self.extension in ['js', 'ts']:
            # Pattern pour trouver les fonctions JS
            func_pattern = r'(?:function\s+(\w+)|(\w+)\s*=\s*function|(\w+)\s*:\s*function)\s*\([^)]*\)\s*{'
            matches = list(re.finditer(func_pattern, self.code))
            
            for i, match in enumerate(matches):
                func_name = match.group(1) or match.group(2) or match.group(3) or f'anonymous_{i}'
                start = match.end()
                
                # Trouver la fin de la fonction (simplifié)
                end = start + 500  # Approximation
                if i + 1 < len(matches):
                    end = matches[i + 1].start()
                
                func_body = self.code[start:end]
                
                # Calculer la complexité cyclomatique approximative
                complexity = 1  # Base
                complexity += len(re.findall(r'\bif\b', func_body))
                complexity += len(re.findall(r'\belse\b', func_body))
                complexity += len(re.findall(r'\bfor\b', func_body))
                complexity += len(re.findall(r'\bwhile\b', func_body))
                complexity += len(re.findall(r'\bswitch\b', func_body))
                complexity += len(re.findall(r'\bcase\b', func_body))
                complexity += len(re.findall(r'\bcatch\b', func_body))
                complexity += len(re.findall(r'\?\s*[^:]+:', func_body))  # Ternaire
                
                if complexity > 10:
                    complex_functions.append((func_name, complexity))
        
        # Trier par complexité décroissante
        complex_functions.sort(key=lambda x: x[1], reverse=True)
        return complex_functions
    
    # ========================================
    # HELPERS
    # ========================================
    def count_functions(self) -> int:
        """Compte le nombre de fonctions/méthodes - AMÉLIORÉ pour AMD/CommonJS"""
        if self.extension == 'java':
            return len(re.findall(r'(public|private|protected)\s+\w+\s+\w+\s*\([^)]*\)\s*{', self.code))
        elif self.extension == 'py':
            return len(re.findall(r'def\s+\w+\s*\(', self.code))
        elif self.extension in ['ts', 'js']:
            count = 0
            # Pattern 1: function name() { - fonctions classiques
            count += len(re.findall(r'\bfunction\s+\w+\s*\(', self.code))
            # Pattern 2: var/let/const name = function() { - fonctions assignées (AMD style)
            count += len(re.findall(r'(?:var|let|const)\s+\w+\s*=\s*function\s*\(', self.code))
            # Pattern 3: name: function() { - méthodes d'objet
            count += len(re.findall(r'\w+\s*:\s*function\s*\(', self.code))
            # Pattern 4: name = function() { - assignation simple
            count += len(re.findall(r'[a-zA-Z_]\w*\s*=\s*function\s*\(', self.code))
            # Pattern 5: (params) => { - arrow functions
            count += len(re.findall(r'\([^)]*\)\s*=>\s*{', self.code))
            # Pattern 6: prototype.name = function
            count += len(re.findall(r'\.prototype\.\w+\s*=\s*function', self.code))
            # Éviter les doublons en limitant
            return min(count, count // 2 + 5) if count > 10 else count
        return 0
    
    def count_classes(self) -> int:
        """Compte le nombre de classes"""
        if self.extension == 'java':
            return len(re.findall(r'class\s+\w+', self.code))
        elif self.extension == 'py':
            return len(re.findall(r'class\s+\w+', self.code))
        elif self.extension in ['ts', 'js']:
            count = 0
            # Classes ES6
            count += len(re.findall(r'\bclass\s+\w+', self.code))
            # Constructeurs (function Name avec majuscule)
            count += len(re.findall(r'\bfunction\s+[A-Z]\w+\s*\(', self.code))
            # AMD modules
            if 'define(' in self.code:
                count += 1
            return max(1, count)
        return 1  # Par défaut, considérer comme 1 module


def analyze_code(source_code: str, filename: str, use_ai: bool = False) -> Dict[str, Any]:
    """Fonction utilitaire pour analyser du code"""
    analyzer = CodeAnalyzer(source_code, filename, use_ai)
    return analyzer.analyze_all()
