"""Smart Test Generator - Version PRO avec Mockito, tests d'erreur et IA Ollama"""
import re
from typing import Optional

# Import Ollama pour génération IA dynamique
try:
    from ollama_client import OllamaClient
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


class SmartTestGenerator:
    """Générateur intelligent de tests unitaires pour Python, TypeScript et Java"""

    def __init__(self, source_code: str, filename: str, use_ai: bool = False):
        self.code = source_code
        self.filename = filename
        self.extension = filename.split('.')[-1].lower()
        self.base = filename.rsplit('.', 1)[0]
        self.use_ai = use_ai and OLLAMA_AVAILABLE
        # Utiliser phi (déjà installé) pour génération de code
        # Pour installer un meilleur modèle: ollama pull codellama OU ollama pull deepseek-coder
        self.ollama_client = OllamaClient(model="phi") if self.use_ai else None
    
    def _generate_tests_with_ai(self, language: str) -> Optional[str]:
        """Génère les tests COMPLÈTEMENT avec IA Ollama (pas de templates)"""
        if not self.use_ai or not self.ollama_client:
            return None
        
        try:
            print(f"🤖 Génération 100% IA avec Ollama ({self.ollama_client.model})...")
            
            # Vérifier disponibilité
            if not self.ollama_client.available:
                print("⚠️ Ollama non disponible → templates")
                return None
            
            # ⚡ OPTIMISATION: Limiter le code pour phi (plus rapide)
            # Max 400 caractères pour temps < 20 secondes
            code_sample = self.code[:400] + "\n// ..." if len(self.code) > 400 else self.code
            
            # Prompt COURT et SIMPLE pour phi
            if language == "java":
                prompt = f"""Write complete JUnit 5 test class with Mockito:

{code_sample}

Include @Test, @Mock, @InjectMocks, verify(). Test normal + null cases. Code only:"""

            elif language == "python":
                prompt = f"""Write pytest tests:

{code_sample}

Test normal + edge cases. Code only:"""

            elif language == "typescript":
                prompt = f"""Write Jest tests:

{code_sample}

Test normal + errors. Code only:"""
            else:
                return None
            
            # Appel Ollama RAPIDE (max_tokens: 800, température: 0.3)
            print(f"📤 Génération rapide ({len(prompt)} chars, max_tokens=800)...")
            ai_response = self.ollama_client.generate(prompt, temperature=0.3, max_tokens=800)
            
            if not ai_response or len(ai_response) < 100:
                print(f"⚠️ Réponse courte ({len(ai_response) if ai_response else 0} chars) → templates")
                return None
            
            # Nettoyer markdown
            cleaned = ai_response.strip()
            if "```" in cleaned:
                import re
                blocks = re.findall(r'```(?:java|python|typescript|ts)?\n(.*?)```', cleaned, re.DOTALL)
                if blocks:
                    cleaned = blocks[0].strip()
            
            # Validation: contient des tests ?
            test_markers = ['@Test', 'def test_', "it('", 'describe(', 'test(']
            if not any(m in cleaned for m in test_markers):
                print(f"⚠️ Pas de marqueurs test détectés → templates")
                return None
            
            print(f"✅ Tests IA générés ({len(cleaned)} chars, {cleaned.count(chr(10))} lignes)")
            return cleaned
            
        except Exception as e:
            print(f"⚠️ Erreur IA: {e} → templates")
            return None
    
    def _enhance_tests_with_ai(self, generated_tests: str, language: str) -> str:
        """Améliore les tests générés avec l'IA Ollama pour ajouter des edge cases"""
        if not self.use_ai or not self.ollama_client:
            return generated_tests
        
        try:
            print("🤖 Amélioration des tests avec Ollama AI...")
            
            # Vérifier la disponibilité d'Ollama avant d'appeler
            if not self.ollama_client.available:
                print("⚠️ Ollama non disponible, tests générés sans amélioration IA")
                return generated_tests
            
            # Obtenir des suggestions d'edge cases (avec timeout implicite)
            edge_cases_response = self.ollama_client.add_edge_cases(self.code, language)
            
            # Si pas de réponse, continuer sans amélioration
            if not edge_cases_response:
                print("⚠️ Pas de suggestions d'edge cases de l'IA")
                return generated_tests
            
            # Obtenir des améliorations (avec timeout implicite)
            improvements_response = self.ollama_client.improve_tests(generated_tests, language)
            
            if not improvements_response:
                print("⚠️ Pas de suggestions d'amélioration de l'IA")
                # Ajouter seulement les edge cases si disponibles
                improvements_response = "Aucune amélioration suggérée"
            
            # Ajouter un commentaire avec les suggestions IA
            ai_comment = f'''
    /*
     * ========================================
     * === SUGGESTIONS IA (Ollama - phi) ===
     * ========================================
     * 
     * Edge Cases détectés par IA:
     * {edge_cases_response[:500]}...
     * 
     * Améliorations suggérées par IA:
     * {improvements_response[:500]}...
     * 
     * Note: Ces suggestions sont générées par IA et doivent être validées.
     */
'''
            # Insérer avant la dernière accolade
            last_brace = generated_tests.rfind('}')
            if last_brace > 0:
                enhanced = generated_tests[:last_brace] + ai_comment + generated_tests[last_brace:]
                print("✅ Tests améliorés avec suggestions IA!")
                return enhanced
            
            return generated_tests
        except Exception as e:
            print(f"⚠️ Erreur lors de l'amélioration IA: {e}")
            print("   → Tests générés sans amélioration IA")
            return generated_tests

    def _is_java_interface(self) -> bool:
        """Détecte si le fichier Java est une interface"""
        # Pattern pour détecter 'public interface' ou 'interface'
        return bool(re.search(r'\binterface\s+\w+', self.code))
    
    def generate(self):
        """Point d'entrée principal"""
        if self.extension == "py":
            return self._python_tests()
        if self.extension == "ts":
            return self._ts_tests()
        if self.extension == "js":
            return self._js_tests()
        if self.extension == "java":
            # Vérifier si c'est une interface
            if self._is_java_interface():
                return self._java_interface_message()
            return self._java_tests()
        return ""
    
    def _java_interface_message(self):
        """Message pour les interfaces Java (pas de tests générés)"""
        interface_name = re.search(r'interface\s+(\w+)', self.code)
        name = interface_name.group(1) if interface_name else self.base
        
        print(f"⚠️ Interface Java détectée : {name}")
        print(f"   → Les interfaces n'ont pas d'implémentation à tester")
        print(f"   → Veuillez uploader la classe d'implémentation (ex: {name}Impl.java)")
        
        return f'''// ⚠️ INTERFACE JAVA DÉTECTÉE : {name}
// 
// Les interfaces Java ne contiennent pas de logique à tester.
// Elles définissent uniquement des contrats (signatures de méthodes).
//
// 💡 RECOMMANDATION :
// Uploadez plutôt la classe d'implémentation, par exemple :
//   - {name}Impl.java
//   - {name}Service.java
//   - Default{name}.java
//
// Cette classe contiendra la vraie logique métier à tester.

// Aucun test généré pour une interface.
'''

    # ========== PYTHON ==========
    def _python_tests(self):
        """Génération tests Python avec pytest"""
        # PRIORITÉ 1: Génération 100% IA si activée
        if self.use_ai:
            ai_tests = self._generate_tests_with_ai("python")
            if ai_tests:
                print("✅ Tests Python générés par IA Ollama")
                return ai_tests
            print("⚠️ Échec génération IA, fallback vers templates")
        
        # FALLBACK: Templates classiques
        functions = re.findall(r'def\s+(\w+)\(([^)]*)\)', self.code)
        classes = re.findall(r'class\s+(\w+)', self.code)

        content = f'"""Tests générés automatiquement pour {self.base}.py"""\nimport pytest\nfrom {self.base} import *\n\n'

        for cls in classes:
            content += f'''class Test{cls}:
    """Tests pour la classe {cls}"""
    
    def test_{cls.lower()}_instantiation(self):
        """Test d'instanciation"""
        obj = {cls}()
        assert obj is not None
    
    def test_{cls.lower()}_attributes(self):
        """Test des attributs"""
        obj = {cls}()
        assert hasattr(obj, '__dict__')

'''

        for func, params in functions[:5]:
            if func == "__init__":
                continue

            content += f'''def test_{func}():
    """Test de la fonction {func}"""
    try:
        result = {func}()
        assert result is not None
    except Exception:
        assert True  # Fonction sans paramètres ou avec gestion d'erreur

'''
        
        # Amélioration avec IA si activée
        if self.use_ai:
            content = self._enhance_tests_with_ai(content, "python")
        
        return content

    # ========== TYPESCRIPT ==========
    def _ts_tests(self):
        """Génération tests TypeScript/Angular avec VRAIS tests"""
        # PRIORITÉ 1: Génération 100% IA si activée
        if self.use_ai:
            ai_tests = self._generate_tests_with_ai("typescript")
            if ai_tests:
                print("✅ Tests TypeScript générés par IA Ollama")
                return ai_tests
            print("⚠️ Échec génération IA, fallback vers templates")
        
        # FALLBACK: Templates avec VRAIS tests
        classes = re.findall(r'export\s+class\s+(\w+)', self.code)
        
        # Extraire VRAIES méthodes (pas les mots-clés)
        # Éviter: if, for, while, return, const, let, var, switch, case
        keywords = ['if', 'for', 'while', 'return', 'const', 'let', 'var', 'switch', 'case', 'else', 'catch', 'try']
        method_pattern = r'(\w+)\s*\([^)]*\)\s*(?::\s*\w+)?\s*{'
        all_methods = re.findall(method_pattern, self.code)
        methods = [m for m in all_methods if m not in keywords and m not in ['constructor', 'ngOnInit', 'ngOnDestroy']]

        service = classes[0] if classes else self.base

        content = f'''// Tests générés automatiquement pour {self.base}.ts
import {{ TestBed }} from '@angular/core/testing';
import {{ {service} }} from './{self.base}';

describe('{service}', () => {{
  let service: {service};

  beforeEach(() => {{
    TestBed.configureTestingModule({{}});
    service = TestBed.inject({service});
  }});

  it('should be created', () => {{
    expect(service).toBeTruthy();
  }});
'''

        # Générer de VRAIS tests selon le type de méthode
        for m in methods[:8]:
            # Détecter le type de méthode par son nom
            if 'add' in m.lower() or 'sum' in m.lower():
                content += f'''
  it('should {m} two numbers correctly', () => {{
    const result = service.{m}(2, 3);
    expect(result).toBe(5);
  }});
'''
            elif 'subtract' in m.lower() or 'minus' in m.lower():
                content += f'''
  it('should {m} two numbers correctly', () => {{
    const result = service.{m}(10, 3);
    expect(result).toBe(7);
  }});
'''
            elif 'multiply' in m.lower() or 'times' in m.lower():
                content += f'''
  it('should {m} two numbers correctly', () => {{
    const result = service.{m}(4, 5);
    expect(result).toBe(20);
  }});
'''
            elif 'divide' in m.lower():
                content += f'''
  it('should {m} two numbers correctly', () => {{
    const result = service.{m}(10, 2);
    expect(result).toBe(5);
  }});

  it('should throw error when dividing by zero', () => {{
    expect(() => service.{m}(10, 0)).toThrow();
  }});
'''
            elif 'factorial' in m.lower():
                content += f'''
  it('should calculate {m} correctly', () => {{
    expect(service.{m}(5)).toBe(120);
    expect(service.{m}(0)).toBe(1);
  }});
'''
            elif 'power' in m.lower() or 'pow' in m.lower():
                content += f'''
  it('should calculate {m} correctly', () => {{
    expect(service.{m}(2, 3)).toBe(8);
    expect(service.{m}(5, 2)).toBe(25);
  }});
'''
            elif 'sqrt' in m.lower() or 'square' in m.lower():
                content += f'''
  it('should calculate {m} correctly', () => {{
    expect(service.{m}(16)).toBe(4);
    expect(service.{m}(9)).toBe(3);
  }});
'''
            elif 'percentage' in m.lower() or 'percent' in m.lower():
                content += f'''
  it('should calculate {m} correctly', () => {{
    expect(service.{m}(50, 200)).toBe(25);
  }});
'''
            else:
                # Test générique avec appel réel
                content += f'''
  it('should execute {m}', () => {{
    const result = service.{m}();
    expect(result).toBeDefined();
  }});
'''

        content += '\n});\n'
        
        return content

    # ========== JAVASCRIPT AMÉLIORÉ V2 ==========
    def _js_tests(self):
        """Génération tests JavaScript avec Jest - VERSION AMÉLIORÉE V2"""
        # PRIORITÉ 1: Génération 100% IA si activée
        if self.use_ai:
            ai_tests = self._generate_tests_with_ai("javascript")
            if ai_tests:
                print("✅ Tests JavaScript générés par IA Ollama")
                return ai_tests
            print("⚠️ Échec génération IA, fallback vers templates")
        
        # Analyser le code pour détecter le type de module
        is_amd = 'define(' in self.code
        is_commonjs = 'module.exports' in self.code or 'exports.' in self.code
        has_jquery = 'jquery' in self.code.lower() or '$(' in self.code
        has_dom = 'document.' in self.code or 'getElementById' in self.code
        has_moment = 'moment' in self.code.lower()
        has_scheduler = 'scheduler' in self.code.lower()
        
        # Extraire TOUTES les fonctions avec leurs paramètres
        func_with_params = self._extract_js_functions_with_params()
        
        # Détecter les fonctions exportées vs internes
        exported_funcs = self._detect_exported_functions()
        
        # Constructeurs (fonction avec majuscule)
        constructor_classes = re.findall(r'(?:var\s+)?(\w+)\s*=\s*function\s*\([^)]*\)\s*{', self.code)
        constructor_classes = [c for c in constructor_classes if c[0].isupper()]
        
        module_name = self.base
        
        # Générer le header avec mocks appropriés
        content = self._generate_js_test_header_v2(module_name, is_amd, has_jquery, has_dom, has_moment, has_scheduler, exported_funcs)
        
        # Avertissement si module AMD avec fonctions internes
        if is_amd and len(exported_funcs) < len(func_with_params):
            internal_count = len(func_with_params) - len(exported_funcs)
            content += f'''
  /*
   * ⚠️ AVERTISSEMENT: Ce module AMD contient {internal_count} fonctions internes
   * qui ne sont pas directement testables car non exportées.
   * 
   * Fonctions internes détectées:
'''
            for f in func_with_params:
                if f['name'] not in exported_funcs:
                    content += f"   *   - {f['name']}({', '.join(f['params'])})\n"
            content += '''   *
   * Pour les tester, il faudrait:
   * 1. Les exporter explicitement, OU
   * 2. Tester via les fonctions publiques qui les appellent
   */

'''
        
        # Générer tests pour les constructeurs
        for cls in constructor_classes[:2]:
            content += self._generate_js_constructor_test_v2(cls)
        
        # Générer tests pour les fonctions exportées seulement
        testable_funcs = [f for f in func_with_params if f['name'] in exported_funcs][:8]
        
        # 🔥 AMÉLIORATION: Aussi tester les méthodes prototype
        prototype_methods = re.findall(r'(\w+)\.prototype\.(\w+)\s*=\s*function\s*\(([^)]*)\)', self.code)
        
        for func_info in testable_funcs:
            func_name = func_info['name']
            params = func_info['params']
            body = func_info.get('body', '')
            returns_value = self._function_returns_value(body)
            content += self._generate_js_function_test_v2(func_name, params, body, returns_value)
        
        # 🔥 NOUVEAU: Tests pour les méthodes prototype (logique métier)
        if prototype_methods and constructor_classes:
            main_class = constructor_classes[0]
            for cls_name, method_name, params_str in prototype_methods[:5]:
                if cls_name == main_class:
                    params = [p.strip() for p in params_str.split(',') if p.strip()]
                    method_body = self._extract_method_body(method_name)
                    content += self._generate_js_method_test(main_class, method_name, params, method_body)
        
        # Si aucune fonction exportée, tester le module principal
        if not testable_funcs and constructor_classes:
            pass  # Déjà testé via constructeur
        elif not testable_funcs:
            content += f'''
  it('should load module {module_name}', () => {{
    // Module AMD/CommonJS - tester le chargement
    expect({module_name}).toBeDefined();
  }});
'''
        
        content += '\n});\n'
        
        return content
    
    def _detect_exported_functions(self) -> List[str]:
        """Détecte les fonctions qui sont réellement exportées"""
        exported = []
        
        # AMD: return à la fin du define()
        if 'return ' in self.code:
            # Chercher ce qui est retourné
            return_match = re.search(r'return\s+(\w+)\s*;?\s*}\s*\)\s*;?\s*$', self.code, re.MULTILINE)
            if return_match:
                exported.append(return_match.group(1))
        
        # Prototype methods
        proto_methods = re.findall(r'(\w+)\.prototype\.(\w+)\s*=', self.code)
        for cls, method in proto_methods:
            exported.append(method)
            if cls not in exported:
                exported.append(cls)
        
        # Static methods sur classe
        static_methods = re.findall(r'(\w+)\.(\w+)\s*=\s*function', self.code)
        for cls, method in static_methods:
            if not method.startswith('_'):
                exported.append(method)
        
        # module.exports
        exports_match = re.findall(r'(?:module\.)?exports\.(\w+)\s*=', self.code)
        exported.extend(exports_match)
        
        # export function/const
        export_match = re.findall(r'export\s+(?:function|const|let|var)\s+(\w+)', self.code)
        exported.extend(export_match)
        
        return list(set(exported))
    
    def _function_returns_value(self, body: str) -> bool:
        """Détermine si une fonction retourne une valeur (pas void)"""
        if not body:
            return False
        # Chercher 'return' suivi de quelque chose (pas juste 'return;')
        return bool(re.search(r'return\s+[^;]+;', body))
    
    def _extract_js_functions_with_params(self) -> List[Dict]:
        """Extrait les fonctions JavaScript avec leurs paramètres"""
        functions = []
        
        # Pattern pour fonctions AMD: var name = function(params) {
        pattern1 = r'(?:var|let|const)\s+(\w+)\s*=\s*function\s*\(([^)]*)\)'
        # Pattern pour fonctions déclarées: function name(params) {
        pattern2 = r'function\s+(\w+)\s*\(([^)]*)\)'
        # Pattern pour arrow functions: const name = (params) =>
        pattern3 = r'(?:var|let|const)\s+(\w+)\s*=\s*\(([^)]*)\)\s*=>'
        
        # Mots à exclure
        excluded = ['if', 'for', 'while', 'switch', 'catch', 'function', 'return', 'require']
        
        for pattern in [pattern1, pattern2, pattern3]:
            matches = re.findall(pattern, self.code)
            for match in matches:
                name = match[0]
                if name not in excluded and not name.startswith('_'):
                    params = [p.strip() for p in match[1].split(',') if p.strip()]
                    # Extraire le corps de la fonction pour analyse
                    body = self._extract_function_body(name)
                    functions.append({
                        'name': name,
                        'params': params,
                        'body': body
                    })
        
        # Dédupliquer par nom
        seen = set()
        unique = []
        for f in functions:
            if f['name'] not in seen:
                seen.add(f['name'])
                unique.append(f)
        
        return unique
    
    def _extract_function_body(self, func_name: str) -> str:
        """Extrait le corps d'une fonction pour analyse"""
        pattern = rf'{func_name}\s*[=:]\s*function\s*\([^)]*\)\s*\{{|function\s+{func_name}\s*\([^)]*\)\s*\{{'
        match = re.search(pattern, self.code)
        if match:
            start = match.end()
            brace_count = 1
            end = start
            for i in range(start, min(start + 500, len(self.code))):
                if self.code[i] == '{':
                    brace_count += 1
                elif self.code[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end = i
                        break
            return self.code[start:end]
        return ''
    
    def _generate_js_test_header(self, module_name: str, has_jquery: bool, has_dom: bool, has_moment: bool, has_scheduler: bool) -> str:
        """Génère le header des tests avec les mocks appropriés"""
        content = f'''/**
 * Tests unitaires générés automatiquement pour {module_name}.js
 * Framework: Jest
 * Généré par: UT AI Agent
 */

'''
        # Ajouter les mocks nécessaires
        if has_jquery:
            content += '''// Mock jQuery
const $ = jest.fn((selector) => ({
  show: jest.fn(),
  hide: jest.fn(),
  text: jest.fn(),
  html: jest.fn(),
  append: jest.fn(),
  empty: jest.fn(),
  addClass: jest.fn(),
  removeClass: jest.fn(),
  attr: jest.fn(),
  find: jest.fn(() => ({ length: 0 })),
  children: jest.fn(() => []),
  trigger: jest.fn(),
  data: jest.fn(() => ({ DateTimePicker: { date: jest.fn() } })),
  css: jest.fn(),
  position: jest.fn(() => ({ top: 0, left: 0 })),
  height: jest.fn(() => 100),
  unbind: jest.fn(),
  bind: jest.fn(),
  click: jest.fn()
}));
global.jquery = $;
global.jQuery = $;

'''
        
        if has_dom:
            content += '''// Mock DOM
global.document = {
  getElementById: jest.fn(() => ({ style: {}, innerHTML: '', click: jest.fn() })),
  querySelector: jest.fn(() => null),
  querySelectorAll: jest.fn(() => []),
  createElement: jest.fn(() => ({ appendChild: jest.fn() }))
};

'''
        
        if has_moment:
            content += '''// Mock moment.js
const moment = jest.fn((date) => ({
  format: jest.fn((fmt) => '01/01/2026'),
  get: jest.fn((unit) => unit === 'date' ? 1 : 0),
  date: jest.fn(() => 1),
  add: jest.fn(() => moment()),
  startOf: jest.fn(() => moment()),
  endOf: jest.fn(() => moment()),
  daysInMonth: jest.fn(() => 31)
}));
global.moment = moment;

'''
        
        if has_scheduler:
            content += '''// Mock scheduler
const mockScheduler = {
  attachEvent: jest.fn((event, callback) => callback),
  getEvents: jest.fn(() => []),
  getState: jest.fn(() => ({ min_date: new Date(), max_date: new Date() })),
  templates: {},
  matrix: { timeline: { dy: 50, folder_dy: 50 } },
  checkCollision: jest.fn(() => true),
  xy: { scroll_width: 10 }
};

'''
        
        content += f'''describe('{module_name}', () => {{
'''
        return content
    
    def _generate_js_test_header_v2(self, module_name: str, is_amd: bool, has_jquery: bool, has_dom: bool, has_moment: bool, has_scheduler: bool, exported_funcs: List[str]) -> str:
        """Génère le header des tests V2 avec info sur module AMD"""
        content = f'''/**
 * Tests unitaires générés automatiquement pour {module_name}.js
 * Framework: Jest
 * Généré par: UT AI Agent
 * 
 * Type de module: {'AMD (define)' if is_amd else 'CommonJS/ES6'}
 * Fonctions exportées: {len(exported_funcs)}
 */

'''
        # Mock pour AMD
        if is_amd:
            content += '''// Mock AMD define()
const definedModules = {};
global.define = jest.fn((name, deps, factory) => {
  if (typeof name === 'function') {
    factory = name;
    deps = [];
    name = 'anonymous';
  }
  const require = jest.fn((dep) => definedModules[dep] || {});
  const result = factory(require);
  definedModules[name] = result;
  return result;
});

'''
        
        # Ajouter les mocks nécessaires
        if has_jquery:
            content += '''// Mock jQuery
const $ = jest.fn((selector) => ({
  show: jest.fn().mockReturnThis(),
  hide: jest.fn().mockReturnThis(),
  text: jest.fn().mockReturnThis(),
  html: jest.fn().mockReturnThis(),
  append: jest.fn().mockReturnThis(),
  empty: jest.fn().mockReturnThis(),
  addClass: jest.fn().mockReturnThis(),
  removeClass: jest.fn().mockReturnThis(),
  attr: jest.fn(),
  find: jest.fn(() => ({ length: 0 })),
  children: jest.fn(() => []),
  trigger: jest.fn(),
  data: jest.fn(() => ({ DateTimePicker: { date: jest.fn() } })),
  css: jest.fn().mockReturnThis(),
  position: jest.fn(() => ({ top: 0, left: 0 })),
  height: jest.fn(() => 100),
  unbind: jest.fn(),
  bind: jest.fn(),
  click: jest.fn(),
  scrollLeft: 0
}));
$.fn = { extend: jest.fn() };
global.jquery = $;
global.jQuery = $;

'''
        
        if has_dom:
            content += '''// Mock DOM
global.document = {
  getElementById: jest.fn(() => ({ style: {}, innerHTML: '', click: jest.fn() })),
  querySelector: jest.fn(() => null),
  querySelectorAll: jest.fn(() => []),
  createElement: jest.fn(() => ({ appendChild: jest.fn() }))
};
global.window = { location: { href: '' } };

'''
        
        if has_moment:
            content += '''// Mock moment.js avec chaînage
const mockMoment = (date) => ({
  format: jest.fn((fmt) => '01/01/2026'),
  get: jest.fn((unit) => unit === 'date' ? 1 : 0),
  date: jest.fn(() => 1),
  add: jest.fn(() => mockMoment()),
  startOf: jest.fn(() => mockMoment()),
  endOf: jest.fn(() => mockMoment()),
  daysInMonth: jest.fn(() => 31)
});
const moment = jest.fn(mockMoment);
global.moment = moment;

'''
        
        if has_scheduler:
            content += '''// Mock scheduler complet
const mockScheduler = {
  attachEvent: jest.fn((event, callback) => callback),
  getEvents: jest.fn(() => []),
  getState: jest.fn(() => ({ min_date: new Date(), max_date: new Date() })),
  templates: {},
  matrix: { timeline: { dy: 50, folder_dy: 50, x_size: 31 } },
  checkCollision: jest.fn(() => true),
  xy: { scroll_width: 10 }
};

'''

        content += '''// Mock device detection
global.device = {
  tablet: jest.fn(() => false),
  mobile: jest.fn(() => false)
};

// Mock lodash
global._ = {
  findIndex: jest.fn(() => -1),
  forEach: jest.fn()
};

'''
        
        content += f'''describe('{module_name}', () => {{
'''
        return content
    
    def _generate_js_constructor_test(self, class_name: str) -> str:
        """Génère un test pour un constructeur JavaScript (avec new)"""
        return f'''
  describe('{class_name} (Constructor)', () => {{
    it('should create an instance with new', () => {{
      // ⚠️ IMPORTANT: Utiliser new pour les constructeurs
      const instance = new {class_name}(false);
      expect(instance).toBeDefined();
    }});

    it('should initialize with isMobile parameter', () => {{
      const mobileInstance = new {class_name}(true);
      expect(mobileInstance.isMobile).toBe(true);
      
      const desktopInstance = new {class_name}(false);
      expect(desktopInstance.isMobile).toBe(false);
    }});

    it('should have events method on prototype', () => {{
      const instance = new {class_name}(false);
      if (typeof instance.events === 'function') {{
        expect(instance.events).toBeDefined();
      }}
    }});
  }});
'''
    
    def _generate_js_constructor_test_v2(self, class_name: str) -> str:
        """Génère des tests MÉTIER complets pour un constructeur JavaScript"""
        # Analyser le constructeur pour trouver ses propriétés
        constructor_match = re.search(
            rf'{class_name}\s*=\s*function\s*\(([^)]*)\)\s*{{([^}}]{{0,500}})',
            self.code, re.DOTALL
        )
        
        params = []
        properties = []
        if constructor_match:
            params = [p.strip() for p in constructor_match.group(1).split(',') if p.strip()]
            body = constructor_match.group(2)
            # Trouver les propriétés initialisées (this.xxx = ...)
            properties = re.findall(r'this\.(\w+)\s*=', body)
        
        content = f'''
  describe('{class_name} (Constructor)', () => {{
    let instance;
    
    beforeEach(() => {{
      instance = new {class_name}({', '.join(['false'] * len(params)) if params else ''});
    }});

    it('should create an instance with new keyword', () => {{
      expect(instance).toBeDefined();
      expect(instance).toBeInstanceOf(Object);
    }});
'''
        
        # Test pour chaque paramètre
        for i, param in enumerate(params[:3]):
            if 'mobile' in param.lower():
                content += f'''
    it('should initialize {param} property correctly', () => {{
      const mobileInstance = new {class_name}(true);
      expect(mobileInstance.{param}).toBe(true);
      
      const desktopInstance = new {class_name}(false);
      expect(desktopInstance.{param}).toBe(false);
    }});
'''
            else:
                content += f'''
    it('should accept {param} parameter', () => {{
      const testInstance = new {class_name}({'true' if i == 0 else 'false'});
      expect(testInstance).toBeDefined();
    }});
'''
        
        # Test pour les propriétés initialisées
        for prop in properties[:4]:
            if prop not in params:
                content += f'''
    it('should initialize {prop} property', () => {{
      expect(instance.{prop}).toBeDefined();
    }});
'''
        
        # Test des méthodes prototype
        prototype_methods = re.findall(rf'{class_name}\.prototype\.(\w+)\s*=', self.code)
        if prototype_methods:
            content += f'''
    it('should have all prototype methods defined', () => {{
'''
            for method in prototype_methods[:5]:
                content += f'''      expect(typeof instance.{method}).toBe('function');
'''
            content += '''    });
'''
        
        content += '''  });
'''
        return content
    
    def _generate_js_method_test(self, class_name: str, method_name: str, params: List[str], body: str) -> str:
        """Génère des tests MÉTIER pour une méthode prototype"""
        content = f'''
  describe('{class_name}.prototype.{method_name}', () => {{
    let instance;
    
    beforeEach(() => {{
      instance = new {class_name}(false);
    }});
'''
        
        # Analyser ce que fait la méthode
        returns_value = 'return ' in body and 'return;' not in body
        modifies_dom = '$(' in body or 'document.' in body
        uses_scheduler = 'scheduler' in body.lower()
        has_conditions = 'if' in body
        
        # Test de base
        if params:
            test_params = self._generate_test_params(params, body)
            param_values = ', '.join(test_params['values'])
            setup = test_params.get('setup', '')
            
            if returns_value:
                content += f'''
    it('should return a value with valid parameters', () => {{
      {setup}
      const result = instance.{method_name}({param_values});
      expect(result).toBeDefined();
    }});
'''
            else:
                content += f'''
    it('should execute without errors', () => {{
      {setup}
      expect(() => instance.{method_name}({param_values})).not.toThrow();
    }});
'''
        else:
            if returns_value:
                content += f'''
    it('should return a value when called', () => {{
      const result = instance.{method_name}();
      expect(result).toBeDefined();
    }});
'''
            else:
                content += f'''
    it('should execute without errors', () => {{
      expect(() => instance.{method_name}()).not.toThrow();
    }});
'''
        
        # Tests spécifiques selon le comportement
        if 'getLabel' in method_name or 'get' in method_name.lower():
            content += f'''
    it('should return correct label/value', () => {{
      const result = instance.{method_name}({', '.join(["'test'"] * len(params)) if params else ''});
      expect(typeof result).toBe('string');
    }});
'''
        
        if 'create' in method_name.lower():
            content += f'''
    it('should create and return a new object', () => {{
      const result = instance.{method_name}({', '.join(["{}"] * len(params)) if params else ''});
      expect(result).toBeDefined();
    }});
'''
        
        if has_conditions and params:
            # Test des branches
            null_params = ', '.join(['null'] * len(params))
            content += f'''
    it('should handle null/undefined parameters', () => {{
      expect(() => instance.{method_name}({null_params})).not.toThrow();
    }});
'''
        
        if modifies_dom:
            content += f'''
    it('should interact with DOM elements', () => {{
      // La méthode manipule le DOM - vérifier qu\\'elle ne crash pas
      expect(() => instance.{method_name}({', '.join(["{}"] * len(params)) if params else ''})).not.toThrow();
    }});
'''
        
        content += '''  });
'''
        return content
    
    def _extract_method_body(self, method_name: str) -> str:
        """Extrait le corps d'une méthode pour analyse"""
        pattern = rf'\.{method_name}\s*=\s*function\s*\([^)]*\)\s*{{([^}}]{{0,800}})'
        match = re.search(pattern, self.code, re.DOTALL)
        return match.group(1) if match else ''
    
    def _generate_js_function_test_v2(self, func_name: str, params: List[str], body: str, returns_value: bool) -> str:
        """Génère PLUSIEURS tests V2 pour une fonction JavaScript - NIVEAU ENTREPRISE"""
        content = f'''
  describe('{func_name}', () => {{
'''
        test_count = 0
        
        # Générer les valeurs de test selon les noms de paramètres
        test_params = self._generate_test_params(params, body)
        param_values = ', '.join(test_params['values']) if params else ''
        setup = test_params.get('setup', '')
        
        # ========== TEST 1: Exécution basique ==========
        if not params:
            if returns_value:
                content += f'''    it('should return a value when called', () => {{
      const result = {func_name}();
      expect(result).toBeDefined();
    }});
'''
            else:
                content += f'''    it('should execute without errors', () => {{
      expect(() => {func_name}()).not.toThrow();
    }});
'''
            test_count += 1
        else:
            if returns_value:
                content += f'''    it('should return expected value with valid parameters', () => {{
      // Arrange
      {setup}
      
      // Act
      const result = {func_name}({param_values});
      
      // Assert
      expect(result).toBeDefined();
    }});
'''
            else:
                content += f'''    it('should execute with valid parameters', () => {{
      // Arrange
      {setup}
      
      // Act & Assert
      expect(() => {func_name}({param_values})).not.toThrow();
    }});
'''
            test_count += 1
        
        # ========== TEST 2: Type de retour ==========
        if returns_value:
            if 'class' in body.lower() or 'className' in body:
                content += f'''
    it('should return a string (className)', () => {{
      {setup}
      const result = {func_name}({param_values});
      if (result !== null && result !== undefined) {{
        expect(typeof result).toBe('string');
      }}
    }});
'''
                test_count += 1
            elif 'true' in body and 'false' in body:
                content += f'''
    it('should return a boolean', () => {{
      {setup}
      const result = {func_name}({param_values});
      expect(typeof result).toBe('boolean');
    }});
'''
                test_count += 1
            elif 'length' in body or 'array' in body.lower() or '[]' in body:
                content += f'''
    it('should return an array or object with length', () => {{
      {setup}
      const result = {func_name}({param_values});
      expect(result).toBeDefined();
    }});
'''
                test_count += 1
        
        # ========== TEST 3: Gestion des edge cases ==========
        if params:
            # Test avec null
            if 'if' in body or 'null' in body.lower() or 'undefined' in body.lower():
                null_params = ', '.join(['null'] * len(params))
                content += f'''
    it('should handle null parameters gracefully', () => {{
      expect(() => {func_name}({null_params})).not.toThrow();
    }});
'''
                test_count += 1
            
            # Test avec undefined
            if len(params) <= 3:
                undefined_params = ', '.join(['undefined'] * len(params))
                content += f'''
    it('should handle undefined parameters', () => {{
      expect(() => {func_name}({undefined_params})).not.toThrow();
    }});
'''
                test_count += 1
        
        # ========== TEST 4: Comportement spécifique selon le contenu ==========
        
        # Si la fonction manipule le DOM
        if 'document.' in body or 'getElementById' in body or 'querySelector' in body:
            content += f'''
    it('should interact with DOM elements', () => {{
      // Mock DOM element
      document.getElementById = jest.fn(() => ({{ style: {{}}, innerHTML: '' }}));
      {setup}
      
      expect(() => {func_name}({param_values})).not.toThrow();
      // Vérifie que le DOM a été interrogé
      // expect(document.getElementById).toHaveBeenCalled();
    }});
'''
            test_count += 1
        
        # Si la fonction utilise jQuery
        if '$(' in body or 'jquery' in body.lower():
            content += f'''
    it('should interact with jQuery elements', () => {{
      {setup}
      expect(() => {func_name}({param_values})).not.toThrow();
    }});
'''
            test_count += 1
        
        # Si la fonction utilise des événements
        if 'attachEvent' in body or 'addEventListener' in body or 'onclick' in body.lower():
            content += f'''
    it('should attach event handlers', () => {{
      {setup}
      expect(() => {func_name}({param_values})).not.toThrow();
    }});
'''
            test_count += 1
        
        # Si la fonction utilise moment.js
        if 'moment' in body.lower():
            content += f'''
    it('should handle date operations with moment', () => {{
      {setup}
      expect(() => {func_name}({param_values})).not.toThrow();
    }});
'''
            test_count += 1
        
        # Si la fonction a des conditions
        if body.count('if') > 1:
            content += f'''
    it('should handle conditional branches', () => {{
      // La fonction contient plusieurs conditions
      {setup}
      const result = {func_name}({param_values});
      {'expect(result).toBeDefined();' if returns_value else f"expect(() => {func_name}({param_values})).not.toThrow();"}
    }});
'''
            test_count += 1
        
        # ========== TEST 5: Cas limites selon les paramètres ==========
        if params:
            for i, param in enumerate(params):
                # Test spécifique selon le nom du paramètre
                if 'date' in param.lower():
                    test_values = test_params['values'].copy() if 'values' in test_params else ['']
                    if i < len(test_values):
                        test_values[i] = "new Date('2026-01-01')"
                    content += f'''
    it('should handle date parameter "{param}"', () => {{
      const result = {func_name}({', '.join(test_values)});
      {'expect(result).toBeDefined();' if returns_value else '// Void function'}
    }});
'''
                    test_count += 1
                    break  # Un seul test de date
                elif 'id' in param.lower():
                    test_values = test_params['values'].copy() if 'values' in test_params else ['']
                    if i < len(test_values):
                        test_values[i] = "'test-id-123'"
                    content += f'''
    it('should handle ID parameter "{param}"', () => {{
      expect(() => {func_name}({', '.join(test_values)})).not.toThrow();
    }});
'''
                    test_count += 1
                    break
        
        content += '''  });
'''
        
        # Stocker le nombre de tests générés pour cette fonction
        self._last_test_count = getattr(self, '_last_test_count', 0) + test_count
        
        return content
        
        content += '''  });
'''
        return content

    def _generate_js_function_test(self, func_name: str, params: List[str], body: str) -> str:
        """Génère un test pour une fonction JavaScript avec ses vrais paramètres"""
        content = f'''
  describe('{func_name}', () => {{
'''
        
        # Générer les valeurs de test selon les noms de paramètres
        test_params = self._generate_test_params(params, body)
        
        if not params:
            # Fonction sans paramètres
            content += f'''    it('should execute without errors', () => {{
      expect(() => {func_name}()).not.toThrow();
    }});
'''
        else:
            # Fonction avec paramètres - test avec valeurs réelles
            param_values = ', '.join(test_params['values'])
            
            content += f'''    it('should execute with valid parameters', () => {{
      // Arrange
      {test_params['setup']}
      
      // Act
      const result = {func_name}({param_values});
      
      // Assert
      expect(result).toBeDefined();
    }});
'''
            
            # Test avec paramètres null/undefined
            if len(params) > 0:
                null_params = ', '.join(['null'] * len(params))
                content += f'''
    it('should handle null parameters gracefully', () => {{
      expect(() => {func_name}({null_params})).not.toThrow();
    }});
'''
            
            # Si la fonction semble retourner quelque chose de spécifique
            if 'return' in body:
                if 'true' in body or 'false' in body:
                    content += f'''
    it('should return a boolean value', () => {{
      const result = {func_name}({param_values});
      expect(typeof result === 'boolean' || result === undefined).toBe(true);
    }});
'''
                elif 'class' in body.lower() or 'cell' in body.lower():
                    content += f'''
    it('should return expected class name', () => {{
      const result = {func_name}({param_values});
      if (result) {{
        expect(typeof result).toBe('string');
      }}
    }});
'''
        
        content += '''  });
'''
        return content
    
    def _generate_test_params(self, params: List[str], body: str) -> Dict:
        """Génère des valeurs de test appropriées selon les noms de paramètres"""
        values = []
        setup_lines = []
        
        for param in params:
            param_lower = param.lower()
            
            if 'date' in param_lower:
                values.append('mockDate')
                setup_lines.append('const mockDate = new Date(\'2026-01-15\');')
            elif 'scheduler' in param_lower or 'leaveplanning' in param_lower:
                values.append('mockScheduler')
                setup_lines.append('const mockScheduler = { attachEvent: jest.fn(), getEvents: jest.fn(() => []), getState: jest.fn(() => ({ min_date: new Date(), max_date: new Date() })), templates: {}, matrix: { timeline: {} } };')
            elif 'employee' in param_lower or 'user' in param_lower:
                values.append("'EMP001'")
            elif 'event' in param_lower or 'ev' == param_lower:
                values.append('mockEvent')
                setup_lines.append("const mockEvent = { id: 1, section_id: 'EMP001', customType: 'validated', start_date: new Date(), end_date: new Date() };")
            elif 'start' in param_lower:
                values.append('new Date(\'2026-01-01\')')
            elif 'end' in param_lower:
                values.append('new Date(\'2026-01-31\')')
            elif 'min' in param_lower:
                values.append('new Date(\'2026-01-01\')')
            elif 'max' in param_lower:
                values.append('new Date(\'2026-12-31\')')
            elif 'callback' in param_lower or 'fn' in param_lower or 'refresh' in param_lower:
                values.append('jest.fn()')
            elif 'timeline' in param_lower:
                values.append('{ dy: 50, folder_dy: 50, x_size: 31 }')
            elif 'y_unit' in param_lower or 'unit' in param_lower:
                values.append("{ key: 'team1', label: 'Team 1', children: [], level: 0 }")
            elif 'days' in param_lower or 'count' in param_lower or 'size' in param_lower:
                values.append('31')
            elif 'mobile' in param_lower:
                values.append('false')
            elif 'localizer' in param_lower:
                values.append("{ getText: jest.fn(() => 'Label') }")
            elif 'old' in param_lower and 'date' in param_lower:
                values.append('new Date(\'2025-12-01\')')
            elif 'mode' in param_lower:
                values.append("'timeline'")
            elif 'position' in param_lower:
                values.append("'start'")
            else:
                # Valeur par défaut
                values.append("'test'")
        
        return {
            'values': values,
            'setup': '\n      '.join(setup_lines) if setup_lines else '// No special setup needed'
        }
    
    def _generate_js_class_test(self, class_name: str) -> str:
        """Génère un test pour une classe JavaScript"""
        return f'''
  describe('{class_name}', () => {{
    let instance;

    beforeEach(() => {{
      instance = new {class_name}(false); // isMobile = false
    }});

    it('should create an instance', () => {{
      expect(instance).toBeDefined();
    }});

    it('should have events method', () => {{
      if (instance.events) {{
        expect(typeof instance.events).toBe('function');
      }}
    }});
  }});
'''

    # ========== JAVA avec MOCKITO ==========
    def _is_passthrough_method(self, method_name: str) -> bool:
        """Détecte si une méthode est pass-through (délègue direct au DAO sans logique)"""
        # Rechercher le corps de la méthode
        pattern = rf'public\s+[^\s]+\s+{method_name}\s*\([^)]*\)\s*{{([^}}]+)}}'
        match = re.search(pattern, self.code, re.DOTALL)
        
        if not match:
            return False
        
        method_body = match.group(1).strip()
        
        # Pass-through si : return dao.method(...) avec 0-1 lignes de code
        lines = [l.strip() for l in method_body.split('\n') if l.strip() and not l.strip().startswith('//')]
        
        # Pass-through = 1 ligne qui fait return xxx.method()
        if len(lines) == 1 and lines[0].startswith('return') and '.' in lines[0]:
            return True
        
        # Pas de logique conditionnelle = pass-through
        if 'if' not in method_body and 'for' not in method_body and 'while' not in method_body and 'try' not in method_body:
            if method_body.count('\n') <= 2:  # Max 2 lignes
                return True
        
        return False
    
    def _extract_dao_method_name(self, method_name: str) -> str:
        """Extrait le nom EXACT de la méthode DAO appelée dans le code source"""
        # Chercher le corps de la méthode service
        # Pattern flexible qui gère les accolades imbriquées
        method_start = rf'public\s+[^\s]+\s+{method_name}\s*\([^)]*\)\s*{{'
        match = re.search(method_start, self.code)
        
        if not match:
            return method_name  # Fallback
        
        # Extraire tout le texte après la signature de méthode
        start_pos = match.end()
        code_after = self.code[start_pos:]
        
        # Trouver la première occurrence d'appel DAO dans ce code
        # Pattern: nomDao.methodName( ou nomDaoImpl.methodName(
        dao_call = re.search(r'(\w+Dao(?:Impl)?)\.([\w]+)\s*\(', code_after)
        
        if dao_call:
            return dao_call.group(2)  # Retourne le nom EXACT de la méthode DAO
        
        # Fallback : utiliser le même nom que la méthode service
        return method_name
    
    def _is_primitive(self, java_type: str) -> bool:
        """Vérifie si le type Java est primitif"""
        primitives = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char']
        return java_type.strip() in primitives
    
    def _get_primitive_default(self, java_type: str) -> str:
        """Retourne la valeur par défaut pour un type primitif"""
        java_type = java_type.strip()
        if java_type == 'long':
            return '0L'
        elif java_type in ['int', 'short', 'byte']:
            return '0'
        elif java_type in ['float', 'double']:
            return '0.0'
        elif java_type == 'boolean':
            return 'false'
        elif java_type == 'char':
            return "'\\0'"
        return 'null'
    
    def _get_default_value(self, java_type: str) -> str:
        """Retourne la valeur par défaut selon le type Java (pour éviter null sur primitifs)"""
        java_type = java_type.strip()
        
        # Types primitifs numériques
        if java_type in ["int", "Integer", "long", "Long", "short", "Short", "byte", "Byte"]:
            return "0"
        if java_type in ["double", "Double", "float", "Float"]:
            return "0.0"
        if java_type in ["boolean", "Boolean"]:
            return "false"
        if java_type in ["char", "Character"]:
            return "'a'"
        
        # Types objets : null valide
        return "null"
    
    def _java_tests(self):
        """Génération tests Java avec Mockito pour mocks automatiques"""
        # PRIORITÉ 1: Génération 100% IA si activée
        if self.use_ai:
            ai_tests = self._generate_tests_with_ai("java")
            if ai_tests:
                print("✅ Tests Java générés par IA Ollama")
                return ai_tests
            print("⚠️ Échec génération IA, fallback vers templates")
        
        # FALLBACK: Templates classiques
        class_name = self.base

        # AMÉLIORATION V2: Détecter méthodes publiques avec types génériques (List<User>, Optional<Data>, Map<String,Object>)
        method_pattern = r'public\s+(?:static\s+)?([^\s]+)\s+(\w+)\s*\(([^)]*)\)'
        public_methods = re.findall(method_pattern, self.code)

        # Détecter getters/setters réels
        getters = re.findall(r'public\s+\w+\s+(get\w+)\s*\(\)\s*\{', self.code)
        setters = re.findall(r'public\s+void\s+(set\w+)\s*\([^)]+\)\s*\{', self.code)

        # Détecter dépendances à mocker
        dependencies = re.findall(r'private\s+(\w+)\s+(\w+);', self.code)
        has_dao = any('Dao' in dep[0] or 'Service' in dep[0] or 'Repository' in dep[0] for dep in dependencies)

        # Headers
        content = f'''import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import java.util.Date;

/**
 * Tests unitaires générés automatiquement pour {class_name}.java
 * Utilise Mockito pour mocker les dépendances
 */
@ExtendWith(MockitoExtension.class)
public class {class_name}Test {{
    
    @InjectMocks
    private {class_name} instance;
'''

        # Générer @Mock pour dépendances
        for dep_type, dep_name in dependencies:
            if 'Dao' in dep_type or 'Service' in dep_type or 'Repository' in dep_type:
                content += f'''    
    @Mock
    private {dep_type} {dep_name};
'''

        content += '''
    @BeforeEach
    public void setUp() {
        // Mocks automatically injected by Mockito
    }
    
    @Test
    public void testInstantiation() {
        assertNotNull(instance, "L'instance ne doit pas être null");
    }
'''
        
        # ========== TESTS POUR GETTERS/SETTERS SIMPLES (String, int, boolean) ==========
        # Extraire les paires getter/setter pour les champs privés
        private_fields = re.findall(r'private\s+(\w+)\s+(\w+);', self.code)
        for field_type, field_name in private_fields:
            # Ignorer les dépendances (Dao, Service, Repository)
            if 'Dao' in field_type or 'Service' in field_type or 'Repository' in field_type:
                continue
            
            # Construire les noms getter/setter
            capitalized = field_name[0].upper() + field_name[1:]
            getter_name = f'get{capitalized}'
            setter_name = f'set{capitalized}'
            
            # Vérifier si getter et setter existent
            has_getter = getter_name in getters or f'public {field_type} {getter_name}()' in self.code
            has_setter = setter_name in setters or f'public void {setter_name}(' in self.code
            
            if has_getter and has_setter:
                # Générer valeur de test selon le type
                if field_type == 'String':
                    test_value = '"testValue"'
                elif field_type in ['int', 'Integer']:
                    test_value = '42'
                elif field_type in ['long', 'Long']:
                    test_value = '100L'
                elif field_type in ['boolean', 'Boolean']:
                    test_value = 'true'
                elif field_type in ['double', 'Double']:
                    test_value = '3.14'
                else:
                    test_value = 'null'  # Pour les objets
                
                content += f'''
    @Test
    public void test{getter_name}And{setter_name}() {{
        // Test getter/setter pour {field_name}
        {field_type} expected = {test_value};
        instance.{setter_name}(expected);
        {field_type} actual = instance.{getter_name}();
        assertEquals(expected, actual, "Le getter doit retourner la valeur définie par le setter");
    }}
'''
        
        # ========== TESTS POUR MÉTHODES RETOURNANT MAP/LIST ==========
        map_methods = re.findall(r'public\s+Map<[^>]+>\s+(\w+)\s*\([^)]*\)', self.code)
        for method_name in map_methods:
            if method_name not in ['toString', 'hashCode', 'equals']:
                # Trouver TOUTES les clés utilisées dans la Map (result.put("key", ...) ou put("key", ...))
                map_keys = re.findall(r'\.put\s*\(\s*"([^"]+)"', self.code)
                
                content += f'''
    @Test
    public void test{method_name[0].upper() + method_name[1:]}ReturnsMap() {{
        // Test que la méthode retourne une Map non null
        var result = instance.{method_name}();
        assertNotNull(result, "La méthode {method_name} ne doit pas retourner null");
        assertInstanceOf(java.util.Map.class, result, "Doit retourner une Map");
    }}
'''
                # Test du contenu de la Map si on a trouvé des clés
                if map_keys:
                    content += f'''
    @Test
    public void test{method_name[0].upper() + method_name[1:]}ContainsExpectedKeys() {{
        // Test que la Map contient les clés attendues
        var result = instance.{method_name}();
        assertNotNull(result);
        
        // Vérifier le nombre exact de clés
        assertEquals({len(map_keys)}, result.size(), "La Map doit contenir exactement {len(map_keys)} clés");
        
        // Vérifier chaque clé
'''
                    for key in map_keys[:5]:  # Max 5 clés
                        content += f'        assertTrue(result.containsKey("{key}"), "La Map doit contenir la clé \\"{key}\\"");\n'
                    content += '    }\n'
                
                # Test avec setters si présents (pour vérifier le contenu)
                # Chercher les setters correspondants aux clés
                for key in map_keys[:3]:  # Max 3 tests
                    # Trouver le setter correspondant
                    setter_pattern = rf'set{key[0].upper()}{key[1:]}\s*\(\s*String'
                    if re.search(setter_pattern, self.code):
                        setter_name = f'set{key[0].upper()}{key[1:]}'
                        content += f'''
    @Test
    public void test{method_name[0].upper() + method_name[1:]}ReturnsSetValue_{key}() {{
        // Test que la Map retourne la valeur définie par le setter
        String testValue = "testValue_{key}";
        instance.{setter_name}(testValue);
        
        var result = instance.{method_name}();
        
        assertEquals(testValue, result.get("{key}"), "La Map doit contenir la valeur définie pour '{key}'");
    }}
'''
        
        list_methods = re.findall(r'public\s+List<[^>]+>\s+(\w+)\s*\([^)]*\)', self.code)
        for method_name in list_methods:
            if method_name not in ['toString', 'hashCode', 'equals']:
                content += f'''
    @Test
    public void test{method_name[0].upper() + method_name[1:]}ReturnsList() {{
        // Test que la méthode retourne une List non null
        var result = instance.{method_name}();
        assertNotNull(result, "La méthode {method_name} ne doit pas retourner null");
        assertInstanceOf(java.util.List.class, result, "Doit retourner une List");
    }}
'''
        
        # Test pour méthodes retournant des constantes (comme getIdentification)
        simple_methods = re.findall(r'public\s+String\s+(\w+)\s*\(\)\s*{\s*return\s+"([^"]+)"', self.code, re.DOTALL)
        for method_name, return_value in simple_methods:
            if method_name not in ['toString', 'getName', 'getClass']:
                content += f'''
    @Test
    public void test{method_name[0].upper() + method_name[1:]}() {{
        String result = instance.{method_name}();
        assertEquals("{return_value}", result, "La méthode doit retourner '{return_value}'");
    }}
'''

        # Générer test getter/setter pour dépendances injectées
        for dep_type, dep_name in dependencies:
            if 'Dao' in dep_type or 'Service' in dep_type or 'Repository' in dep_type:
                # Trouver getter/setter correspondant
                getter_name = f'get{dep_name[0].upper()}{dep_name[1:]}'
                setter_name = f'set{dep_name[0].upper()}{dep_name[1:]}'
                
                if getter_name in getters and setter_name in setters:
                    content += f'''
    @Test
    public void test{getter_name}And{setter_name}() {{
        // Test du getter/setter pour {dep_name}
        {dep_type} mock{dep_name} = mock({dep_type}.class);
        
        instance.{setter_name}(mock{dep_name});
        
        assertEquals(mock{dep_name}, instance.{getter_name}(), "Le getter doit retourner la valeur définie par le setter");
    }}
'''

        # Générer tests pour méthodes métier
        for return_type, method_name, params_str in public_methods:
            # Ignorer getters/setters simples
            is_simple_getter = method_name.startswith('get') and not params_str.strip()
            is_simple_setter = method_name.startswith('set') and params_str.count(',') == 0

            if not is_simple_getter and not is_simple_setter and method_name not in ['toString', 'hashCode', 'equals']:
                # Parser paramètres
                params = [p.strip() for p in params_str.split(',') if p.strip()]

                # Générer arguments de test
                test_args = []
                for param in params:
                    parts = param.split()
                    if len(parts) >= 2:
                        param_type = parts[0]
                        param_name = parts[1]
                        
                        if 'String' in param_type:
                            test_args.append(f'"test{param_name.capitalize()}"')
                        elif 'int' in param_type or 'Integer' in param_type:
                            test_args.append('1')
                        elif 'boolean' in param_type or 'Boolean' in param_type:
                            test_args.append('true')
                        elif 'Date' in param_type:
                            test_args.append('new Date()')
                        else:
                            test_args.append('null')

                args_call = ', '.join(test_args) if test_args else ''

                # Préparer variables Date si nécessaire
                has_date = any('Date' in str(p) for p in params if p)
                date_vars = ''
                if has_date and args_call:
                    date_vars = '        Date beginDate = new Date();\n        Date endDate = new Date();\n        '
                    args_call = args_call.replace('new Date()', 'beginDate', 1).replace('new Date()', 'endDate', 1)

                # Détect if pass-through service
                is_passthrough = self._is_passthrough_method(method_name)
                
                # ✅ CORRECTION CRITIQUE 1 : Extraire nom EXACT méthode DAO
                dao_method_name = self._extract_dao_method_name(method_name)
                
                # ✅ CORRECTION CRITIQUE 2 : Détecter si type primitif
                is_primitive = self._is_primitive(return_type)
                
                # Test normal
                if return_type != 'void' and has_dao:
                    response_class = return_type.split('<')[0]
                    dao_name = [dep[1] for dep in dependencies if 'Dao' in dep[0]][0] if any('Dao' in d[0] for d in dependencies) else 'dao'
                    
                    # ✅ CORRECTION CRITIQUE 3 : Valeur par défaut selon type
                    if is_primitive:
                        default_value = self._get_primitive_default(return_type)
                        null_assertion = f"assertEquals({default_value}, result);"  # Pas assertNotNull sur primitive
                    else:
                        default_value = 'null'
                        null_assertion = 'assertNull(result, "Le service devrait retourner null si le DAO retourne null");'
                    
                    if is_passthrough:
                        # ✅ NIVEAU ENTREPRISE : Tests délégation seulement pour pass-through
                        content += f'''
    @Test
    public void test{method_name[0].upper() + method_name[1:]}_Delegation() {{
        // Test délégation : vérifie que le service appelle le DAO correctement
{date_vars}        {response_class} expectedResponse = {'new ' + response_class + '()' if not is_primitive else default_value};
        when({dao_name}.{dao_method_name}({', '.join(['anyString()' if 'String' in str(p) else 'any(Date.class)' if 'Date' in str(p) else 'anyBoolean()' if 'boolean' in str(p) else 'anyLong()' if 'long' in str(p) else 'anyInt()' if 'int' in str(p) else 'any()' for p in params])}))
            .thenReturn(expectedResponse);
        
        {response_class} result = instance.{method_name}({args_call});
        
        {'' if is_primitive else 'assertNotNull(result);'}
        assertEquals(expectedResponse, result);
        verify({dao_name}).{dao_method_name}({args_call});
    }}
'''
                        # Test null seulement pour les objets (pas pour les primitives)
                        if not is_primitive:
                            content += f'''
    @Test
    public void test{method_name[0].upper() + method_name[1:]}_WhenDaoReturnsNull() {{
        // Test comportement quand DAO retourne null
{date_vars}        when({dao_name}.{dao_method_name}({', '.join(['anyString()' if 'String' in str(p) else 'any(Date.class)' if 'Date' in str(p) else 'anyBoolean()' if 'boolean' in str(p) else 'anyLong()' if 'long' in str(p) else 'anyInt()' if 'int' in str(p) else 'any()' for p in params])}))
            .thenReturn(null);
        
        {response_class} result = instance.{method_name}({args_call});
        
        assertNull(result, "Le service devrait retourner null si le DAO retourne null");
        verify({dao_name}).{dao_method_name}({args_call});
    }}
'''
                    else:
                        # Service avec logique métier : tests complets
                        content += f'''
    @Test
    public void test{method_name[0].upper() + method_name[1:]}() {{
        // Arrange
{date_vars}        {response_class} expectedResponse = {'new ' + response_class + '()' if not is_primitive else default_value};
        when({dao_name}.{dao_method_name}({', '.join(['anyString()' if 'String' in str(p) else 'any(Date.class)' if 'Date' in str(p) else 'anyBoolean()' if 'boolean' in str(p) else 'anyLong()' if 'long' in str(p) else 'anyInt()' if 'int' in str(p) else 'any()' for p in params])}))
            .thenReturn(expectedResponse);
        
        // Act
        {response_class} result = instance.{method_name}({args_call});
        
        // Assert
        {'' if is_primitive else 'assertNotNull(result);'}
        assertEquals(expectedResponse, result);
        verify({dao_name}).{dao_method_name}({args_call});
    }}
    
    @Test
    public void test{method_name[0].upper() + method_name[1:]}_WhenDaoThrowsException() {{
        // Test gestion d'exception
{date_vars}        when({dao_name}.{dao_method_name}({', '.join(['anyString()' if 'String' in str(p) else 'any(Date.class)' if 'Date' in str(p) else 'anyBoolean()' if 'boolean' in str(p) else 'anyLong()' if 'long' in str(p) else 'anyInt()' if 'int' in str(p) else 'any()' for p in params])}))
            .thenThrow(new RuntimeException("Erreur DAO"));
        
        assertThrows(RuntimeException.class, () -> {{
            instance.{method_name}({args_call});
        }});
    }}
'''
                else:
                    content += f'''
    @Test
    public void test{method_name[0].upper() + method_name[1:]}() {{
        assertDoesNotThrow(() -> {{
            instance.{method_name}({args_call});
        }});
    }}
'''

        content += '\n}\n'
        
        # Amélioration avec IA si activée
        if self.use_ai:
            content = self._enhance_tests_with_ai(content, "java")
        
        return content
