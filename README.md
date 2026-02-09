# Python Code Metrics Viewer

Инструмент для анализа архитектуры Python кода и визуализации метрик в виде интерактивного treemap.

## Возможности

- 🏗️ **Архитектурный анализ** - анализ классов, функций, декораторов и зависимостей
- 📊 **Treemap визуализация** - интерактивная визуализация метрик кода
- 🔍 **Метрики сложности** - цикломатическая сложность, глубина вложенности, размер кода
- 📝 **Генерация отчетов** - Markdown и JSON отчеты с инсайтами
- 🎯 **Определение неиспользуемого кода** - поиск функций и классов, которые не вызываются

## Быстрый старт

### Базовое использование

```bash
# Анализ проекта с генерацией treemap метрик
python3 main.py . --dirs src/ --treemap --output metrics

# Только архитектурный анализ
python3 main.py . --dirs src/ --output analysis

# С генерацией HTML отчета
python3 main.py . --dirs src/ --html --open
```

### Пример использования API

```python
from core import analyze_project, write_metrics

# Анализ проекта
metrics = analyze_project(
    project_path="./my_project",
    include_patterns=["src/"],
    exclude_patterns=['venv', '__pycache__']
)

# Генерация метрик для визуализации
write_metrics(metrics, "metrics.prom")
```

### Визуализация treemap

1. Откройте `viewer.html` в браузере
2. Перетащите файл `*_treemap.prom` в окно браузера
3. Или используйте URL: `viewer.html?data=/path/to/metrics_treemap.prom`

**Важно:** Prometheus сервер не требуется! Формат Prometheus используется только для структуры данных, совместимой с viewer.html.

## Документация

- [README_TREEMAP.md](README_TREEMAP.md) - подробная документация по treemap метрикам
- [TESTING.md](TESTING.md) - инструкции по тестированию
- [CHANGELOG.md](CHANGELOG.md) - история изменений

## Примеры команд

```bash
# Архитектурный анализ с Cursor интеграцией
python3 main.py . --dirs src/ --cursor --output test

# Trace файл для конкретного модуля
python3 main.py . --trace-file src/etc/export.py --output export_trace
```

## Анализ внешних проектов

### Быстрый способ (скрипт)
```bash
# Анализ проекта с автоматическим именованием
./analyze_project.sh /path/to/project

# С указанием директорий
./analyze_project.sh /path/to/project "src/ tests/"

# С указанием имени выходного файла
./analyze_project.sh /path/to/project "src/" my_analysis
```

### Прямой вызов
```bash
# Анализ внешнего проекта с treemap метриками
python3 main.py /path/to/project --dirs src/ --treemap --output project_metrics
```

### Визуализация результатов
1. Откройте `viewer.html` в браузере
2. Перетащите файл `*_treemap.prom` в окно браузера
3. Или используйте URL: `viewer.html?data=/absolute/path/to/metrics_treemap.prom`

**Важно:** Prometheus сервер не требуется! Формат Prometheus используется только для структуры данных, совместимой с viewer.html.
