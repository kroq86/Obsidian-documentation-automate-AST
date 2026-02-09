"""
Публичный API для анализа Python проектов и генерации метрик для treemap визуализации.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Set
from collections import defaultdict

from metrics import analyze_file_for_treemap, find_unused_functions
from prometheus import write_prometheus


def get_module_name(file_path: str, project_root: str) -> str:
    """Получить имя модуля из пути к файлу относительно корня проекта."""
    rel_path = os.path.relpath(file_path, project_root)
    # Убрать расширение .py
    module_path = rel_path.replace('.py', '').replace(os.sep, '.')
    # Убрать __init__ из пути
    if module_path.endswith('.__init__'):
        module_path = module_path[:-9]
    return module_path or 'root'


def analyze_project(
    project_path: str,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None
) -> Dict:
    """Анализирует Python проект и возвращает метрики для treemap визуализации.
    
    Args:
        project_path: Путь к корню проекта
        include_patterns: Паттерны для включения файлов (например, ['src/**'])
        exclude_patterns: Паттерны для исключения (например, ['test', '__pycache__'])
    
    Returns:
        Словарь с ключами:
            - compiler: список функций и классов с метриками
            - classloader: список классов с метриками байткода (пока пусто)
            - errors: список ошибок анализа
    """
    project_root = Path(project_path).resolve()
    
    if not project_root.exists():
        raise ValueError(f"Project path does not exist: {project_path}")
    
    # Найти все .py файлы
    py_files = list(project_root.rglob("*.py"))
    
    # Применить фильтры
    if exclude_patterns:
        py_files = [
            f for f in py_files
            if not any(pattern in str(f) for pattern in exclude_patterns)
        ]
    
    if include_patterns:
        py_files = [
            f for f in py_files
            if any(pattern in str(f) for pattern in include_patterns)
        ]
    
    # Исключить виртуальные окружения и кэш
    py_files = [
        f for f in py_files
        if 'venv' not in str(f) 
        and '__pycache__' not in str(f)
        and '.venv' not in str(f)
        and 'site-packages' not in str(f)
    ]
    
    all_functions = []
    all_classes = []
    all_calls: Set[str] = set()
    errors = []
    
    # Анализ каждого файла
    for py_file in py_files:
        module_name = get_module_name(str(py_file), str(project_root))
        
        result = analyze_file_for_treemap(str(py_file), module_name)
        
        if result.get('error'):
            errors.append({
                'file': str(py_file),
                'error': result['error']
            })
        else:
            all_functions.extend(result['functions'])
            all_classes.extend(result['classes'])
            all_calls.update(result['calls'])
    
    # Определение неиспользуемых функций
    unused_functions = find_unused_functions(all_functions, all_calls)
    
    # Добавление флага unused к функциям
    for func in all_functions:
        func['metrics']['unused'] = (
            func['name'] in unused_functions or 
            func['full_name'] in unused_functions
        )
    
    # Объединяем функции и классы для compiler метрик
    compiler_data = all_functions + all_classes
    
    return {
        'compiler': compiler_data,
        'classloader': [],  # Можно добавить анализ .pyc файлов позже
        'errors': errors
    }


def write_metrics(metrics_data: Dict, output_path: str) -> str:
    """Записывает метрики в файл в формате Prometheus.
    
    Args:
        metrics_data: Данные метрик из analyze_project
        output_path: Путь к выходному файлу
    
    Returns:
        Абсолютный путь к записанному файлу
    """
    return write_prometheus(metrics_data, output_path)


def analyze_captured() -> Dict:
    """Анализирует уже захваченные метрики (для совместимости с Clojure API).
    
    В Python версии это просто алиас для analyze_project, так как мы не используем
    runtime захват как в Clojure. Но можно расширить для поддержки инкрементального анализа.
    """
    # Пока просто возвращаем пустые данные
    # Можно расширить для поддержки инкрементального анализа
    return {
        'compiler': [],
        'classloader': [],
        'errors': []
    }
