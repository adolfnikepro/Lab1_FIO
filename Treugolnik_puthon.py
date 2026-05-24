import math
import logging
from datetime import datetime




logger = logging.getLogger("triangle_logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)


file_handler = logging.FileHandler("triangle.log", encoding="utf-8")
file_handler.setFormatter(formatter)


console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)


if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)






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
        
      
       

        a = float(str_a)
        b = float(str_b)
        c = float(str_c)

        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Стороны должны быть положительными числами")

       
       

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

        
        
        

        if a == b == c:
            triangle_type = "равносторонний"
        elif a == b or a == c or b == c:
            triangle_type = "равнобедренный"
        else:
            triangle_type = "разносторонний"

     

        x1, y1 = 0.0, 0.0
        x2, y2 = c, 0.0

        x3 = (b**2 + c**2 - a**2) / (2 * c)

        
        y3_square = b**2 - x3**2

      
        y3_square = max(y3_square, 0)

        y3 = math.sqrt(y3_square)

       
        points = [
            (x1, y1),
            (x2, y2),
            (x3, y3)
        ]

        max_x = max(p[0] for p in points)
        max_y = max(p[1] for p in points)

        
        scale_x = 90 / max_x if max_x != 0 else 1
        scale_y = 90 / max_y if max_y != 0 else 1

        scale = min(scale_x, scale_y)

        scaled_points = []

        for x, y in points:
            sx = int(x * scale) + 5
            sy = int(y * scale) + 5
            scaled_points.append((sx, sy))

        result = (triangle_type, scaled_points)

      

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
