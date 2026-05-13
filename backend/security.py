"""Security module for authentication and password management.

This module provides secure password handling and JWT token management
for the application. It implements industry-standard security practices:

- Passwords are hashed using bcrypt with automatic salt generation
- JWT tokens are issued with configurable expiration times
- Token verification prevents unauthorized access to protected routes

Security Features:
- Bcrypt password hashing (salted and iterated)
- JWT token-based authentication
- Configurable token expiration
- Protection against common attacks (tampering, expiration)
"""

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from config import settings

# ============ Password Hashing Configuration ============
# Bcrypt context for secure password storage with automatic salt generation
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain password using bcrypt.
    
    Bcrypt is a password hashing function designed to be slow and secure.
    It automatically generates a salt and uses multiple iterations.
    
    Args:
        password (str): Plain text password to hash
        
    Returns:
        str: Bcrypt hashed password (safe to store in database)
        
    Note:
        Never store plain passwords. Always hash before storage.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verify a plain password against its bcrypt hash.
    
    Uses constant-time comparison to prevent timing attacks.
    
    Args:
        plain_password (str): Plain text password from user input
        password_hash (str): Bcrypt hash from database
        
    Returns:
        bool: True if password matches hash, False otherwise
        
    Security:
        - Constant-time comparison prevents timing attacks
        - Does not reveal whether email/username exists if wrong
    """
    return pwd_context.verify(plain_password, password_hash)

# ============ JWT Token Management ============

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token with claims.
    
    JWT tokens are used for stateless authentication. The token contains
    claims (user data) signed with a secret key.
    
    Args:
        data (dict): Claims to encode in token (e.g., {"sub": username})
        expires_delta (timedelta, optional): Token expiration time.
                     Defaults to ACCESS_TOKEN_EXPIRE_MINUTES from config
        
    Returns:
        str: Encoded JWT token as a string
        
    Security:
        - Tokens expire after configured time to limit exposure
        - Secret key is required to verify and prevent tampering
        - Use HTTPS to transmit tokens
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    to_encode.update({"exp": expire})
    
    # Sign token with secret key
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify a JWT token and extract its claims.
    
    Validates token signature and expiration time. Returns None if invalid.
    
    Args:
        token (str): JWT token string to verify
        
    Returns:
        dict: Token claims if valid, None if invalid/expired
        
    Security:
        - Verifies signature to detect tampering
        - Checks expiration time
        - Returns None on any verification failure
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            return None
        return payload
    except JWTError:
        # Invalid signature, expired token, or other JWT errors
        return None
