"""Module de calcul avancé pour démonstration."""

from typing import List, Union
import math


def calculate_average(numbers: List[Union[int, float]]) -> float:
    """
    Calcule la moyenne d'une liste de nombres.
    
    Args:
        numbers: Liste de nombres (int ou float)
    
    Returns:
        La moyenne des nombres
    
    Raises:
        ValueError: Si la liste est vide
        TypeError: Si la liste contient des éléments non numériques
    """
    if not numbers:
        raise ValueError("La liste ne peut pas être vide")
    
    if not all(isinstance(n, (int, float)) for n in numbers):
        raise TypeError("Tous les éléments doivent être des nombres")
    
    return sum(numbers) / len(numbers)


def factorial(n: int) -> int:
    """
    Calcule la factorielle d'un nombre.
    
    Args:
        n: Nombre entier positif
    
    Returns:
        La factorielle de n
    
    Raises:
        ValueError: Si n est négatif
        TypeError: Si n n'est pas un entier
    """
    if not isinstance(n, int):
        raise TypeError("n doit être un entier")
    
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    
    if n == 0 or n == 1:
        return 1
    
    return math.factorial(n)


def is_prime(n: int) -> bool:
    """
    Vérifie si un nombre est premier.
    
    Args:
        n: Nombre entier à tester
    
    Returns:
        True si le nombre est premier, False sinon
    """
    if not isinstance(n, int):
        return False
    
    if n < 2:
        return False
    
    if n == 2:
        return True
    
    if n % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    
    return True


def divide_safe(a: float, b: float) -> Union[float, None]:
    """
    Division sécurisée qui gère la division par zéro.
    
    Args:
        a: Numérateur
        b: Dénominateur
    
    Returns:
        Le résultat de la division ou None si b est zéro
    """
    if b == 0:
        return None
    
    return a / b
