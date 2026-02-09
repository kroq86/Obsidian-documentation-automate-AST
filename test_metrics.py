#!/usr/bin/env python3
"""
Простой тест для проверки работы метрик без Prometheus.
Проверяет, что файлы создаются и содержат корректные данные.
"""

import os
import sys
from pathlib import Path


def test_treemap_generation():
    """Тест генерации treemap метрик."""
    print("🧪 Тестирование генерации treemap метрик...")
    
    # Проверяем наличие необходимых модулей
    try:
        from core import analyze_project, write_metrics
        print("✅ Модули импортированы успешно")
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    
    # Анализируем тестовую директорию
    project_path = "."
    test_dirs = ["src/"]
    
    print(f"\n📂 Анализ проекта: {os.path.abspath(project_path)}")
    print(f"📁 Директории: {test_dirs}")
    
    try:
        metrics = analyze_project(
            project_path=project_path,
            include_patterns=test_dirs,
            exclude_patterns=['venv', '__pycache__', '.venv', 'site-packages']
        )
        print(f"✅ Анализ завершен успешно")
    except Exception as e:
        print(f"❌ Ошибка анализа: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Проверяем результаты
    compiler_data = metrics.get('compiler', [])
    errors = metrics.get('errors', [])
    
    print(f"\n📊 Результаты анализа:")
    print(f"  - Функций/классов найдено: {len(compiler_data)}")
    print(f"  - Ошибок: {len(errors)}")
    
    if errors:
        print(f"\n⚠️  Ошибки анализа:")
        for error in errors[:3]:
            print(f"  - {error.get('file', 'unknown')}: {error.get('error', 'unknown')}")
    
    if len(compiler_data) == 0:
        print("⚠️  Предупреждение: не найдено функций или классов")
        return False
    
    # Проверяем структуру данных
    print(f"\n🔍 Проверка структуры данных...")
    sample = compiler_data[0]
    required_fields = ['name', 'ns', 'metrics']
    
    for field in required_fields:
        if field not in sample:
            print(f"❌ Отсутствует обязательное поле: {field}")
            return False
    
    print(f"✅ Структура данных корректна")
    
    # Генерируем файл метрик
    test_output = "test_metrics.prom"
    print(f"\n💾 Генерация файла метрик: {test_output}")
    
    try:
        abs_path = write_metrics(metrics, test_output)
        print(f"✅ Файл создан: {abs_path}")
    except Exception as e:
        print(f"❌ Ошибка записи файла: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Проверяем содержимое файла
    if not os.path.exists(test_output):
        print(f"❌ Файл не создан: {test_output}")
        return False
    
    with open(test_output, 'r') as f:
        content = f.read()
    
    # Проверяем формат Prometheus
    required_metrics = ['python_expressions', 'python_max_depth']
    found_metrics = []
    
    for metric in required_metrics:
        if metric in content:
            found_metrics.append(metric)
            print(f"  ✅ Найдена метрика: {metric}")
        else:
            print(f"  ⚠️  Метрика не найдена: {metric}")
    
    if len(found_metrics) == 0:
        print("❌ Не найдено ни одной метрики в файле")
        return False
    
    # Проверяем HELP и TYPE комментарии
    if '# HELP' in content and '# TYPE' in content:
        print(f"  ✅ Формат Prometheus корректен (есть HELP и TYPE)")
    else:
        print(f"  ⚠️  Отсутствуют HELP или TYPE комментарии")
    
    print(f"\n📄 Первые 10 строк файла:")
    lines = content.split('\n')[:10]
    for i, line in enumerate(lines, 1):
        print(f"  {i:2d}: {line}")
    
    print(f"\n✅ Все тесты пройдены успешно!")
    print(f"\n💡 Для визуализации:")
    print(f"   1. Откройте viewer.html в браузере")
    print(f"   2. Перетащите файл {test_output} в окно браузера")
    print(f"   3. Или используйте URL: viewer.html?data={os.path.abspath(test_output)}")
    
    return True


def test_existing_files():
    """Проверяет существующие файлы метрик."""
    print("\n" + "="*60)
    print("🧪 Проверка существующих файлов метрик...")
    
    files_to_check = [
        "metrics_treemap.prom",
        "metrics.md",
        "metrics.json"
    ]
    
    for filename in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename} существует ({size} байт)")
        else:
            print(f"⚠️  {filename} не найден")


if __name__ == "__main__":
    print("="*60)
    print("Тестирование Python Metrics Viewer")
    print("="*60)
    
    # Проверяем существующие файлы
    test_existing_files()
    
    # Запускаем тесты
    success = test_treemap_generation()
    
    print("\n" + "="*60)
    if success:
        print("✅ Все тесты пройдены!")
        sys.exit(0)
    else:
        print("❌ Некоторые тесты не пройдены")
        sys.exit(1)
