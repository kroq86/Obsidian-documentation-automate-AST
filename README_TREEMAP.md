# Python Treemap Metrics Viewer

Расширение для анализа Python проектов с визуализацией метрик в виде интерактивного treemap.

## Быстрый старт

```bash
# Анализ проекта и генерация метрик
python example_usage.py

# Или через основной анализатор с флагом --treemap
python main.py . --dirs src/ --treemap --output metrics
```

## Использование

### Базовый пример

```python
from core import analyze_project, write_metrics

# Анализ проекта
metrics = analyze_project(
    project_path="./my_project",
    exclude_patterns=['venv', '__pycache__']
)

# Запись метрик в Prometheus формат
write_metrics(metrics, "metrics.prom")
```

### Визуализация

1. Откройте `viewer.html` в браузере
2. Перетащите файл `.prom` в окно браузера
3. Или используйте URL параметр: `viewer.html?data=metrics.prom`

## Метрики

### Compiler метрики (функции и классы)

- **expressions** - Количество узлов AST (размер кода)
- **max-depth** - Максимальная глубина вложенности
- **complexity** - Цикломатическая сложность
- **unused?** - Флаг неиспользуемого кода (определен, но не вызывается)

### Classloader метрики (байткод)

- **bytecode-size** - Размер скомпилированного байткода (пока не реализовано)

## Структура проекта

```
python-metrics-viewer/
├── main.py              # Существующий архитектурный анализатор
├── metrics.py           # Сбор метрик для treemap
├── prometheus.py        # Экспорт в Prometheus формат
├── core.py              # Публичный API
├── viewer.html          # D3.js treemap визуализация
└── example_usage.py     # Пример использования
```

## Интеграция с существующим кодом

Новый функционал интегрирован с существующим `main.py`:

```bash
# Генерация архитектурного анализа + treemap метрик
python main.py . --dirs src/ --treemap --output analysis
```

Это создаст:
- `analysis.md` - архитектурный анализ
- `analysis.json` - JSON данные
- `analysis_treemap.prom` - метрики для treemap

## Отличия от Clojure версии

1. **Нет макросов** - только одна версия метрик (нет raw/expanded)
2. **AST-based анализ** - не требует Java agent
3. **Проще развертывание** - только Python код
4. **Дополнительные метрики** - цикломатическая сложность

## Совместимость

- Формат Prometheus совместим с оригинальным `viewer.html`
- Поддерживает как Clojure, так и Python метрики
- Можно визуализировать оба типа проектов в одном viewer
