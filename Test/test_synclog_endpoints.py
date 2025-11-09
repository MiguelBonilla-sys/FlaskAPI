"""
Tests para endpoints de SyncLog.
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from src.Config.Database import db
from src.Models.SyncLog import SyncLog
from src.Models.Videojuego import Videojuego


class TestSyncLogEndpoints(unittest.TestCase):
    """Tests para endpoints de SyncLog."""
    
    def setUp(self):
        """Configurar test."""
        # Configurar variables de entorno ANTES de crear la app
        os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
        os.environ['RAWG_API_KEY'] = 'test_key'
        os.environ['TESTING'] = 'True'
        
        # Configurar app para testing
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Crear tablas en memoria
        db.create_all()
        
        # Crear datos de prueba
        self._create_test_data()
        
        # Cliente de pruebas
        self.client = self.app.test_client()
    
    def tearDown(self):
        """Limpiar después del test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def _create_test_data(self):
        """Crear datos de prueba."""
        # Crear videojuego de prueba
        self.videojuego = Videojuego(
            nombre="Test Game",
            categoria="RPG",
            precio=29.99,
            valoracion=8.5,
            external_id="1234",
            api_source="rawg"
        )
        db.session.add(self.videojuego)
        db.session.commit()
        
        # Crear logs de sincronización
        self.sync_log1 = SyncLog(
            external_id="1234",
            api_source="rawg",
            status="success",
            videojuego_id=self.videojuego.id
        )
        self.sync_log1.mark_success(videojuego_id=self.videojuego.id, duration_seconds=1.5)
        
        self.sync_log2 = SyncLog(
            external_id="5678",
            api_source="rawg",
            status="failed"
        )
        self.sync_log2.mark_failed("API Error", duration_seconds=0.5)
        
        self.sync_log3 = SyncLog(
            external_id="9999",
            api_source="rawg",
            status="pending"
        )
        # No marcar como completado para mantener pending
        db.session.add(self.sync_log1)
        db.session.add(self.sync_log2)
        db.session.add(self.sync_log3)
        db.session.commit()
    
    def test_get_all_sync_logs(self):
        """Test GET /api/sync-logs - Obtener todos los logs."""
        response = self.client.get('/api/sync-logs')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        # Los logs están en data.logs
        logs = data['data'].get('logs', data['data']) if isinstance(data['data'], dict) else data['data']
        self.assertGreaterEqual(len(logs), 2)  # Al menos 2 logs (puede haber más de los creados)
    
    def test_get_all_sync_logs_with_pagination(self):
        """Test GET /api/sync-logs con paginación."""
        response = self.client.get('/api/sync-logs?page=1&per_page=2')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        # Los logs están en data.logs
        logs = data['data'].get('logs', data['data']) if isinstance(data['data'], dict) else data['data']
        self.assertLessEqual(len(logs), 2)
    
    def test_get_all_sync_logs_with_filters(self):
        """Test GET /api/sync-logs con filtros."""
        # Filtrar por status
        response = self.client.get('/api/sync-logs?status=success')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        # Los logs están en data.logs
        logs = data['data'].get('logs', data['data']) if isinstance(data['data'], dict) else data['data']
        if logs:
            self.assertEqual(logs[0]['status'], 'success')
        
        # Filtrar por api_source
        response = self.client.get('/api/sync-logs?api_source=rawg')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
    
    def test_get_sync_log_by_id(self):
        """Test GET /api/sync-logs/<id> - Obtener log por ID."""
        response = self.client.get(f'/api/sync-logs/{self.sync_log1.id}')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['id'], self.sync_log1.id)
        self.assertEqual(data['data']['status'], 'success')
    
    def test_get_sync_log_not_found(self):
        """Test GET /api/sync-logs/<id> - Log no encontrado."""
        response = self.client.get('/api/sync-logs/99999')
        
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertFalse(data['success'])
    
    def test_get_recent_sync_logs(self):
        """Test GET /api/sync-logs/recent - Obtener logs recientes."""
        response = self.client.get('/api/sync-logs/recent?limit=10')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertGreaterEqual(len(data['data']), 3)
    
    def test_get_recent_sync_logs_with_limit(self):
        """Test GET /api/sync-logs/recent con límite."""
        response = self.client.get('/api/sync-logs/recent?limit=2')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertLessEqual(len(data['data']), 2)
    
    def test_get_recent_sync_logs_with_filter(self):
        """Test GET /api/sync-logs/recent con filtro de API."""
        response = self.client.get('/api/sync-logs/recent?limit=10&api_source=rawg')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        if data['data']:
            self.assertEqual(data['data'][0]['api_source'], 'rawg')
    
    def test_get_sync_statistics(self):
        """Test GET /api/sync-logs/statistics - Obtener estadísticas."""
        response = self.client.get('/api/sync-logs/statistics')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        stats = data['data']
        self.assertIn('total', stats)
        self.assertIn('successful', stats)
        self.assertIn('failed', stats)
        self.assertIn('pending', stats)
        self.assertIn('success_rate', stats)
        self.assertGreaterEqual(stats['total'], 3)
    
    def test_get_sync_statistics_with_days(self):
        """Test GET /api/sync-logs/statistics con días específicos."""
        response = self.client.get('/api/sync-logs/statistics?days=30')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
    
    def test_get_sync_statistics_with_filter(self):
        """Test GET /api/sync-logs/statistics con filtro de API."""
        response = self.client.get('/api/sync-logs/statistics?api_source=rawg')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])


if __name__ == '__main__':
    unittest.main()

