# Changelog - Treemap Metrics Integration

## Добавлено

### Новые модули

1. **`metrics.py`** - Сбор метрик для treemap визуализации
   - `TreemapMetricsCollector` - AST visitor для сбора метрик
   - Подсчет выражений (AST nodes)
   - Вычисление максимальной глубины вложенности
   - Определение неиспользуемых функций
   - Цикломатическая сложность

2. **`prometheus.py`** - Экспорт метрик в Prometheus формат
   - Совместимость с оригинальным `viewer.html`
   - Поддержка метрик компилятора и classloader
   - Правильное экранирование меток

3. **`core.py`** - Публичный API
   - `analyze_project()` - анализ Python проекта
   - `write_metrics()` - запись метрик в файл
   - Интеграция с существующим кодом

4. **`example_usage.py`** - Пример использования

### Интеграция

- Добавлен флаг `--treemap` в `main.py` для генерации treemap метрик
- Скопирован и адаптирован `viewer.html` для поддержки Python метрик
- Обновлен парсинг Prometheus формата для поддержки `python_*` метрик

### Метрики

**Compiler метрики:**
- `python_expressions` - количество узлов AST
- `python_max_depth` - максимальная глубина вложенности
- `python_unused` - флаг неиспользуемого кода
- `python_complexity` - цикломатическая сложность

**Classloader метрики:**
- `python_bytecode_size` - размер байткода (заглушка для будущей реализации)

## Использование

```bash
# Базовое использование
python example_usage.py

# Через основной анализатор
python main.py . --dirs src/ --treemap --output metrics

# Программно
from core import analyze_project, write_metrics
metrics = analyze_project("./project")
write_metrics(metrics, "metrics.prom")
```

## Совместимость

- Формат Prometheus совместим с оригинальным `viewer.html` из Clojure проекта
- Поддерживает как Clojure, так и Python метрики
- Можно визуализировать оба типа проектов в одном viewer

## Отличия от Clojure версии

1. **Нет макросов** - только одна версия метрик (нет raw/expanded)
2. **AST-based анализ** - не требует Java agent
3. **Проще развертывание** - только Python код
4. **Дополнительные метрики** - цикломатическая сложность
