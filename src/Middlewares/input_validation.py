"""
Middleware de validación de entrada para endpoints sensibles.
"""
import re
from functools import wraps
from flask import request, current_app
from src.Utils import create_error_response

class InputValidator:
    """
    Validador de entrada para prevenir ataques de inyección y datos maliciosos.
    """
    
    def __init__(self):
        """
        Inicializa el validador.
        """
        # Patrones sospechosos
        self.sql_injection_patterns = [
            r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)',
            r'(\b(OR|AND)\s+\d+\s*=\s*\d+)',
            r'(--|\#|\/\*|\*\/)',
            r'(\b(SCRIPT|JAVASCRIPT|VBSCRIPT)\b)',
            r'(<|>|&lt;|&gt;)'
        ]
        
        self.xss_patterns = [
            r'<\s*script[^>]*>',
            r'javascript\s*:',
            r'on\w+\s*=',
            r'<\s*iframe[^>]*>',
            r'<\s*object[^>]*>',
            r'<\s*embed[^>]*>'
        ]
        
        # Límites de tamaño
        self.max_string_length = 500
        self.max_payload_size = 10240  # 10KB
    
    def validate_string(self, value, field_name="campo"):
        """
        Valida una cadena de texto.
        
        Args:
            value (str): Valor a validar
            field_name (str): Nombre del campo
            
        Returns:
            tuple: (is_valid, errors)
        """
        errors = []
        
        if not isinstance(value, str):
            return False, [f"{field_name} debe ser una cadena de texto"]
        
        # Verificar longitud
        if len(value) > self.max_string_length:
            errors.append(f"{field_name} no puede tener más de {self.max_string_length} caracteres")
        
        # Verificar patrones de SQL injection
        for pattern in self.sql_injection_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                errors.append(f"Contenido sospechoso detectado en {field_name}")
                break
        
        # Verificar patrones de XSS
        for pattern in self.xss_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                errors.append(f"Contenido potencialmente peligroso detectado en {field_name}")
                break
        
        return len(errors) == 0, errors
    
    def validate_number(self, value, field_name="número", min_val=None, max_val=None):
        """
        Valida un número.
        
        Args:
            value: Valor a validar
            field_name (str): Nombre del campo
            min_val: Valor mínimo
            max_val: Valor máximo
            
        Returns:
            tuple: (is_valid, errors)
        """
        errors = []
        
        try:
            num = float(value)
            
            if min_val is not None and num < min_val:
                errors.append(f"{field_name} debe ser mayor o igual a {min_val}")
            
            if max_val is not None and num > max_val:
                errors.append(f"{field_name} debe ser menor o igual a {max_val}")
        
        except (ValueError, TypeError):
            errors.append(f"{field_name} debe ser un número válido")
        
        return len(errors) == 0, errors
    
    def validate_json_payload(self, data):
        """
        Valida un payload JSON completo.
        
        Args:
            data (dict): Datos a validar
            
        Returns:
            tuple: (is_valid, errors)
        """
        errors = []
        
        if not isinstance(data, dict):
            return False, ["El payload debe ser un objeto JSON válido"]
        
        # Verificar tamaño del payload
        payload_str = str(data)
        if len(payload_str) > self.max_payload_size:
            errors.append(f"Payload demasiado grande (máximo {self.max_payload_size} caracteres)")
        
        # Validar strings en el payload
        for key, value in data.items():
            if isinstance(value, str):
                is_valid, field_errors = self.validate_string(value, key)
                if not is_valid:
                    errors.extend(field_errors)
        
        return len(errors) == 0, errors
    
    def sanitize_string(self, value):
        """
        Sanitiza una cadena de texto removiendo caracteres peligrosos.
        
        Args:
            value (str): Cadena a sanitizar
            
        Returns:
            str: Cadena sanitizada
        """
        if not isinstance(value, str):
            return value
        
        # Remover caracteres potencialmente peligrosos
        sanitized = re.sub(r'[<>&"\']', '', value)
        
        # Remover patrones de script
        sanitized = re.sub(r'javascript\s*:', '', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()

# Instancia global del validador
input_validator = InputValidator()

def validate_json_input(sanitize=False):
    """
    Decorador para validar entrada JSON.
    
    Args:
        sanitize (bool): Si sanitizar automáticamente las cadenas
        
    Returns:
        function: Decorador
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verificar que hay datos JSON
            data = request.get_json()
            if not data:
                return f(*args, **kwargs)
            
            # Validar payload
            is_valid, errors = input_validator.validate_json_payload(data)
            
            if not is_valid:
                current_app.logger.warning(
                    f'Payload inválido en {request.endpoint}: {errors}'
                )
                return create_error_response(
                    message="Datos de entrada inválidos",
                    status_code=400,
                    errors=errors
                )
            
            # Sanitizar si está habilitado
            if sanitize:
                for key, value in data.items():
                    if isinstance(value, str):
                        data[key] = input_validator.sanitize_string(value)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_videojuego_data(f):
    """
    Decorador específico para validar datos de videojuego.
    
    Args:
        f (function): Función a decorar
        
    Returns:
        function: Función decorada
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json()
        if not data:
            return f(*args, **kwargs)
        
        errors = []
        
        # Validar nombre
        if 'nombre' in data:
            is_valid, field_errors = input_validator.validate_string(data['nombre'], 'nombre')
            if not is_valid:
                errors.extend(field_errors)
        
        # Validar categoría
        if 'categoria' in data:
            is_valid, field_errors = input_validator.validate_string(data['categoria'], 'categoria')
            if not is_valid:
                errors.extend(field_errors)
        
        # Validar precio
        if 'precio' in data:
            is_valid, field_errors = input_validator.validate_number(
                data['precio'], 'precio', min_val=0, max_val=9999.99
            )
            if not is_valid:
                errors.extend(field_errors)
        
        # Validar valoración
        if 'valoracion' in data:
            is_valid, field_errors = input_validator.validate_number(
                data['valoracion'], 'valoracion', min_val=0, max_val=10
            )
            if not is_valid:
                errors.extend(field_errors)
        
        if errors:
            current_app.logger.warning(
                f'Datos de videojuego inválidos en {request.endpoint}: {errors}'
            )
            return create_error_response(
                message="Datos de videojuego inválidos",
                status_code=400,
                errors=errors
            )
        
        return f(*args, **kwargs)
    return decorated_function

def setup_input_validation(app):
    """
    Configura la validación de entrada para la aplicación.
    
    Args:
        app: Instancia de Flask
    """
    
    @app.before_request
    def validate_request_size():
        """Valida el tamaño de la petición."""
        # Limitar tamaño de petición (10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        
        content_length = request.content_length
        if content_length and content_length > max_size:
            current_app.logger.warning(
                f'Petición demasiado grande: {content_length} bytes desde {request.remote_addr}'
            )
            return create_error_response(
                message="Petición demasiado grande",
                status_code=413,
                errors=[f"El tamaño máximo permitido es {max_size // (1024*1024)}MB"]
            )
    
    app.logger.info('Validación de entrada configurada exitosamente')
