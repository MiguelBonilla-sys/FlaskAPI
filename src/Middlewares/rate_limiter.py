"""
Middleware de Rate Limiting para controlar la cantidad de peticiones.
"""
import os
import time
from collections import defaultdict, deque
from functools import wraps
from flask import request, jsonify, current_app
from src.Utils import create_error_response
import logging

class RateLimiter:
    """
    Rate limiter usando sliding window approach.
    """
    
    def __init__(self):
        """
        Inicializa el rate limiter.
        """
        # Almacenar peticiones por IP: {ip: deque([timestamp1, timestamp2, ...])}
        self.requests = defaultdict(deque)
        # Configuraciones por defecto
        self.default_limits = {
            'requests_per_minute': 60,  # 60 peticiones por minuto
            'requests_per_hour': 1000,  # 1000 peticiones por hora
            'burst_limit': 10,  # 10 peticiones en ráfaga (10 segundos)
        }
        
    def is_allowed(self, client_ip, limit_type='requests_per_minute'):
        """
        Verifica si una petición está permitida.
        
        Args:
            client_ip (str): IP del cliente
            limit_type (str): Tipo de límite a verificar
            
        Returns:
            tuple: (is_allowed, retry_after_seconds)
        """
        current_time = time.time()
        
        # Configurar ventanas de tiempo
        time_windows = {
            'requests_per_minute': 60,
            'requests_per_hour': 3600,
            'burst_limit': 10
        }
        
        # Configurar límites
        limits = {
            'requests_per_minute': 60,
            'requests_per_hour': 1000,
            'burst_limit': 10
        }
        
        window_seconds = time_windows.get(limit_type, 60)
        max_requests = limits.get(limit_type, 60)
        
        # Limpiar peticiones antiguas
        client_requests = self.requests[client_ip]
        while client_requests and client_requests[0] < current_time - window_seconds:
            client_requests.popleft()
        
        # Verificar si se excede el límite
        if len(client_requests) >= max_requests:
            # Calcular tiempo de espera
            oldest_request = client_requests[0]
            retry_after = window_seconds - (current_time - oldest_request)
            return False, max(1, int(retry_after))
        
        # Agregar la petición actual
        client_requests.append(current_time)
        return True, 0
    
    def cleanup_old_requests(self):
        """
        Limpia peticiones antiguas para evitar memory leaks.
        """
        current_time = time.time()
        cleanup_threshold = current_time - 3600  # Limpiar después de 1 hora
        
        # Limpiar IPs sin actividad reciente
        ips_to_remove = []
        for ip, requests_deque in self.requests.items():
            # Limpiar peticiones antiguas
            while requests_deque and requests_deque[0] < cleanup_threshold:
                requests_deque.popleft()
            
            # Marcar IP para eliminación si no tiene peticiones recientes
            if not requests_deque:
                ips_to_remove.append(ip)
        
        # Eliminar IPs inactivas
        for ip in ips_to_remove:
            del self.requests[ip]

# Instancia global del rate limiter
rate_limiter = RateLimiter()

def get_client_ip():
    """
    Obtiene la IP real del cliente considerando proxies.
    
    Returns:
        str: IP del cliente
    """
    # Verificar headers de proxy comunes
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        # Tomar la primera IP (IP original del cliente)
        return forwarded_for.split(',')[0].strip()
    
    real_ip = request.headers.get('X-Real-IP')
    if real_ip:
        return real_ip
    
    # IP directa
    return request.remote_addr or '127.0.0.1'

def rate_limit(limit_type='requests_per_minute', skip_on_debug=True):
    """
    Decorador para aplicar rate limiting a endpoints.
    
    Args:
        limit_type (str): Tipo de límite a aplicar
        skip_on_debug (bool): Omitir rate limiting en modo debug
        
    Returns:
        function: Decorador
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Omitir en modo debug si está configurado
            if skip_on_debug and current_app.config.get('DEBUG', False):
                return f(*args, **kwargs)
            
            # Verificar si rate limiting está habilitado (para Railway)
            if os.getenv('RATE_LIMIT_ENABLED', 'true').lower() != 'true':
                return f(*args, **kwargs)
            
            client_ip = get_client_ip()
            
            # Verificar límite
            is_allowed, retry_after = rate_limiter.is_allowed(client_ip, limit_type)
            
            if not is_allowed:
                # Log del rate limiting
                current_app.logger.warning(
                    f'Rate limit exceeded for IP {client_ip} on {request.endpoint} '
                    f'(limit_type: {limit_type})'
                )
                
                # Respuesta de rate limiting
                response = create_error_response(
                    message="Límite de peticiones excedido",
                    status_code=429,
                    errors=[
                        "Has excedido el límite de peticiones permitidas",
                        f"Intenta nuevamente en {retry_after} segundos"
                    ]
                )
                
                # Agregar headers informativos
                response[0].headers['Retry-After'] = str(retry_after)
                response[0].headers['X-RateLimit-Limit'] = str(rate_limiter.default_limits.get(limit_type, 60))
                response[0].headers['X-RateLimit-Remaining'] = '0'
                response[0].headers['X-RateLimit-Reset'] = str(int(time.time() + retry_after))
                
                return response
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def strict_rate_limit(requests_per_minute=30):
    """
    Rate limiter estricto para endpoints sensibles.
    
    Args:
        requests_per_minute (int): Límite de peticiones por minuto
        
    Returns:
        function: Decorador
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = get_client_ip()
            current_time = time.time()
            
            # Usar una ventana de tiempo más estricta
            client_requests = rate_limiter.requests[client_ip]
            
            # Limpiar peticiones de más de 1 minuto
            while client_requests and client_requests[0] < current_time - 60:
                client_requests.popleft()
            
            # Verificar límite estricto
            if len(client_requests) >= requests_per_minute:
                current_app.logger.warning(
                    f'Strict rate limit exceeded for IP {client_ip} on {request.endpoint}'
                )
                
                return create_error_response(
                    message="Límite estricto de peticiones excedido",
                    status_code=429,
                    errors=[
                        f"Has excedido el límite estricto de {requests_per_minute} peticiones por minuto",
                        "Este endpoint tiene restricciones adicionales de seguridad"
                    ]
                )
            
            # Agregar petición
            client_requests.append(current_time)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def setup_rate_limiting(app):
    """
    Configura rate limiting global para la aplicación.
    
    Args:
        app: Instancia de Flask
    """
    
    @app.before_request
    def cleanup_rate_limiter():
        """Limpia el rate limiter periódicamente."""
        # Limpiar cada 100 peticiones aproximadamente
        if hasattr(cleanup_rate_limiter, 'counter'):
            cleanup_rate_limiter.counter += 1
        else:
            cleanup_rate_limiter.counter = 1
            
        if cleanup_rate_limiter.counter % 100 == 0:
            rate_limiter.cleanup_old_requests()
    
    @app.after_request
    def add_rate_limit_headers(response):
        """Agrega headers informativos de rate limiting."""
        client_ip = get_client_ip()
        current_time = time.time()
        
        # Calcular peticiones restantes
        client_requests = rate_limiter.requests[client_ip]
        recent_requests = sum(1 for req_time in client_requests if req_time > current_time - 60)
        remaining = max(0, rate_limiter.default_limits['requests_per_minute'] - recent_requests)
        
        # Agregar headers informativos
        response.headers['X-RateLimit-Limit'] = str(rate_limiter.default_limits['requests_per_minute'])
        response.headers['X-RateLimit-Remaining'] = str(remaining)
        response.headers['X-RateLimit-Reset'] = str(int(current_time + 60))
        
        return response
    
    app.logger.info('Rate limiting configurado exitosamente')
