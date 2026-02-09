#!/bin/bash
# Скрипт для быстрого анализа Python проекта

set -e

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Получаем путь к проекту (первый аргумент или текущая директория)
PROJECT_PATH="${1:-.}"

# Получаем директории для анализа (второй аргумент или "src")
DIRS="${2:-src/}"

# Получаем имя выходного файла (третий аргумент или автоматическое)
if [ -z "$3" ]; then
    # Автоматически генерируем имя из пути проекта
    PROJECT_NAME=$(basename "$PROJECT_PATH" | tr '/' '_' | tr ' ' '_')
    OUTPUT_NAME="${PROJECT_NAME}_metrics"
else
    OUTPUT_NAME="$3"
fi

echo -e "${BLUE}🔍 Анализ Python проекта${NC}"
echo -e "  Проект: ${GREEN}$PROJECT_PATH${NC}"
echo -e "  Директории: ${GREEN}$DIRS${NC}"
echo -e "  Выходной файл: ${GREEN}$OUTPUT_NAME${NC}"
echo ""

# Переходим в директорию скрипта
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Запускаем анализ
python3 main.py "$PROJECT_PATH" --dirs $DIRS --treemap --output "$OUTPUT_NAME"

echo ""
echo -e "${GREEN}✅ Анализ завершен!${NC}"
echo ""
echo -e "${YELLOW}📊 Созданные файлы:${NC}"
ls -lh "${OUTPUT_NAME}"* 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'

echo ""
echo -e "${YELLOW}🌐 Для визуализации:${NC}"
PROM_FILE="${OUTPUT_NAME}_treemap.prom"
if [ -f "$PROM_FILE" ]; then
    ABS_PATH=$(cd "$(dirname "$PROM_FILE")" && pwd)/$(basename "$PROM_FILE")
    echo -e "  1. Откройте ${BLUE}viewer.html${NC} в браузере"
    echo -e "  2. Перетащите файл ${BLUE}$PROM_FILE${NC} в окно"
    echo -e "  3. Или используйте URL:"
    echo -e "     ${BLUE}file://$SCRIPT_DIR/viewer.html?data=$ABS_PATH${NC}"
fi
