#!/usr/bin/env python3
"""
Пример использования Python метрик анализатора для treemap визуализации.
"""

from core import analyze_project, write_metrics
import os


def main():
    # Анализ текущего проекта
    project_path = "."
    
    print("🔍 Анализ Python проекта...")
    print(f"Путь: {os.path.abspath(project_path)}")
    
    # Анализируем проект
    metrics = analyze_project(
        project_path=project_path,
        exclude_patterns=['venv', '__pycache__', '.venv', 'site-packages']
    )
    
    print(f"\n✅ Анализ завершен:")
    print(f"  - Функций/классов найдено: {len(metrics['compiler'])}")
    print(f"  - Ошибок: {len(metrics['errors'])}")
    
    if metrics['errors']:
        print("\n⚠️  Ошибки анализа:")
        for error in metrics['errors'][:5]:  # Показываем первые 5
            print(f"  - {error['file']}: {error['error']}")
    
    # Записываем метрики в Prometheus формат
    output_file = "python_metrics.prom"
    abs_path = write_metrics(metrics, output_file)
    
    print(f"\n📝 Метрики записаны в: {abs_path}")
    print(f"\n🌐 Откройте viewer.html в браузере и загрузите файл {output_file}")
    print(f"   Или используйте: file://{os.path.abspath('viewer.html')}?data={os.path.abspath(output_file)}")


if __name__ == "__main__":
    main()
