"""
Tests unitarios para servicios (RAWGService, GameService).
Usa mocks para evitar llamadas reales a APIs externas.
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock, Mock
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from src.Services.RAWGService import RAWGService
from src.Services.GameService import GameService
from src.Mappers.RAWGMapper import RAWGMapper
from src.Models.Videojuego import Videojuego
from src.Config.Database import db


class TestRAWGMapper(unittest.TestCase):
    """Tests para RAWGMapper."""
    
    def test_to_internal_model_basic(self):
        """Test de transformación básica de datos RAWG."""
        rawg_data = {
            'id': 3328,
            'name': 'The Witcher 3: Wild Hunt',
            'genres': [{'name': 'RPG'}],
            'rating': 4.5,
            'metacritic': 92,
            'description_raw': 'A great RPG game',
            'background_image': 'https://example.com/image.jpg',
            'developers': [{'name': 'CD Projekt RED'}]
        }
        
        result = RAWGMapper.to_internal_model(rawg_data)
        
        self.assertEqual(result['nombre'], 'The Witcher 3: Wild Hunt')
        self.assertEqual(result['categoria'], 'RPG')
        self.assertEqual(result['external_id'], '3328')
        self.assertEqual(result['api_source'], 'rawg')
        self.assertEqual(result['valoracion'], 9.2)  # Metacritic 92 / 10
        self.assertEqual(result['desarrollador'], 'CD Projekt RED')
    
    def test_to_internal_model_no_metacritic(self):
        """Test cuando no hay Metacritic, usa rating de RAWG."""
        rawg_data = {
            'id': 1234,
            'name': 'Test Game',
            'genres': [{'name': 'Action'}],
            'rating': 4.0,  # 0-5 scale
            'description_raw': 'Test',
            'background_image': '',
            'developers': []
        }
        
        result = RAWGMapper.to_internal_model(rawg_data)
        
        self.assertEqual(result['valoracion'], 8.0)  # 4.0 * 2 = 8.0
    
    def test_to_internal_model_no_genres(self):
        """Test cuando no hay géneros."""
        rawg_data = {
            'id': 1234,
            'name': 'Test Game',
            'genres': [],
            'rating': 0,
            'description_raw': '',
            'background_image': '',
            'developers': []
        }
        
        result = RAWGMapper.to_internal_model(rawg_data)
        
        self.assertEqual(result['categoria'], 'Sin categoría')


class TestRAWGService(unittest.TestCase):
    """Tests para RAWGService con mocks."""
    
    def setUp(self):
        """Configurar test."""
        # Configurar variables de entorno ANTES de crear la app
        os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
        os.environ['RAWG_API_KEY'] = 'test_key'
        os.environ['TESTING'] = 'True'  # Marcar como testing antes de crear app
        
        # Configurar app para testing (usa SQLite en memoria y caché simple)
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Crear tablas en memoria
        db.create_all()
        
        # Asegurar que la API key esté configurada
        self.app.config['RAWG_API_KEY'] = 'test_key'
    
    def tearDown(self):
        """Limpiar después del test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    @patch('src.Services.RAWGService.RAWGService._make_request')
    def test_search_games(self, mock_request):
        """Test de búsqueda de juegos."""
        # Mock de respuesta
        mock_request.return_value = {
            'results': [
                {
                    'id': 3328,
                    'name': 'The Witcher 3',
                    'genres': [{'name': 'RPG'}],
                    'rating': 4.5
                }
            ],
            'count': 1
        }
        
        service = RAWGService()
        result = service.search_games('witcher')
        
        self.assertIn('results', result)
        self.assertEqual(len(result['results']), 1)
        mock_request.assert_called_once()
    
    @patch('src.Services.RAWGService.RAWGService._make_request')
    def test_get_game_details(self, mock_request):
        """Test de obtener detalles de juego."""
        mock_request.return_value = {
            'id': 3328,
            'name': 'The Witcher 3',
            'genres': [{'name': 'RPG'}],
            'rating': 4.5,
            'metacritic': 92
        }
        
        service = RAWGService()
        result = service.get_game_details('3328')
        
        self.assertEqual(result['id'], 3328)
        self.assertEqual(result['name'], 'The Witcher 3')
        mock_request.assert_called_once()


class TestGameService(unittest.TestCase):
    """Tests para GameService."""
    
    def setUp(self):
        """Configurar test."""
        # Configurar variables de entorno ANTES de crear la app
        os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
        os.environ['RAWG_API_KEY'] = 'test_key'
        os.environ['TESTING'] = 'True'  # Marcar como testing antes de crear app
        
        # Configurar app para testing (usa SQLite en memoria y caché simple)
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Crear tablas en memoria
        db.create_all()
        
        # Asegurar que la API key esté configurada
        self.app.config['RAWG_API_KEY'] = 'test_key'
    
    def tearDown(self):
        """Limpiar después del test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    @patch('src.Services.GameService.RAWGService.get_game_details')
    def test_import_game(self, mock_get_details):
        """Test de importación de juego."""
        # Mock de respuesta RAWG
        mock_get_details.return_value = {
            'id': 9999,
            'name': 'Test Game Import',
            'genres': [{'name': 'Action'}],
            'rating': 4.0,
            'metacritic': 80,
            'description_raw': 'Test description',
            'background_image': 'https://example.com/img.jpg',
            'developers': [{'name': 'Test Developer'}]
        }
        
        service = GameService()
        game = service.import_game('9999')
        
        self.assertIsNotNone(game)
        self.assertEqual(game.nombre, 'Test Game Import')
        self.assertEqual(game.external_id, '9999')
        self.assertEqual(game.api_source, 'rawg')
        self.assertIsNotNone(game.last_synced)
    
    def test_search_hybrid_local_only(self):
        """Test de búsqueda híbrida solo local."""
        service = GameService()
        result = service.search_hybrid('test', include_external=False)
        
        self.assertIn('local', result)
        self.assertIn('external', result)
        self.assertEqual(len(result['external']), 0)
    
    @patch('src.Services.GameService.RAWGService.search_games')
    def test_search_hybrid_with_external(self, mock_search):
        """Test de búsqueda híbrida con resultados externos."""
        mock_search.return_value = {
            'results': [
                {
                    'id': 1234,
                    'name': 'External Game',
                    'genres': [{'name': 'RPG'}],
                    'rating': 4.5,
                    'background_image': 'https://example.com/img.jpg'
                }
            ]
        }
        
        service = GameService()
        result = service.search_hybrid('test', include_external=True)
        
        self.assertIn('local', result)
        self.assertIn('external', result)
        self.assertGreater(len(result['external']), 0)


def run_unit_tests():
    """Ejecuta todos los tests unitarios."""
    print("=" * 60)
    print("TESTS UNITARIOS DE SERVICIOS")
    print("=" * 60)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestRAWGMapper))
    suite.addTests(loader.loadTestsFromTestCase(TestRAWGService))
    suite.addTests(loader.loadTestsFromTestCase(TestGameService))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_unit_tests()
    sys.exit(0 if success else 1)

