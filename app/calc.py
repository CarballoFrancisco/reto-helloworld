import app

class InvalidPermissions(Exception):
    pass

class Calculator:
    def add(self, x, y):
        self.check_types(x, y)
        return x + y

    def subtract(self, x, y):  # Corregido el nombre del método
        self.check_types(x, y)
        return x - y

    def multiply(self, x, y):
        self.check_types(x, y)
        return x * y

    def divide(self, x, y):
        self.check_types(x, y)
        if y == 0:
            raise TypeError("Division by zero is not possible")  # Indentación corregida
        return x / y

    def power(self, x, y):
        self.check_types(x, y)
        return x ** y

    def check_types(self, x, y):
        if not all(isinstance(i, (int, float)) for i in (x, y)):  # Mejor validación
            raise TypeError("Parameters must be numbers")

if __name__ == "__main__":  # pragma: no cover
    calc = Calculator()
    result = calc.add(2, 2)
    print(result)

