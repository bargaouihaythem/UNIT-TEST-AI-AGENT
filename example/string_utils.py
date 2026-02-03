"""String utilities module."""
from typing import Optional


def reverse_string(text: str) -> str:
    """Reverse a string."""
    if not isinstance(text, str):
        return ""
    return text[::-1]


def is_palindrome(text: str) -> bool:
    """
    Check if string is a palindrome.
    
    Args:
        text: String to check
        
    Returns:
        True if palindrome, False otherwise
    """
    if not text or not isinstance(text, str):
        return False
    
    # Remove spaces and convert to lowercase
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


def count_words(text: str) -> int:
    """
    Count words in text.
    
    Args:
        text: Text to analyze
        
    Returns:
        Number of words
    """
    if not text or not isinstance(text, str):
        return 0
    
    return len(text.split())


def capitalize_words(text: str) -> str:
    """
    Capitalize first letter of each word.
    
    Args:
        text: Text to capitalize
        
    Returns:
        Capitalized text
    """
    if not isinstance(text, str):
        return ""
    
    return text.title()


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to max length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if not isinstance(text, str):
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
