"""Email validation module."""
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    # Basic email pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def extract_domain(email: str) -> Optional[str]:
    """
    Extract domain from email address.
    
    Args:
        email: Email address
        
    Returns:
        Domain name or None if invalid
    """
    if not validate_email(email):
        return None
    
    return email.split('@')[1]


def is_corporate_email(email: str, domains: list) -> bool:
    """
    Check if email belongs to corporate domains.
    
    Args:
        email: Email to check
        domains: List of corporate domains
        
    Returns:
        True if corporate email
    """
    domain = extract_domain(email)
    if not domain:
        return False
    
    return domain in domains
