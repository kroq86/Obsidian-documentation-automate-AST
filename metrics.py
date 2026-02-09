"""
Метрики для treemap визуализации Python кода.
Расширяет существующий анализатор метриками для визуализации.
"""

import ast
from typing import Dict, List, Set, Optional
from collections import defaultdict


class TreemapMetricsCollector(ast.NodeVisitor):
    """Собирает метрики для treemap визуализации из AST."""
    
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.functions: List[Dict] = []
        self.classes: List[Dict] = []
        self.function_calls: Set[str] = set()  # Для определения неиспользуемых
        self.current_function: Optional[str] = None
        self.current_class: Optional[str] = None
        
    def visit_FunctionDef(self, node):
        """Обработка определения функции."""
        old_function = self.current_function
        
        # Полное имя функции (с классом если есть)
        if self.current_class:
            full_name = f"{self.current_class}.{node.name}"
        else:
            full_name = node.name
            
        self.current_function = full_name
        
        # Подсчет метрик
        expressions = self._count_ast_nodes(node)
        max_depth = self._calculate_max_depth(node)
        
        func_data = {
            'name': node.name,
            'full_name': full_name,
            'ns': self.module_name,
            'line': node.lineno,
            'end_line': getattr(node, 'end_lineno', node.lineno),
            'file_path': self.module_name,  # Будет установлено позже
            'metrics': {
                'expressions': expressions,
                'max_depth': max_depth,
                'complexity': self._calculate_complexity(node),
                'unused': None  # Определится позже
            }
        }
        
        self.functions.append(func_data)
        
        # Рекурсивный обход тела функции
        self.generic_visit(node)
        
        self.current_function = old_function
    
    def visit_ClassDef(self, node):
        """Обработка определения класса."""
        old_class = self.current_class
        self.current_class = node.name
        
        class_data = {
            'name': node.name,
            'ns': self.module_name,
            'line': node.lineno,
            'end_line': getattr(node, 'end_lineno', node.lineno),
            'file_path': self.module_name,
            'metrics': {
                'expressions': self._count_ast_nodes(node),
                'max_depth': self._calculate_max_depth(node)
            }
        }
        
        self.classes.append(class_data)
        
        self.generic_visit(node)
        
        self.current_class = old_class
    
    def visit_Call(self, node):
        """Отслеживание вызовов функций для определения неиспользуемых."""
        if isinstance(node.func, ast.Name):
            # Прямой вызов: func()
            call_name = node.func.id
            self.function_calls.add(call_name)
        elif isinstance(node.func, ast.Attribute):
            # Вызов метода: obj.method()
            if isinstance(node.func.value, ast.Name):
                # Может быть методом класса
                attr_name = node.func.attr
                self.function_calls.add(attr_name)
        
        self.generic_visit(node)
    
    def _count_ast_nodes(self, node: ast.AST) -> int:
        """Подсчитать количество узлов AST (аналог expressions count)."""
        count = 1
        for child in ast.iter_child_nodes(node):
            count += self._count_ast_nodes(child)
        return count
    
    def _calculate_max_depth(self, node: ast.AST, depth: int = 0) -> int:
        """Вычислить максимальную глубину вложенности."""
        max_d = depth
        
        # Увеличиваем глубину для вложенных структур
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.If, ast.For, 
                            ast.While, ast.With, ast.Try, ast.With)):
            depth += 1
        
        for child in ast.iter_child_nodes(node):
            max_d = max(max_d, self._calculate_max_depth(child, depth))
        
        return max_d
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Вычислить цикломатическую сложность."""
        complexity = 1  # Базовая сложность
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
        
        return complexity


def analyze_file_for_treemap(file_path: str, module_name: str) -> Dict:
    """Анализирует Python файл и возвращает метрики для treemap."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        tree = ast.parse(source, filename=file_path)
        collector = TreemapMetricsCollector(module_name)
        collector.visit(tree)
        
        # Установить file_path для всех функций и классов
        for func in collector.functions:
            func['file_path'] = file_path
        for cls in collector.classes:
            cls['file_path'] = file_path
        
        return {
            'functions': collector.functions,
            'classes': collector.classes,
            'calls': collector.function_calls,
            'error': None
        }
    except Exception as e:
        return {
            'functions': [],
            'classes': [],
            'calls': set(),
            'error': str(e)
        }


def find_unused_functions(all_functions: List[Dict], all_calls: Set[str]) -> Set[str]:
    """Найти неиспользуемые функции."""
    defined_names = {f['name'] for f in all_functions}
    unused = defined_names - all_calls
    
    # Также проверяем полные имена для методов классов
    defined_full_names = {f['full_name'] for f in all_functions}
    unused_full = defined_full_names - all_calls
    
    return unused | {name for name in unused_full if '.' in name}
