import math
import logging
from datetime import datetime

# =========================
# НАСТРОЙКА ЛОГИРОВАНИЯ
# =========================

logger = logging.getLogger("triangle_logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

# Логирование в файл
file_handler = logging.FileHandler("triangle.log", encoding="utf-8")
file_handler.setFormatter(formatter)

# Логирование в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Добавляем handlers только один раз
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# =========================
# ОСНОВНАЯ ФУНКЦИЯ
# =========================

def triangle_info(str_a, str_b, str_c):
    """
    Определяет тип треугольника и вычисляет координаты вершин.

    Вход:
        str_a, str_b, str_c - строки

    Выход:
        (triangle_type, coordinates)

    triangle_type:
        "равносторонний"
        "равнобедренный"
        "разносторонний"
        "не треугольник"
        ""

    coordinates:
        [(x1, y1), (x2, y2), (x3, y3)]
    """

    try:
        # =========================
        # ПРОВЕРКА И ПРЕОБРАЗОВАНИЕ
        # =========================

        a = float(str_a)
        b = float(str_b)
        c = float(str_c)

        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Стороны должны быть положительными числами")

        # =========================
        # ПРОВЕРКА СУЩЕСТВОВАНИЯ
        # =========================

        if a + b <= c or a + c <= b or b + c <= a:
            result = (
                "не треугольник",
                [(-1, -1), (-1, -1), (-1, -1)]
            )

            logger.warning(
                f"Неуспешный запрос | "
                f"params=({str_a}, {str_b}, {str_c}) | "
                f"result={result}"
            )

            return result

        # =========================
        # ОПРЕДЕЛЕНИЕ ТИПА
        # =========================

        if a == b == c:
            triangle_type = "равносторонний"
        elif a == b or a == c or b == c:
            triangle_type = "равнобедренный"
        else:
            triangle_type = "разносторонний"

        # =========================
        # ВЫЧИСЛЕНИЕ КООРДИНАТ
        # =========================
        #
        # A = (0, 0)
        # B = (c, 0)
        # C вычисляется по формуле

        x1, y1 = 0.0, 0.0
        x2, y2 = c, 0.0

        # Формула координаты X вершины C
        x3 = (b**2 + c**2 - a**2) / (2 * c)

        # Формула координаты Y вершины C
        y3_square = b**2 - x3**2

        # Защита от отрицательного из-за ошибок float
        y3_square = max(y3_square, 0)

        y3 = math.sqrt(y3_square)

        # =========================
        # МАСШТАБИРОВАНИЕ В 100x100
        # =========================

        points = [
            (x1, y1),
            (x2, y2),
            (x3, y3)
        ]

        max_x = max(p[0] for p in points)
        max_y = max(p[1] for p in points)

        # Защита от деления на ноль
        scale_x = 90 / max_x if max_x != 0 else 1
        scale_y = 90 / max_y if max_y != 0 else 1

        scale = min(scale_x, scale_y)

        scaled_points = []

        for x, y in points:
            sx = int(x * scale) + 5
            sy = int(y * scale) + 5
            scaled_points.append((sx, sy))

        result = (triangle_type, scaled_points)

        # =========================
        # УСПЕШНОЕ ЛОГИРОВАНИЕ
        # =========================

        logger.info(
            f"Успешный запрос | "
            f"params=({str_a}, {str_b}, {str_c}) | "
            f"result={result}"
        )

        return result

    except Exception as e:

        result = ("", [(-2, -2), (-2, -2), (-2, -2)])

        logger.exception(
            f"Ошибка запроса | "
            f"params=({str_a}, {str_b}, {str_c}) | "
            f"error={e}"
        )

        return result


# =========================
# ПРИМЕРЫ
# =========================

if __name__ == "__main__":

    tests = [
        ("3", "3", "3"),
        ("5", "5", "8"),
        ("3", "4", "5"),
        ("1", "2", "10"),
        ("abc", "4", "5"),
        ("-1", "2", "3")
    ]

    for t in tests:
        print(f"\nВход: {t}")
        print("Выход:", triangle_info(*t))