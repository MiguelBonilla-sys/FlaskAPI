"""
Clase base para servicios de APIs externas.
Proporciona funcionalidad común: retry logic, circuit breaker, manejo de errores.
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from flask import current_app
import logging
from datetime import datetime, timedelta
from src.Utils.exceptions import APIError, APITimeoutError, RateLimitError, CircuitBreakerOpen


class CircuitBreaker:
    """Circuit breaker pattern básico para prevenir llamadas a APIs fallidas."""
    
    def __init__(self, failure_threshold=5, timeout=60):
        """
        Args:
            failure_threshold: Número de fallos antes de abrir el circuito
            timeout: Tiempo en segundos antes de intentar cerrar el circuito
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = 'closed'  # closed, open, half_open
    
    def call(self, func, *args, **kwargs):
        """Ejecuta función con protección de circuit breaker."""
        if self.state == 'open':
            if self.last_failure_time and \
               datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout):
                self.state = 'half_open'
            else:
                raise CircuitBreakerOpen("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Resetea contador de fallos cuando hay éxito."""
        self.failures = 0
        self.state = 'closed'
    
    def _on_failure(self):
        """Incrementa contador de fallos y abre circuito si es necesario."""
        self.failures += 1
        self.last_failure_time = datetime.now()
        if self.failures >= self.failure_threshold:
            self.state = 'open'


class ExternalAPIService:
    """Clase base para servicios de APIs externas."""
    
    def __init__(self):
        """Inicializa el servicio con session HTTP y circuit breaker."""
        self.session = self._create_session()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.circuit_breaker = CircuitBreaker()
    
    def _create_session(self):
        """Crea session HTTP con retry strategy y connection pooling."""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20
        )
        
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _make_request(self, url, params=None, headers=None, timeout=10):
        """
        Realiza petición HTTP con manejo de errores.
        
        Args:
            url: URL a llamar
            params: Parámetros de query
            headers: Headers HTTP
            timeout: Timeout en segundos
        
        Returns:
            dict: Respuesta JSON
        
        Raises:
            APITimeoutError: Si hay timeout
            RateLimitError: Si se excede rate limit
            APIError: Para otros errores
        """
        def _request():
            try:
                response = self.session.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=timeout
                )
                response.raise_for_status()
                return response.json()
            except requests.Timeout:
                self.logger.error(f"Timeout calling {url}")
                raise APITimeoutError("External API timeout")
            except requests.HTTPError as e:
                if e.response.status_code == 429:
                    self.logger.warning("Rate limit hit")
                    raise RateLimitError("Rate limit exceeded")
                self.logger.error(f"HTTP error: {e}")
                raise APIError(f"HTTP error: {e}")
            except requests.RequestException as e:
                self.logger.error(f"Request error: {e}")
                raise APIError(f"Request error: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                raise APIError(f"Unexpected error: {e}")
        
        # Usar circuit breaker
        return self.circuit_breaker.call(_request)

