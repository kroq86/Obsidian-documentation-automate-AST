"""
Экспорт метрик в формат Prometheus для совместимости с viewer.html.
"""

from typing import Dict, List, Optional


def escape_label_value(s: Optional[str]) -> str:
    """Экранировать строку для использования как значение метки Prometheus.
    
    По спецификации: обратный слэш, двойные кавычки и перенос строки должны быть экранированы.
    """
    if s is None:
        return ""
    
    s = str(s)
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    s = s.replace("\n", "\\n")
    return s


def format_labels(labels: Dict[str, Optional[str]]) -> str:
    """Форматировать словарь меток как строку меток Prometheus. Пропускает None значения."""
    pairs = []
    for k, v in labels.items():
        if v is not None:
            pairs.append(f'{k}="{escape_label_value(v)}"')
    
    if pairs:
        return "{" + ",".join(pairs) + "}"
    return ""


def metric_line(metric_name: str, labels: Dict[str, Optional[str]], value: int) -> str:
    """Создать строку метрики в формате Prometheus."""
    label_str = format_labels(labels)
    return f"{metric_name}{label_str} {value}"


def compiler_entry_to_lines(entry: Dict) -> List[str]:
    """Преобразовать запись компилятора в строки метрик Prometheus."""
    name = entry.get('name', '')
    ns = entry.get('ns', '')
    line = entry.get('line')
    metrics = entry.get('metrics', {})
    
    labels = {
        'ns': ns,
        'name': name,
        'line': str(line) if line else None
    }
    
    lines = []
    
    # Expressions метрика
    expressions = metrics.get('expressions', 0)
    if expressions > 0:
        lines.append(metric_line("python_expressions", labels, expressions))
    
    # Max depth метрика
    max_depth = metrics.get('max_depth', 0)
    if max_depth > 0:
        lines.append(metric_line("python_max_depth", labels, max_depth))
    
    # Unused метрика (только для функций)
    unused = metrics.get('unused')
    if unused is not None:
        lines.append(metric_line("python_unused", labels, 1 if unused else 0))
    
    # Complexity метрика (только для функций)
    complexity = metrics.get('complexity', 0)
    if complexity > 0:
        lines.append(metric_line("python_complexity", labels, complexity))
    
    return lines


def classloader_entry_to_lines(entry: Dict) -> List[str]:
    """Преобразовать запись classloader в строки метрик Prometheus."""
    name = entry.get('name', '')
    ns = entry.get('ns', '')
    full_name = entry.get('full_name', name)
    metrics = entry.get('metrics', {})
    
    labels = {
        'ns': ns,
        'name': name,
        'full_name': full_name
    }
    
    bytecode_size = metrics.get('bytecode_size', 0)
    
    return [
        metric_line("python_bytecode_size", labels, bytecode_size)
    ]


def format_prometheus(metrics_data: Dict) -> str:
    """Форматировать данные метрик как строку в формате Prometheus exposition."""
    lines = []
    
    # Заголовок
    lines.append("# Python code metrics - Prometheus format")
    lines.append("")
    
    # HELP и TYPE для компиляторных метрик
    lines.append("# HELP python_expressions AST node count")
    lines.append("# TYPE python_expressions gauge")
    lines.append("# HELP python_max_depth Maximum nesting depth")
    lines.append("# TYPE python_max_depth gauge")
    lines.append("# HELP python_unused 1 if function/class defined but never referenced")
    lines.append("# TYPE python_unused gauge")
    lines.append("# HELP python_complexity Cyclomatic complexity")
    lines.append("# TYPE python_complexity gauge")
    
    # Компиляторные метрики
    compiler_data = metrics_data.get('compiler', [])
    for entry in compiler_data:
        lines.extend(compiler_entry_to_lines(entry))
    
    lines.append("")
    
    # HELP и TYPE для classloader метрик
    lines.append("# HELP python_bytecode_size Compiled bytecode size in bytes")
    lines.append("# TYPE python_bytecode_size gauge")
    
    # Classloader метрики
    classloader_data = metrics_data.get('classloader', [])
    for entry in classloader_data:
        lines.extend(classloader_entry_to_lines(entry))
    
    return "\n".join(lines)


def write_prometheus(metrics_data: Dict, path: str) -> str:
    """Записать данные метрик в файл в формате Prometheus.
    
    Возвращает абсолютный путь к записанному файлу.
    """
    import os
    abs_path = os.path.abspath(path)
    
    with open(abs_path, 'w', encoding='utf-8') as f:
        f.write(format_prometheus(metrics_data))
    
    return abs_path
