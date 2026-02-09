"""
Простой калькулятор для тестирования метрик.
"""


class Calculator:
    """Класс для выполнения математических операций."""
    
    def __init__(self):
        self.history = []
    
    def add(self, a: float, b: float) -> float:
        """Сложение двух чисел."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """Вычитание двух чисел."""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """Умножение двух чисел."""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a: float, b: float) -> float:
        """Деление двух чисел."""
        if b == 0:
            raise ValueError("Division by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def complex_calculation(self, values: list) -> float:
        """Сложный расчет с высокой цикломатической сложностью."""
        result = 0
        for value in values:
            if value > 0:
                if value < 10:
                    result += value * 2
                elif value < 100:
                    result += value * 1.5
                else:
                    result += value
            elif value < 0:
                result -= abs(value)
            else:
                result += 0
        
        if result > 1000:
            return result * 0.9
        elif result > 100:
            return result * 0.95
        else:
            return result


def unused_function():
    """Эта функция не используется нигде."""
    return 42


def helper_function(x: int) -> int:
    """Вспомогательная функция."""
    return x * 2
