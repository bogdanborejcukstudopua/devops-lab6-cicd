import unittest
import json
# Импортируем наше приложение и класс модели из main.py
from main import app, TransientModel

class TestRLCAPI(unittest.TestCase):
    def setUp(self):
        # Создаем тестовый клиент Flask
        self.app = app.test_client()
        self.app.testing = True

    def test_model_math(self):
        """Проверка математической логики модели RLC"""
        model = TransientModel(R=10.0, L=0.1, C=0.001)
        self.assertEqual(model.R, 10.0)
        self.assertEqual(model.L, 0.1)

    def test_calculate_endpoint(self):
        """Проверка POST-запроса к API (наш JSON вариант из ЛР5)"""
        payload = {"R": 15.0, "L": 0.2, "C": 0.0015}
        response = self.app.post(
            '/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Проверяем, что сервер ответил 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Проверяем, что JSON-ответ содержит правильные входные данные
        data = json.loads(response.data)
        self.assertEqual(data["input"]["R"], 15.0)
        self.assertIn("result", data)

if __name__ == '__main__':
    unittest.main()
