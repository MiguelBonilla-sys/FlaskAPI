"""
Excepciones personalizadas para manejo de errores de APIs externas.
"""

class APIError(Exception):
    """Error genérico de API externa."""
    pass

class APITimeoutError(APIError):
    """Error de timeout en llamada a API externa."""
    pass

class RateLimitError(APIError):
    """Error de rate limit excedido."""
    pass

class CircuitBreakerOpen(APIError):
    """Error cuando el circuit breaker está abierto."""
    pass

class InvalidDataError(APIError):
    """Error cuando los datos son inválidos después de transformación."""
    pass

