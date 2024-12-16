import pytest
import unittest

from app.calc import Calculator


@pytest.mark.unit
class TestCalculate(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_method_returns_correct_result(self):
        self.assertEqual(4, self.calc.add(2, 2))
        self.assertEqual(0, self.calc.add(2, -2))
        self.assertEqual(0, self.calc.add(-2, 2))
        self.assertEqual(1, self.calc.add(1, 0))

    def test_substract_method_returns_correct_result(self):
        self.assertEqual(4, self.calc.substract(10, 6))
        self.assertEqual(-2, self.calc.substract(256, 258))
        self.assertEqual(-1, self.calc.substract(-1, 0))
        self.assertEqual(0, self.calc.substract(0, 0))

    def test_multiply_method_returns_correct_result(self):
        self.assertEqual(4, self.calc.multiply(2, 2))
        self.assertEqual(0, self.calc.multiply(1, 0))
        self.assertEqual(0, self.calc.multiply(-1, 0))
        self.assertEqual(-2, self.calc.multiply(-1, 2))
        self.assertEqual(0, self.calc.multiply(0, 0))
        self.assertRaises(TypeError, self.calc.multiply, "0", 0)

    def test_divide_method_returns_correct_result(self):
        self.assertEqual(1, self.calc.divide(2, 2))
        self.assertEqual(1.5, self.calc.divide(3, 2))
        self.assertEqual(3.0, self.calc.divide(6, 2))
        
    def test_divide_method_fails_with_zero_divisor(self):
        # Verifica que se maneje correctamente la división por cero
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(2, 0)
        
    def test_multiply_method_fails_with_invalid_parameters(self):
        # Verifica que se manejen los casos con parámetros no numéricos
        self.assertRaises(TypeError, self.calc.multiply, "0", 0)
        self.assertRaises(TypeError, self.calc.multiply, 0, "0")

    def test_divide_method_fails_with_invalid_parameters(self):
        # Verifica que se manejen los casos con parámetros no numéricos
        self.assertRaises(TypeError, self.calc.divide, "2", 2)
        self.assertRaises(TypeError, self.calc.divide, 2, "2")
        self.assertRaises(TypeError, self.calc.divide, "2", "2")

if __name__ == "__main__":  # pragma: no cover
    unittest.main()
