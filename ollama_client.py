"""Client IA gratuit utilisant Ollama (IA locale)."""
import requests
import json
from typing import Optional

class OllamaClient:
    """Client pour interagir avec Ollama (IA locale gratuite)."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        """
        Initialise le client Ollama.
        
        Args:
            base_url: URL de l'API Ollama (par défaut localhost:11434)
            model: Modèle à utiliser (llama3, phi, codellama, etc.)
        """
        self.base_url = base_url
        self.model = model
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """Vérifie si Ollama est disponible."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt: str, temperature: float = 0.3, max_tokens: int = 2048) -> Optional[str]:
        """
        Génère du contenu avec Ollama.
        
        Args:
            prompt: Le prompt à envoyer à l'IA
            temperature: Température de génération (0.0-1.0)
            max_tokens: Nombre maximum de tokens
            
        Returns:
            str: La réponse générée ou None si erreur
        """
        if not self.available:
            return None
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=120  # 2 minutes timeout pour génération complexe
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return None
        except Exception as e:
            print(f"❌ Erreur Ollama: {e}")
            return None
    
    def explain_code(self, code: str, language: str = "java") -> str:
        """
        Explique le code fourni.
        
        Args:
            code: Le code source à expliquer
            language: Le langage du code
            
        Returns:
            str: L'explication générée
        """
        prompt = f"""Tu es un expert en {language}. Explique ce code de manière claire et concise:

```{language}
{code}
```

Fournis:
1. Ce que fait le code (1-2 phrases)
2. Les points clés (design patterns, bonnes pratiques)
3. Les potentiels problèmes ou améliorations

Sois concis et technique."""

        response = self.generate(prompt, temperature=0.2)
        return response if response else "❌ Ollama non disponible. Installez Ollama: https://ollama.com"
    
    def detect_bugs(self, code: str, language: str = "java") -> str:
        """
        Détecte les bugs potentiels dans le code.
        
        Args:
            code: Le code source à analyser
            language: Le langage du code
            
        Returns:
            str: Les bugs détectés
        """
        prompt = f"""Tu es un expert en détection de bugs {language}. Analyse ce code et trouve les bugs potentiels:

```{language}
{code}
```

Liste uniquement les bugs RÉELS (pas de faux positifs):
- Null pointer exceptions
- Fuites mémoire
- Conditions raciales
- Erreurs logiques

Format: Bug → Impact → Solution"""

        response = self.generate(prompt, temperature=0.1)
        return response if response else "❌ Ollama non disponible"
    
    def improve_tests(self, test_code: str, language: str = "java") -> str:
        """
        Suggère des améliorations pour les tests unitaires.
        
        Args:
            test_code: Le code de test à améliorer
            language: Le langage du code
            
        Returns:
            str: Les suggestions d'amélioration
        """
        prompt = f"""Tu es un expert en tests unitaires {language}. Analyse ces tests et suggère des améliorations:

```{language}
{test_code}
```

Suggère:
1. Cas limites manquants (edge cases)
2. Cas d'erreur manquants
3. Assertions plus robustes
4. Améliorations de lisibilité

Sois concret avec des exemples."""

        response = self.generate(prompt, temperature=0.3)
        return response if response else "❌ Ollama non disponible"
    
    def add_edge_cases(self, code: str, language: str = "java") -> str:
        """
        Identifie les cas limites à tester.
        
        Args:
            code: Le code source à analyser
            language: Le langage du code
            
        Returns:
            str: Les cas limites identifiés
        """
        prompt = f"""Tu es un expert en tests {language}. Identifie tous les cas limites (edge cases) pour ce code:

```{language}
{code}
```

Liste les cas limites à tester:
- Null/undefined
- Valeurs limites (0, -1, MAX_VALUE)
- Collections vides
- Exceptions
- Cas spéciaux métier

Format: Cas limite → Pourquoi important → Assertion suggérée"""

        response = self.generate(prompt, temperature=0.2)
        return response if response else "❌ Ollama non disponible"


def get_ai_client():
    """
    Retourne un client IA (Ollama si disponible, sinon message).
    
    Returns:
        OllamaClient: Le client IA
    """
    client = OllamaClient()
    
    if client.available:
        print("✅ Ollama détecté - IA gratuite activée")
        return client
    else:
        print("⚠️  Ollama non trouvé. Installez-le: https://ollama.com")
        print("   Puis: ollama pull llama3")
        return client


if __name__ == "__main__":
    # Test du client
    client = get_ai_client()
    
    if client.available:
        print("\n🧪 Test: Explication de code")
        code = """
public int add(int a, int b) {
    return a + b;
}
"""
        explanation = client.explain_code(code, "java")
        print(explanation)
