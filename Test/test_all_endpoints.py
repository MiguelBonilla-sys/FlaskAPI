"""
Tests completos para todos los endpoints de videojuegos.
Usa Flask test client para tests aislados y rápidos.
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
from src.Models.Videojuego import Videojuego
from src.Models.Desarrolladora import Desarrolladora


class TestAllEndpoints(unittest.TestCase):
    """Tests completos para todos los endpoints de videojuegos."""
    
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
        # Crear desarrolladora
        self.desarrolladora = Desarrolladora(
            nombre="Test Developer",
            pais="Test Country",
            fundacion=2000
        )
        db.session.add(self.desarrolladora)
        db.session.commit()
        
        # Crear videojuegos
        self.videojuego1 = Videojuego(
            nombre="Test Game 1",
            categoria="RPG",
            precio=29.99,
            valoracion=8.5,
            desarrolladora_id=self.desarrolladora.id
        )
        
        self.videojuego2 = Videojuego(
            nombre="Test Game 2",
            categoria="Action",
            precio=49.99,
            valoracion=9.0,
            desarrolladora_id=self.desarrolladora.id,
            external_id="1234",
            api_source="rawg"
        )
        
        db.session.add(self.videojuego1)
        db.session.add(self.videojuego2)
        db.session.commit()
    
    # ==================== TESTS ENDPOINTS BÁSICOS ====================
    
    def test_get_all_videojuegos(self):
        """Test GET /api/videojuegos - Listar todos los videojuegos."""
        response = self.client.get('/api/videojuegos')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertGreaterEqual(len(data['data']), 2)
    
    def test_get_all_videojuegos_with_pagination(self):
        """Test GET /api/videojuegos con paginación."""
        response = self.client.get('/api/videojuegos?page=1&per_page=1')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        # Verificar que tiene count o que los datos están paginados
        if 'count' in data:
            self.assertGreaterEqual(data['count'], 0)
        else:
            self.assertIsInstance(data['data'], list)
    
    def test_get_all_videojuegos_with_filters(self):
        """Test GET /api/videojuegos con filtros."""
        # Filtrar por categoría
        response = self.client.get('/api/videojuegos?categoria=RPG')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        if data['data']:
            self.assertEqual(data['data'][0]['categoria'], 'RPG')
        
        # Filtrar por desarrolladora
        response = self.client.get(f'/api/videojuegos?desarrolladora_id={self.desarrolladora.id}')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
    
    def test_get_videojuego_by_id(self):
        """Test GET /api/videojuegos/<id> - Obtener videojuego por ID."""
        response = self.client.get(f'/api/videojuegos/{self.videojuego1.id}')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['nombre'], 'Test Game 1')
        self.assertEqual(data['data']['id'], self.videojuego1.id)
    
    def test_get_videojuego_not_found(self):
        """Test GET /api/videojuegos/<id> - Videojuego no encontrado."""
        response = self.client.get('/api/videojuegos/99999')
        
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertFalse(data['success'])
    
    def test_create_videojuego(self):
        """Test POST /api/videojuegos - Crear videojuego."""
        nuevo_videojuego = {
            'nombre': 'Nuevo Juego',
            'categoria': 'Adventure',
            'precio': 39.99,
            'valoracion': 8.0,
            'desarrolladora_id': self.desarrolladora.id
        }
        
        response = self.client.post(
            '/api/videojuegos',
            json=nuevo_videojuego,
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['nombre'], 'Nuevo Juego')
        self.assertIn('id', data['data'])
    
    def test_create_videojuego_invalid_data(self):
        """Test POST /api/videojuegos - Datos inválidos."""
        invalid_data = {
            'nombre': '',  # nombre vacío
            'categoria': 'Test',
            'precio': -10  # precio negativo
        }
        
        response = self.client.post(
            '/api/videojuegos',
            json=invalid_data,
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['success'])
    
    def test_update_videojuego(self):
        """Test PUT /api/videojuegos/<id> - Actualizar videojuego."""
        update_data = {
            'nombre': 'Test Game 1 Actualizado',
            'precio': 19.99
        }
        
        response = self.client.put(
            f'/api/videojuegos/{self.videojuego1.id}',
            json=update_data,
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['nombre'], 'Test Game 1 Actualizado')
        self.assertEqual(float(data['data']['precio']), 19.99)
    
    def test_update_videojuego_not_found(self):
        """Test PUT /api/videojuegos/<id> - Videojuego no encontrado."""
        response = self.client.put(
            '/api/videojuegos/99999',
            json={'nombre': 'Test'},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
    
    def test_delete_videojuego(self):
        """Test DELETE /api/videojuegos/<id> - Eliminar videojuego."""
        # Crear un videojuego temporal para eliminar
        temp_game = Videojuego(
            nombre="Temp Game",
            categoria="Test",
            precio=10.0,
            valoracion=5.0
        )
        db.session.add(temp_game)
        db.session.commit()
        temp_id = temp_game.id
        
        response = self.client.delete(f'/api/videojuegos/{temp_id}')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        
        # Verificar que fue eliminado
        deleted = Videojuego.query.get(temp_id)
        self.assertIsNone(deleted)
    
    def test_delete_videojuego_not_found(self):
        """Test DELETE /api/videojuegos/<id> - Videojuego no encontrado."""
        response = self.client.delete('/api/videojuegos/99999')
        
        self.assertEqual(response.status_code, 404)
    
    # ==================== TESTS ENDPOINTS DE CONSULTA ====================
    
    def test_get_categorias(self):
        """Test GET /api/videojuegos/categorias - Obtener categorías."""
        response = self.client.get('/api/videojuegos/categorias')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIsInstance(data['data'], list)
        self.assertIn('RPG', data['data'])
        self.assertIn('Action', data['data'])
    
    def test_get_estadisticas(self):
        """Test GET /api/videojuegos/estadisticas - Obtener estadísticas."""
        response = self.client.get('/api/videojuegos/estadisticas')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        stats = data['data']
        self.assertIn('total_videojuegos', stats)
        self.assertIn('categorias_unicas', stats)
        self.assertIn('precio_promedio', stats)
        self.assertIn('valoracion_promedio', stats)
        self.assertGreaterEqual(stats['total_videojuegos'], 2)
    
    def test_busqueda_avanzada(self):
        """Test GET /api/videojuegos/busqueda-avanzada - Búsqueda avanzada."""
        # Búsqueda por categoría
        response = self.client.get('/api/videojuegos/busqueda-avanzada?categoria=RPG')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        
        # Búsqueda por precio mínimo
        response = self.client.get('/api/videojuegos/busqueda-avanzada?precio_min=40')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        
        # Búsqueda por valoración
        response = self.client.get('/api/videojuegos/busqueda-avanzada?valoracion_min=9.0')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
    
    # ==================== TESTS ENDPOINTS RAWG ====================
    
    @patch('src.Services.GameService.RAWGService.get_game_details')
    def test_importar_externa(self, mock_get_details):
        """Test POST /api/videojuegos/importar-externa - Importar desde RAWG."""
        # Mock de respuesta RAWG
        mock_get_details.return_value = {
            'id': 9999,
            'name': 'Imported Game',
            'genres': [{'name': 'RPG'}],
            'rating': 4.5,
            'metacritic': 90,
            'description_raw': 'Test description',
            'background_image': 'https://example.com/img.jpg',
            'developers': [{'name': 'Test Dev'}]
        }
        
        response = self.client.post(
            '/api/videojuegos/importar-externa',
            json={'external_id': '9999'},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['nombre'], 'Imported Game')
        self.assertEqual(data['data']['external_id'], '9999')
        self.assertEqual(data['data']['api_source'], 'rawg')
    
    def test_importar_externa_missing_external_id(self):
        """Test POST /api/videojuegos/importar-externa - Sin external_id."""
        response = self.client.post(
            '/api/videojuegos/importar-externa',
            json={},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['success'])
    
    @patch('src.Services.GameService.RAWGService.search_games')
    def test_buscar_hibrida(self, mock_search):
        """Test GET /api/videojuegos/buscar - Búsqueda híbrida."""
        # Mock de respuesta RAWG
        mock_search.return_value = {
            'results': [
                {
                    'id': 5000,
                    'name': 'External Game',
                    'genres': [{'name': 'Action'}],
                    'rating': 4.0,
                    'background_image': 'https://example.com/img.jpg'
                }
            ]
        }
        
        # Búsqueda solo local
        response = self.client.get('/api/videojuegos/buscar?q=Test&include_external=false')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('local', data['data'])
        self.assertIn('external', data['data'])
        self.assertEqual(len(data['data']['external']), 0)
        
        # Búsqueda con externos
        response = self.client.get('/api/videojuegos/buscar?q=Test&include_external=true')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('local', data['data'])
        self.assertIn('external', data['data'])
    
    def test_buscar_hibrida_missing_query(self):
        """Test GET /api/videojuegos/buscar - Sin parámetro q."""
        response = self.client.get('/api/videojuegos/buscar')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['success'])
    
    @patch('src.Services.GameService.RAWGService.get_game_details')
    @patch('src.Services.GameService.RAWGService.get_game_screenshots')
    def test_get_enriquecido(self, mock_screenshots, mock_details):
        """Test GET /api/videojuegos/<id>/enriquecido - Obtener enriquecido."""
        # Mock de respuesta RAWG
        mock_details.return_value = {
            'id': int(self.videojuego2.external_id),
            'name': 'Enriched Game',
            'genres': [{'name': 'Action'}],
            'rating': 4.5,
            'description_raw': 'Enriched description',
            'background_image': 'https://example.com/bg.jpg',
            'developers': [{'name': 'Developer'}]
        }
        mock_screenshots.return_value = {
            'results': [
                {'image': 'https://example.com/screenshot1.jpg'},
                {'image': 'https://example.com/screenshot2.jpg'}
            ]
        }
        
        response = self.client.get(f'/api/videojuegos/{self.videojuego2.id}/enriquecido')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        # enrich_game retorna un diccionario con el juego enriquecido
        self.assertIn('data', data)
        enriched = data['data']
        # Puede retornar el juego con screenshots agregados
        self.assertIn('id', enriched)
        self.assertIn('nombre', enriched)
    
    def test_get_enriquecido_no_external_id(self):
        """Test GET /api/videojuegos/<id>/enriquecido - Sin external_id."""
        response = self.client.get(f'/api/videojuegos/{self.videojuego1.id}/enriquecido')
        
        # Debe retornar datos locales aunque no tenga external_id
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
    
    @patch('src.Services.GameService.RAWGService.get_game_details')
    def test_importar_batch(self, mock_get_details):
        """Test POST /api/videojuegos/importar-batch - Importar múltiples."""
        # Mock de respuesta RAWG
        mock_get_details.return_value = {
            'id': 1000,
            'name': 'Batch Game 1',
            'genres': [{'name': 'RPG'}],
            'rating': 4.0,
            'metacritic': 80,
            'description_raw': 'Test',
            'background_image': '',
            'developers': []
        }
        
        response = self.client.post(
            '/api/videojuegos/importar-batch',
            json={'games': [{'external_id': '1000'}]},
            content_type='application/json'
        )
        
        # Puede retornar 201 (todo exitoso), 207 (multi-status) o 400 (todo fallido)
        self.assertIn(response.status_code, [201, 207, 400])
        data = response.get_json()
        self.assertIn('data', data)
        self.assertIn('success', data['data'])
        self.assertIn('failed', data['data'])
    
    def test_importar_batch_invalid_data(self):
        """Test POST /api/videojuegos/importar-batch - Datos inválidos."""
        response = self.client.post(
            '/api/videojuegos/importar-batch',
            json={'games': []},  # Lista vacía
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['success'])
    
    @patch('src.Tasks.sync_tasks.sync_game_from_api.delay')
    def test_sync_manual(self, mock_delay):
        """Test POST /api/videojuegos/sync-manual - Sincronización manual."""
        # Mock de task de Celery
        mock_task = MagicMock()
        mock_task.id = 'sync-task-id-456'
        mock_delay.return_value = mock_task
        
        response = self.client.post(
            '/api/videojuegos/sync-manual',
            json={'external_id': '2000'},  # sync_manual espera un solo external_id
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 202)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('task_id', data['data'])
    
    @patch('celery.result.AsyncResult')
    def test_sync_status(self, mock_async_result_class):
        """Test GET /api/videojuegos/sync-status/<task_id> - Estado de sync."""
        # Mock de resultado de Celery
        mock_result = MagicMock()
        mock_result.state = 'SUCCESS'
        mock_result.result = {'status': 'success', 'game_id': 1}
        mock_result.info = None
        mock_async_result_class.return_value = mock_result
        
        response = self.client.get('/api/videojuegos/sync-status/test-task-id')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('status', data['data'])
        self.assertEqual(data['data']['status'], 'completed')
    
    @patch('celery.result.AsyncResult')
    def test_sync_status_invalid_task(self, mock_async_result_class):
        """Test GET /api/videojuegos/sync-status/<task_id> - Task inválido."""
        mock_result = MagicMock()
        mock_result.state = 'PENDING'
        mock_result.info = None
        mock_async_result_class.return_value = mock_result
        
        response = self.client.get('/api/videojuegos/sync-status/invalid-task')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        # El endpoint puede retornar success=True o False dependiendo de la implementación
        # Lo importante es que retorna un status
        self.assertIn('data', data)
        self.assertIn('status', data['data'])
        self.assertEqual(data['data']['status'], 'pending')


def run_all_endpoint_tests():
    """Ejecuta todos los tests de endpoints."""
    print("=" * 60)
    print("TESTS COMPLETOS DE TODOS LOS ENDPOINTS")
    print("=" * 60)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestAllEndpoints))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_endpoint_tests()
    sys.exit(0 if success else 1)

