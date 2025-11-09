"""
Tests para el modelo SyncLog.
"""
import os
import sys
import unittest
from datetime import datetime, timedelta

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from src.Models.SyncLog import SyncLog
from src.Config.Database import db


class TestSyncLog(unittest.TestCase):
    """Tests para el modelo SyncLog."""
    
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
    
    def tearDown(self):
        """Limpiar después del test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_create_synclog(self):
        """Test de creación de SyncLog."""
        sync_log = SyncLog(
            external_id='1234',
            api_source='rawg',
            status='pending'
        )
        db.session.add(sync_log)
        db.session.commit()
        
        self.assertIsNotNone(sync_log.id)
        self.assertEqual(sync_log.external_id, '1234')
        self.assertEqual(sync_log.api_source, 'rawg')
        self.assertEqual(sync_log.status, 'pending')
        self.assertIsNotNone(sync_log.started_at)
        self.assertIsNone(sync_log.completed_at)
    
    def test_mark_success(self):
        """Test de marcar sincronización como exitosa."""
        sync_log = SyncLog(external_id='1234', api_source='rawg')
        db.session.add(sync_log)
        db.session.commit()
        
        # Marcar como exitoso
        sync_log.mark_success(videojuego_id=1, duration_seconds=2.5)
        db.session.commit()
        
        self.assertEqual(sync_log.status, 'success')
        self.assertIsNotNone(sync_log.completed_at)
        self.assertEqual(sync_log.videojuego_id, 1)
        self.assertEqual(sync_log.duration_seconds, 2.5)
        self.assertIsNone(sync_log.error_message)
    
    def test_mark_failed(self):
        """Test de marcar sincronización como fallida."""
        sync_log = SyncLog(external_id='1234', api_source='rawg')
        db.session.add(sync_log)
        db.session.commit()
        
        # Marcar como fallido
        error_msg = "API timeout"
        sync_log.mark_failed(error_message=error_msg, duration_seconds=5.0)
        db.session.commit()
        
        self.assertEqual(sync_log.status, 'failed')
        self.assertIsNotNone(sync_log.completed_at)
        self.assertEqual(sync_log.error_message, error_msg)
        self.assertEqual(sync_log.duration_seconds, 5.0)
    
    def test_to_dict(self):
        """Test de conversión a diccionario."""
        sync_log = SyncLog(external_id='1234', api_source='rawg')
        sync_log.mark_success(videojuego_id=1, duration_seconds=2.5)
        db.session.add(sync_log)
        db.session.commit()
        
        result = sync_log.to_dict()
        
        self.assertIn('id', result)
        self.assertIn('external_id', result)
        self.assertIn('api_source', result)
        self.assertIn('status', result)
        self.assertIn('videojuego_id', result)
        self.assertIn('duration_seconds', result)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['external_id'], '1234')
    
    def test_get_recent_syncs(self):
        """Test de obtener sincronizaciones recientes."""
        # Crear varios registros
        for i in range(5):
            sync_log = SyncLog(external_id=f'{1000+i}', api_source='rawg')
            if i % 2 == 0:
                sync_log.mark_success(duration_seconds=1.0)
            else:
                sync_log.mark_failed('Error', duration_seconds=1.0)
            db.session.add(sync_log)
        
        db.session.commit()
        
        # Obtener recientes
        recent = SyncLog.get_recent_syncs(limit=3)
        
        self.assertEqual(len(recent), 3)
        self.assertIsNotNone(recent[0].id)
    
    def test_get_recent_syncs_with_filter(self):
        """Test de obtener sincronizaciones con filtro de API."""
        # Crear registros de diferentes APIs
        sync1 = SyncLog(external_id='1', api_source='rawg')
        sync1.mark_success(duration_seconds=1.0)
        db.session.add(sync1)
        
        sync2 = SyncLog(external_id='2', api_source='steam')
        sync2.mark_success(duration_seconds=1.0)
        db.session.add(sync2)
        
        db.session.commit()
        
        # Filtrar por rawg
        rawg_syncs = SyncLog.get_recent_syncs(limit=10, api_source='rawg')
        
        self.assertEqual(len(rawg_syncs), 1)
        self.assertEqual(rawg_syncs[0].api_source, 'rawg')
    
    def test_get_stats(self):
        """Test de obtener estadísticas."""
        # Crear registros con diferentes estados
        for i in range(10):
            sync_log = SyncLog(external_id=f'{2000+i}', api_source='rawg')
            if i < 7:
                sync_log.mark_success(duration_seconds=1.0)
            elif i < 9:
                sync_log.mark_failed('Error', duration_seconds=1.0)
            # else: pending (default)
            db.session.add(sync_log)
        
        db.session.commit()
        
        # Obtener estadísticas
        stats = SyncLog.get_stats(api_source='rawg', days=7)
        
        self.assertEqual(stats['total'], 10)
        self.assertEqual(stats['successful'], 7)
        self.assertEqual(stats['failed'], 2)
        self.assertEqual(stats['pending'], 1)
        self.assertAlmostEqual(stats['success_rate'], 70.0, places=1)
    
    def test_duration_calculation(self):
        """Test de cálculo automático de duración."""
        sync_log = SyncLog(external_id='1234', api_source='rawg')
        db.session.add(sync_log)
        db.session.commit()
        
        # Simular tiempo transcurrido
        import time
        time.sleep(0.1)  # Esperar un poco
        
        # Marcar como exitoso sin especificar duración
        sync_log.mark_success()
        db.session.commit()
        
        self.assertIsNotNone(sync_log.duration_seconds)
        self.assertGreater(sync_log.duration_seconds, 0)


def run_synclog_tests():
    """Ejecuta todos los tests de SyncLog."""
    print("=" * 60)
    print("TESTS DEL MODELO SYNCLOG")
    print("=" * 60)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestSyncLog))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_synclog_tests()
    sys.exit(0 if success else 1)

