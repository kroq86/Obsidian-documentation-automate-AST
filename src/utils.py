"""
Утилиты для работы с данными.
"""


def format_number(num: float, decimals: int = 2) -> str:
    """Форматирует число с заданным количеством знаков после запятой."""
    return f"{num:.{decimals}f}"


def validate_input(value: str) -> bool:
    """Проверяет корректность входных данных."""
    if not value:
        return False
    
    try:
        float(value)
        return True
    except ValueError:
        return False


class DataProcessor:
    """Обрабатывает данные."""
    
    def __init__(self):
        self.processed_count = 0
    
    def process(self, data: list) -> list:
        """Обрабатывает список данных."""
        result = []
        for item in data:
            if isinstance(item, (int, float)):
                result.append(item * 2)
            elif isinstance(item, str):
                result.append(item.upper())
            else:
                result.append(item)
        
        self.processed_count += len(result)
        return result
    
    def get_stats(self) -> dict:
        """Возвращает статистику обработки."""
        return {
            'processed': self.processed_count,
            'average': self.processed_count / max(1, len(self.stats)) if hasattr(self, 'stats') else 0
        }
