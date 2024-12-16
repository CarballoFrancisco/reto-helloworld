import http.client
import os
import unittest
from urllib.request import urlopen
import pytest

BASE_URL = "http://localhost:5000"
DEFAULT_TIMEOUT = 2  # en segundos

@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        # Prueba de suma con números válidos
        url = f"{BASE_URL}/calc/add/1/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3", "ERROR ADD"
        )

    def test_api_substract(self):
        # Prueba de resta con números válidos
        url = f"{BASE_URL}/calc/substract/5/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "2", "ERROR SUBSTRACT"
        )

    def test_api_multiply(self):
        # Prueba de multiplicación con números reales
        url = f"{BASE_URL}/calc/multiply/3.5/2.1"  # Usamos 3.5 y 2.1 como números reales
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "7.35", "ERROR MULTIPLY"
        )

    def test_api_divide(self):
        # Prueba de división con números reales
        url = f"{BASE_URL}/calc/divide/7.5/2.5"  # Usamos 7.5 y 2.5 como números reales
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3.0", "ERROR DIVIDE"
        )

    def test_api_divide_by_zero(self):
        # Prueba de división por cero
        url = f"{BASE_URL}/calc/divide/6/0"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.NOT_ACCEPTABLE, f"Error en la petición API a {url}"
        )
        self.assertIn(
            "Cannot divide by zero", response.read().decode(), "ERROR DIVIDE BY ZERO"
        )

    def test_api_multiply_invalid_input(self):
        # Prueba de entrada no válida en multiplicación
        url = f"{BASE_URL}/calc/multiply/2/a"  # Usamos 2 y 'a' para simular un error
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.BAD_REQUEST, f"Error en la petición API a {url}"
        )
        self.assertIn(
            "Invalid input", response.read().decode(), "ERROR INVALID INPUT MULTIPLY"
        )

    def test_api_divide_invalid_input(self):
        # Prueba de entrada no válida en división
        url = f"{BASE_URL}/calc/divide/2/a"  # Usamos 2 y 'a' para simular un error
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.BAD_REQUEST, f"Error en la petición API a {url}"
        )
        self.assertIn(
            "Invalid input", response.read().decode(), "ERROR INVALID INPUT DIVIDE"
        )

if __name__ == "__main__":  # pragma: no cover
    unittest.main()

